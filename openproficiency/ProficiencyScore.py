"""ProficiencyScore module for OpenProficiency library."""

import json
from enum import Enum
from typing import Union
from .validators import validate_kebab_case


class ProficiencyScoreName(Enum):
    """Enum for proficiency score names."""

    UNAWARE = 0.0
    AWARE = 0.1
    FAMILIAR = 0.5
    PROFICIENT = 0.8
    PROFICIENT_WITH_EVIDENCE = 1.0


class ProficiencyScore:
    """Class representing a proficiency score for a topic."""

    # Initializers
    def __init__(
        self,
        # Required
        topic_id: str,
        score: Union[float, ProficiencyScoreName],
    ):
        # Required
        self.topic_id = topic_id
        self.score = score

    # Properties
    @property
    def topic_id(self) -> str:
        """Get the topic ID."""
        return self._topic_id

    @topic_id.setter
    def topic_id(self, value: str) -> None:
        """Set the topic ID. kebab-case"""
        validate_kebab_case(value)
        self._topic_id = value

    @property
    def score(self) -> float:
        """Get the score as a numeric value between 0.0 and 1.0."""
        return self._score

    @score.setter
    def score(self, value: Union[float, ProficiencyScoreName]) -> None:
        """Set the score numerically or using a ProficiencyScoreName enum."""
        # If numeric, directly store it.
        if isinstance(value, (int, float)):
            if not (0.0 <= value <= 1.0):
                raise ValueError(f"Score must be between 0.0 and 1.0, got {value}")
            self._score = float(value)

        # If enum, store as numeric value.
        elif isinstance(value, ProficiencyScoreName):
            self._score = value.value

        else:
            raise ValueError(f"Score must be numeric or ProficiencyScoreName enum. Got type: '{type(value)}'")

    # Properties - Score
    @property
    def score_name(self) -> ProficiencyScoreName:
        """Get the proficiency name as an enum value."""
        return ProficiencyScore.get_score_name(self._score)

    # Methods
    def to_dict(self) -> dict[str, float]:
        """Convert to a JSON-serializable dictionary."""
        return {
            "topic_id": self.topic_id,
            "score": self._score,
        }

    def to_json(self) -> str:
        """Convert to a JSON string."""
        return json.dumps(self.to_dict())

    # Static Methods
    @staticmethod
    def get_score_name(score: float) -> ProficiencyScoreName:
        """Internal method to determine proficiency name from numeric score."""
        if score == 1.0:
            return ProficiencyScoreName.PROFICIENT_WITH_EVIDENCE

        elif score >= 0.8:
            return ProficiencyScoreName.PROFICIENT

        elif score >= 0.5:
            return ProficiencyScoreName.FAMILIAR

        elif score >= 0.1:
            return ProficiencyScoreName.AWARE

        elif score >= 0.0:
            return ProficiencyScoreName.UNAWARE

        else:
            raise ValueError(f"Invalid score value: {score}")

    # Debugging
    def __repr__(self) -> str:
        """String representation of ProficiencyScore."""
        return f"ProficiencyScore(topic_id='{self.topic_id}', score={self._score}, name={self.score_name.name})"
