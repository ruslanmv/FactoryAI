"""Tests for configuration management module.

Author: Ruslan Magana
Website: https://ruslanmv.com
License: Apache 2.0
"""

import json
import tempfile
from pathlib import Path

import pytest

from factoryai.config import (
    FactoryAIConfig,
    SubmoduleConfig,
    get_default_config,
    setup_logging,
)
from factoryai.exceptions import ConfigurationError


class TestSubmoduleConfig:
    """Tests for SubmoduleConfig dataclass."""

    def test_submodule_config_creation(self) -> None:
        """Test SubmoduleConfig creation."""
        config = SubmoduleConfig(
            name="Test-Module",
            path="src/test",
            url="https://github.com/test/test-module"
        )

        assert config.name == "Test-Module"
        assert config.path == "src/test"
        assert config.url == "https://github.com/test/test-module"
        assert config.enabled is True

    def test_submodule_config_disabled(self) -> None:
        """Test SubmoduleConfig with disabled flag."""
        config = SubmoduleConfig(
            name="Test-Module",
            path="src/test",
            url="https://github.com/test/test-module",
            enabled=False
        )

        assert config.enabled is False


class TestFactoryAIConfig:
    """Tests for FactoryAIConfig class."""

    def test_config_creation_with_defaults(self) -> None:
        """Test FactoryAIConfig creation with default components."""
        config = FactoryAIConfig(root_dir=Path("/test/root"))

        assert config.root_dir == Path("/test/root")
        assert config.submodules_dir == Path("/test/root/src/platfom")
        assert config.log_level == "INFO"
        assert config.log_file is None
        assert len(config.components) == 3

    def test_config_component_initialization(self) -> None:
        """Test that default components are initialized correctly."""
        config = FactoryAIConfig(root_dir=Path("/test/root"))

        assert "factory-app-ai" in config.components
        assert "factory-feature" in config.components
        assert "factory-debug" in config.components

        app_ai = config.components["factory-app-ai"]
        assert app_ai.name == "Factory-App-AI"
        assert app_ai.enabled is True

    def test_get_component_path(self) -> None:
        """Test getting component path."""
        config = FactoryAIConfig(root_dir=Path("/test/root"))
        path = config.get_component_path("factory-app-ai")

        assert path == Path("/test/root/src/platfom/Factory-App-AI")

    def test_get_component_path_not_found(self) -> None:
        """Test getting path for non-existent component."""
        config = FactoryAIConfig(root_dir=Path("/test/root"))

        with pytest.raises(ConfigurationError):
            config.get_component_path("non-existent")

    def test_is_component_available(self) -> None:
        """Test checking component availability."""
        config = FactoryAIConfig(root_dir=Path("/test/root"))

        # Component exists but directory doesn't
        assert config.is_component_available("factory-app-ai") is False

        # Non-existent component
        assert config.is_component_available("non-existent") is False

    def test_to_dict(self) -> None:
        """Test converting config to dictionary."""
        config = FactoryAIConfig(root_dir=Path("/test/root"))
        config_dict = config.to_dict()

        assert config_dict["root_dir"] == "/test/root"
        assert config_dict["log_level"] == "INFO"
        assert "components" in config_dict
        assert "factory-app-ai" in config_dict["components"]

    def test_from_dict(self) -> None:
        """Test creating config from dictionary."""
        data = {
            "root_dir": "/test/root",
            "submodules_dir": "src/platfom",
            "log_level": "DEBUG",
            "log_file": "/test/log.txt",
            "components": {
                "test-component": {
                    "name": "Test-Component",
                    "path": "src/test",
                    "url": "https://github.com/test/test",
                    "enabled": True
                }
            }
        }

        config = FactoryAIConfig.from_dict(data)

        assert config.root_dir == Path("/test/root")
        assert config.log_level == "DEBUG"
        assert config.log_file == Path("/test/log.txt")
        assert "test-component" in config.components

    def test_save_and_load(self) -> None:
        """Test saving and loading configuration."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.json"

            # Create and save config
            original_config = FactoryAIConfig(root_dir=Path("/test/root"))
            original_config.log_level = "DEBUG"
            original_config.save(config_path)

            # Load config
            loaded_config = FactoryAIConfig.load(config_path)

            assert loaded_config.root_dir == original_config.root_dir
            assert loaded_config.log_level == "DEBUG"
            assert len(loaded_config.components) == len(original_config.components)

    def test_load_nonexistent_file(self) -> None:
        """Test loading from non-existent file."""
        with pytest.raises(ConfigurationError):
            FactoryAIConfig.load(Path("/nonexistent/config.json"))


class TestGetDefaultConfig:
    """Tests for get_default_config function."""

    def test_get_default_config(self) -> None:
        """Test getting default configuration."""
        config = get_default_config()

        assert isinstance(config, FactoryAIConfig)
        assert config.root_dir.exists()
        assert config.log_level in ["DEBUG", "INFO", "WARNING", "ERROR"]


class TestSetupLogging:
    """Tests for setup_logging function."""

    def test_setup_logging(self) -> None:
        """Test setting up logging."""
        config = FactoryAIConfig(root_dir=Path("/test/root"))
        config.log_level = "DEBUG"

        # Should not raise any exceptions
        setup_logging(config)

    def test_setup_logging_with_file(self) -> None:
        """Test setting up logging with file output."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "test.log"
            config = FactoryAIConfig(root_dir=Path("/test/root"))
            config.log_file = log_file

            setup_logging(config)

            # Log file should exist after logging is set up
            # (though it may be empty until something is logged)
