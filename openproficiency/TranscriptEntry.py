"""TranscriptEntry module for OpenProficiency library."""

import json
from datetime import datetime
from typing import Optional
from .ProficiencyScore import ProficiencyScore


class TranscriptEntry:
    """A user's proficiency score, validated by a particular issuer."""

    # Initializers
    def __init__(
        self,
        # Required
        user_id: str,
        topic_id: str,
        score: float,
        issuer: str,

        # Optional
        timestamp: Optional[datetime] = None,
    ):
        # Required
        self.user_id = user_id
        self._proficiency_score = ProficiencyScore(
            topic_id=topic_id,
            score=score
        )
        self.issuer = issuer

        # Optional
        self.timestamp = timestamp or datetime.now()

    # Properties
    @property
    def proficiency_score(self) -> ProficiencyScore:
        """Get the topic ID from the proficiency score."""
        return self._proficiency_score

    # Methods
    def to_dict(self) -> dict:
        """Convert Topic to JSON-serializable dictionary."""
        return {
            "user_id": self.user_id,
            "topic_id": self._proficiency_score.topic_id,
            "score": self._proficiency_score.score,
            "issuer": self.issuer,
            "timestamp": self.timestamp.isoformat()
        }

    def to_json(self) -> str:
        """Convert Topic to JSON string."""
        return json.dumps(self.to_dict())

    # Debugging
    def __repr__(self) -> str:
        """String representation of TranscriptEntry."""
        return f"TranscriptEntry(user_id='{self.user_id}', topic_id='{self._proficiency_score.topic_id}', score={self._proficiency_score.score}, issuer='{self.issuer}')"
