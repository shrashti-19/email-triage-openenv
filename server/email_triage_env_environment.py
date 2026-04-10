from uuid import uuid4
from typing import List

from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import State

try:
    from ..models import EmailTriageAction, EmailTriageObservation, Email
except ImportError:
    from models import EmailTriageAction, EmailTriageObservation, Email


class EmailTriageEnvironment(Environment):

    SUPPORTS_CONCURRENT_SESSIONS: bool = True

    def __init__(self):
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self.emails: List[Email] = []
        self.processed = []

        self.true_labels = {}
        self.true_priorities = {}

    def reset(self) -> EmailTriageObservation:
        self._state = State(episode_id=str(uuid4()), step_count=0)

        self.emails = [
            Email(id=1, subject="Meeting Tomorrow", content="Discuss project", sender="boss@company.com"),
            Email(id=2, subject="Win a free iPhone!!!", content="Click here now", sender="spam@ads.com"),
            Email(id=3, subject="Invoice attached", content="Please review invoice", sender="finance@company.com"),
            Email(id=4, subject="Party Invite", content="Join us this weekend!", sender="friend@gmail.com"),
            Email(id=5, subject="Security Alert", content="Suspicious login detected", sender="security@bank.com"),
        ]

        self.true_labels = {
            1: "important",
            2: "spam",
            3: "important",
            4: "important",
            5: "important",
        }

        self.true_priorities = {
            1: "high",
            2: "low",
            3: "medium",
            4: "low",
            5: "high",
        }

        self.processed = []

        return EmailTriageObservation(
            emails=self.emails,
            processed=[],
            done=False,
            reward=0.0,
        )

    def step(self, action: EmailTriageAction) -> EmailTriageObservation:
        self._state.step_count += 1

        email_id = int(action.email_id)
        predicted_label = action.label
        predicted_priority = action.priority

        # fallback (stateless safety)
        if not self.true_labels:
            self.true_labels = {
                1: "important",
                2: "spam",
                3: "important",
                4: "important",
                5: "important",
            }

            self.true_priorities = {
                1: "high",
                2: "low",
                3: "medium",
                4: "low",
                5: "high",
            }

        true_label = self.true_labels.get(email_id)
        true_priority = self.true_priorities.get(email_id)

        # ✅ SAFE reward: always between (0,1)
        reward = 0.2  # base reward

        if predicted_label == true_label:
            reward += 0.3

        if predicted_priority == true_priority:
            reward += 0.3

        # Final clamp (VERY IMPORTANT)
        if reward >= 1.0:
            reward = 0.9
        if reward <= 0.0:
            reward = 0.1

        # track processed emails
        if email_id not in self.processed:
            self.processed.append(email_id)

        done = len(self.processed) == len(self.true_labels)

        return EmailTriageObservation(
            emails=self.emails,
            processed=self.processed,
            done=done,
            reward=round(reward, 2),
        )

    @property
    def state(self) -> State:
        return self._state