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
        ps = ProficiencyScore(topic_id=topic_id, score=score)

        # Assert
        assert ps.topic_id == topic_id
        assert ps.score == score

    def test_init_with_enum_score(self):
        """Create a proficiency score with ProficiencyScoreName enum."""

        # Arrange
        topic_id = "git-commit"
        score_name = ProficiencyScoreName.PROFICIENT

        # Act
        ps = ProficiencyScore(topic_id=topic_id, score=score_name)

        # Assert
        assert ps.topic_id == topic_id
        assert ps.score == 0.8

    def test_init_invalid_score_too_low(self):
        """Test that score below 0.0 raises ValueError."""

        # Act & Assert
        try:
            ProficiencyScore(topic_id="test", score=-0.1)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "between 0.0 and 1.0" in str(e)

    def test_init_invalid_score_too_high(self):
        """Test that score above 1.0 raises ValueError."""

        # Act & Assert
        try:
            ProficiencyScore(topic_id="test", score=1.1)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "between 0.0 and 1.0" in str(e)

    def test_init_invalid_score_type(self):
        """Test that invalid score type raises ValueError."""

        # Act & Assert
        try:
            ProficiencyScore(topic_id="test", score="invalid")
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "numeric or ProficiencyScoreName" in str(e)

    # Properties - Score
    def test_score_getter(self):
        """Test getting score property."""

        # Arrange
        ps = ProficiencyScore(topic_id="test", score=0.5)

        # Act & Assert
        assert ps.score == 0.5

    def test_score_setter_numeric(self):
        """Test setting score with numeric value."""

        # Arrange
        ps = ProficiencyScore(topic_id="test", score=0.1)

        # Act
        ps.score = 0.9

        # Assert
        assert ps.score == 0.9

    def test_score_setter_enum(self):
        """Test setting score with enum value."""

        # Arrange
        ps = ProficiencyScore(topic_id="test", score=0.1)

        # Act
        ps.score = ProficiencyScoreName.FAMILIAR

        # Assert
        assert ps.score == 0.5

    def test_score_setter_invalid(self):
        """Test setting invalid score raises ValueError."""

        # Arrange
        ps = ProficiencyScore(topic_id="test", score=0.1)

        # Act & Assert
        try:
            ps.score = 1.5
            assert False, "Should have raised ValueError"
        except ValueError:
            pass

    # Properties - Score Name
    def test_score_name_unaware(self):
        """Test score_name property for UNAWARE level."""

        # Arrange
        ps = ProficiencyScore(topic_id="test", score=0.0)

        # Act & Assert
        assert ps.score_name == ProficiencyScoreName.UNAWARE

    def test_score_name_aware(self):
        """Test score_name property for AWARE level."""

        # Arrange
        ps = ProficiencyScore(topic_id="test", score=0.05)

        # Act & Assert
        assert ps.score_name == ProficiencyScoreName.AWARE

    def test_score_name_familiar(self):
        """Test score_name property for FAMILIAR level."""

        # Arrange
        ps = ProficiencyScore(topic_id="test", score=0.3)

        # Act & Assert
        assert ps.score_name == ProficiencyScoreName.FAMILIAR

    def test_score_name_proficient(self):
        """Test score_name property for PROFICIENT level."""

        # Arrange
        ps = ProficiencyScore(topic_id="test", score=0.8)

        # Act & Assert
        assert ps.score_name == ProficiencyScoreName.PROFICIENT

    def test_score_name_proficient_with_evidence(self):
        """Test score_name property for PROFICIENT_WITH_EVIDENCE level."""

        # Arrange
        ps = ProficiencyScore(topic_id="test", score=1.0)

        # Act & Assert
        assert ps.score_name == ProficiencyScoreName.PROFICIENT_WITH_EVIDENCE

    def test_score_name_setter(self):
        """Test setting score_name property."""

        # Arrange
        ps = ProficiencyScore(topic_id="test", score=0.1)

        # Act
        ps.score_name = ProficiencyScoreName.PROFICIENT

        # Assert
        assert ps.score == 0.8

    def test_score_name_setter_invalid_type(self):
        """Test setting score_name with invalid type raises ValueError."""

        # Arrange
        ps = ProficiencyScore(topic_id="test", score=0.1)

        # Act & Assert
        try:
            ps.score_name = 0.5
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "ProficiencyScoreName enum" in str(e)

    # Methods

    def test_to_json(self):
        """Test conversion to JSON-serializable dictionary."""

        # Arrange
        topic_id = "git-commit"
        score = 0.8
        ps = ProficiencyScore(topic_id=topic_id, score=score)

        # Act
        json_dict = ps.to_json()

        # Assert
        assert json_dict == {
            "topic_id": topic_id,
            "score": score
        }

    # Debugging
    def test_repr(self):
        """Test string representation of ProficiencyScore."""

        # Arrange
        ps = ProficiencyScore(topic_id="git-commit", score=0.8)

        # Act
        repr_str = repr(ps)

        # Assert
        assert "ProficiencyScore" in repr_str
        assert "git-commit" in repr_str
        assert "0.8" in repr_str
        assert "PROFICIENT" in repr_str
