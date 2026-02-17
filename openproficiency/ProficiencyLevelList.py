"""ProficiencyLevelList module for OpenProficiency library."""

import json
import re
from datetime import datetime, timezone
from typing import Optional, Dict, Any, Union, List
from .ProficiencyLevel import ProficiencyLevel
from .TopicList import TopicList
from .validators import validate_kebab_case, validate_hostname


class ProficiencyLevelList:
    """Class representing a collection of proficiency levels with dependencies."""

    # Initializers
    def __init__(
        self,
        # Required
        owner: str,
        name: str,
        version: str,
        timestamp: Union[str, datetime],
        certificate: str,
        # Optional
        description: Optional[str] = None,
        levels: Optional[Dict[str, ProficiencyLevel]] = None,
        dependencies: Optional[Dict[str, TopicList]] = None,
    ):
        # Required
        self.owner = owner
        self.name = name
        self.version = version
        self.timestamp = timestamp
        self.certificate = certificate

        # Optional
        self.description = description
        self.levels = levels or {}
        self.dependencies = dependencies or {}

    # Properties
    @property
    def owner(self) -> str:
        """Get the owner name."""
        return self._owner

    @owner.setter
    def owner(self, value: str) -> None:
        """Set the owner with hostname validation. Format: hostname, Ex: `example.com`"""
        validate_hostname(value)
        self._owner = value

    @property
    def name(self) -> str:
        """Get the ProficiencyLevelList name. Format: kebab-case"""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Set the ProficiencyLevelList name with kebab-case validation."""
        validate_kebab_case(value)
        self._name = value

    @property
    def version(self) -> Union[str, None]:
        """Get the semantic version of the ProficiencyLevelList."""
        return self._version

    @version.setter
    def version(self, value: Union[str, None]) -> None:
        """Set the semantic version with X.Y.Z format validation."""
        if value is not None and not re.match(r"^\d+\.\d+\.\d+$", value):
            raise ValueError(f"Invalid version format: '{value}'. Must be semantic versioning (X.Y.Z)")
        self._version = value

    @property
    def timestamp(self) -> datetime:
        """Get the timestamp as a datetime object."""
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value: Union[datetime, str, None]) -> None:
        """Set the timestamp from a string or datetime object."""
        if value is None:
            self._timestamp = datetime.now(timezone.utc)
        elif isinstance(value, datetime):
            self._timestamp = value
        elif isinstance(value, str):
            self._timestamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
        else:
            raise ValueError("Invalid timestamp format. Must be a datetime object or ISO 8601 string.")

    @property
    def full_name(self) -> str:
        """Get the full name of the ProficiencyLevelList in 'owner/name@version' format."""
        full_name = f"{self.owner}/{self.name}"
        if self.version:
            full_name += f"@{self.version}"
        return full_name

    # Methods
    def add_level(self, level: ProficiencyLevel) -> None:
        """
        Add a proficiency level to this list.
        Validates that all pretopics reference valid topics in dependencies.
        """
        # Check for duplicate ID
        if level.id in self.levels:
            raise ValueError(f"A proficiency level with ID '{level.id}' already exists in this list")

        # Validate pretopics
        self._validate_pretopics(level)

        # Add the level
        self.levels[level.id] = level

    def add_dependency(self, namespace: str, topic_list: TopicList) -> None:
        """
        Add an imported TopicList as a dependency.
        """
        # Validate namespace format (kebab-case)
        validate_kebab_case(namespace)

        # Check for duplicate namespace
        if namespace in self.dependencies:
            raise ValueError(f"A dependency with namespace '{namespace}' already exists in this list")

        # Add the dependency
        self.dependencies[namespace] = topic_list

    def _validate_pretopics(self, level: ProficiencyLevel) -> None:
        """
        Validate that all pretopics in a level reference valid topics in dependencies.
        Pretopics must be in format 'namespace.topic-id'.
        """
        errors: List[str] = []

        for pretopic in level.pretopics:
            # Parse namespace and topic ID
            if "." not in pretopic:
                errors.append(
                    f"Pretopic '{pretopic}' in level '{level.id}' is not in "
                    "namespace notation format (expected 'namespace.topic-id')"
                )
                continue

            parts = pretopic.split(".", 1)
            namespace = parts[0]
            topic_id = parts[1]

            # Check if namespace exists in dependencies
            if namespace not in self.dependencies:
                errors.append(
                    f"Pretopic '{pretopic}' in level '{level.id}' references unknown " f"namespace '{namespace}'"
                )
                continue

            # Check if topic exists in the TopicList
            topic_list = self.dependencies[namespace]
            if topic_list.get_topic(topic_id) is None:
                errors.append(
                    f"Pretopic '{pretopic}' in level '{level.id}' references "
                    f"non-existent topic '{topic_id}' in namespace '{namespace}'"
                )

        # If there are any errors, raise them all together
        if errors:
            error_message = "; ".join(errors)
            raise ValueError(error_message)

    def to_dict(self) -> Dict[str, Any]:
        """
        Export the ProficiencyLevelList to a dictionary.
        """
        # Create dictionary
        data: Dict[str, Any] = {
            "owner": self.owner,
            "name": self.name,
            "version": self.version,
            "timestamp": self.timestamp.isoformat(),
            "certificate": self.certificate,
            "proficiency-levels": {},
            "dependencies": {},
        }

        # Add description if set
        if self.description is not None:
            data["description"] = self.description

        # Add dependencies
        for namespace, topic_list in self.dependencies.items():
            data["dependencies"][namespace] = topic_list.full_name

        # Add each level
        for level_id, level in self.levels.items():
            data["proficiency-levels"][level_id] = level.to_dict()

        return data

    def to_json(self) -> str:
        """Convert ProficiencyLevelList to JSON string."""
        return json.dumps(self.to_dict())


    # Debugging
    def __repr__(self) -> str:
        """String representation of ProficiencyLevelList."""
        return (
            f"ProficiencyLevelList(owner='{self.owner}', name='{self.name}', "
            f"levels_count={len(self.levels)}, dependencies_count={len(self.dependencies)})"
        )
