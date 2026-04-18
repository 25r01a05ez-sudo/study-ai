import logging

from fastapi import Depends, FastAPI, HTTPException, Request

from .config import settings
from .guardrails import enforce_rate_limit, moderate_user_input, now_iso, require_api_key
from .memory import get_metrics, get_session, init_db, save_audit, save_feedback
from .models import FeedbackRequest, MetricsResponse, RunRequest, RunResponse, SessionResponse
from .orchestrator import CofounderOrchestrator

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="StudyAI Cofounder API", version="0.1.0")
orchestrator = CofounderOrchestrator()


@app.on_event("startup")
def startup() -> None:
    init_db()
    logger.info("app_started", extra={"debug": settings.app_debug})


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/cofounder/run", response_model=RunResponse)
def run_pipeline(payload: RunRequest, request: Request, api_key: str = Depends(require_api_key)) -> dict:
    moderate_user_input(payload.idea)
    enforce_rate_limit(api_key, payload.tier)
    result = orchestrator.run(payload.idea)
    save_audit("run_requested", {"session_id": result["session_id"], "tier": payload.tier}, now_iso())
    return result


@app.get("/api/cofounder/session/{session_id}", response_model=SessionResponse)
def get_pipeline_session(session_id: str, _: str = Depends(require_api_key)) -> dict:
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@app.post("/api/cofounder/feedback")
def submit_feedback(payload: FeedbackRequest, _: str = Depends(require_api_key)) -> dict:
    session = get_session(payload.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    created_at = now_iso()
    save_feedback(payload.session_id, payload.score, payload.comments, created_at)
    save_audit("feedback_submitted", {"session_id": payload.session_id, "score": payload.score}, created_at)
    return {"status": "received"}


@app.get("/api/cofounder/metrics", response_model=MetricsResponse)
def read_metrics(_: str = Depends(require_api_key)) -> dict:
    return get_metrics()
