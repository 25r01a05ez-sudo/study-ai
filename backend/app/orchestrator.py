import uuid

from . import agents
from .config import settings
from .guardrails import now_iso
from .memory import save_audit, save_session


class CofounderOrchestrator:
    def run(self, idea: str) -> dict:
        session_id = str(uuid.uuid4())
        created_at = now_iso()

        plan = agents.planner_agent(idea)
        research = agents.researcher_agent(idea)
        prd = agents.writer_agent(idea, plan, research)
        reviewed = agents.reviewer_agent(prd)

        artifacts = {
            "plan": plan,
            "research": research,
            "output": reviewed,
        }

        save_session(session_id=session_id, created_at=created_at, idea=idea, artifacts=artifacts)
        save_audit("pipeline_run", {"session_id": session_id, "prompt_version": settings.prompt_version}, created_at)

        return {
            "session_id": session_id,
            "idea": idea,
            "artifacts": artifacts,
            "prompt_version": settings.prompt_version,
        }
