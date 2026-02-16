"""Tests for the ProficiencyScore class."""

from openproficiency import ProficiencyScore, ProficiencyScoreName


class TestProficiencyScore:

    # Initializers
    def test_init_with_numeric_score(self):
        """Create a proficiency score with numeric value."""

        # Arrange
        topic_id = "git-commit"
        score = 0.8

        # Act
        ps = ProficiencyScore(
            topic_id=topic_id,
            score=score,
        )

        # Assert
        assert ps.topic_id == topic_id
        assert ps.score == score

    def test_init_with_enum_score(self):
        """Create a proficiency score with ProficiencyScoreName enum."""

        # Arrange
        topic_id = "git-commit"
        score_name = ProficiencyScoreName.PROFICIENT

        # Act
        ps = ProficiencyScore(
            topic_id=topic_id,
            score=score_name,
        )

        # Assert
        assert ps.topic_id == topic_id
        assert ps.score == 0.8

    def test_init_invalid_score_too_low(self):
        """Test that score below 0.0 raises ValueError."""

        # Act
        result = None
        try:
            ProficiencyScore(
                topic_id="test",
                score=-0.1,
            )
        except Exception as e:
            result = e

        # Assert
        assert isinstance(result, ValueError)
        assert "0.0" in str(result)
        assert "1.0" in str(result)

    def test_init_invalid_score_too_high(self):
        """Test that score above 1.0 raises ValueError."""

        # Act
        result = None
        try:
            ProficiencyScore(
                topic_id="test",
                score=1.1,
            )
        except Exception as e:
            result = e

        # Assert
        assert isinstance(result, ValueError)
        assert "0.0" in str(result)
        assert "1.0" in str(result)

    def test_init_invalid_score_type(self):
        """Test that invalid score type raises ValueError."""

        # Act
        result = None
        try:
            ProficiencyScore(
                topic_id="test",
                score="invalid",
            )
        except Exception as e:
            result = e

        # Assert
        assert isinstance(result, ValueError)
        assert "ProficiencyScoreName" in str(result)

    # Properties
    def test_score_numeric(self):
        """Test setting score with numeric value."""

        # Arrange
        ps = ProficiencyScore(
            topic_id="test",
            score=0.1,
        )

        # Act
        ps.score = 0.9

        # Assert
        assert ps.score == 0.9
        assert ps.score_name == ProficiencyScoreName.PROFICIENT

    def test_score_numeric_invalid(self):
        """Test setting invalid numeric score raises ValueError."""

        # Arrange
        ps = ProficiencyScore(
            topic_id="test",
            score=0.1,
        )

        # Act
        result = None
        try:
            ps.score = 1.5
        except Exception as e:
            result = e

        # Assert
        # Check that result is a ValueError and contains the expected message
        assert isinstance(result, ValueError)
        assert "0.0" in str(result)
        assert "1.0" in str(result)

    def test_score_enum(self):
        """Test setting score with enum value."""

        # Arrange
        ps = ProficiencyScore(
            topic_id="test",
            score=0.1,
        )

        # Act
        ps.score = ProficiencyScoreName.FAMILIAR

        # Assert
        assert ps.score == 0.5
        assert ps.score_name == ProficiencyScoreName.FAMILIAR

    def test_score_name_unaware(self):
        """Test score_name property for UNAWARE level."""

        # Arrange
        ps = ProficiencyScore(
            topic_id="test",
            score=0.0,
        )

        # Act
        result = ps.score_name

        # Assert
        assert result == ProficiencyScoreName.UNAWARE

    def test_score_name_aware(self):
        """Test score_name property for AWARE level."""

        # Arrange
        ps = ProficiencyScore(
            topic_id="test",
            score=0.1,
        )

        # Act
        result = ps.score_name

        # Assert
        assert result == ProficiencyScoreName.AWARE

    def test_score_name_familiar(self):
        """Test score_name property for FAMILIAR level."""

        # Arrange
        ps = ProficiencyScore(
            topic_id="test",
            score=0.5,
        )

        # Act
        result = ps.score_name

        # Assert
        assert result == ProficiencyScoreName.FAMILIAR

    def test_score_name_proficient(self):
        """Test score_name property for PROFICIENT level."""

        # Arrange
        ps = ProficiencyScore(
            topic_id="test",
            score=0.8,
        )

        # Act
        result = ps.score_name

        # Assert
        assert result == ProficiencyScoreName.PROFICIENT

    def test_score_name_proficient_with_evidence(self):
        """Test score_name property for PROFICIENT_WITH_EVIDENCE level."""

        # Arrange
        ps = ProficiencyScore(
            topic_id="test",
            score=1.0,
        )

        # Act
        result = ps.score_name

        # Assert
        assert result == ProficiencyScoreName.PROFICIENT_WITH_EVIDENCE

    # Static Methods
    def test_get_score_name_unaware(self):
        """Test get_score_name returns UNAWARE for score 0.0."""

        # Arrange
        score = 0.0

        # Act
        result = ProficiencyScore.get_score_name(score)

        # Assert
        assert result == ProficiencyScoreName.UNAWARE

    def test_get_score_name_aware(self):
        """Test get_score_name returns AWARE for score 0.1."""

        # Arrange
        score = 0.1

        # Act
        result = ProficiencyScore.get_score_name(score)

        # Assert
        assert result == ProficiencyScoreName.AWARE

    def test_get_score_name_familiar(self):
        """Test get_score_name returns FAMILIAR for score 0.5."""

        # Arrange
        score = 0.5

        # Act
        result = ProficiencyScore.get_score_name(score)

        # Assert
        assert result == ProficiencyScoreName.FAMILIAR

    def test_get_score_name_proficient(self):
        """Test get_score_name returns PROFICIENT for score 0.8."""

        # Arrange
        score = 0.8

        # Act
        result = ProficiencyScore.get_score_name(score)

        # Assert
        assert result == ProficiencyScoreName.PROFICIENT

    def test_get_score_name_proficient_with_evidence(self):
        """Test get_score_name returns PROFICIENT_WITH_EVIDENCE for score 1.0."""

        # Arrange
        score = 1.0

        # Act
        result = ProficiencyScore.get_score_name(score)

        # Assert
        assert result == ProficiencyScoreName.PROFICIENT_WITH_EVIDENCE

    def test_get_score_name_invalid(self):
        """Test get_score_name static method with invalid score."""

        # Act
        result = None
        try:
            ProficiencyScore.get_score_name(-0.1)
        except Exception as e:
            result = e

        # Assert
        assert isinstance(result, ValueError)
        assert "Invalid" in str(result)

    # Methods
    def test_to_dict(self):
        """Test conversion to JSON-serializable dictionary."""

        # Arrange
        topic_id = "git-commit"
        score = 0.8
        ps = ProficiencyScore(
            topic_id=topic_id,
            score=score,
        )

        # Act
        json_dict = ps.to_dict()

        # Assert
        assert json_dict == {
            "topic_id": topic_id,
            "score": score,
        }

    def test_to_json(self):
        """Test conversion to JSON string."""

        # Arrange
        topic_id = "git-commit"
        score = 0.8
        ps = ProficiencyScore(
            topic_id=topic_id,
            score=score,
        )

        # Act
        json_str = ps.to_json()

        # Assert
        expected_json = '{"topic_id": "git-commit", "score": 0.8}'
        assert json_str == expected_json

    # Debugging
    def test_repr(self):
        """Test string representation of ProficiencyScore."""

        # Arrange
        ps = ProficiencyScore(
            topic_id="git-commit",
            score=0.8,
        )

        # Act
        repr_str = repr(ps)

        # Assert
        assert "ProficiencyScore" in repr_str
        assert "git-commit" in repr_str
        assert "0.8" in repr_str
        assert "PROFICIENT" in repr_str
