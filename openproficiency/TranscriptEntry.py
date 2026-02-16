"""TranscriptEntry module for OpenProficiency library."""

import json
from datetime import datetime
from typing import Any, Dict, Optional, Union
from .ProficiencyScore import ProficiencyScore


class TranscriptEntry:
    """A user's proficiency score, validated by a particular issuer."""

    # Initializers
    def __init__(
        self,
        # Required
        user_id: str,
        topic_id: str,
        topic_list: str,
        score: float,
        timestamp: Union[datetime, str],
        issuer: str,
        # Optional
        certificate: Optional[str] = None,
    ):
        # Required
        self.user_id = user_id
        self._proficiency_score = ProficiencyScore(
            topic_id=topic_id,
            score=score,
        )
        self.topic_list = topic_list
        self.timestamp = timestamp
        self.issuer = issuer
        # Optional
        self.certificate = certificate

    # Properties
    @property
    def proficiency_score(self) -> ProficiencyScore:
        """Get the topic ID from the proficiency score."""
        return self._proficiency_score

    @property
    def topic_list(self) -> str:
        """Get the topic list reference."""
        return self._topic_list

    @topic_list.setter
    def topic_list(self, value: str) -> None:
        """Set the topic list reference from TopicList instance"""
        self._topic_list = value

    @property
    def certificate(self) -> Optional[str]:
        """Get the certificate text."""
        return self._certificate

    @certificate.setter
    def certificate(self, value: Optional[str]) -> None:
        """Set the certificate text."""
        self._certificate = value

    @property
    def timestamp(self) -> datetime:
        """Get the time this entry was created"""
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value: Union[datetime, str]) -> None:
        """Set the time this entry was created"""
        # Directly store datetime object.
        if isinstance(value, datetime):
            self._timestamp = value

        # Convert ISO 8601 string to datetime object.
        elif isinstance(value, str):
            self._timestamp = datetime.fromisoformat(value)

        else:
            raise ValueError("Timestamp must be a datetime object or ISO 8601 string")

    # Methods
    def to_dict(self) -> Dict[str, Union[str, float]]:
        """Convert TranscriptEntry to JSON-serializable dictionary."""
        data = {
            "user_id": self.user_id,
            "topic": self._proficiency_score.topic_id,
            "topic_list": self.topic_list,
            "score": self._proficiency_score.score,
            "timestamp": self.timestamp.isoformat(),
            "issuer": self.issuer,
        }

        # Attach certificate if it exists
        if self.certificate is not None:
            data["certificate"] = self.certificate

        return data

    def to_json(self) -> str:
        """Convert TranscriptEntry to JSON string."""
        data = self.to_dict()
        # Change keys to camelCase for JSON output
        data["userID"] = data.pop("user_id")
        data["topicList"] = data.pop("topic_list")
        return json.dumps(data)

    # Methods - Static
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "TranscriptEntry":
        """Create a TranscriptEntry from a dictionary."""
        return TranscriptEntry(
            # Required
            user_id=data["user_id"],
            topic_id=data["topic"],
            topic_list=data["topic_list"],
            score=data["score"],
            timestamp=data["timestamp"],
            issuer=data["issuer"],
            # Optional
            certificate=data.get("certificate"),
        )

    @staticmethod
    def from_json(json_str: str) -> "TranscriptEntry":
        """Create a TranscriptEntry from a JSON string."""
        # Load JSON string. Map camelCase to snake_case if needed
        data = json.loads(json_str)
        data["user_id"] = data.pop("userID")
        data["topic_list"] = data.pop("topicList")
        return TranscriptEntry.from_dict(data)

    # Debugging
    def __repr__(self) -> str:
        """String representation of TranscriptEntry."""
        return (
            f"TranscriptEntry(user_id='{self.user_id}', "
            f"topic_id='{self._proficiency_score.topic_id}', "
            f"topic_list='{self.topic_list}', "
            f"score={self._proficiency_score.score}, "
            f"issuer='{self.issuer}'"
        )
