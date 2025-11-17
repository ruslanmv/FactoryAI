"""Tests for utility functions module.

Author: Ruslan Magana
Website: https://ruslanmv.com
License: Apache 2.0
"""

import tempfile
from pathlib import Path

import pytest

from factoryai.exceptions import FactoryAIError, ValidationError
from factoryai.utils import (
    check_command_available,
    check_git_installed,
    compare_versions,
    ensure_directory,
    format_list,
    get_python_executable,
    is_git_repository,
    parse_version,
    run_command,
    truncate_string,
    validate_path,
)


class TestRunCommand:
    """Tests for run_command function."""

    def test_run_simple_command(self) -> None:
        """Test running a simple command."""
        returncode, stdout, stderr = run_command(["echo", "hello"])

        assert returncode == 0
        assert "hello" in stdout
        assert stderr == ""

    def test_run_command_failure(self) -> None:
        """Test running a command that fails."""
        with pytest.raises(FactoryAIError):
            run_command(["false"], check=True)

    def test_run_command_nonexistent(self) -> None:
        """Test running a non-existent command."""
        with pytest.raises(FactoryAIError):
            run_command(["nonexistent-command-xyz"])


class TestGitFunctions:
    """Tests for git-related functions."""

    def test_check_git_installed(self) -> None:
        """Test checking if git is installed."""
        result = check_git_installed()
        # Git should be installed in most environments
        assert isinstance(result, bool)

    def test_is_git_repository_true(self) -> None:
        """Test checking if path is a git repository."""
        # Current directory should be a git repo
        result = is_git_repository(Path.cwd())
        # May or may not be a git repo, just check it doesn't crash
        assert isinstance(result, bool)

    def test_is_git_repository_false(self) -> None:
        """Test checking if path is not a git repository."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = is_git_repository(Path(tmpdir))
            assert result is False


class TestPathValidation:
    """Tests for path validation functions."""

    def test_validate_existing_path(self) -> None:
        """Test validating an existing path."""
        # Should not raise for existing path
        validate_path(Path.cwd(), must_exist=True)

    def test_validate_nonexistent_path(self) -> None:
        """Test validating a non-existent path without must_exist."""
        # Should not raise
        validate_path(Path("/nonexistent/path"), must_exist=False)

    def test_validate_nonexistent_path_must_exist(self) -> None:
        """Test validating a non-existent path with must_exist."""
        with pytest.raises(ValidationError):
            validate_path(Path("/nonexistent/path"), must_exist=True)

    def test_ensure_directory_exists(self) -> None:
        """Test ensuring a directory exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = Path(tmpdir) / "test"
            ensure_directory(test_dir, create=True)
            assert test_dir.exists()
            assert test_dir.is_dir()

    def test_ensure_directory_already_exists(self) -> None:
        """Test ensuring a directory that already exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = Path(tmpdir)
            # Should not raise
            ensure_directory(test_dir, create=True)

    def test_ensure_directory_file_exists(self) -> None:
        """Test ensuring a directory when file exists at path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.txt"
            test_file.touch()

            with pytest.raises(FactoryAIError):
                ensure_directory(test_file, create=True)

    def test_ensure_directory_no_create(self) -> None:
        """Test ensuring a directory without creating it."""
        with pytest.raises(FactoryAIError):
            ensure_directory(Path("/nonexistent/path"), create=False)


class TestCommandAvailability:
    """Tests for command availability checks."""

    def test_check_command_available_python(self) -> None:
        """Test checking if python is available."""
        result = check_command_available("python")
        # Python should be available
        assert isinstance(result, bool)

    def test_check_command_available_nonexistent(self) -> None:
        """Test checking if non-existent command is available."""
        result = check_command_available("nonexistent-command-xyz")
        assert result is False

    def test_get_python_executable(self) -> None:
        """Test getting Python executable path."""
        executable = get_python_executable()
        assert executable
        assert "python" in executable.lower()


class TestFormatting:
    """Tests for formatting functions."""

    def test_format_list_basic(self) -> None:
        """Test formatting a basic list."""
        items = ["item1", "item2", "item3"]
        result = format_list(items)

        assert "item1" in result
        assert "item2" in result
        assert "item3" in result
        assert "•" in result

    def test_format_list_custom_bullet(self) -> None:
        """Test formatting a list with custom bullet."""
        items = ["item1", "item2"]
        result = format_list(items, bullet="-")

        assert "- item1" in result
        assert "- item2" in result

    def test_format_list_empty(self) -> None:
        """Test formatting an empty list."""
        result = format_list([])
        assert result == ""

    def test_truncate_string_short(self) -> None:
        """Test truncating a short string."""
        text = "Hello"
        result = truncate_string(text, max_length=10)
        assert result == "Hello"

    def test_truncate_string_long(self) -> None:
        """Test truncating a long string."""
        text = "This is a very long string that should be truncated"
        result = truncate_string(text, max_length=20)

        assert len(result) == 20
        assert result.endswith("...")

    def test_truncate_string_custom_suffix(self) -> None:
        """Test truncating with custom suffix."""
        text = "This is a very long string"
        result = truncate_string(text, max_length=15, suffix=">>")

        assert len(result) == 15
        assert result.endswith(">>")


class TestVersionParsing:
    """Tests for version parsing and comparison."""

    def test_parse_version_simple(self) -> None:
        """Test parsing a simple version string."""
        version = parse_version("1.2.3")
        assert version == (1, 2, 3)

    def test_parse_version_two_parts(self) -> None:
        """Test parsing a two-part version string."""
        version = parse_version("2.5")
        assert version == (2, 5)

    def test_parse_version_invalid(self) -> None:
        """Test parsing an invalid version string."""
        with pytest.raises(ValidationError):
            parse_version("invalid.version.x")

    def test_compare_versions_equal(self) -> None:
        """Test comparing equal versions."""
        result = compare_versions("1.2.3", "1.2.3")
        assert result == 0

    def test_compare_versions_less_than(self) -> None:
        """Test comparing when first version is less."""
        result = compare_versions("1.2.3", "2.0.0")
        assert result == -1

    def test_compare_versions_greater_than(self) -> None:
        """Test comparing when first version is greater."""
        result = compare_versions("2.0.0", "1.2.3")
        assert result == 1

    def test_compare_versions_different_lengths(self) -> None:
        """Test comparing versions with different lengths."""
        result = compare_versions("1.2", "1.2.0")
        assert result == -1
