from openproficiency.validators import validate_kebab_case, validate_hostname


class TestValidateKebabCase:

    # Valid kebab-case strings
    def test_valid_single_word(self):
        """Single lowercase word should be valid."""

        # Arrange
        value = "topic"

        # Act
        validate_kebab_case(value)

        # Assert
        # No exception raised

    def test_valid_two_words(self):
        """Two words with hyphen should be valid."""

        # Arrange
        value = "topic-id"

        # Act
        validate_kebab_case(value)

        # Assert
        # No exception raised

    def test_valid_multiple_words(self):
        """Multiple words with hyphens should be valid."""

        # Arrange
        value = "multi-part-topic-name"

        # Act
        validate_kebab_case(value)

        # Assert
        # No exception raised

    def test_valid_with_numbers(self):
        """Kebab-case with numbers should be valid."""

        # Arrange
        value = "math-level-1"

        # Act
        validate_kebab_case(value)

        # Assert
        # No exception raised

    def test_valid_starting_with_number(self):
        """Starting with a number should be valid."""

        # Arrange
        value = "3d-graphics"

        # Act
        validate_kebab_case(value)

        # Assert
        # No exception raised

    def test_valid_ending_with_number(self):
        """Ending with a number should be valid."""

        # Arrange
        value = "python-3"

        # Act
        validate_kebab_case(value)

        # Assert
        # No exception raised

    def test_valid_only_numbers(self):
        """Only numbers should be valid."""

        # Arrange
        value = "123"

        # Act
        validate_kebab_case(value)

        # Assert
        # No exception raised

    def test_valid_numbers_with_hyphens(self):
        """Numbers with hyphens should be valid."""

        # Arrange
        value = "123-456"

        # Act
        validate_kebab_case(value)

        # Assert
        # No exception raised

    # Invalid kebab-case strings
    def test_invalid_empty_string(self):
        """Empty string should raise ValueError."""

        # Arrange
        value = ""

        # Act
        exception_raised = None
        try:
            validate_kebab_case(value)
        except Exception as e:
            exception_raised = e

        # Assert
        assert isinstance(exception_raised, ValueError)
        assert "cannot be empty" in str(exception_raised)

    def test_invalid_uppercase_letter(self):
        """Uppercase letters should raise ValueError."""

        # Arrange
        value = "Topic"

        # Act
        exception_raised = None
        try:
            validate_kebab_case(value)
        except Exception as e:
            exception_raised = e

        # Assert
        assert isinstance(exception_raised, ValueError)
        assert "kebab-case" in str(exception_raised)

    def test_invalid_mixed_case(self):
        """Mixed case should raise ValueError."""

        # Arrange
        value = "Topic-Id"

        # Act
        exception_raised = None
        try:
            validate_kebab_case(value)
        except Exception as e:
            exception_raised = e

        # Assert
        assert isinstance(exception_raised, ValueError)
        assert "kebab-case" in str(exception_raised)

    def test_invalid_underscore(self):
        """Underscores should raise ValueError."""

        # Arrange
        value = "topic_id"

        # Act
        exception_raised = None
        try:
            validate_kebab_case(value)
        except Exception as e:
            exception_raised = e

        # Assert
        assert isinstance(exception_raised, ValueError)
        assert "kebab-case" in str(exception_raised)

    def test_invalid_double_hyphen(self):
        """Double hyphens should raise ValueError."""

        # Arrange
        value = "topic--id"

        # Act

        exception_raised = None
        try:
            validate_kebab_case(value)
        except Exception as e:
            exception_raised = e

        # Assert
        assert isinstance(exception_raised, ValueError)
        assert "kebab-case" in str(exception_raised)

    def test_invalid_leading_hyphen(self):
        """Leading hyphen should raise ValueError."""

        # Arrange
        value = "-topic"

        # Act

        exception_raised = None
        try:
            validate_kebab_case(value)
        except Exception as e:
            exception_raised = e

        # Assert
        assert isinstance(exception_raised, ValueError)
        assert "kebab-case" in str(exception_raised)

    def test_invalid_trailing_hyphen(self):
        """Trailing hyphen should raise ValueError."""

        # Arrange
        value = "topic-"

        # Act

        exception_raised = None
        try:
            validate_kebab_case(value)
        except Exception as e:
            exception_raised = e

        # Assert
        assert isinstance(exception_raised, ValueError)
        assert "kebab-case" in str(exception_raised)

    def test_invalid_space(self):
        """Spaces should raise ValueError."""

        # Arrange
        value = "topic id"

        # Act
        exception_raised = None
        try:
            validate_kebab_case(value)
        except Exception as e:
            exception_raised = e

        # Assert
        assert isinstance(exception_raised, ValueError)
        assert "kebab-case" in str(exception_raised)

    def test_invalid_special_characters(self):
        """Special characters should raise ValueError."""

        # Arrange
        value = "topic@id"

        # Act
        exception_raised = None
        try:
            validate_kebab_case(value)
        except Exception as e:
            exception_raised = e

        # Assert
        assert isinstance(exception_raised, ValueError)
        assert "kebab-case" in str(exception_raised)

    def test_invalid_dot(self):
        """Dots should raise ValueError."""

        # Arrange
        value = "topic.id"

        # Act
        exception_raised = None
        try:
            validate_kebab_case(value)
        except Exception as e:
            exception_raised = e

        # Assert
        assert isinstance(exception_raised, ValueError)
        assert "kebab-case" in str(exception_raised)

    def test_invalid_error_message_structure(self):
        """Error message should contain value that was rejected."""

        # Arrange
        value = "Invalid"

        # Act
        exception_raised = None
        try:
            validate_kebab_case(value)
        except Exception as e:
            exception_raised = e

        # Assert
        assert isinstance(exception_raised, ValueError)
        assert "Invalid" in str(exception_raised)


