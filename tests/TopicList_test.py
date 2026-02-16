"""Tests for the TopicList class."""

import json
from datetime import datetime
from openproficiency import Topic, TopicList


class TestTopicList:

    # Initializers
    def test_init_required_params(self):
        """Create a topic list with required."""

        # Arrange
        owner = "example.com"
        name = "example-topics-list"

        # Act
        topic_list = TopicList(
            owner=owner,
            name=name,
        )

        # Assert
        assert topic_list.owner == owner
        assert topic_list.name == name
        assert topic_list.topics == {}
        assert topic_list.dependencies == {}

    def test_init_with_description(self):
        """Create a topic list with description field."""

        # Arrange
        owner = "example.com"
        name = "example-topics-list"
        description = "Features of the GitHub platform"

        # Act
        topic_list = TopicList(
            owner=owner,
            name=name,
            description=description,
        )

        # Assert
        assert topic_list.owner == owner
        assert topic_list.name == name
        assert topic_list.description == description

    def test_init_with_version(self):
        """Create a topic list with custom version."""

        # Arrange
        owner = "example.com"
        name = "example-topics-list"
        version = "2.1.0"

        # Act
        topic_list = TopicList(
            owner=owner,
            name=name,
            version=version,
        )

        # Assert
        assert topic_list.version == version

    def test_init_with_timestamp(self):
        """Create a topic list with custom timestamp."""

        # Arrange
        owner = "example.com"
        name = "example-topics-list"
        timestamp = "2025-01-15T10:30:00+00:00"

        # Act
        topic_list = TopicList(
            owner=owner,
            name=name,
            timestamp=timestamp,
        )

        # Assert
        assert topic_list.timestamp == datetime.fromisoformat(timestamp)

    def test_init_with_certificate(self):
        """Create a topic list with custom certificate."""

        # Arrange
        owner = "example.com"
        name = "example-topics-list"
        certificate = "cert-12345"

        # Act
        topic_list = TopicList(
            owner=owner,
            name=name,
            certificate=certificate,
        )

        # Assert
        assert topic_list.certificate == certificate
        print("Warning: Certificate format is currently not validated.")

    def test_init_timestamp_defaults_to_current_utc(self):
        """Verify timestamp defaults to current UTC when not provided."""

        # Act
        topic_list = TopicList(
            owner="example.com",
            name="example",
        )

        # Assert
        assert topic_list.timestamp is not None
        assert isinstance(topic_list.timestamp, datetime)
        # Should have UTC timezone info
        assert topic_list.timestamp.tzinfo is not None

    def test_version_default(self):
        """Verify version defaults to None."""

        # Act
        topic_list = TopicList(
            owner="example.com",
            name="example",
        )

        # Assert
        assert topic_list.version is None

    # Methods
    def test_add_topic_string(self):
        """Add a new topic using a string ID."""

        # Arrange
        topic_list = TopicList(
            owner="example.com",
            name="example-topics-list",
        )
        topic_id = "git-commit"

        # Act
        topic_list.add_topic(topic_id)

        # Assert
        assert "git-commit" in topic_list.topics
        assert isinstance(topic_list.topics["git-commit"], Topic)

    def test_add_topic_topic(self):
        """Add a new topic using a Topic instance."""

        # Arrange
        topic_list = TopicList(
            owner="example.com",
            name="example-topics-list",
        )
        topic1 = Topic(
            id="git-commit",
            description="Storing changes to the Git history",
        )

        # Act
        topic_list.add_topic(topic1)

        # Assert
        assert "git-commit" in topic_list.topics
        assert topic_list.topics["git-commit"] == topic1

    def test_get_topic(self):
        """Test retrieving a topic that exists in the list."""

        # Arrange
        topic_list = TopicList(
            owner="example.com",
            name="example-topics-list",
        )
        topic = Topic(id="git-commit")
        topic_list.topics[topic.id] = topic

        # Act
        retrieved = topic_list.get_topic("git-commit")

        # Assert
        assert retrieved is not None
        assert retrieved.id == "git-commit"

    def test_get_topic_nonexistent(self):
        """Test retrieving a topic that does not exist in the list."""

        # Arrange
        topic_list = TopicList(
            owner="example.com",
            name="example-topics-list",
        )
        topic = Topic(id="git-commit")
        topic_list.topics[topic.id] = topic

        # Act
        retrieved = topic_list.get_topic("nonexistent")

        # Assert
        assert retrieved is None

    # Properties
    def test_full_name(self):
        """Test getting the full name of the topic list."""

        # Arrange
        owner = "example.com"
        name = "example-topic-list"
        topic_list = TopicList(
            owner=owner,
            name=name,
        )

        # Act
        full_name = topic_list.full_name

        # Assert
        assert full_name == "example.com/example-topic-list"

    def test_full_name_with_version(self):
        """Test getting the full name of the topic list, including version."""

        # Arrange
        owner = "example.com"
        name = "example-topic-list"
        topic_list = TopicList(
            owner=owner,
            name=name,
            version="1.2.3",
        )

        # Act
        full_name = topic_list.full_name

        # Assert
        assert full_name == "example.com/example-topic-list@1.2.3"

    def test_version_setter_valid_format(self):
        """Test setting version with valid semantic versioning."""

        # Arrange
        topic_list = TopicList(
            owner="example.com",
            name="example",
        )

        # Act
        topic_list.version = "3.2.1"

        # Assert
        assert topic_list.version == "3.2.1"

    def test_version_setter_invalid_format_missing_patch(self):
        """Test setting version with invalid format (missing patch number)."""

        # Arrange
        topic_list = TopicList(
            owner="example.com",
            name="example",
        )

        # Act & Assert
        try:
            topic_list.version = "3.2"
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "Invalid version format" in str(e)
            assert "Must be semantic versioning" in str(e)

    def test_version_setter_invalid_format_extra_component(self):
        """Test setting version with invalid format (too many components)."""

        # Arrange
        topic_list = TopicList(
            owner="example.com",
            name="example",
        )

        # Act
        result = None
        try:
            topic_list.version = "3.2.1.5"
            assert False, "Should have raised ValueError"
        except Exception as e:
            result = e

        # Assert
        assert isinstance(result, ValueError)
        assert "Invalid" in str(result)

    def test_version_setter_invalid_format_non_numeric(self):
        """Test setting version with invalid format (non-numeric components)."""

        # Arrange
        topic_list = TopicList(
            owner="example.com",
            name="example",
        )

        # Act
        result = None
        try:
            topic_list.version = "v3.2.1"
            assert False, "Should have raised ValueError"
        except Exception as e:
            result = e

        # Assert
        assert isinstance(result, ValueError)
        assert "Invalid" in str(result)

    def test_version_zero_values(self):
        """Test setting version with zero values."""

        # Arrange
        topic_list = TopicList(
            owner="example.com",
            name="example",
        )

        # Act
        topic_list.version = "0.0.0"

        # Assert
        assert topic_list.version == "0.0.0"

    # Methods - Class
    def test_load_from_json_basic_info(self):
        """Load a list with only list info."""

        # Arrange
        json_data = """
        {
            "owner": "example.com",
            "name": "example-features"
        }
        """

        # Act
        topic_list = TopicList.from_json(json_data)

        # Assert - list details
        assert topic_list.owner == "example.com"
        assert topic_list.name == "example-features"

    def test_load_from_json_optional_inputs(self):
        """Load a list with version, timestamp, and certificate fields."""

        # Arrange
        json_data = """
        {
            "owner": "example.com",
            "name": "example-features",
            "description": "Features of the GitHub platform",
            "version": "2.3.1",
            "timestamp": "2025-01-15T10:30:00+00:00",
            "certificate": "cert-abc123"
        }
        """

        # Act
        topic_list = TopicList.from_json(json_data)

        # Assert
        assert topic_list.version == "2.3.1"
        assert topic_list.timestamp == datetime.fromisoformat("2025-01-15T10:30:00+00:00")
        assert topic_list.certificate == "cert-abc123"

    def test_load_from_json_simple(self):
        """Load a list with only top-level topics."""

        # Arrange
        json_data = """
        {
            "owner": "example.com",
            "name": "example-features",
            "description": "Features of the GitHub platform",
            "topics": {
                "actions": {
                    "description": "Storing changes to the Git history"
                },
                "repositories": {
                    "description": "Versioning code with Git repositories"
                }
            }
        }
        """

        # Act
        topic_list = TopicList.from_json(json_data)

        # Assert - topics
        assert "actions" in topic_list.topics
        assert topic_list.topics["actions"].description == "Storing changes to the Git history"

        assert "repositories" in topic_list.topics
        assert topic_list.topics["repositories"].description == "Versioning code with Git repositories"

    def test_load_from_json_subtopics(self):
        """Load a list with subtopics."""

        # Arrange
        json_data = """
        {
            "owner": "example.com",
            "name": "example-features",
            "description": "Features of the GitHub platform",
            "topics": {

                "git-branch": {
                    "description": "Parallel versions of work",
                    "pretopic": ["git-commit"]
                },

                "actions": {
                    "description": "Storing changes to the Git history",
                    "subtopics": ["git-branch"]
                },

                "repositories": {
                    "description": "Versioning code with Git repositories",
                    "subtopics": [
                        "commit-history",
                        "pull-request",
                        "fork"
                    ]
                }
            }
        }
        """

        # Act
        topic_list = TopicList.from_json(json_data)

        # Assert - topics
        assert "actions" in topic_list.topics
        assert "git-branch" in topic_list.topics
        assert topic_list.topics["git-branch"].description == "Parallel versions of work"

        assert "repositories" in topic_list.topics
        assert "commit-history" in topic_list.topics
        assert "pull-request" in topic_list.topics
        assert "fork" in topic_list.topics

    def test_load_from_json_subsubtopics(self):
        """Load a list with multiple layers of subtopics."""

        # Arrange
        json_data = """
        {
            "owner": "example.com",
            "name": "example",
            "description": "Features of the GitHub platform",
            "topics": {

                "repositories": {
                    "description": "Versioning code with Git repositories",
                    "subtopics": [
                        "commit-history",
                        {
                            "id": "community-files",
                            "description": "Essential files for repository community health",
                            "subtopics": [
                                "code-of-conduct-file",
                                "codeowners-file",
                                "contributing-file",
                                "license-file",
                                "readme-file"
                            ]
                        },
                        "pull-request",
                        "fork"
                    ]
                }
            }
        }
        """

        # Act
        topic_list = TopicList.from_json(json_data)

        # Assert
        assert "community-files" in topic_list.topics
        assert topic_list.topics["community-files"].description == "Essential files for repository community health"
        assert "code-of-conduct-file" in topic_list.topics
        assert "codeowners-file" in topic_list.topics
        assert "contributing-file" in topic_list.topics
        assert "license-file" in topic_list.topics
        assert "readme-file" in topic_list.topics

    def test_load_from_json_pretopics(self):
        """Load a list with subtopics."""

        # Arrange
        json_data = """
        {
            "owner": "example.com",
            "name": "example-features",
            "description": "Features of the GitHub platform",
            "topics": {

                "actions": {
                    "description": "Storing changes to the Git history",
                    "pretopics": ["yaml"]
                },

                "git-commit": {
                    "description": "Saving changes to the Git history"
                },

                "repositories": {
                    "description": "Versioning code with Git repositories",
                    "pretopics": [
                        "git-commit",
                        "git-push",
                        "git-pull"
                    ]
                }
            }
        }
        """

        # Act
        topic_list = TopicList.from_json(json_data)

        # Assert - topics
        assert "actions" in topic_list.topics
        assert topic_list.topics["yaml"].description == "Storing changes to the Git history"
        assert "yaml" in topic_list.topics

        assert "repositories" in topic_list.topics
        assert topic_list.topics["repositories"].description == "Versioning code with Git repositories"
        assert "git-commit" in topic_list.topics
        assert "git-push" in topic_list.topics
        assert "git-pull" in topic_list.topics

    def test_load_from_json_prepretopics(self):
        """Load a list with multiple layers of pretopics."""

        # Arrange
        json_data = """
        {
            "owner": "example.com",
            "name": "example-features",
            "description": "Features of the GitHub platform",
            "topics": {

                "repositories": {
                    "description": "Versioning code with Git repositories",
                    "pretopics": [
                        "git-commit",
                        {
                            "id": "git-merge",
                            "description": "Essential files for repository community health",
                            "pretopics": [
                                "git1",
                                "git2",
                                "git3"
                            ]
                        },
                        "git-pull"
                    ]
                }
            }
        }
        """

        # Act
        topic_list = TopicList.from_json(json_data)

        # Assert - topics
        assert "repositories" in topic_list.topics
        assert "git-commit" in topic_list.topics
        assert topic_list.topics["git-commit"].description == "Versioning code with Git repositories"

        assert "git-merge" in topic_list.topics
        assert topic_list.topics["git-merge"].description == "Essential files for repository community health"
        assert "git1" in topic_list.topics
        assert "git2" in topic_list.topics
        assert "git3" in topic_list.topics

        assert "git-pull" in topic_list.topics
        assert topic_list.topics["git-pull"].description == "Versioning code with Git repositories"

    def test_to_dict_simple(self):
        """Exporting a simple TopicList to dictionary."""

        # Arrange
        topic_list = TopicList(
            owner="example.com",
            name="example-features",
            description="Features of the GitHub platform",
        )
        topic_list.add_topic(
            Topic(
                id="actions",
                description="Storing changes to the Git history",
                subtopics=["automation"],
                pretopics=["yaml"],
            )
        )
        topic_list.add_topic(
            Topic(
                id="repositories",
                description="Versioning code with Git repositories",
                subtopics=["git-clone"],
                pretopics=["git-push"],
            )
        )

        # Act
        data = topic_list.to_dict()

        # Assert - List Info
        assert data["owner"] == "example.com"
        assert data["name"] == "example-features"
        assert data["description"] == "Features of the GitHub platform"

        # Assert - Topic 1
        assert "actions" in data["topics"]
        assert data["topics"]["actions"]["description"] == "Storing changes to the Git history"
        assert "automation" in data["topics"]["actions"]["subtopics"]
        assert "yaml" in data["topics"]["actions"]["pretopics"]

        # Assert - Topic 2
        assert "repositories" in data["topics"]
        assert data["topics"]["repositories"]["description"] == "Versioning code with Git repositories"
        assert "git-clone" in data["topics"]["repositories"]["subtopics"]
        assert "git-push" in data["topics"]["repositories"]["pretopics"]

    def test_to_dict(self):
        """Test that to_dict excludes optional fields if set to None."""

        # Arrange
        topic_list = TopicList(
            owner="example.com",
            name="example-features",
        )

        # Act
        data = topic_list.to_dict()

        # Assert
        assert "description" not in data
        assert "version" not in data
        assert "certificate" not in data

    def test_to_dict_with_optionals(self):
        """Test that to_dict includes optional fields."""

        # Arrange
        topic_list = TopicList(
            owner="example.com",
            name="example-features",
            description="Features of the GitHub platform",
            version="2.1.0",
            timestamp="2025-01-15T10:30:00+00:00",
            certificate="cert-xyz789",
        )

        # Act
        data = topic_list.to_dict()

        # Assert
        assert data["version"] == "2.1.0"
        assert data["timestamp"] == "2025-01-15T10:30:00+00:00"
        assert data["certificate"] == "cert-xyz789"

    def test_json_roundtrip_integrity(self):
        """Test that JSON export/import preserves values."""

        # Arrange
        original = TopicList(
            owner="example.com",
            name="example-features",
            description="Test description",
            version="1.2.3",
            timestamp="2025-02-16T14:25:00+00:00",
            certificate="cert-example",
        )

        # Act
        json_str = original.to_json()
        restored = TopicList.from_json(json_str)

        # Assert
        assert restored.owner == original.owner
        assert restored.name == original.name
        assert restored.description == original.description
        assert restored.version == original.version
        assert restored.timestamp == original.timestamp
        assert restored.certificate == original.certificate

    def test_to_json_simple(self):
        """Exporting a simple TopicList to JSON string."""

        # Arrange
        topic_list = TopicList(
            owner="example.com",
            name="example-features",
            description="Features of the GitHub platform",
        )
        topic_list.add_topic(
            Topic(
                id="actions",
                description="Storing changes to the Git history",
                subtopics=["automation"],
                pretopics=["yaml"],
            )
        )
        topic_list.add_topic(
            Topic(
                id="repositories",
                description="Versioning code with Git repositories",
                subtopics=["git-clone"],
                pretopics=["git-push"],
            )
        )

        # Act
        json_data = topic_list.to_json()
        data = json.loads(json_data)

        # Assert - List Info
        assert data["owner"] == "example.com"
        assert data["name"] == "example-features"
        assert data["description"] == "Features of the GitHub platform"

        # Assert - Topic 1
        assert "actions" in data["topics"]
        assert data["topics"]["actions"]["description"] == "Storing changes to the Git history"
        assert "automation" in data["topics"]["actions"]["subtopics"]
        assert "yaml" in data["topics"]["actions"]["pretopics"]

        # Assert - Topic 2
        assert "repositories" in data["topics"]
        assert data["topics"]["repositories"]["description"] == "Versioning code with Git repositories"
        assert "git-clone" in data["topics"]["repositories"]["subtopics"]
        assert "git-push" in data["topics"]["repositories"]["pretopics"]

    def test_from_json_invalid_type(self):
        """Test that from_json raises TypeError for non-string input."""

        # Act
        result = None
        try:
            TopicList.from_json({"owner": "test"})
        except Exception as e:
            result = e

        # Assert
        assert isinstance(result, TypeError)
        assert "must be a JSON string" in str(result)

    def test_from_json_invalid_json(self):
        """Test that from_json raises exception for invalid JSON string."""

        # Arrange
        invalid_json = "{this is not valid json"

        # Act
        result = None
        try:
            TopicList.from_json(invalid_json)
        except Exception as e:
            result = e

        # Assert
        assert isinstance(result, json.JSONDecodeError)
        assert "Expecting" in str(result)

    # Debugging
    def test_repr(self):
        """Test string representation of TopicList."""

        # Arrange
        topic_list = TopicList(
            owner="example.com",
            name="example-topics-list",
        )
        topic_list.add_topic("git-commit")
        topic_list.add_topic("git-push")

        # Act
        repr_str = repr(topic_list)

        # Assert
        assert "TopicList" in repr_str
        assert "example.com" in repr_str
        assert "example-topics-list" in repr_str
        assert "topics_count=2" in repr_str


