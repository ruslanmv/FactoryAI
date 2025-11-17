"""Tests for core orchestration module.

Author: Ruslan Magana
Website: https://ruslanmv.com
License: Apache 2.0
"""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from factoryai.config import FactoryAIConfig
from factoryai.core import FactoryAIOrchestrator
from factoryai.exceptions import ComponentError, FactoryAIError, SubmoduleNotFoundError


class TestFactoryAIOrchestrator:
    """Tests for FactoryAIOrchestrator class."""

    def test_orchestrator_initialization(self) -> None:
        """Test orchestrator initialization."""
        config = FactoryAIConfig(root_dir=Path("/test/root"))
        orchestrator = FactoryAIOrchestrator(config)

        assert orchestrator.config == config

    def test_orchestrator_default_config(self) -> None:
        """Test orchestrator with default configuration."""
        orchestrator = FactoryAIOrchestrator()

        assert isinstance(orchestrator.config, FactoryAIConfig)

    @patch("factoryai.core.check_git_installed")
    @patch("factoryai.core.is_git_repository")
    @patch("factoryai.core.run_command")
    def test_sync_submodules_success(
        self,
        mock_run_command: MagicMock,
        mock_is_git_repo: MagicMock,
        mock_check_git: MagicMock
    ) -> None:
        """Test successful submodule synchronization."""
        mock_check_git.return_value = True
        mock_is_git_repo.return_value = True
        mock_run_command.return_value = (0, "Success", "")

        config = FactoryAIConfig(root_dir=Path("/test/root"))
        orchestrator = FactoryAIOrchestrator(config)

        # Should not raise
        orchestrator.sync_submodules()

        # Verify git command was called
        mock_run_command.assert_called_once()
        call_args = mock_run_command.call_args[0][0]
        assert "git" in call_args
        assert "submodule" in call_args

    @patch("factoryai.core.check_git_installed")
    def test_sync_submodules_git_not_installed(
        self,
        mock_check_git: MagicMock
    ) -> None:
        """Test submodule sync when git is not installed."""
        mock_check_git.return_value = False

        config = FactoryAIConfig(root_dir=Path("/test/root"))
        orchestrator = FactoryAIOrchestrator(config)

        with pytest.raises(FactoryAIError):
            orchestrator.sync_submodules()

    @patch("factoryai.core.check_git_installed")
    @patch("factoryai.core.is_git_repository")
    def test_sync_submodules_not_git_repo(
        self,
        mock_is_git_repo: MagicMock,
        mock_check_git: MagicMock
    ) -> None:
        """Test submodule sync when not in a git repository."""
        mock_check_git.return_value = True
        mock_is_git_repo.return_value = False

        config = FactoryAIConfig(root_dir=Path("/test/root"))
        orchestrator = FactoryAIOrchestrator(config)

        with pytest.raises(FactoryAIError):
            orchestrator.sync_submodules()

    def test_check_component_available(self) -> None:
        """Test checking component availability."""
        config = FactoryAIConfig(root_dir=Path("/test/root"))
        orchestrator = FactoryAIOrchestrator(config)

        # Component exists but directory doesn't
        result = orchestrator.check_component_available("factory-app-ai")
        assert result is False

    def test_get_component_status(self) -> None:
        """Test getting component status."""
        config = FactoryAIConfig(root_dir=Path("/test/root"))
        orchestrator = FactoryAIOrchestrator(config)

        status = orchestrator.get_component_status()

        assert isinstance(status, dict)
        assert "factory-app-ai" in status
        assert "factory-feature" in status
        assert "factory-debug" in status

        # Check status structure
        app_ai_status = status["factory-app-ai"]
        assert "name" in app_ai_status
        assert "enabled" in app_ai_status
        assert "available" in app_ai_status
        assert "path" in app_ai_status
        assert "url" in app_ai_status

    def test_run_component_not_available(self) -> None:
        """Test running a component that is not available."""
        config = FactoryAIConfig(root_dir=Path("/test/root"))
        orchestrator = FactoryAIOrchestrator(config)

        with pytest.raises(SubmoduleNotFoundError):
            orchestrator.run_component("factory-app-ai")

    def test_run_component_disabled(self) -> None:
        """Test running a disabled component."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root_dir = Path(tmpdir)
            config = FactoryAIConfig(root_dir=root_dir)

            # Create component directory but disable it
            component_path = root_dir / "src/platfom/Factory-App-AI"
            component_path.mkdir(parents=True)

            config.components["factory-app-ai"].enabled = False
            orchestrator = FactoryAIOrchestrator(config)

            with pytest.raises(ComponentError):
                orchestrator.run_component("factory-app-ai")

    def test_run_component_no_entry_point(self) -> None:
        """Test running a component without entry point."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root_dir = Path(tmpdir)
            config = FactoryAIConfig(root_dir=root_dir)

            # Create component directory but no main.py or app.py
            component_path = root_dir / "src/platfom/Factory-App-AI"
            component_path.mkdir(parents=True)

            orchestrator = FactoryAIOrchestrator(config)

            with pytest.raises(ComponentError):
                orchestrator.run_component("factory-app-ai")

    @patch("factoryai.core.check_git_installed")
    @patch("factoryai.core.is_git_repository")
    def test_validate_installation(
        self,
        mock_is_git_repo: MagicMock,
        mock_check_git: MagicMock
    ) -> None:
        """Test installation validation."""
        mock_check_git.return_value = True
        mock_is_git_repo.return_value = True

        config = FactoryAIConfig(root_dir=Path("/test/root"))
        orchestrator = FactoryAIOrchestrator(config)

        results = orchestrator.validate_installation()

        assert isinstance(results, dict)
        assert "valid" in results
        assert "git_installed" in results
        assert "is_git_repo" in results
        assert "submodules_initialized" in results
        assert "components" in results
        assert "errors" in results

    def test_info(self) -> None:
        """Test getting installation information."""
        config = FactoryAIConfig(root_dir=Path("/test/root"))
        orchestrator = FactoryAIOrchestrator(config)

        info = orchestrator.info()

        assert isinstance(info, dict)
        assert "version" in info
        assert "root_dir" in info
        assert "submodules_dir" in info
        assert "log_level" in info
        assert "components" in info
