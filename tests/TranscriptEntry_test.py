"""Tests for the TranscriptEntry class."""

import json
from datetime import datetime
from openproficiency import TranscriptEntry, TopicList


class TestTranscriptEntry:

    # Initializers
    def test_init_required_params(self):
        """Create a transcript entry with required fields."""

        # Arrange
        user_id = "user-123"
        topic_id = "git-commit"
        topic_list = "example.com/math@0.0.1"
        score = 0.8
        issuer = "github-learn"
        timestamp = datetime(2024, 1, 15, 10, 30, 0)

        # Act
        entry = TranscriptEntry(
            user_id=user_id,
            topic_id=topic_id,
            topic_list=topic_list,
            score=score,
            issuer=issuer,
            timestamp=timestamp,
        )

        # Assert
        assert entry.user_id == user_id
        assert entry.proficiency_score.topic_id == topic_id
        assert entry.proficiency_score.score == score
        assert entry.topic_list == topic_list
        assert entry.timestamp == timestamp
        assert entry.issuer == issuer
        assert entry.certificate is None

    def test_init_with_optional_params(self):
        """Create a transcript entry with optional parameters."""

        # Arrange
        user_id = "user-123"
        topic_id = "git-commit"
        score = 0.8
        issuer = "github-learn"
        topic_list = "example.com/math@0.0.1"
        timestamp = datetime(2024, 1, 15, 10, 30, 0)
        certificate = "test-certificate"

        # Act
        entry = TranscriptEntry(
            user_id=user_id,
            topic_id=topic_id,
            topic_list=topic_list,
            score=score,
            issuer=issuer,
            certificate=certificate,
            timestamp=timestamp,
        )

        # Assert
        assert entry.timestamp == timestamp
        assert entry.certificate == certificate

    # Properties
    def test_proficiency_score(self):
        """Test that proficiency_score topic and score."""

        # Arrange
        entry = TranscriptEntry(
            user_id="user-123",
            topic_id="git-commit",
            topic_list="example.com/math@0.0.1",
            score=0.8,
            issuer="github-learn",
            timestamp=datetime(2024, 1, 15, 10, 30, 0),
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
            topic_list="example.com/math@0.0.1",
            score=0.8,
            issuer="github-learn",
            certificate="cert-data",
            timestamp=datetime(2024, 1, 15, 10, 30, 0),
        )

        # Act
        entry_dict = entry.to_dict()

        # Assert
        assert entry_dict == {
            "user_id": "user-123",
            "topic": "git-commit",
            "topic_list": "example.com/math@0.0.1",
            "score": 0.8,
            "timestamp": "2024-01-15T10:30:00",
            "issuer": "github-learn",
            "certificate": "cert-data",
        }

    def test_to_json(self):
        """Test conversion of TranscriptEntry to JSON string."""

        # Arrange
        entry = TranscriptEntry(
            user_id="user-123",
            topic_id="git-commit",
            topic_list="example.com/math@0.0.1",
            score=0.8,
            issuer="github-learn",
            certificate="cert-data",
            timestamp=datetime(2024, 1, 15, 10, 30, 0),
        )

        # Act
        json_str = entry.to_json()

        # Assert
        data = json.loads(json_str)
        assert data["userID"] == "user-123"
        assert data["topic"] == "git-commit"
        assert data["topicList"] == "example.com/math@0.0.1"
        assert data["score"] == 0.8
        assert data["timestamp"] == "2024-01-15T10:30:00"
        assert data["issuer"] == "github-learn"
        assert data["certificate"] == "cert-data"

    # Methods - Static
    def test_from_dict(self):
        """Test creating TranscriptEntry from dictionary."""

        # Arrange
        data = {
            "user_id": "user-456",
            "topic": "git-branch",
            "topic_list": "example.com/math@0.0.1",
            "score": 0.6,
            "timestamp": "2024-02-20T15:45:30",
            "issuer": "test-issuer",
            "certificate": "cert-abc",
        }

        # Act
        entry = TranscriptEntry.from_dict(data)

        # Assert
        assert entry.user_id == "user-456"
        assert entry.proficiency_score.topic_id == "git-branch"
        assert entry.proficiency_score.score == 0.6
        assert entry.topic_list == "example.com/math@0.0.1"
        assert entry.timestamp.isoformat() == "2024-02-20T15:45:30"
        assert entry.issuer == "test-issuer"
        assert entry.certificate == "cert-abc"

    def test_from_json(self):
        """Test creating TranscriptEntry from JSON string."""

        # Arrange
        entry_orig = TranscriptEntry(
            user_id="user-789",
            topic_id="git-merge",
            topic_list="example.com/math@0.0.1",
            score=0.9,
            timestamp=datetime(2024, 3, 10, 8, 20, 15),
            issuer="test-system",
            certificate="cert-xyz",
        )
        json_str = entry_orig.to_json()

        # Act
        entry = TranscriptEntry.from_json(json_str)

        # Assert
        assert entry.user_id == "user-789"
        assert entry.proficiency_score.topic_id == "git-merge"
        assert entry.proficiency_score.score == 0.9
        assert entry.issuer == "test-system"
        assert entry.timestamp.isoformat() == "2024-03-10T08:20:15"
        assert entry.topic_list == "example.com/math@0.0.1"
        assert entry.certificate == "cert-xyz"

    def test_json_round_trip_preserves_fields(self):
        """Round-trip JSON preserves topic list fields and certificate."""

        # Arrange
        entry = TranscriptEntry(
            user_id="user-123",
            topic_id="git-commit",
            topic_list="example.com/math@0.0.1",
            score=0.8,
            timestamp=datetime(2024, 1, 15, 10, 30, 0),
            issuer="github-learn",
            certificate="cert-data",
        )

        # Act
        json_str = entry.to_json()
        round_trip = TranscriptEntry.from_json(json_str)

        # Assert
        assert round_trip.user_id == "user-123"
        assert round_trip.proficiency_score.topic_id == "git-commit"
        assert round_trip.topic_list == "example.com/math@0.0.1"
        assert round_trip.proficiency_score.score == 0.8
        assert round_trip.timestamp.isoformat() == "2024-01-15T10:30:00"
        assert round_trip.issuer == "github-learn"
        assert round_trip.certificate == "cert-data"

    # Debugging
    def test_repr(self):
        """Test string representation of TranscriptEntry."""

        # Arrange
        entry = TranscriptEntry(
            user_id="user-123",
            topic_id="git-commit",
            topic_list="example.com/math@0.0.1",
            score=0.8,
            timestamp=datetime(2024, 1, 15, 10, 30, 0),
            issuer="github-learn",
        )

        # Act
        repr_str = repr(entry)

        # Assert
        assert "TranscriptEntry" in repr_str
        assert "user-123" in repr_str
        assert "git-commit" in repr_str
        assert "0.8" in repr_str
