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

        # ground truth
        self.true_labels = {}
        self.true_priorities = {}

    def reset(self) -> EmailTriageObservation:
        self._state = State(episode_id=str(uuid4()), step_count=0)

        # 📩 emails
        self.emails = [
            Email(id=1, subject="Meeting Tomorrow", content="Discuss project", sender="boss@company.com"),
            Email(id=2, subject="Win a free iPhone!!!", content="Click here now", sender="spam@ads.com"),
            Email(id=3, subject="Invoice attached", content="Please review invoice", sender="finance@company.com"),
            Email(id=4, subject="Party Invite", content="Join us this weekend!", sender="friend@gmail.com"),
            Email(id=5, subject="Security Alert", content="Suspicious login detected", sender="security@bank.com"),
        ]

        # ground truth
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

        # ensure correct type
        email_id = int(action.email_id)
        predicted_label = action.label
        predicted_priority = action.priority

        # 🔥 FIX: ensure ground truth exists (for stateless requests)
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

        reward = 0.0

        true_label = self.true_labels.get(email_id)
        true_priority = self.true_priorities.get(email_id)

        # 🎯 classification reward
        if true_label and predicted_label == true_label:
            reward += 0.6
        else:
            reward -= 0.3

        # 🎯 priority reward
        if true_priority and predicted_priority == true_priority:
            reward += 0.4
        else:
            reward -= 0.2

        # track processed emails
        if email_id not in self.processed:
            self.processed.append(email_id)

        done = len(self.processed) == len(self.true_labels)

        return EmailTriageObservation(
            emails=self.emails,
            processed=self.processed,
            done=done,
            reward=reward,
        )

    @property
    def state(self) -> State:
        return self._state