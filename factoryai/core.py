"""Core orchestration logic for FactoryAI Suite.

This module provides the main orchestration functionality for managing
and executing FactoryAI components.

Author: Ruslan Magana
Website: https://ruslanmv.com
License: Apache 2.0
"""

import logging
from pathlib import Path
from typing import Optional, Dict, Any
import subprocess

from factoryai.config import FactoryAIConfig, get_default_config
from factoryai.exceptions import (
    SubmoduleNotFoundError,
    ComponentError,
    FactoryAIError
)
from factoryai.utils import (
    run_command,
    check_git_installed,
    is_git_repository,
    ensure_directory
)


logger = logging.getLogger(__name__)


class FactoryAIOrchestrator:
    """Main orchestrator for FactoryAI Suite components.

    This class manages the initialization, synchronization, and execution
    of all FactoryAI components.

    Attributes:
        config: FactoryAI configuration instance.
    """

    def __init__(self, config: Optional[FactoryAIConfig] = None) -> None:
        """Initialize the FactoryAI orchestrator.

        Args:
            config: Optional FactoryAIConfig instance. If not provided,
                   default configuration will be used.
        """
        self.config = config or get_default_config()
        logger.info(f"Initialized FactoryAI orchestrator at {self.config.root_dir}")

    def sync_submodules(self, force: bool = False) -> None:
        """Synchronize all git submodules.

        Args:
            force: Whether to force re-initialization of submodules.

        Raises:
            FactoryAIError: If synchronization fails.
        """
        logger.info("Synchronizing submodules...")

        if not check_git_installed():
            raise FactoryAIError(
                "Git is not installed",
                details="Please install Git to use FactoryAI."
            )

        if not is_git_repository(self.config.root_dir):
            raise FactoryAIError(
                f"Not a git repository: {self.config.root_dir}",
                details="Please clone the FactoryAI repository properly."
            )

        try:
            # Ensure submodules directory exists
            ensure_directory(self.config.submodules_dir.parent)

            # Initialize and update submodules
            command = ["git", "submodule", "update", "--init", "--recursive"]
            if force:
                command.append("--force")

            returncode, stdout, stderr = run_command(
                command,
                cwd=self.config.root_dir,
                check=True
            )

            logger.info("Submodules synchronized successfully")
            logger.debug(f"Git output: {stdout}")

        except FactoryAIError:
            raise
        except Exception as e:
            raise FactoryAIError(f"Failed to sync submodules: {e}")

    def check_component_available(self, component: str) -> bool:
        """Check if a component is available.

        Args:
            component: Component name (e.g., 'factory-app-ai').

        Returns:
            True if component is available, False otherwise.
        """
        return self.config.is_component_available(component)

    def get_component_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all components.

        Returns:
            Dictionary mapping component names to their status information.
        """
        status = {}

        for component_name, component_config in self.config.components.items():
            component_path = self.config.get_component_path(component_name)
            is_available = component_path.exists()

            status[component_name] = {
                "name": component_config.name,
                "enabled": component_config.enabled,
                "available": is_available,
                "path": str(component_path),
                "url": component_config.url
            }

        return status

    def run_component(
        self,
        component: str,
        args: Optional[list] = None,
        interactive: bool = True
    ) -> int:
        """Run a FactoryAI component.

        Args:
            component: Component name (e.g., 'factory-app-ai').
            args: Optional arguments to pass to the component.
            interactive: Whether to run in interactive mode.

        Returns:
            Exit code from the component.

        Raises:
            SubmoduleNotFoundError: If component is not available.
            ComponentError: If component execution fails.
        """
        if not self.check_component_available(component):
            raise SubmoduleNotFoundError(component)

        component_config = self.config.components[component]
        if not component_config.enabled:
            raise ComponentError(
                component,
                "Component is not enabled"
            )

        component_path = self.config.get_component_path(component)
        logger.info(f"Running component: {component_config.name}")

        try:
            # Check for main entry point
            main_script = component_path / "main.py"
            if not main_script.exists():
                main_script = component_path / "app.py"

            if not main_script.exists():
                raise ComponentError(
                    component,
                    f"No main entry point found at {component_path}"
                )

            # Build command
            command = ["python", str(main_script)]
            if args:
                command.extend(args)

            # Run component
            if interactive:
                # Run interactively (user can see output in real-time)
                returncode = subprocess.run(
                    command,
                    cwd=component_path
                ).returncode
            else:
                # Run and capture output
                returncode, stdout, stderr = run_command(
                    command,
                    cwd=component_path,
                    check=False
                )
                if stdout:
                    logger.info(f"Component output:\n{stdout}")
                if stderr:
                    logger.error(f"Component errors:\n{stderr}")

            if returncode != 0:
                raise ComponentError(
                    component,
                    f"Component exited with code {returncode}"
                )

            logger.info(f"Component {component_config.name} completed successfully")
            return returncode

        except ComponentError:
            raise
        except Exception as e:
            raise ComponentError(component, str(e))

    def validate_installation(self) -> Dict[str, Any]:
        """Validate the FactoryAI installation.

        Returns:
            Dictionary containing validation results.
        """
        results = {
            "valid": True,
            "git_installed": False,
            "is_git_repo": False,
            "submodules_initialized": False,
            "components": {},
            "errors": []
        }

        # Check git
        results["git_installed"] = check_git_installed()
        if not results["git_installed"]:
            results["valid"] = False
            results["errors"].append("Git is not installed")

        # Check if git repository
        results["is_git_repo"] = is_git_repository(self.config.root_dir)
        if not results["is_git_repo"]:
            results["valid"] = False
            results["errors"].append("Not a git repository")

        # Check components
        component_status = self.get_component_status()
        results["components"] = component_status

        # Check if at least one component is available
        available_components = [
            name for name, status in component_status.items()
            if status["available"] and status["enabled"]
        ]

        results["submodules_initialized"] = len(available_components) > 0
        if not results["submodules_initialized"]:
            results["errors"].append(
                "No components are initialized. Run 'factoryai sync' or 'make sync'."
            )

        return results

    def info(self) -> Dict[str, Any]:
        """Get information about the FactoryAI installation.

        Returns:
            Dictionary containing installation information.
        """
        from factoryai import __version__

        return {
            "version": __version__,
            "root_dir": str(self.config.root_dir),
            "submodules_dir": str(self.config.submodules_dir),
            "log_level": self.config.log_level,
            "components": self.get_component_status()
        }
