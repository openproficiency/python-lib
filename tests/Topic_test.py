import json
from openproficiency import Topic


class TestTopic:

    # Initializers
    def test_init_required_params(self):
        """Create a topic with requied fields only"""

        # Arrange
        id = "git-commit"

        # Act
        topic = Topic(id=id)

        # Assert
        assert topic.id == id

        # Assert - default values
        assert topic.description == ""
        assert topic.subtopics == []
        assert topic.pretopics == []

    def test_init_optional_params(self):
        """Test creating a topic with subtopics."""

        # Arrange
        id = "git-commit"
        description = "Saving changes to the Git history"
        subtopics = ["git-branch", "git-merge"]
        pretopics = ["cli"]

        # Act
        topic = Topic(
            id=id,
            description=description,
            subtopics=subtopics,
            pretopics=pretopics,
        )

        # Assert
        assert topic.description == description
        assert len(topic.subtopics) == 2
        assert len(topic.pretopics) == 1

    # Methods

    def test_add_subtopic_string(self):
        """Test adding a subtopic as a string."""

        # Arrange
        topic = Topic(id="git")
        subtopic_id = "git-commit"

        # Act
        topic.add_subtopic(subtopic_id)

        # Assert
        assert subtopic_id in topic.subtopics

    def test_add_subtopic_topic(self):
        """Test adding a subtopic as a Topic instance."""

        # Arrange
        topic = Topic(id="git")
        subtopic = Topic(
            id="git-commit",
            description="Saving changes to the Git history",
        )

        # Act
        topic.add_subtopic(subtopic)

        # Assert
        assert subtopic.id in topic.subtopics

    def test_add_subtopic_invalid_type(self):
        """Test that adding a subtopic with invalid type raises ValueError."""

        # Arrange
        topic = Topic(id="git")

        # Act
        result = None
        try:
            topic.add_subtopic(123)
        except Exception as e:
            result = e

        # Assert
        assert isinstance(result, ValueError)
        assert "string" in str(result)
        assert "dictionary" in str(result)

    def test_add_subtopics_mixed(self):
        """Test adding multiple subtopics as a mix of strings and Topic instances."""

        # Arrange
        topic = Topic(id="git")
        subtopic1 = "git-commit"
        subtopic2 = Topic(id="git-branch", description="Managing branches in Git")
        subtopics = [subtopic1, subtopic2]

        # Act
        topic.add_subtopics(subtopics)

        # Assert
        assert subtopic1 in topic.subtopics
        assert subtopic2.id in topic.subtopics

    def test_add_pretopic_string(self):
        """Test adding a pretopic as a string."""

        # Arrange
        topic = Topic(id="git")
        pretopic_id = "version-control"

        # Act
        topic.add_pretopic(pretopic_id)

        # Assert
        assert pretopic_id in topic.pretopics

    def test_add_pretopic_topic(self):
        """Test adding a pretopic as a Topic instance."""

        # Arrange
        topic = Topic(id="git")
        pretopic = Topic(
            id="version-control",
            description="Managing changes to code over time",
        )

        # Act
        topic.add_pretopic(pretopic)

        # Assert
        assert pretopic.id in topic.pretopics

    def test_add_pretopic_invalid_type(self):
        """Test that adding a pretopic with invalid type raises ValueError."""

        # Arrange
        topic = Topic(id="git")

        # Act
        result = None
        try:
            topic.add_pretopic(123)
        except Exception as e:
            result = e

        # Assert
        assert isinstance(result, ValueError)
        assert "string" in str(result)
        assert "dictionary" in str(result)

    def test_add_pretopics_mixed(self):
        """Test adding multiple pretopics as a mix of strings and Topic instances."""

        # Arrange
        topic = Topic(id="git")
        pretopic1 = "version-control"
        pretopic2 = Topic(
            id="software-development",
            description="The process of creating software",
        )
        pretopics = [pretopic1, pretopic2]

        # Act
        topic.add_pretopics(pretopics)

        # Assert
        assert pretopic1 in topic.pretopics
        assert pretopic2.id in topic.pretopics

    def test_to_dict(self):
        """Test converting a Topic to JSON."""

        # Arrange
        topic = Topic(
            id="git-merge",
            description="Combining branches in Git",
            subtopics=["git-branch", "git-commit"],
            pretopics=["cli"],
        )

        # Act
        topic_json = topic.to_dict()

        # Assert
        assert topic_json["id"] == "git-merge"
        assert topic_json["description"] == "Combining branches in Git"
        assert "git-branch" in topic_json["subtopics"]
        assert "git-commit" in topic_json["subtopics"]
        assert "cli" in topic_json["pretopics"]

    def test_to_json(self):
        """Test converting a Topic to JSON string."""

        # Arrange
        topic = Topic(
            id="git-merge",
            description="Combining branches in Git",
            subtopics=["git-branch", "git-commit"],
            pretopics=["cli"],
        )

        # Act
        topic_json_str = topic.to_json()
        topic_json = json.loads(topic_json_str)

        # Assert
        assert topic_json["id"] == "git-merge"
        assert topic_json["description"] == "Combining branches in Git"
        assert "git-branch" in topic_json["subtopics"]
        assert "git-commit" in topic_json["subtopics"]
        assert "cli" in topic_json["pretopics"]

    # Debugging
    def test_topic_repr(self):
        """Check string representation of a Topic"""

        # Arrange
        topic = Topic(id="git", description="Git version control")

        # Act
        repr_str = repr(topic)

        # Assert
        assert "git" in repr_str
        assert "Git version control" in repr_str
        assert "Topic" in repr_str


