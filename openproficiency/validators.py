"""Validation utilities for OpenProficiency library."""

import re


def validate_kebab_case(value: str) -> None:
    """
    Validate that a string follows kebab-case format.

    Pattern: lowercase alphanumeric characters with hyphens as separators.
    Examples: "topic", "topic-id", "math-level-1"

    Args:
        value: The string to validate

    Raises:
        ValueError: If the value is not in valid kebab-case format
    """
    if not value:
        raise ValueError("Value cannot be empty")

    # Pattern: starts and ends with alphanumeric, can have hyphens between
    pattern = r"^[a-z0-9]+(?:-[a-z0-9]+)*$"

    if not re.match(pattern, value):
        raise ValueError(
            f"Value must be in kebab-case format (lowercase alphanumeric with hyphens). "
            f"Got: '{value}'. Examples: 'topic', 'topic-id', 'math-level-1'"
        )


def validate_hostname(value: str) -> None:
    """
    Validate that a string is a valid hostname or domain name.

    Pattern: lowercase alphanumeric characters with hyphens and dots as separators.
    Examples: "example.com", "sub.example.com"

    Args:
        value: The string to validate

    Raises:
        ValueError: If the value is not in valid hostname format
    """
    if not value:
        raise ValueError("Value cannot be empty")

    # Pattern: hostname components separated by dots (requires at least 2 components)
    # Each component: starts and ends with alphanumeric, can have hyphens between
    component_pattern = r"[a-z0-9]+(?:-[a-z0-9]+)*"
    pattern = f"^{component_pattern}(?:\\.{component_pattern})+$"

    if not re.match(pattern, value):
        raise ValueError(
            f"Value must be a valid hostname (lowercase alphanumeric with hyphens and dots). "
            f"Got: '{value}'. Examples: 'example.com','sub.example.com'"
        )
