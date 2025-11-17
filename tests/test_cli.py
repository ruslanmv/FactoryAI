"""Tests for command-line interface module.

Author: Ruslan Magana
Website: https://ruslanmv.com
License: Apache 2.0
"""

from pathlib import Path
from unittest.mock import MagicMock, patch
from argparse import Namespace

import pytest

from factoryai.cli import (
    cmd_info,
    cmd_list,
    cmd_run,
    cmd_status,
    cmd_sync,
    cmd_validate,
    create_parser,
    main,
)
from factoryai.core import FactoryAIOrchestrator
from factoryai.exceptions import FactoryAIError


class TestCreateParser:
    """Tests for create_parser function."""

    def test_create_parser(self) -> None:
        """Test parser creation."""
        parser = create_parser()

        assert parser is not None
        assert parser.prog == "factoryai"

    def test_parser_version(self) -> None:
        """Test version argument."""
        parser = create_parser()

        with pytest.raises(SystemExit):
            parser.parse_args(["--version"])

    def test_parser_verbose(self) -> None:
        """Test verbose argument."""
        parser = create_parser()
        args = parser.parse_args(["--verbose", "status"])

        assert args.verbose is True

    def test_parser_sync_command(self) -> None:
        """Test sync command parsing."""
        parser = create_parser()
        args = parser.parse_args(["sync"])

        assert args.command == "sync"
        assert args.force is False

    def test_parser_sync_force(self) -> None:
        """Test sync command with force flag."""
        parser = create_parser()
        args = parser.parse_args(["sync", "--force"])

        assert args.force is True

    def test_parser_run_command(self) -> None:
        """Test run command parsing."""
        parser = create_parser()
        args = parser.parse_args(["run", "app"])

        assert args.command == "run"
        assert args.component == "app"

    def test_parser_run_with_args(self) -> None:
        """Test run command with additional arguments."""
        parser = create_parser()
        args = parser.parse_args(["run", "app", "--arg1", "value1"])

        assert args.component == "app"
        assert args.args == ["--arg1", "value1"]


class TestCommandFunctions:
    """Tests for CLI command functions."""

    @patch("factoryai.cli.FactoryAIOrchestrator.sync_submodules")
    def test_cmd_sync_success(self, mock_sync: MagicMock) -> None:
        """Test sync command success."""
        from factoryai.config import FactoryAIConfig

        config = FactoryAIConfig(root_dir=Path("/test/root"))
        orchestrator = FactoryAIOrchestrator(config)
        args = Namespace(force=False)

        result = cmd_sync(orchestrator, args)

        assert result == 0
        mock_sync.assert_called_once()

    @patch("factoryai.cli.FactoryAIOrchestrator.sync_submodules")
    def test_cmd_sync_failure(self, mock_sync: MagicMock) -> None:
        """Test sync command failure."""
        from factoryai.config import FactoryAIConfig

        mock_sync.side_effect = FactoryAIError("Sync failed")

        config = FactoryAIConfig(root_dir=Path("/test/root"))
        orchestrator = FactoryAIOrchestrator(config)
        args = Namespace(force=False)

        result = cmd_sync(orchestrator, args)

        assert result == 1

    def test_cmd_status(self) -> None:
        """Test status command."""
        from factoryai.config import FactoryAIConfig

        config = FactoryAIConfig(root_dir=Path("/test/root"))
        orchestrator = FactoryAIOrchestrator(config)
        args = Namespace()

        result = cmd_status(orchestrator, args)

        assert result == 0

    def test_cmd_info(self) -> None:
        """Test info command."""
        from factoryai.config import FactoryAIConfig

        config = FactoryAIConfig(root_dir=Path("/test/root"))
        orchestrator = FactoryAIOrchestrator(config)
        args = Namespace()

        result = cmd_info(orchestrator, args)

        assert result == 0

    @patch("factoryai.cli.FactoryAIOrchestrator.validate_installation")
    def test_cmd_validate_success(self, mock_validate: MagicMock) -> None:
        """Test validate command with successful validation."""
        from factoryai.config import FactoryAIConfig

        mock_validate.return_value = {
            "valid": True,
            "git_installed": True,
            "is_git_repo": True,
            "submodules_initialized": True,
            "components": {},
            "errors": []
        }

        config = FactoryAIConfig(root_dir=Path("/test/root"))
        orchestrator = FactoryAIOrchestrator(config)
        args = Namespace()

        result = cmd_validate(orchestrator, args)

        assert result == 0

    @patch("factoryai.cli.FactoryAIOrchestrator.validate_installation")
    def test_cmd_validate_failure(self, mock_validate: MagicMock) -> None:
        """Test validate command with validation errors."""
        from factoryai.config import FactoryAIConfig

        mock_validate.return_value = {
            "valid": False,
            "git_installed": False,
            "is_git_repo": True,
            "submodules_initialized": False,
            "components": {},
            "errors": ["Git is not installed"]
        }

        config = FactoryAIConfig(root_dir=Path("/test/root"))
        orchestrator = FactoryAIOrchestrator(config)
        args = Namespace()

        result = cmd_validate(orchestrator, args)

        assert result == 1

    def test_cmd_list(self) -> None:
        """Test list command."""
        from factoryai.config import FactoryAIConfig

        config = FactoryAIConfig(root_dir=Path("/test/root"))
        orchestrator = FactoryAIOrchestrator(config)
        args = Namespace()

        result = cmd_list(orchestrator, args)

        assert result == 0

    @patch("factoryai.cli.FactoryAIOrchestrator.run_component")
    def test_cmd_run_success(self, mock_run: MagicMock) -> None:
        """Test run command success."""
        from factoryai.config import FactoryAIConfig

        mock_run.return_value = 0

        config = FactoryAIConfig(root_dir=Path("/test/root"))
        orchestrator = FactoryAIOrchestrator(config)
        args = Namespace(component="app", args=None, non_interactive=False)

        result = cmd_run(orchestrator, args)

        assert result == 0
        mock_run.assert_called_once()

    @patch("factoryai.cli.FactoryAIOrchestrator.run_component")
    def test_cmd_run_failure(self, mock_run: MagicMock) -> None:
        """Test run command failure."""
        from factoryai.config import FactoryAIConfig

        mock_run.side_effect = FactoryAIError("Component failed")

        config = FactoryAIConfig(root_dir=Path("/test/root"))
        orchestrator = FactoryAIOrchestrator(config)
        args = Namespace(component="app", args=None, non_interactive=False)

        result = cmd_run(orchestrator, args)

        assert result == 1


class TestMain:
    """Tests for main entry point."""

    def test_main_no_args(self) -> None:
        """Test main with no arguments."""
        result = main([])

        # Should show help and return 0
        assert result == 0

    @patch("factoryai.cli.cmd_status")
    def test_main_status_command(self, mock_cmd_status: MagicMock) -> None:
        """Test main with status command."""
        mock_cmd_status.return_value = 0

        result = main(["status"])

        assert result == 0
        mock_cmd_status.assert_called_once()

    def test_main_verbose_flag(self) -> None:
        """Test main with verbose flag."""
        # Should not crash with verbose flag
        result = main(["--verbose", "info"])

        assert isinstance(result, int)
