"""Tests for the TranscriptEntry class."""

from datetime import datetime
from openproficiency import TranscriptEntry, ProficiencyScore, ProficiencyScoreName


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
            issuer=issuer
        )

        # Assert
        assert entry.user_id == user_id
        assert entry._proficiency_score.topic_id == topic_id
        assert entry._proficiency_score.score == score
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
            timestamp=timestamp
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
            issuer=issuer
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
            issuer="github-learn"
        )

        # Act
        topic_id = entry.proficiency_score.topic_id
        score = entry.proficiency_score.score

        # Assert
        assert topic_id == "git-commit"
        assert score == 0.8

    # Debugging
    def test_repr(self):
        """Test string representation of TranscriptEntry."""

        # Arrange
        entry = TranscriptEntry(
            user_id="user-123",
            topic_id="git-commit",
            score=0.8,
            issuer="github-learn"
        )

        # Act
        repr_str = repr(entry)

        # Assert
        assert "TranscriptEntry" in repr_str
        assert "user-123" in repr_str
        assert "git-commit" in repr_str
        assert "0.8" in repr_str
        assert "github-learn" in repr_str