class TestTopicIdentifierValidation:
    """Tests for Topic ID kebab-case validation."""

    # Valid identifiers
    def test_valid_single_word(self):
        """Test that single word lowercase IDs are valid."""

        # Arrange
        id = "topic"

        # Act
        topic = Topic(id=id)

        # Assert
        assert topic.id == id

    def test_valid_kebab_case(self):
        """Test that kebab-case IDs are valid."""

        # Arrange
        id = "topic-id"

        # Act
        topic = Topic(id=id)

        # Assert
        assert topic.id == id

    def test_valid_with_numbers(self):
        """Test that kebab-case with numbers is valid."""

        # Arrange
        id = "math-level-1"

        # Act
        topic = Topic(id=id)

        # Assert
        assert topic.id == id

    def test_valid_multiple_hyphens(self):
        """Test that multiple hyphen-separated parts are valid."""

        # Arrange
        id = "multi-part-topic-name"

        # Act
        topic = Topic(id=id)

        # Assert
        assert topic.id == id

    # Invalid identifiers - construction time
    def test_invalid_uppercase_construction(self):
        """Test that uppercase letters are rejected during construction."""

        # Arrange
        invalid_id = "Topic"

        # Act
        result = None
        try:
            Topic(id=invalid_id)
        except Exception as e:
            result = e

        # Assert
        assert isinstance(result, ValueError)
        assert "kebab-case" in str(result)

    def test_invalid_mixed_case_construction(self):
        """Test that mixed case is rejected during construction."""

        # Arrange
        invalid_id = "Topic-Id"

        # Act
        result = None
        try:
            Topic(id=invalid_id)
        except Exception as e:
            result = e

        # Assert
        assert isinstance(result, ValueError)
        assert "kebab-case" in str(result)

    def test_invalid_underscore_construction(self):
        """Test that underscores are rejected during construction."""

        # Arrange
        invalid_id = "topic_id"

        # Act
        result = None
        try:
            Topic(id=invalid_id)
        except Exception as e:
            result = e

        # Assert
        assert isinstance(result, ValueError)
        assert "kebab-case" in str(result)

    def test_invalid_double_hyphen_construction(self):
        """Test that double hyphens are rejected during construction."""

        # Arrange
        invalid_id = "topic--id"

        # Act
        result = None
        try:
            Topic(id=invalid_id)
        except Exception as e:
            result = e

        # Assert
        assert isinstance(result, ValueError)
        assert "kebab-case" in str(result)

    def test_invalid_leading_hyphen_construction(self):
        """Test that leading hyphens are rejected during construction."""

        # Arrange
        invalid_id = "-topic"

        # Act
        result = None
        try:
            Topic(id=invalid_id)
        except Exception as e:
            result = e

        # Assert
        assert isinstance(result, ValueError)
        assert "kebab-case" in str(result)

    def test_invalid_trailing_hyphen_construction(self):
        """Test that trailing hyphens are rejected during construction."""

        # Arrange
        invalid_id = "topic-"

        # Act
        result = None
        try:
            Topic(id=invalid_id)
        except Exception as e:
            result = e

        # Assert
        assert isinstance(result, ValueError)
        assert "kebab-case" in str(result)

    def test_invalid_empty_string_construction(self):
        """Test that empty strings are rejected during construction."""

        # Arrange
        invalid_id = ""

        # Act
        result = None
        try:
            Topic(id=invalid_id)
        except Exception as e:
            result = e

        # Assert
        assert isinstance(result, ValueError)
        assert "cannot be empty" in str(result)

    # Invalid identifiers - property update
    def test_invalid_uppercase_update(self):
        """Test that uppercase letters are rejected during property update."""

        # Arrange
        topic = Topic(id="valid-id")
        invalid_id = "Invalid"

        # Act
        result = None
        try:
            topic.id = invalid_id
        except Exception as e:
            result = e

        # Assert
        assert isinstance(result, ValueError)
        assert "kebab-case" in str(result)

    def test_invalid_underscore_update(self):
        """Test that underscores are rejected during property update."""

        # Arrange
        topic = Topic(id="valid-id")
        invalid_id = "invalid_id"

        # Act
        result = None
        try:
            topic.id = invalid_id
        except Exception as e:
            result = e

        # Assert
        assert isinstance(result, ValueError)
        assert "kebab-case" in str(result)
