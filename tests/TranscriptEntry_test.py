"""Tests for the TranscriptEntry class."""

from datetime import datetime
from openproficiency import TranscriptEntry


class TestTranscriptEntry:

    # Initializers
    def test_init_required_params(self):
        """Create a transcript entry with required fields."""

        # Arrange
        user_id = "user-123"
        topic_id = "git-commit"
        score = 0.8
        issuer = "github-learn"

        # Act
        entry = TranscriptEntry(
            user_id=user_id,
            topic_id=topic_id,
            score=score,
            issuer=issuer,
        )

        # Assert
        assert entry.user_id == user_id
        assert entry.proficiency_score.topic_id == topic_id
        assert entry.proficiency_score.score == score
        assert entry.issuer == issuer
        assert entry.timestamp is not None

    def test_init_with_optional_params(self):
        """Create a transcript entry with optional parameters."""

        # Arrange
        user_id = "user-123"
        topic_id = "git-commit"
        score = 0.8
        issuer = "github-learn"
        timestamp = datetime(2024, 1, 15, 10, 30, 0)

        # Act
        entry = TranscriptEntry(
            user_id=user_id,
            topic_id=topic_id,
            score=score,
            issuer=issuer,
            timestamp=timestamp,
        )

        # Assert
        assert entry.timestamp == timestamp

    def test_init_default_timestamp(self):
        """Test that timestamp defaults to current time."""

        # Arrange
        user_id = "user-123"
        topic_id = "git-commit"
        score = 0.8
        issuer = "github-learn"

        # Act
        before = datetime.now()
        entry = TranscriptEntry(
            user_id=user_id,
            topic_id=topic_id,
            score=score,
            issuer=issuer,
        )
        after = datetime.now()

        # Assert
        assert entry.timestamp >= before
        assert entry.timestamp <= after

    # Properties
    def test_proficiency_score(self):
        """Test that proficiency_score topic and score."""

        # Arrange
        entry = TranscriptEntry(
            user_id="user-123",
            topic_id="git-commit",
            score=0.8,
            issuer="github-learn",
        )

        # Act
        topic_id = entry.proficiency_score.topic_id
        score = entry.proficiency_score.score

        # Assert
        assert topic_id == "git-commit"
        assert score == 0.8

    # Methods
    def test_to_dict(self):
        """Test conversion of TranscriptEntry to dictionary."""

        # Arrange
        entry = TranscriptEntry(
            user_id="user-123",
            topic_id="git-commit",
            score=0.8,
            issuer="github-learn",
            timestamp=datetime(2024, 1, 15, 10, 30, 0),
        )

        # Act
        entry_dict = entry.to_dict()

        # Assert
        assert entry_dict == {
            "user_id": "user-123",
            "topic_id": "git-commit",
            "score": 0.8,
            "issuer": "github-learn",
            "timestamp": "2024-01-15T10:30:00",
        }

    def test_to_json(self):
        """Test conversion of TranscriptEntry to JSON string."""

        # Arrange
        entry = TranscriptEntry(
            user_id="user-123",
            topic_id="git-commit",
            score=0.8,
            issuer="github-learn",
            timestamp=datetime(2024, 1, 15, 10, 30, 0),
        )

        # Act
        json_str = entry.to_json()

        # Assert
        expected_json = (
            '{"user_id": "user-123", "topic_id": "git-commit", '
            '"score": 0.8, "issuer": "github-learn", '
            '"timestamp": "2024-01-15T10:30:00"}'
        )
        assert json_str == expected_json

    # Methods - Static
    def test_from_dict(self):
        """Test creating TranscriptEntry from dictionary."""

        # Arrange
        data = {
            "user_id": "user-456",
            "topic_id": "git-branch",
            "score": 0.6,
            "issuer": "test-issuer",
            "timestamp": "2024-02-20T15:45:30",
        }

        # Act
        entry = TranscriptEntry.from_dict(data)

        # Assert
        assert entry.user_id == "user-456"
        assert entry.proficiency_score.topic_id == "git-branch"
        assert entry.proficiency_score.score == 0.6
        assert entry.issuer == "test-issuer"
        assert entry.timestamp.year == 2024
        assert entry.timestamp.month == 2
        assert entry.timestamp.day == 20

    def test_from_json(self):
        """Test creating TranscriptEntry from JSON string."""

        # Arrange
        json_str = (
            '{"user_id": "user-789", "topic_id": "git-merge", '
            '"score": 0.9, "issuer": "test-system", '
            '"timestamp": "2024-03-10T08:20:15"}'
        )

        # Act
        entry = TranscriptEntry.from_json(json_str)

        # Assert
        assert entry.user_id == "user-789"
        assert entry.proficiency_score.topic_id == "git-merge"
        assert entry.proficiency_score.score == 0.9
        assert entry.issuer == "test-system"
        assert entry.timestamp.year == 2024
        assert entry.timestamp.month == 3
        assert entry.timestamp.day == 10

    # Debugging
    def test_repr(self):
        """Test string representation of TranscriptEntry."""

        # Arrange
        entry = TranscriptEntry(
            user_id="user-123",
            topic_id="git-commit",
            score=0.8,
            issuer="github-learn",
        )

        # Act
        repr_str = repr(entry)

        # Assert
        assert "TranscriptEntry" in repr_str
        assert "user-123" in repr_str
        assert "git-commit" in repr_str
        assert "0.8" in repr_str
        assert "github-learn" in repr_str