class TestTopicListIdentifierValidation:
    """Tests for TopicList name and owner validation."""

    # Valid TopicList names
    def test_valid_name_single_word(self):
        """Test that single word lowercase names are valid."""

        # Arrange
        owner = "example.com"
        name = "example-topic-list"

        # Act
        topic_list = TopicList(owner=owner, name=name)

        # Assert
        assert topic_list.name == name

    def test_valid_name_kebab_case(self):
        """Test that kebab-case names are valid."""

        # Arrange
        owner = "example.com"
        name = "topic-list"

        # Act
        topic_list = TopicList(owner=owner, name=name)

        # Assert
        assert topic_list.name == name

    def test_valid_name_with_numbers(self):
        """Test that kebab-case names with numbers are valid."""

        # Arrange
        owner = "example.com"
        name = "python-3"

        # Act
        topic_list = TopicList(owner=owner, name=name)

        # Assert
        assert topic_list.name == name

    # Invalid TopicList names - construction time
    def test_invalid_name_uppercase_construction(self):
        """Test that uppercase letters in name are rejected during construction."""

        # Arrange
        owner = "example.com"
        invalid_name = "GitHub"

        # Act
        result = None
        try:
            TopicList(owner=owner, name=invalid_name)
        except Exception as e:
            result = e

        # Assert
        assert isinstance(result, ValueError)
        assert "kebab-case" in str(result)

    def test_invalid_name_underscore_construction(self):
        """Test that underscores in name are rejected during construction."""

        # Arrange
        owner = "example.com"
        invalid_name = "topic_list"

        # Act
        result = None
        try:
            TopicList(owner=owner, name=invalid_name)
        except Exception as e:
            result = e

        # Assert
        assert isinstance(result, ValueError)
        assert "kebab-case" in str(result)

    def test_invalid_name_double_hyphen_construction(self):
        """Test that double hyphens in name are rejected during construction."""

        # Arrange
        owner = "example.com"
        invalid_name = "topic--list"

        # Act
        result = None
        try:
            TopicList(owner=owner, name=invalid_name)
        except Exception as e:
            result = e

        # Assert
        assert isinstance(result, ValueError)
        assert "kebab-case" in str(result)

    def test_invalid_name_leading_hyphen_construction(self):
        """Test that leading hyphens in name are rejected during construction."""

        # Arrange
        owner = "example.com"
        invalid_name = "-topic"

        # Act
        result = None
        try:
            TopicList(owner=owner, name=invalid_name)
        except Exception as e:
            result = e

        # Assert
        assert isinstance(result, ValueError)
        assert "kebab-case" in str(result)

    def test_invalid_name_trailing_hyphen_construction(self):
        """Test that trailing hyphens in name are rejected during construction."""

        # Arrange
        owner = "example.com"
        invalid_name = "topic-"

        # Act
        result = None
        try:
            TopicList(owner=owner, name=invalid_name)
        except Exception as e:
            result = e

        # Assert
        assert isinstance(result, ValueError)
        assert "kebab-case" in str(result)

    def test_invalid_name_empty_construction(self):
        """Test that empty name is rejected during construction."""

        # Arrange
        owner = "example.com"
        invalid_name = ""

        # Act
        result = None
        try:
            TopicList(owner=owner, name=invalid_name)
        except Exception as e:
            result = e

        # Assert
        assert isinstance(result, ValueError)
        assert "cannot be empty" in str(result)

    # Invalid TopicList names - property update
    def test_invalid_name_update(self):
        """Test that invalid names are rejected during property update."""

        # Arrange
        topic_list = TopicList(
            owner="example.com",
            name="valid-name",
        )
        invalid_name = "Invalid_Name"

        # Act
        result = None
        try:
            topic_list.name = invalid_name
        except Exception as e:
            result = e

        # Assert
        assert isinstance(result, ValueError)
        assert "kebab-case" in str(result)

    # Valid owners
    def test_valid_owner_single_word(self):
        """Test that single word lowercase owners are valid."""

        # Arrange
        owner = "example.com"
        name = "example-topic-list"

        # Act
        topic_list = TopicList(owner=owner, name=name)

        # Assert
        assert topic_list.owner == owner

    def test_valid_owner_with_hyphen(self):
        """Test that kebab-case owners are valid."""

        # Arrange
        owner = "acme-corp.com"
        name = "example-topic-list"

        # Act
        topic_list = TopicList(owner=owner, name=name)

        # Assert
        assert topic_list.owner == owner

    def test_valid_owner_domain(self):
        """Test that domain-style owners are valid."""

        # Arrange
        owner = "example.com"
        name = "example-topic-list"

        # Act
        topic_list = TopicList(owner=owner, name=name)

        # Assert
        assert topic_list.owner == owner

    def test_valid_owner_subdomain(self):
        """Test that subdomain-style owners are valid."""

        # Arrange
        owner = "sub.example.com"
        name = "example-topic-list"

        # Act
        topic_list = TopicList(owner=owner, name=name)

        # Assert
        assert topic_list.owner == owner

    # Invalid owners - construction time
    def test_invalid_owner_uppercase_construction(self):
        """Test that uppercase letters in owner are rejected during construction."""

        # Arrange
        invalid_owner = "GitHub"
        name = "example-topic-list"

        # Act
        result = None
        try:
            TopicList(owner=invalid_owner, name=name)
        except Exception as e:
            result = e

        # Assert
        assert isinstance(result, ValueError)
        assert "hostname" in str(result)

    def test_invalid_owner_underscore_construction(self):
        """Test that underscores in owner are rejected during construction."""

        # Arrange
        invalid_owner = "example_org"
        name = "example-topic-list"

        # Act
        result = None
        try:
            TopicList(owner=invalid_owner, name=name)
        except Exception as e:
            result = e

        # Assert
        assert isinstance(result, ValueError)
        assert "hostname" in str(result)

    def test_invalid_owner_leading_hyphen_construction(self):
        """Test that leading hyphens in owner are rejected during construction."""

        # Arrange
        invalid_owner = "-example"
        name = "example-topic-list"

        # Act
        result = None
        try:
            TopicList(owner=invalid_owner, name=name)
        except Exception as e:
            result = e

        # Assert
        assert isinstance(result, ValueError)
        assert "hostname" in str(result)

    def test_invalid_owner_trailing_hyphen_construction(self):
        """Test that trailing hyphens in owner are rejected during construction."""

        # Arrange
        invalid_owner = "example-"
        name = "example-topic-list"

        # Act
        result = None
        try:
            TopicList(owner=invalid_owner, name=name)
        except Exception as e:
            result = e

        # Assert
        assert isinstance(result, ValueError)
        assert "hostname" in str(result)

    def test_invalid_owner_leading_dot_construction(self):
        """Test that leading dots in owner are rejected during construction."""

        # Arrange
        invalid_owner = ".example.com"
        name = "example-topic-list"

        # Act
        result = None
        try:
            TopicList(owner=invalid_owner, name=name)
        except Exception as e:
            result = e

        # Assert
        assert isinstance(result, ValueError)
        assert "hostname" in str(result)

    def test_invalid_owner_trailing_dot_construction(self):
        """Test that trailing dots in owner are rejected during construction."""

        # Arrange
        invalid_owner = "example.com."
        name = "example-topic-list"

        # Act
        result = None
        try:
            TopicList(owner=invalid_owner, name=name)
        except Exception as e:
            result = e

        # Assert
        assert isinstance(result, ValueError)
        assert "hostname" in str(result)

    def test_invalid_owner_empty_construction(self):
        """Test that empty owner is rejected during construction."""

        # Arrange
        invalid_owner = ""
        name = "example-topic-list"

        # Act
        result = None
        try:
            TopicList(owner=invalid_owner, name=name)
        except Exception as e:
            result = e

        # Assert
        assert isinstance(result, ValueError)
        assert "cannot be empty" in str(result)

    # Invalid owners - property update
    def test_invalid_owner_update(self):
        """Test that invalid owners are rejected during property update."""

        # Arrange
        topic_list = TopicList(
            owner="example.com",
            name="example-topics-list",
        )
        invalid_owner = "Invalid_Owner"

        # Act
        result = None
        try:
            topic_list.owner = invalid_owner
        except Exception as e:
            result = e

        # Assert
        assert isinstance(result, ValueError)
        assert "hostname" in str(result)
