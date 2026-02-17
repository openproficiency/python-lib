"""ProficiencyLevel module for OpenProficiency library."""

import json
from typing import Any, Dict, Optional, Union, Set
from .validators import validate_kebab_case


class ProficiencyLevel:
    """Class representing a proficiency level defined by prerequisite topics."""

    # Initializers
    def __init__(
        self,
        # Required
        id: str,
        # Optional
        description: Optional[str] = None,
        pretopics: Optional[Set[str]] = None,
    ):
        # Required
        self.id = id
        # Optional
        self.description = description
        if pretopics is None:
            pretopics = set()
        self.pretopics = pretopics

    # Properties
    @property
    def id(self) -> str:
        """Get the proficiency level ID."""
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        """Set the proficiency level ID. kebab-case"""
        validate_kebab_case(value)
        self._id = value

    @property
    def description(self) -> Optional[str]:
        """Get the description."""
        return self._description

    @description.setter
    def description(self, value: Optional[Union[str, None]]) -> None:
        """Set the description. Max 100 characters."""
        if value is not None and len(value) > 100:
            raise ValueError(f"Description must be 100 characters or less. Got {len(value)} characters.")
        self._description = value

    # Methods
    def add_pretopic(self, pretopic: str) -> None:
        """
        Add a pretopic (prerequisite topic) to this proficiency level.
        """
        self.pretopics.add(pretopic)

    def add_pretopics(self, pretopics: Set[str]) -> None:
        """
        Add multiple pretopics to this proficiency level.
        """
        self.pretopics.update(pretopics)

    def remove_pretopic(self, pretopic: str) -> None:
        """Remove a pretopic by its ID."""
        self.pretopics.discard(pretopic)

    def to_dict(self) -> Dict[str, Any]:
        """Convert ProficiencyLevel to JSON-serializable dictionary."""
        return {
            "id": self.id,
            "description": self.description,
            "pretopics": list(self.pretopics),
        }

    def to_json(self) -> str:
        """Convert ProficiencyLevel to JSON string."""
        return json.dumps(self.to_dict())

    # Methods - Static
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "ProficiencyLevel":
        """Create a ProficiencyLevel instance from a dictionary."""
        return ProficiencyLevel(
            id=data["id"],
            description=data.get("description", ""),
            pretopics=set(data.get("pretopics", [])),
        )

    @staticmethod
    def from_json(json_str: str) -> "ProficiencyLevel":
        """Create a ProficiencyLevel instance from a JSON string."""
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")
        return ProficiencyLevel.from_dict(data)

    def __eq__(self, other: Any) -> bool:
        """Check equality based and pretopics."""
        if not isinstance(other, ProficiencyLevel):
            return False
        return set(self.pretopics) == set(other.pretopics)

    # Debugging
    def __repr__(self) -> str:
        """String representation of ProficiencyLevel."""
        return f"ProficiencyLevel(id='{self.id}', " f"description='{self.description}', " f"pretopics={self.pretopics})"
