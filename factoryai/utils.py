"""Utility functions for FactoryAI Suite.

This module provides utility functions used across the FactoryAI suite,
including file operations, subprocess management, and validation.

Author: Ruslan Magana
Website: https://ruslanmv.com
License: Apache 2.0
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Tuple
import logging
import shutil

from factoryai.exceptions import FactoryAIError, ValidationError


logger = logging.getLogger(__name__)


def run_command(
    command: List[str],
    cwd: Optional[Path] = None,
    capture_output: bool = True,
    check: bool = True
) -> Tuple[int, str, str]:
    """Run a shell command and return its output.

    Args:
        command: Command and arguments as a list.
        cwd: Working directory for the command.
        capture_output: Whether to capture stdout and stderr.
        check: Whether to raise exception on non-zero exit code.

    Returns:
        Tuple of (return_code, stdout, stderr).

    Raises:
        FactoryAIError: If command fails and check is True.
    """
    logger.debug(f"Running command: {' '.join(command)}")

    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=capture_output,
            text=True,
            check=False
        )

        stdout = result.stdout if capture_output else ""
        stderr = result.stderr if capture_output else ""

        if check and result.returncode != 0:
            raise FactoryAIError(
                f"Command failed with exit code {result.returncode}",
                details=f"Command: {' '.join(command)}\nStderr: {stderr}"
            )

        return result.returncode, stdout, stderr

    except FileNotFoundError:
        raise FactoryAIError(
            f"Command not found: {command[0]}",
            details="Please ensure the command is installed and in your PATH."
        )
    except Exception as e:
        raise FactoryAIError(f"Failed to run command: {e}")


def check_git_installed() -> bool:
    """Check if git is installed and available.

    Returns:
        True if git is installed, False otherwise.
    """
    try:
        run_command(["git", "--version"], check=True)
        return True
    except FactoryAIError:
        return False


def is_git_repository(path: Path) -> bool:
    """Check if a path is a git repository.

    Args:
        path: Path to check.

    Returns:
        True if path is a git repository, False otherwise.
    """
    git_dir = path / ".git"
    return git_dir.exists() and git_dir.is_dir()


def validate_path(path: Path, must_exist: bool = False) -> None:
    """Validate a file system path.

    Args:
        path: Path to validate.
        must_exist: Whether the path must exist.

    Raises:
        ValidationError: If validation fails.
    """
    if must_exist and not path.exists():
        raise ValidationError(f"Path does not exist: {path}")

    try:
        # Check if path is accessible
        if path.exists():
            path.stat()
    except PermissionError:
        raise ValidationError(f"Permission denied: {path}")
    except Exception as e:
        raise ValidationError(f"Invalid path: {path} - {e}")


def ensure_directory(path: Path, create: bool = True) -> None:
    """Ensure a directory exists.

    Args:
        path: Directory path.
        create: Whether to create the directory if it doesn't exist.

    Raises:
        FactoryAIError: If directory cannot be created.
    """
    if path.exists():
        if not path.is_dir():
            raise FactoryAIError(
                f"Path exists but is not a directory: {path}"
            )
        return

    if create:
        try:
            path.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Created directory: {path}")
        except Exception as e:
            raise FactoryAIError(f"Failed to create directory {path}: {e}")
    else:
        raise FactoryAIError(f"Directory does not exist: {path}")


def get_python_executable() -> str:
    """Get the current Python executable path.

    Returns:
        Path to the Python executable.
    """
    return sys.executable


def check_command_available(command: str) -> bool:
    """Check if a command is available in the system PATH.

    Args:
        command: Command name to check.

    Returns:
        True if command is available, False otherwise.
    """
    return shutil.which(command) is not None


def format_list(items: List[str], bullet: str = "•") -> str:
    """Format a list of items as a bulleted list.

    Args:
        items: List of strings to format.
        bullet: Bullet character to use.

    Returns:
        Formatted string with bulleted items.
    """
    if not items:
        return ""
    return "\n".join(f"{bullet} {item}" for item in items)


def truncate_string(text: str, max_length: int = 80, suffix: str = "...") -> str:
    """Truncate a string to a maximum length.

    Args:
        text: String to truncate.
        max_length: Maximum length (including suffix).
        suffix: Suffix to add if truncated.

    Returns:
        Truncated string.
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def parse_version(version_string: str) -> Tuple[int, ...]:
    """Parse a version string into a tuple of integers.

    Args:
        version_string: Version string (e.g., "1.2.3").

    Returns:
        Tuple of version numbers.

    Raises:
        ValidationError: If version string is invalid.
    """
    try:
        return tuple(int(x) for x in version_string.split("."))
    except ValueError:
        raise ValidationError(f"Invalid version string: {version_string}")


def compare_versions(version1: str, version2: str) -> int:
    """Compare two version strings.

    Args:
        version1: First version string.
        version2: Second version string.

    Returns:
        -1 if version1 < version2, 0 if equal, 1 if version1 > version2.
    """
    v1 = parse_version(version1)
    v2 = parse_version(version2)

    if v1 < v2:
        return -1
    elif v1 > v2:
        return 1
    else:
        return 0
