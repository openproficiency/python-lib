"""Tests for the ProficiencyLevel class."""

import json
from openproficiency import ProficiencyLevel


class TestProficiencyLevel:

    # Initializers
    def test_init_required_params(self):
        """Create a proficiency level with required fields only."""

        # Arrange
        id = "beginner"

        # Act
        level = ProficiencyLevel(id=id)

        # Assert
        assert level.id == id
        assert level.description is None
        assert level.pretopics == set()

    def test_init_optional_params(self):
        """Test creating a proficiency level with optional parameters."""

        # Arrange
        id = "intermediate"
        description = "Intermediate level of proficiency"
        pretopics = {"topic-1", "topic-2", "topic-3"}

        # Act
        level = ProficiencyLevel(
            id=id,
            description=description,
            pretopics=pretopics,
        )

        # Assert
        assert level.id == id
        assert level.description == description
        assert len(level.pretopics) == 3
        assert "topic-1" in level.pretopics
        assert "topic-2" in level.pretopics
        assert "topic-3" in level.pretopics

    # Properties - ID
    def test_id(self):
        """Test that ID setter works."""

        # Arrange
        level = ProficiencyLevel(id="level-1")
        new_id = "beginner"

        # Act
        level.id = new_id

        # Assert
        assert level.id == new_id

    # Properties - Description
    def test_description(self):
        """Test that valid descriptions are accepted."""

        # Arrange
        level = ProficiencyLevel(id="beginner")
        desc = "Short description"

        # Act
        level.description = desc

        # Assert
        assert level.description == desc

    def test_description_too_long(self):
        """Test that descriptions over 100 characters raise ValueError."""

        # Arrange
        level = ProficiencyLevel(id="beginner")
        long_description = "a" * 101

        # Act & Assert
        try:
            level.description = long_description
            assert False, "Expected ValueError for description too long"
        except ValueError as e:
            assert "100 characters" in str(e)

    def test_description_init_too_long(self):
        """Test that init with too-long description raises ValueError."""

        # Act & Assert
        try:
            ProficiencyLevel(id="beginner", description="a" * 101)
            assert False, "Expected ValueError for description too long"
        except ValueError as e:
            assert "100 characters" in str(e)

    # Methods - Pretopics
    def test_add_pretopic_string(self):
        """Test adding a pretopic as a string."""

        # Arrange
        level = ProficiencyLevel(id="beginner")
        pretopic_id = "git-basics"

        # Act
        level.add_pretopic(pretopic_id)

        # Assert
        assert pretopic_id in level.pretopics

    def test_add_pretopic_with_existing_pretopics(self):
        """Test adding a pretopic when level already has pretopics."""

        # Arrange
        level = ProficiencyLevel(id="intermediate", pretopics={"existing-topic"})
        new_pretopic = "new-topic"

        # Act
        level.add_pretopic(new_pretopic)

        # Assert
        assert new_pretopic in level.pretopics
        assert "existing-topic" in level.pretopics

    def test_add_pretopic_no_duplicates(self):
        """Test that duplicate pretopics are not added."""

        # Arrange
        level = ProficiencyLevel(id="beginner")
        pretopic_id = "git-basics"

        # Act
        level.add_pretopic(pretopic_id)
        level.add_pretopic(pretopic_id)

        # Assert
        assert len(level.pretopics) == 1
        assert pretopic_id in level.pretopics

    def test_add_pretopics_no_duplicates(self):
        """Test adding multiple pretopics."""

        # Arrange
        level = ProficiencyLevel(id="intermediate")
        pretopic_ids = {"git-basics", "cli-basics", "version-control"}

        # Act
        level.add_pretopics(pretopic_ids)

        # Assert
        assert len(level.pretopics) == 3
        for pretopic_id in pretopic_ids:
            assert pretopic_id in level.pretopics

    def test_add_pretopics_to_existing(self):
        """Test adding multiple pretopics to an existing set."""

        # Arrange
        level = ProficiencyLevel(id="intermediate", pretopics={"existing-topic"})
        new_pretopics = {"git-basics", "cli-basics"}

        # Act
        level.add_pretopics(new_pretopics)

        # Assert
        assert "existing-topic" in level.pretopics
        assert "git-basics" in level.pretopics
        assert "cli-basics" in level.pretopics
        assert len(level.pretopics) == 3

    def test_remove_pretopic(self):
        """Test removing a pretopic."""

        # Arrange
        level = ProficiencyLevel(id="intermediate", pretopics={"git-basics", "cli-basics"})

        # Act
        level.remove_pretopic("git-basics")

        # Assert
        assert "git-basics" not in level.pretopics
        assert "cli-basics" in level.pretopics

    def test_remove_pretopic_nonexistent(self):
        """Test removing a pretopic that doesn't exist."""

        # Arrange
        level = ProficiencyLevel(id="intermediate", pretopics={"git-basics"})

        # Act
        level.remove_pretopic("nonexistent-topic")

        # Assert
        assert level.pretopics == {"git-basics"}

    # Methods - to_dict and to_json
    def test_to_dict(self):
        """Test conversion to dictionary."""

        # Arrange
        level = ProficiencyLevel(
            id="intermediate",
            description="Intermediate level",
            pretopics={"git-basics", "cli-basics"},
        )

        # Act
        result = level.to_dict()

        # Assert
        assert isinstance(result, dict)
        assert result["id"] == "intermediate"
        assert result["description"] == "Intermediate level"
        assert isinstance(result["pretopics"], list)
        assert "git-basics" in result["pretopics"]
        assert "cli-basics" in result["pretopics"]

    def test_to_dict_empty_pretopics(self):
        """Test to_dict with empty pretopics."""

        # Arrange
        level = ProficiencyLevel(id="beginner", description="Beginner")

        # Act
        result = level.to_dict()

        # Assert
        assert result["pretopics"] == []

    def test_to_json(self):
        """Test conversion to JSON string."""

        # Arrange
        level = ProficiencyLevel(
            id="intermediate",
            description="Intermediate level",
            pretopics={"git-basics", "cli-basics"},
        )

        # Act
        json_str = level.to_json()

        # Assert
        assert isinstance(json_str, str)
        parsed = json.loads(json_str)
        assert parsed["id"] == "intermediate"
        assert parsed["description"] == "Intermediate level"
        assert isinstance(parsed["pretopics"], list)
        assert "git-basics" in parsed["pretopics"]
        assert "cli-basics" in parsed["pretopics"]

    # Methods - from_dict and from_json
    def test_from_dict_all_fields(self):
        """Test creating ProficiencyLevel from dict with all fields."""

        # Arrange
        data = {
            "id": "intermediate",
            "description": "Intermediate level",
            "pretopics": ["git-basics", "cli-basics"],
        }

        # Act
        level = ProficiencyLevel.from_dict(data)

        # Assert
        assert level.id == "intermediate"
        assert level.description == "Intermediate level"
        assert level.pretopics == {"git-basics", "cli-basics"}

    def test_from_dict_minimal_fields(self):
        """Test creating ProficiencyLevel from dict with only required fields."""

        # Arrange
        data = {"id": "beginner"}

        # Act
        level = ProficiencyLevel.from_dict(data)

        # Assert
        assert level.id == "beginner"
        assert level.description == ""
        assert level.pretopics == set()

    def test_from_json_valid(self):
        """Test creating ProficiencyLevel from valid JSON string."""

        # Arrange
        json_data = {
            "id": "intermediate",
            "description": "Intermediate level",
            "pretopics": ["git-basics"],
        }
        json_str = json.dumps(json_data)

        # Act
        level = ProficiencyLevel.from_json(json_str)

        # Assert
        assert level.id == "intermediate"
        assert level.description == "Intermediate level"
        assert level.pretopics == {"git-basics"}

    def test_from_json_invalid(self):
        """Test that invalid JSON raises ValueError."""

        # Arrange
        invalid_json = '{"id": "intermediate", invalid json}'

        # Act & Assert
        result = None
        try:
            ProficiencyLevel.from_json(invalid_json)
        except Exception as e:
            result = e

        # Assert
        assert isinstance(result, ValueError)
        assert "Invalid" in str(result)
        assert "JSON" in str(result)

    # Round-trip tests
    def test_to_dict_from_dict_roundtrip(self):
        """Test that to_dict and from_dict are inverse operations."""

        # Arrange
        original = ProficiencyLevel(
            id="advanced",
            description="Advanced level of proficiency",
            pretopics={"topic-1", "topic-2", "topic-3"},
        )

        # Act
        dict_data = original.to_dict()
        restored = ProficiencyLevel.from_dict(dict_data)

        # Assert
        assert restored == original

    def test_to_json_from_json_roundtrip(self):
        """Test that to_json and from_json are inverse operations."""

        # Arrange
        original = ProficiencyLevel(
            id="expert",
            description="Expert level",
            pretopics={"advanced-topic-1", "advanced-topic-2"},
        )

        # Act
        json_str = original.to_json()
        restored = ProficiencyLevel.from_json(json_str)

        # Assert
        assert restored == original

    # Equality and Representation
    def test_equality_same_pretopics(self):
        """Test equality when pretopics are the same."""
        # Arrange
        pretopics = {"topic-1", "topic-2"}

        # Act
        levelA = ProficiencyLevel(id="intermediate", description="level 1", pretopics=pretopics)
        levelB = ProficiencyLevel(id="intermediate", description="beginner", pretopics=pretopics)

        # Assert
        assert levelA == levelB

    def test_equality_different_pretopics(self):
        """Test equality when pretopics are the different."""
        # Arrange
        pretopicsA = {"topic-1", "topic-2"}
        pretopicsB = {"topic-2", "topic-3"}

        # Act
        levelA = ProficiencyLevel(id="intermediate", description="level 1", pretopics=pretopicsA)
        levelB = ProficiencyLevel(id="intermediate", description="beginner", pretopics=pretopicsB)

        # Assert
        assert levelA != levelB

    def test_repr(self):
        """Test string representation."""

        # Arrange
        level = ProficiencyLevel(
            id="intermediate",
            description="Intermediate level",
            pretopics={"topic-1", "topic-2"},
        )

        # Act
        repr_str = repr(level)

        # Assert
        assert "ProficiencyLevel" in repr_str
        assert "intermediate" in repr_str
        assert "Intermediate level" in repr_str
        assert "topic-1" in repr_str or "pretopics" in repr_str

    # Integration tests
    def test_complete_workflow(self):
        """Test a complete workflow with a proficiency level."""

        # Arrange
        # Create a proficiency level with prerequisites
        level = ProficiencyLevel(
            id="intermediate",
            description="Intermediate proficiency",
            pretopics={"beginner", "advanced-basics"},
        )

        # Act
        # Prepare for JSON export
        json_str = level.to_json()

        # Restore from JSON
        restored = ProficiencyLevel.from_json(json_str)

        # Assert
        assert restored.id == "intermediate"
        assert "beginner" in restored.pretopics
        assert "advanced-basics" in restored.pretopics
        assert len(restored.pretopics) == 2
