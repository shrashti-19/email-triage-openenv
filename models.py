from openenv.core.env_server.types import Action, Observation
from pydantic import BaseModel, Field
from typing import List


# 📩 Email structure
class Email(BaseModel):
    id: int
    subject: str
    content: str
    sender: str


# 🎯 Action model (what agent does)
class EmailTriageAction(Action):
    email_id: int = Field(..., description="ID of the email to act on")
    label: str = Field(..., description="spam or important")
    priority: str = Field(..., description="low, medium, or high")


# 👀 Observation model (what agent sees)
class EmailTriageObservation(Observation):
    emails: List[Email] = Field(..., description="List of emails")
    processed: List[int] = Field(default_factory=list, description="IDs of processed emails")


# 💰 Reward model (scoring)
class EmailTriageReward(BaseModel):
    score: float = Field(..., description="Reward score between 0 and 1")