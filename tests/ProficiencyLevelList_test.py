"""Tests for the ProficiencyLevelList class."""

import json
from datetime import datetime
from typing import Any, Dict
from openproficiency import (
    ProficiencyLevelList,
    ProficiencyLevel,
    TopicList,
    Topic,
)


class TestProficiencyLevelList:

    # Initializers
    def test_init_required_params(self):
        """Create a level list with required params."""

        # Arrange
        owner = "example.com"
        name = "proficiency-levels"
        version = "1.0.0"
        timestamp = "2025-01-15T10:30:00+00:00"
        certificate = "https://example.com/cert.pem"

        # Act
        level_list = ProficiencyLevelList(
            owner=owner,
            name=name,
            version=version,
            timestamp=timestamp,
            certificate=certificate,
        )

        # Assert
        assert level_list.owner == owner
        assert level_list.name == name
        assert level_list.version == version
        assert level_list.certificate == certificate
        assert level_list.levels == {}
        assert level_list.dependencies == {}

    def test_init_with_description(self):
        """Create a level list with description field."""

        # Arrange
        owner = "example.com"
        name = "proficiency-levels"
        version = "1.0.0"
        timestamp = "2025-01-15T10:30:00+00:00"
        certificate = "https://example.com/cert.pem"
        description = "Standard proficiency levels for the platform"

        # Act
        level_list = ProficiencyLevelList(
            owner=owner,
            name=name,
            version=version,
            timestamp=timestamp,
            certificate=certificate,
            description=description,
        )

        # Assert
        assert level_list.owner == owner
        assert level_list.name == name
        assert level_list.description == description

    def test_init_with_version(self):
        """Create a level list with custom version."""

        # Arrange
        owner = "example.com"
        name = "proficiency-levels"
        version = "1.2.0"
        timestamp = "2025-01-15T10:30:00+00:00"
        certificate = "https://example.com/cert.pem"

        # Act
        level_list = ProficiencyLevelList(
            owner=owner,
            name=name,
            version=version,
            timestamp=timestamp,
            certificate=certificate,
        )

        # Assert
        assert level_list.version == version

    def test_init_with_timestamp(self):
        """Create a level list with custom timestamp."""

        # Arrange
        owner = "example.com"
        name = "proficiency-levels"
        version = "1.0.0"
        timestamp = "2025-01-15T10:30:00+00:00"
        certificate = "https://example.com/cert.pem"

        # Act
        level_list = ProficiencyLevelList(
            owner=owner,
            name=name,
            version=version,
            timestamp=timestamp,
            certificate=certificate,
        )

        # Assert
        assert isinstance(level_list.timestamp, datetime)
        assert level_list.timestamp.isoformat() == timestamp

    def test_init_with_certificate(self):
        """Create a level list with certificate field."""

        # Arrange
        owner = "example.com"
        name = "proficiency-levels"
        version = "1.0.0"
        timestamp = "2025-01-15T10:30:00+00:00"
        certificate = "https://example.com/cert.pem"

        # Act
        level_list = ProficiencyLevelList(
            owner=owner,
            name=name,
            version=version,
            timestamp=timestamp,
            certificate=certificate,
        )

        # Assert
        assert level_list.certificate == certificate

    # Properties - Owner
    def test_owner_validation(self):
        """Test that owner is validated as hostname."""

        # Act & Assert
        try:
            ProficiencyLevelList(
                owner="not a hostname!",
                name="test",
                version="1.0.0",
                timestamp="2025-01-15T10:30:00+00:00",
                certificate="cert",
            )
            assert False, "Expected ValueError for invalid hostname"
        except ValueError as e:
            assert "hostname" in str(e).lower()

    # Properties - Name
    def test_name_validation(self):
        """Test that name is validated as kebab-case."""

        # Act & Assert
        try:
            ProficiencyLevelList(
                owner="example.com",
                name="InvalidName",
                version="1.0.0",
                timestamp="2025-01-15T10:30:00+00:00",
                certificate="cert",
            )
            assert False, "Expected ValueError for invalid kebab-case"
        except ValueError as e:
            assert "kebab-case" in str(e).lower()

    def test_name_change(self):
        """Test changing name after creation."""

        # Arrange
        level_list = ProficiencyLevelList(
            owner="example.com",
            name="original-name",
            version="1.0.0",
            timestamp="2025-01-15T10:30:00+00:00",
            certificate="cert",
        )

        # Act
        level_list.name = "new-name"

        # Assert
        assert level_list.name == "new-name"

    # Properties - Version
    def test_version_validation(self):
        """Test that version must be semantic versioning."""

        # Act & Assert
        try:
            ProficiencyLevelList(
                owner="example.com",
                name="test",
                version="1.2",
                timestamp="2025-01-15T10:30:00+00:00",
                certificate="cert",
            )
            assert False, "Expected ValueError for invalid version"
        except ValueError as e:
            assert "semantic versioning" in str(e).lower()

    def test_version_set_valid(self):
        """Test setting a valid version."""

        # Arrange
        level_list = ProficiencyLevelList(
            owner="example.com",
            name="test",
            version="1.0.0",
            timestamp="2025-01-15T10:30:00+00:00",
            certificate="cert",
        )

        # Act
        level_list.version = "2.3.1"

        # Assert
        assert level_list.version == "2.3.1"

    # Properties - Timestamp
    def test_timestamp_from_iso_string(self):
        """Test setting timestamp from ISO string."""

        # Arrange
        iso_string = "2025-06-15T14:30:00+00:00"

        # Act
        level_list = ProficiencyLevelList(
            owner="example.com",
            name="test",
            version="1.0.0",
            timestamp=iso_string,
            certificate="cert",
        )

        # Assert
        assert level_list.timestamp.isoformat() == iso_string

    def test_timestamp_from_z_format(self):
        """Test setting timestamp from Z-format string."""

        # Arrange
        z_string = "2025-06-15T14:30:00Z"

        # Act
        level_list = ProficiencyLevelList(
            owner="example.com",
            name="test",
            version="1.0.0",
            timestamp=z_string,
            certificate="cert",
        )

        # Assert
        assert level_list.timestamp.isoformat() == "2025-06-15T14:30:00+00:00"

    def test_timestamp_from_datetime(self):
        """Test setting timestamp from datetime object."""

        # Arrange
        dt = datetime(2025, 6, 15, 14, 30, 0)

        # Act
        level_list = ProficiencyLevelList(
            owner="example.com",
            name="test",
            version="1.0.0",
            timestamp=dt,
            certificate="cert",
        )

        # Assert
        assert level_list.timestamp == dt

    # Properties - Full Name
    def test_full_name_without_version(self):
        """Test full name when version is set (version is required)."""

        # Arrange
        level_list = ProficiencyLevelList(
            owner="example.com",
            name="test-levels",
            version="1.0.0",
            timestamp="2025-01-15T10:30:00+00:00",
            certificate="cert",
        )

        # Act & Assert
        assert level_list.full_name == "example.com/test-levels@1.0.0"

    def test_full_name_with_version(self):
        """Test full name with version."""

        # Arrange
        level_list = ProficiencyLevelList(
            owner="example.com",
            name="test-levels",
            version="2.0.0",
            timestamp="2025-01-15T10:30:00+00:00",
            certificate="cert",
        )

        # Act & Assert
        assert level_list.full_name == "example.com/test-levels@2.0.0"

    # Methods - Add Level
    def test_add_level(self):
        """Test adding a proficiency level without pretopics."""

        # Arrange
        level_list = ProficiencyLevelList(
            owner="example.com",
            name="levels",
            version="1.0.0",
            timestamp="2025-01-15T10:30:00+00:00",
            certificate="cert",
        )
        level = ProficiencyLevel(
            id="beginner",
            description="Beginner level",
        )

        # Act
        level_list.add_level(level)

        # Assert
        assert "beginner" in level_list.levels
        assert level_list.levels["beginner"] == level

    def test_add_level_with_pretopics_and_dependencies(self):
        """Test adding a level with valid pretopics."""

        # Arrange
        math_topic_list = TopicList(
            owner="example.com",
            name="math-topics",
            version="1.0.0",
            timestamp="2025-01-15T10:30:00+00:00",
            certificate="cert",
        )
        math_topic_list.add_topic(Topic(id="addition"))
        math_topic_list.add_topic(Topic(id="subtraction"))

        level_list = ProficiencyLevelList(
            owner="example.com",
            name="math-proficiency-levels",
            version="1.0.0",
            timestamp="2025-01-15T10:30:00+00:00",
            certificate="cert",
            dependencies={
                "math": math_topic_list,
            },
        )

        level = ProficiencyLevel(
            id="beginner",
            description="Beginner level",
            pretopics={
                "math.addition",
                "math.subtraction",
            },
        )

        # Act
        level_list.add_level(level)

        # Assert
        assert "beginner" in level_list.levels
        assert level_list.levels["beginner"] == level

    def test_add_level_duplicate_id_raises_error(self):
        """Test that adding a level with duplicate ID raises error."""

        # Arrange
        level_list = ProficiencyLevelList(
            owner="example.com",
            name="levels",
            version="1.0.0",
            timestamp="2025-01-15T10:30:00+00:00",
            certificate="cert",
        )
        level1 = ProficiencyLevel(id="beginner")
        level2 = ProficiencyLevel(id="beginner")

        level_list.add_level(level1)

        # Act & Assert
        try:
            level_list.add_level(level2)
            assert False, "Expected ValueError for duplicate level ID"
        except ValueError as e:
            assert "already exists" in str(e)

    def test_add_level_invalid_pretopic_format(self):
        """Test that pretopic not in namespace notation raises error."""

        # Arrange
        level_list = ProficiencyLevelList(
            owner="example.com",
            name="levels",
            version="1.0.0",
            timestamp="2025-01-15T10:30:00+00:00",
            certificate="cert",
        )
        level = ProficiencyLevel(
            id="beginner",
            pretopics={"invalid-pretopic"},
        )

        # Act & Assert
        try:
            level_list.add_level(level)
            assert False, "Expected ValueError for invalid pretopic format"
        except ValueError as e:
            assert "namespace notation" in str(e).lower()

    def test_add_level_missing_dependency_namespace(self):
        """Test that pretopic referencing missing namespace raises error."""

        # Arrange
        level_list = ProficiencyLevelList(
            owner="example.com",
            name="levels",
            version="1.0.0",
            timestamp="2025-01-15T10:30:00+00:00",
            certificate="cert",
        )
        level = ProficiencyLevel(
            id="beginner",
            pretopics={"math.addition"},
        )

        # Act & Assert
        try:
            level_list.add_level(level)
            assert False, "Expected ValueError for missing namespace"
        except ValueError as e:
            assert "unknown namespace" in str(e).lower()

    def test_add_level_topic_not_in_dependency(self):
        """Test that pretopic referencing non-existent topic raises error."""

        # Arrange
        topic_list = TopicList(
            owner="example.com",
            name="math-topics",
            version="1.0.0",
            timestamp="2025-01-15T10:30:00+00:00",
            certificate="cert",
        )
        topic_list.add_topic(Topic(id="addition"))

        level_list = ProficiencyLevelList(
            owner="example.com",
            name="levels",
            version="1.0.0",
            timestamp="2025-01-15T10:30:00+00:00",
            certificate="cert",
        )
        level_list.add_dependency("math", topic_list)

        level = ProficiencyLevel(
            id="beginner",
            pretopics={"math.multiplication"},
        )

        # Act & Assert
        try:
            level_list.add_level(level)
            assert False, "Expected ValueError for non-existent topic"
        except ValueError as e:
            assert "non-existent topic" in str(e).lower()

    # Methods - Add Dependency
    def test_add_dependency(self):
        """Test adding a topic list as dependency."""

        # Arrange
        topic_list = TopicList(
            owner="example.com",
            name="math-topics",
            version="1.0.0",
            timestamp="2025-01-15T10:30:00+00:00",
            certificate="cert",
        )
        level_list = ProficiencyLevelList(
            owner="example.com",
            name="levels",
            version="1.0.0",
            timestamp="2025-01-15T10:30:00+00:00",
            certificate="cert",
        )

        # Act
        level_list.add_dependency("math", topic_list)

        # Assert
        assert "math" in level_list.dependencies
        assert level_list.dependencies["math"] == topic_list

    def test_add_dependency_invalid_namespace(self):
        """Test that invalid namespace format raises error."""

        # Arrange
        topic_list = TopicList(
            owner="example.com",
            name="math-topics",
            version="1.0.0",
            timestamp="2025-01-15T10:30:00+00:00",
            certificate="cert",
        )
        level_list = ProficiencyLevelList(
            owner="example.com",
            name="levels",
            version="1.0.0",
            timestamp="2025-01-15T10:30:00+00:00",
            certificate="cert",
        )

        # Act & Assert
        try:
            level_list.add_dependency("InvalidNamespace", topic_list)
            assert False, "Expected ValueError for invalid namespace"
        except ValueError as e:
            assert "kebab-case" in str(e).lower()

    def test_add_dependency_duplicate_namespace(self):
        """Test that duplicate namespace raises error."""

        # Arrange
        topic_list1 = TopicList(
            owner="example.com",
            name="math-topics",
            version="1.0.0",
            timestamp="2025-01-15T10:30:00+00:00",
            certificate="cert",
        )
        topic_list2 = TopicList(
            owner="example.com",
            name="science-topics",
            version="1.0.0",
            timestamp="2025-01-15T10:30:00+00:00",
            certificate="cert",
        )
        level_list = ProficiencyLevelList(
            owner="example.com",
            name="levels",
            version="1.0.0",
            timestamp="2025-01-15T10:30:00+00:00",
            certificate="cert",
        )
        level_list.add_dependency("namespace", topic_list1)

        # Act & Assert
        try:
            level_list.add_dependency("namespace", topic_list2)
            assert False, "Expected ValueError for duplicate namespace"
        except ValueError as e:
            assert "already exists" in str(e)

    # Methods - to_dict
    def test_to_dict_basic(self):
        """Test converting to dictionary with basic metadata."""

        # Arrange
        level_list = ProficiencyLevelList(
            owner="example.com",
            name="levels",
            version="1.0.0",
            timestamp="2025-01-15T10:30:00+00:00",
            certificate="https://example.com/cert.pem",
            description="Test levels",
        )

        # Act
        data = level_list.to_dict()

        # Assert
        assert data["owner"] == "example.com"
        assert data["name"] == "levels"
        assert data["description"] == "Test levels"
        assert data["version"] == "1.0.0"
        assert data["certificate"] == "https://example.com/cert.pem"
        assert "timestamp" in data
        assert data["proficiency-levels"] == {}

    def test_to_dict_with_levels(self):
        """Test converting to dictionary with levels."""

        # Arrange
        math_topic_list = TopicList(
            owner="example.com",
            name="math-topics",
            version="1.0.0",
            timestamp="2025-01-15T10:30:00+00:00",
            certificate="cert",
        )
        math_topic_list.add_topic(Topic(id="addition"))
        math_topic_list.add_topic(Topic(id="subtraction"))
        math_topic_list.add_topic(Topic(id="multiplication"))
        math_topic_list.add_topic(Topic(id="division"))

        level_list = ProficiencyLevelList(
            owner="example.com",
            name="levels",
            version="1.0.0",
            timestamp="2025-01-15T10:30:00+00:00",
            certificate="cert",
            dependencies={
                "math": math_topic_list,
            },
            levels={
                "beginner": ProficiencyLevel(
                    id="beginner",
                    description="Beginner level",
                    pretopics={
                        "math.addition",
                        "math.subtraction",
                    },
                ),
                "intermediate": ProficiencyLevel(
                    id="intermediate",
                    description="Intermediate level",
                    pretopics={
                        "math.multiplication",
                        "math.division",
                    },
                ),
            },
        )

        # Act
        data = level_list.to_dict()

        # Assert
        assert len(data["proficiency-levels"]) == 2
        assert "beginner" in data["proficiency-levels"]
        assert "intermediate" in data["proficiency-levels"]

        assert data["proficiency-levels"]["beginner"]["id"] == "beginner"
        assert data["proficiency-levels"]["beginner"]["description"] == "Beginner level"
        assert "math.addition" in data["proficiency-levels"]["beginner"]["pretopics"]
        assert "math.subtraction" in data["proficiency-levels"]["beginner"]["pretopics"]

        assert data["proficiency-levels"]["intermediate"]["id"] == "intermediate"
        assert data["proficiency-levels"]["intermediate"]["description"] == "Intermediate level"
        assert "math.multiplication" in data["proficiency-levels"]["intermediate"]["pretopics"]
        assert "math.division" in data["proficiency-levels"]["intermediate"]["pretopics"]

    def test_to_dict_with_dependencies(self):
        """Test converting to dictionary with dependencies."""

        # Arrange
        topic_list = TopicList(
            owner="example.com",
            name="math-topics",
            version="1.0.0",
            timestamp="2025-01-15T10:30:00+00:00",
            certificate="cert",
        )

        level_list = ProficiencyLevelList(
            owner="example.com",
            name="levels",
            version="1.0.0",
            timestamp="2025-01-15T10:30:00+00:00",
            certificate="cert",
        )
        level_list.add_dependency("math", topic_list)

        # Act
        data = level_list.to_dict()

        # Assert
        assert "dependencies" in data
        assert "math" in data["dependencies"]
        assert data["dependencies"]["math"] == "example.com/math-topics@1.0.0"

    # Methods - to_json
    def test_to_json(self):
        """Test converting to JSON string."""

        # Arrange
        level_list = ProficiencyLevelList(
            owner="example.com",
            name="levels",
            version="1.0.0",
            timestamp="2025-01-15T10:30:00+00:00",
            certificate="cert",
        )
        level_list.add_level(ProficiencyLevel(id="beginner"))

        # Act
        json_str = level_list.to_json()

        # Assert
        data = json.loads(json_str)
        assert data["owner"] == "example.com"
        assert data["name"] == "levels"
        assert "beginner" in data["proficiency-levels"]

    # Methods - from_dict
    def test_from_dict_simple(self):
        """Test creating from dictionary with minimal details."""

        # Arrange
        data: Dict[str, Any] = {
            "owner": "example.com",
            "name": "levels",
            "description": "Test levels",
            "version": "1.0.0",
            "timestamp": "2025-01-15T10:30:00+00:00",
            "certificate": "--- cert ---",
        }

        # Act
        level_list = ProficiencyLevelList.from_dict(data)

        # Assert
        assert level_list.owner == "example.com"
        assert level_list.name == "levels"
        assert level_list.description == "Test levels"
        assert level_list.version == "1.0.0"
        assert level_list.timestamp.isoformat() == "2025-01-15T10:30:00+00:00"
        assert level_list.certificate == "--- cert ---"

    def test_from_dict_levels_dependencies(self):
        """Test creating from dictionary with levels and dependencies."""

        # Arrange
        data: Dict[str, Any] = {
            "owner": "example.com",
            "name": "levels",
            "version": "1.0.0",
            "timestamp": "2025-01-15T10:30:00+00:00",
            "certificate": "cert",
            "proficiency-levels": {
                "beginner": {
                    "description": "Beginner level",
                    "pretopics": [],
                },
                "advanced": {
                    "description": "Advanced level",
                    "pretopics": [],
                },
            },
            "dependencies": {
                "math": "example.com/math-topics@1.0.0",
            },
        }

        # Act
        level_list = ProficiencyLevelList.from_dict(data)

        # Assert
        assert len(level_list.levels) == 2
        assert "beginner" in level_list.levels
        assert "advanced" in level_list.levels
        assert level_list.levels["beginner"].description == "Beginner level"

        assert "math" in level_list.dependencies
        assert level_list.dependencies["math"].owner == "example.com"
        assert level_list.dependencies["math"].name == "math-topics"
        assert level_list.dependencies["math"].version == "1.0.0"

    # Methods - from_json
    def test_from_json_basic(self):
        """Test creating from JSON string."""

        # Arrange
        json_str = json.dumps(
            {
                "owner": "example.com",
                "name": "levels",
                "description": "Test levels",
                "version": "1.0.0",
                "timestamp": "2025-01-15T10:30:00+00:00",
                "certificate": "--- cert ---",
            }
        )

        # Act
        level_list = ProficiencyLevelList.from_json(json_str)

        # Assert
        assert level_list.owner == "example.com"
        assert level_list.name == "levels"
        assert level_list.description == "Test levels"
        assert level_list.version == "1.0.0"
        assert level_list.timestamp.isoformat() == "2025-01-15T10:30:00+00:00"
        assert level_list.certificate == "--- cert ---"

    def test_from_json_with_levels(self):
        """Test creating from JSON string with levels and dependencies."""

        # Arrange
        json_str = json.dumps(
            {
                "owner": "example.com",
                "name": "levels",
                "version": "1.0.0",
                "timestamp": "2025-01-15T10:30:00+00:00",
                "certificate": "cert",
                "proficiency-levels": {
                    "beginner": {
                        "description": "Beginner level",
                        "pretopics": [],
                    },
                    "advanced": {
                        "description": "Advanced level",
                        "pretopics": [],
                    },
                },
                "dependencies": {
                    "math": "example.com/math-topics@1.0.0",
                },
            }
        )

        # Act
        level_list = ProficiencyLevelList.from_json(json_str)

        # Assert
        assert len(level_list.levels) == 2
        assert "beginner" in level_list.levels
        assert "advanced" in level_list.levels
        assert level_list.levels["beginner"].description == "Beginner level"

        assert "math" in level_list.dependencies
        assert level_list.dependencies["math"].owner == "example.com"
        assert level_list.dependencies["math"].name == "math-topics"
        assert level_list.dependencies["math"].version == "1.0.0"

    def test_from_json_invalid_input(self):
        """Test that non-JSON input raises error."""

        # Arrange
        json_str = "not a json string"

        # Act
        result = None
        try:
            ProficiencyLevelList.from_json(json_data=json_str)
        except Exception as e:
            result = e

        # Assert
        assert isinstance(result, json.JSONDecodeError)

    # Methods - Round trip (to_dict -> from_dict)
    def test_round_trip_to_dict_from_dict(self):
        """Test converting to dict and back preserves data."""

        # Arrange
        topic_list = TopicList(
            owner="example.com",
            name="math-topics",
            version="1.0.0",
            timestamp="2025-01-15T10:30:00+00:00",
            certificate="cert",
        )
        topic_list.add_topic(Topic(id="addition"))
        topic_list.add_topic(Topic(id="subtraction"))

        level_list = ProficiencyLevelList(
            owner="example.com",
            name="levels",
            description="Math proficiency levels",
            version="1.0.0",
            timestamp="2025-01-15T10:30:00+00:00",
            certificate="https://example.com/cert.pem",
            levels={
                "beginner": ProficiencyLevel(
                    id="beginner",
                    description="Beginner level",
                    pretopics={
                        "math.addition",
                    },
                ),
                "intermediate": ProficiencyLevel(
                    id="intermediate",
                    description="Intermediate level",
                    pretopics={
                        "math.subtraction",
                    },
                ),
            },
            dependencies={
                "math": topic_list,
            },
        )

        # Act
        data = level_list.to_dict()
        result = ProficiencyLevelList.from_dict(data)

        # Assert
        assert result.owner == level_list.owner
        assert result.name == level_list.name
        assert result.description == level_list.description
        assert result.version == level_list.version
        assert result.timestamp == level_list.timestamp
        assert result.certificate == level_list.certificate

        assert len(result.dependencies) == 1
        assert "math" in result.dependencies
        assert result.dependencies["math"].full_name == topic_list.full_name

        assert len(result.levels) == 2
        assert result.levels["beginner"].description == "Beginner level"
        assert "math.addition" in result.levels["beginner"].pretopics
        assert result.levels["intermediate"].description == "Intermediate level"
        assert "math.subtraction" in result.levels["intermediate"].pretopics

    def test_round_trip_to_json_from_json(self):
        """Test converting to JSON and back preserves data."""

        # Arrange
        topic_list = TopicList(
            owner="example.com",
            name="math-topics",
            version="1.0.0",
            timestamp="2025-01-15T10:30:00+00:00",
            certificate="cert",
        )
        topic_list.add_topic(Topic(id="addition"))
        topic_list.add_topic(Topic(id="subtraction"))

        level_list = ProficiencyLevelList(
            owner="example.com",
            name="levels",
            description="Math proficiency levels",
            version="1.0.0",
            timestamp="2025-01-15T10:30:00+00:00",
            certificate="https://example.com/cert.pem",
            dependencies={
                "math": topic_list,
            },
        )
        level_list.add_level(
            ProficiencyLevel(
                id="beginner",
                description="Beginner level",
                pretopics={
                    "math.addition",
                },
            )
        )
        level_list.add_level(
            ProficiencyLevel(
                id="intermediate",
                description="Intermediate level",
                pretopics={
                    "math.subtraction",
                },
            )
        )

        # Act
        json_str = level_list.to_json()
        result = ProficiencyLevelList.from_json(json_str)
        round_trip_json = result.to_json()

        # Assert
        data = json.loads(json_str)
        round_trip_data = json.loads(round_trip_json)
        assert round_trip_data == data

    # Debugging
    def test_repr(self):
        """Test string representation."""

        # Arrange
        topic_list = TopicList(
            owner="example.com",
            name="math-topics",
            version="1.0.0",
            timestamp="2025-01-15T10:30:00+00:00",
            certificate="cert",
        )
        topic_list.add_topic(Topic(id="addition"))

        level_list = ProficiencyLevelList(
            owner="example.com",
            name="levels",
            version="1.0.0",
            timestamp="2025-01-15T10:30:00+00:00",
            certificate="cert",
        )
        level_list.add_dependency("math", topic_list)
        level_list.add_level(ProficiencyLevel(id="beginner"))
        level_list.add_level(ProficiencyLevel(id="advanced"))

        # Act
        repr_str = repr(level_list)

        # Assert
        assert "example.com" in repr_str
        assert "levels" in repr_str
        assert "levels_count=2" in repr_str
        assert "dependencies_count=1" in repr_str
