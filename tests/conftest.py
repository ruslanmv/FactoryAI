"""Pytest configuration and shared fixtures.

This module provides shared fixtures and configuration for all tests.

Author: Ruslan Magana
Website: https://ruslanmv.com
License: Apache 2.0
"""

import tempfile
from pathlib import Path
from typing import Generator

import pytest

from factoryai.config import FactoryAIConfig


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Provide a temporary directory for testing.

    Yields:
        Path to temporary directory that is cleaned up after test.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def test_config(temp_dir: Path) -> FactoryAIConfig:
    """Provide a test configuration.

    Args:
        temp_dir: Temporary directory fixture.

    Returns:
        FactoryAIConfig instance for testing.
    """
    config = FactoryAIConfig(root_dir=temp_dir)
    config.log_level = "DEBUG"
    return config


@pytest.fixture
def mock_submodule_structure(temp_dir: Path) -> Path:
    """Create a mock submodule directory structure.

    Args:
        temp_dir: Temporary directory fixture.

    Returns:
        Path to root directory with mock structure.
    """
    # Create submodule directories
    submodules_dir = temp_dir / "src" / "platfom"

    for component in ["Factory-App-AI", "Factory-Feature", "Factory-Debug"]:
        component_dir = submodules_dir / component
        component_dir.mkdir(parents=True, exist_ok=True)

        # Create a dummy main.py file
        main_file = component_dir / "main.py"
        main_file.write_text('print("Mock component")\n')

    return temp_dir
