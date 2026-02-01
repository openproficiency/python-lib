"""ProficiencyScore module for OpenProficiency library."""

from enum import Enum
from typing import Union


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
        score: Union[float, ProficiencyScoreName]
    ):
        # Required
        self.topic_id = topic_id
        self._set_score(score)

    # Properties - Score
    @property
    def score(self) -> float:
        """Get the score as a numeric value between 0.0 and 1.0."""
        return self._score

    @score.setter
    def score(self, value: Union[float, ProficiencyScoreName]) -> None:
        """Set the score numerically or using a ProficiencyScoreName enum."""
        self._set_score(value)

    # Properties - Score
    @property
    def score_name(self) -> ProficiencyScoreName:
        """Get the proficiency name as an enum value."""
        return self._get_name_from_score(self._score)

    @score_name.setter
    def score_name(self, value: ProficiencyScoreName) -> None:
        """Set the proficiency name using a ProficiencyScoreName enum."""
        if not isinstance(value, ProficiencyScoreName):
            raise ValueError(
                f"Name must be a ProficiencyScoreName enum, got {type(value)}")
        self._score = value.value

    # Methods
    def _set_score(self, value: Union[float, ProficiencyScoreName]) -> None:
        """Internal method to set score from numeric or enum value."""
        if isinstance(value, ProficiencyScoreName):
            self._score = value.value

        elif isinstance(value, (int, float)):
            # Validate score is between 0.0 and 1.0
            if not (0.0 <= value <= 1.0):
                raise ValueError(
                    f"Score must be between 0.0 and 1.0, got {value}")
            self._score = float(value)

        else:
            raise ValueError(
                f"Score must be numeric or ProficiencyScoreName enum. Got type: '{type(value)}'")

    def _get_name_from_score(self, score: float) -> ProficiencyScoreName:
        """Internal method to determine proficiency name from numeric score."""
        if score <= 0.0:
            return ProficiencyScoreName.UNAWARE
        elif score <= 0.1:
            return ProficiencyScoreName.AWARE
        elif score <= 0.5:
            return ProficiencyScoreName.FAMILIAR
        elif score <= 0.8:
            return ProficiencyScoreName.PROFICIENT
        elif score <= 1.0:
            return ProficiencyScoreName.PROFICIENT_WITH_EVIDENCE
        else:
            raise ValueError(f"Invalid score value: {score}")

    def to_json(self) -> dict:
        """Convert to a JSON-serializable dictionary."""
        return {
            "topic_id": self.topic_id,
            "score": self._score
        }

    # Debugging

    def __repr__(self) -> str:
        """String representation of ProficiencyScore."""
        return f"ProficiencyScore(topic_id='{self.topic_id}', score={self._score}, name={self.score_name.name})"
