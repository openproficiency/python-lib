"""TopicList module for OpenProficiency library."""

import json
import re
from datetime import datetime, timezone
from typing import Dict, Any, Union, List, cast
from .Topic import Topic


class TopicList:

    # Initializers
    def __init__(
        self,
        # Required
        owner: str,
        name: str,
        # Optional
        description: Union[str, None] = None,
        version: Union[str, None] = None,
        timestamp: Union[str, None] = None,
        certificate: Union[str, None] = None,
    ):
        # Required
        self.owner = owner
        self.name = name

        # Optional
        self.description = description
        self.topics: Dict[str, Topic] = {}
        self.dependencies: Dict[str, "TopicList"] = {}

        # Set version with validation
        self.version = version

        # Set timestamp (convert string to datetime, default to current UTC if not provided)
        if timestamp is None:
            self._timestamp = datetime.now(timezone.utc)
        else:
            self._timestamp = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))

        # Set certificate
        self.certificate = certificate

    # Methods
    def add_topic(self, topic: Union[str, Topic]) -> Topic:
        """
        Add a topic to this list.
        Supports a string ID or a Topic instance.
        """

        # Support string ID
        if isinstance(topic, str):
            topic = Topic(id=topic)

        # Add Topic
        self.topics[topic.id] = topic
        return topic

    def get_topic(self, topic_id: str) -> Union[Topic, None]:
        return self.topics.get(topic_id, None)

    # Properties
    @property
    def version(self) -> Union[str, None]:
        """Get the semantic version of the TopicList."""
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
    def timestamp(self, value: Union[str, datetime, None]) -> None:
        """Set the timestamp from a string or datetime object."""
        if value is None:
            self._timestamp = datetime.now(timezone.utc)
        elif isinstance(value, str):
            self._timestamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
        else:
            self._timestamp = value

    @property
    def full_name(self) -> str:
        """Get the full name of the TopicList in 'owner/name' format."""
        return f"{self.owner}/{self.name}"

    # Debugging
    def __repr__(self) -> str:
        """String representation of TopicList."""
        return f"TopicList(owner='{self.owner}', name='{self.name}', topics_count={len(self.topics)})"

    # Methods - Class
    @classmethod
    def from_json(cls, json_data: str) -> "TopicList":
        """
        Load a TopicList from JSON document.
        If a topic is defined multiple times, only the last definition stays.
        """

        # Verify input is json string
        try:
            data = cast(Dict[str, Any], json.loads(json_data))
        except TypeError:
            raise TypeError("Unable to import. 'json_data' must be a JSON string")
        except Exception as e:
            raise e

        # Create empty TopicList
        topic_list = TopicList(
            owner=data.get("owner", ""),
            name=data.get("name", ""),
            description=data.get("description"),
            version=data.get("version"),
            timestamp=data.get("timestamp"),
            certificate=data.get("certificate"),
        )

        # Add each topic
        topics = cast(Dict[str, Any], data.get("topics", {}))
        for topic_id, topic_data in topics.items():

            # Find or create Topic
            topic = topic_list.get_topic(topic_id)
            if topic is None:
                topic = topic_list.add_topic(Topic(id=topic_id))

            if isinstance(topic_data, dict):
                topic_dict = cast(Dict[str, Any], topic_data)
                topic.description = topic_dict.get("description", "")

                # Add subtopics
                cls._add_subtopics_recursive(
                    topic_list=topic_list,
                    parent_topic=topic,
                    subtopics=cast(List[Any], topic_dict.get("subtopics", [])),
                )

                # Add pretopics
                cls._add_pretopics_recursive(
                    topic_list=topic_list,
                    child_topic=topic,
                    pretopics=cast(List[Any], topic_dict.get("pretopics", [])),
                )

            else:
                print("Unknown topic data format: ${topic_id}='${topic_data}'")

        return topic_list

    @staticmethod
    def _add_subtopics_recursive(
        topic_list: "TopicList",
        parent_topic: Topic,
        subtopics: List[Any],
    ) -> None:
        """
        Process subtopics and add them to the topic list.
        Handles nested subtopics at any depth using an iterative approach.
        """
        stack: List[tuple[List[Any], Topic]] = [(subtopics, parent_topic)]

        while stack:
            current_subtopics, current_parent = stack.pop()

            for subtopic_object in current_subtopics:
                subtopic = None

                # Handle string ID
                if isinstance(subtopic_object, str):
                    # Check if the topic already exists
                    subtopic = topic_list.get_topic(subtopic_object)
                    if subtopic is None:
                        subtopic = Topic(id=subtopic_object)

                # Handle dictionary with id and optional nested subtopics
                elif isinstance(subtopic_object, dict) and "id" in subtopic_object:
                    subtopic_dict = cast(Dict[str, Any], subtopic_object)
                    # Check if the topic already exists
                    subtopic = topic_list.get_topic(subtopic_dict["id"])
                    if subtopic is None:
                        subtopic = Topic(
                            id=subtopic_dict["id"],
                            description=subtopic_dict.get("description", ""),
                        )

                    # Queue nested subtopics for processing
                    nested_subtopics = cast(List[Any], subtopic_dict.get("subtopics", []))
                    if nested_subtopics:
                        stack.append((nested_subtopics, subtopic))

                # Add subtopic to topic list and parent topic
                if subtopic is not None:
                    topic_list.add_topic(subtopic)
                    current_parent.add_subtopic(subtopic)

    @staticmethod
    def _add_pretopics_recursive(
        topic_list: "TopicList",
        child_topic: Topic,
        pretopics: List[Any],
    ) -> None:
        """
        Process pretopics and add them to the topic list.
        Handles nested pretopics at any depth using an iterative approach.
        Pretopics inherit description from child topic if not explicitly set.
        """
        stack: List[tuple[List[Any], Topic]] = [(pretopics, child_topic)]

        while stack:
            current_pretopics, current_child = stack.pop()

            for pretopic_object in current_pretopics:
                pretopic = None

                # Handle string ID - inherit description from child topic
                if isinstance(pretopic_object, str):
                    # Check if the topic already exists
                    pretopic = topic_list.get_topic(pretopic_object)
                    if pretopic is None:
                        pretopic = Topic(id=pretopic_object, description=current_child.description)

                # Handle dictionary with id and optional nested pretopics
                elif isinstance(pretopic_object, dict) and "id" in pretopic_object:
                    pretopic_dict = cast(Dict[str, Any], pretopic_object)
                    # Check if the topic already exists
                    pretopic = topic_list.get_topic(pretopic_dict["id"])
                    if pretopic is None:
                        pretopic = Topic(
                            id=pretopic_dict["id"],
                            description=pretopic_dict.get("description", current_child.description),
                        )

                    # Queue nested pretopics for processing
                    nested_pretopics = cast(List[Any], pretopic_dict.get("pretopics", []))
                    if nested_pretopics:
                        stack.append((nested_pretopics, pretopic))

                # Add pretopic to topic list and child topic
                if pretopic is not None:
                    topic_list.add_topic(pretopic)
                    current_child.add_pretopic(pretopic)

    def to_dict(self) -> Dict[str, Any]:
        """
        Export the TopicList to a dictionary.
        """

        # Create dictionary
        data: Dict[str, Any] = {
            "owner": self.owner,
            "name": self.name,
            "timestamp": self.timestamp.isoformat(),
            "topics": {},
        }

        # Add description if set
        if self.description is not None:
            data["description"] = self.description

        # Add version if set
        if self.version is not None:
            data["version"] = self.version

        # Add certificate if set
        if self.certificate is not None:
            data["certificate"] = self.certificate

        # Add each topic
        for topic_id, topic in self.topics.items():
            # Create topic
            topic_data: Dict[str, Any] = {
                "description": topic.description,
            }
            # Add subtopics
            if topic.subtopics:
                topic_data["subtopics"] = topic.subtopics

            # Add pretopics
            if topic.pretopics:
                topic_data["pretopics"] = topic.pretopics

            # Store in data
            data["topics"][topic_id] = topic_data

        return data

    def to_json(self) -> str:
        """Convert TopicList to JSON string."""
        return json.dumps(self.to_dict())
