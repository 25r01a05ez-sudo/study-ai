from pydantic import BaseModel, Field


class RunRequest(BaseModel):
    idea: str = Field(min_length=5, max_length=4000)
    session_id: str | None = None
    tier: str = Field(default="free", pattern="^(free|pro)$")


class RunResponse(BaseModel):
    session_id: str
    idea: str
    artifacts: dict
    prompt_version: str


class FeedbackRequest(BaseModel):
    session_id: str
    score: int = Field(ge=1, le=5)
    comments: str | None = Field(default=None, max_length=1000)


class SessionResponse(BaseModel):
    session_id: str
    created_at: str
    idea: str
    artifacts: dict