class TestValidateHostname:

    # Valid hostnames
    def test_valid_single_word(self):
        """Single lowercase word should be valid."""

        # Arrange
        value = "github"

        # Act
        validate_hostname(value)

        # Assert
        # No exception raised

    def test_valid_with_hyphen(self):
        """Kebab-case hostname should be valid."""

        # Arrange
        value = "acme-corp"

        # Act
        validate_hostname(value)

        # Assert
        # No exception raised

    def test_valid_simple_domain(self):
        """Simple domain should be valid."""

        # Arrange
        value = "example.com"

        # Act
        validate_hostname(value)

        # Assert
        # No exception raised

    def test_valid_subdomain(self):
        """Subdomain should be valid."""

        # Arrange
        value = "sub.example.com"

        # Act
        validate_hostname(value)

        # Assert
        # No exception raised

    def test_valid_multiple_subdomains(self):
        """Multiple subdomains should be valid."""

        # Arrange
        value = "a.b.c.example.com"

        # Act
        validate_hostname(value)

        # Assert
        # No exception raised

    def test_valid_with_numbers(self):
        """Hostnames with numbers should be valid."""

        # Arrange
        value = "server-1.example.com"

        # Act
        validate_hostname(value)

        # Assert
        # No exception raised

    def test_valid_starting_with_number(self):
        """Components starting with numbers should be valid."""

        # Arrange
        value = "1server.example.com"

        # Act
        validate_hostname(value)

        # Assert
        # No exception raised

    def test_valid_ending_with_number(self):
        """Components ending with numbers should be valid."""

        # Arrange
        value = "server1.example.com"

        # Act
        validate_hostname(value)

        # Assert
        # No exception raised

    def test_valid_only_numbers_in_component(self):
        """Numeric-only components should be valid."""

        # Arrange
        value = "123.456.789"

        # Act
        validate_hostname(value)

        # Assert
        # No exception raised

    def test_valid_hyphenated_subdomain(self):
        """Hyphenated subdomains should be valid."""

        # Arrange
        value = "my-server.my-domain.com"

        # Act
        validate_hostname(value)

        # Assert
        # No exception raised

    # Invalid hostnames
    def test_invalid_empty_string(self):
        """Empty string should raise ValueError."""

        # Arrange
        value = ""

        # Act
        exception_raised = None
        try:
            validate_hostname(value)
        except Exception as e:
            exception_raised = e

        # Assert
        assert isinstance(exception_raised, ValueError)
        assert "cannot be empty" in str(exception_raised)

    def test_invalid_uppercase_letter(self):
        """Uppercase letters should raise ValueError."""

        # Arrange
        value = "GitHub"

        # Act
        exception_raised = None
        try:
            validate_hostname(value)
        except Exception as e:
            exception_raised = e

        # Assert
        assert isinstance(exception_raised, ValueError)
        assert "hostname" in str(exception_raised)

    def test_invalid_mixed_case(self):
        """Mixed case should raise ValueError."""

        # Arrange
        value = "Example.Com"

        # Act
        exception_raised = None
        try:
            validate_hostname(value)
        except Exception as e:
            exception_raised = e

        # Assert
        assert isinstance(exception_raised, ValueError)
        assert "hostname" in str(exception_raised)

    def test_invalid_underscore(self):
        """Underscores should raise ValueError."""

        # Arrange
        value = "my_server"

        # Act
        exception_raised = None
        try:
            validate_hostname(value)
        except Exception as e:
            exception_raised = e

        # Assert
        assert isinstance(exception_raised, ValueError)
        assert "hostname" in str(exception_raised)

    def test_invalid_double_hyphen(self):
        """Double hyphens should raise ValueError."""

        # Arrange
        value = "my--server"

        # Act
        exception_raised = None
        try:
            validate_hostname(value)
        except Exception as e:
            exception_raised = e

        # Assert
        assert isinstance(exception_raised, ValueError)
        assert "hostname" in str(exception_raised)

    def test_invalid_leading_hyphen(self):
        """Leading hyphen should raise ValueError."""

        # Arrange
        value = "-github"

        # Act
        exception_raised = None
        try:
            validate_hostname(value)
        except Exception as e:
            exception_raised = e

        # Assert
        assert isinstance(exception_raised, ValueError)
        assert "hostname" in str(exception_raised)

    def test_invalid_trailing_hyphen(self):
        """Trailing hyphen should raise ValueError."""

        # Arrange
        value = "github-"

        # Act
        exception_raised = None
        try:
            validate_hostname(value)
        except Exception as e:
            exception_raised = e

        # Assert
        assert isinstance(exception_raised, ValueError)
        assert "hostname" in str(exception_raised)

    def test_invalid_leading_hyphen_in_component(self):
        """Leading hyphen in component should raise ValueError."""

        # Arrange
        value = "example.-com"

        # Act
        exception_raised = None
        try:
            validate_hostname(value)
        except Exception as e:
            exception_raised = e

        # Assert
        assert isinstance(exception_raised, ValueError)
        assert "hostname" in str(exception_raised)

    def test_invalid_trailing_hyphen_in_component(self):
        """Trailing hyphen in component should raise ValueError."""

        # Arrange
        value = "example-.com"

        # Act
        exception_raised = None
        try:
            validate_hostname(value)
        except Exception as e:
            exception_raised = e

        # Assert
        assert isinstance(exception_raised, ValueError)
        assert "hostname" in str(exception_raised)

    def test_invalid_leading_dot(self):
        """Leading dot should raise ValueError."""

        # Arrange
        value = ".example.com"

        # Act
        exception_raised = None
        try:
            validate_hostname(value)
        except Exception as e:
            exception_raised = e

        # Assert
        assert isinstance(exception_raised, ValueError)
        assert "hostname" in str(exception_raised)

    def test_invalid_trailing_dot(self):
        """Trailing dot should raise ValueError."""

        # Arrange
        value = "example.com."

        # Act
        exception_raised = None
        try:
            validate_hostname(value)
        except Exception as e:
            exception_raised = e

        # Assert
        assert isinstance(exception_raised, ValueError)
        assert "hostname" in str(exception_raised)

    def test_invalid_double_dot(self):
        """Double dots should raise ValueError."""

        # Arrange
        value = "example..com"

        # Act
        exception_raised = None
        try:
            validate_hostname(value)
        except Exception as e:
            exception_raised = e

        # Assert
        assert isinstance(exception_raised, ValueError)
        assert "hostname" in str(exception_raised)

    def test_invalid_space(self):
        """Spaces should raise ValueError."""

        # Arrange
        value = "my server"

        # Act
        exception_raised = None
        try:
            validate_hostname(value)
        except Exception as e:
            exception_raised = e

        # Assert
        assert isinstance(exception_raised, ValueError)
        assert "hostname" in str(exception_raised)

    def test_invalid_special_characters(self):
        """Special characters should raise ValueError."""

        # Arrange
        value = "example@com"

        # Act
        exception_raised = None
        try:
            validate_hostname(value)
        except Exception as e:
            exception_raised = e

        # Assert
        assert isinstance(exception_raised, ValueError)
        assert "hostname" in str(exception_raised)

    def test_invalid_path_separator(self):
        """Path separators should raise ValueError."""

        # Arrange
        value = "example.com/path"

        # Act
        exception_raised = None
        try:
            validate_hostname(value)
        except Exception as e:
            exception_raised = e

        # Assert
        assert isinstance(exception_raised, ValueError)
        assert "hostname" in str(exception_raised)

    def test_invalid_error_message_structure(self):
        """Error message should contain value that was rejected."""

        # Arrange
        value = "Invalid_Host"

        # Act
        exception_raised = None
        try:
            validate_hostname(value)
        except Exception as e:
            exception_raised = e

        # Assert
        assert isinstance(exception_raised, ValueError)
        assert "Invalid_Host" in str(exception_raised)
