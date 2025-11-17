"""Configuration management for FactoryAI Suite.

This module handles configuration loading, validation, and management
for all FactoryAI components.

Author: Ruslan Magana
Website: https://ruslanmv.com
License: Apache 2.0
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Optional, Any
import json
import logging

from factoryai.exceptions import ConfigurationError


logger = logging.getLogger(__name__)


@dataclass
class SubmoduleConfig:
    """Configuration for a FactoryAI submodule component.

    Attributes:
        name: Name of the submodule.
        path: Relative path to the submodule.
        url: Git repository URL.
        enabled: Whether the submodule is enabled.
    """

    name: str
    path: str
    url: str
    enabled: bool = True


@dataclass
class FactoryAIConfig:
    """Main configuration class for FactoryAI Suite.

    Attributes:
        root_dir: Root directory of the FactoryAI installation.
        submodules_dir: Directory containing submodules.
        log_level: Logging level.
        log_file: Optional log file path.
        components: Dictionary of component configurations.
    """

    root_dir: Path
    submodules_dir: Path = field(default_factory=lambda: Path("src/platfom"))
    log_level: str = "INFO"
    log_file: Optional[Path] = None
    components: Dict[str, SubmoduleConfig] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Post-initialization processing."""
        # Ensure paths are Path objects
        if not isinstance(self.root_dir, Path):
            self.root_dir = Path(self.root_dir)
        if not isinstance(self.submodules_dir, Path):
            self.submodules_dir = Path(self.submodules_dir)

        # Convert relative paths to absolute
        if not self.submodules_dir.is_absolute():
            self.submodules_dir = self.root_dir / self.submodules_dir

        # Initialize default components if not provided
        if not self.components:
            self._init_default_components()

    def _init_default_components(self) -> None:
        """Initialize default component configurations."""
        self.components = {
            "factory-app-ai": SubmoduleConfig(
                name="Factory-App-AI",
                path="src/platfom/Factory-App-AI",
                url="https://github.com/ruslanmv/Factory-App-AI"
            ),
            "factory-feature": SubmoduleConfig(
                name="Factory-Feature",
                path="src/platfom/Factory-Feature",
                url="https://github.com/ruslanmv/Factory-Feature"
            ),
            "factory-debug": SubmoduleConfig(
                name="Factory-Debug",
                path="src/platfom/Factory-Debug",
                url="https://github.com/ruslanmv/Factory-Debug",
                enabled=False  # Coming soon
            )
        }

    def get_component_path(self, component_name: str) -> Path:
        """Get the absolute path to a component.

        Args:
            component_name: Name of the component.

        Returns:
            Absolute path to the component directory.

        Raises:
            ConfigurationError: If component is not found.
        """
        if component_name not in self.components:
            raise ConfigurationError(
                f"Component '{component_name}' not found in configuration."
            )

        component = self.components[component_name]
        component_path = self.root_dir / component.path
        return component_path

    def is_component_available(self, component_name: str) -> bool:
        """Check if a component is available and initialized.

        Args:
            component_name: Name of the component.

        Returns:
            True if component is available, False otherwise.
        """
        if component_name not in self.components:
            return False

        component_path = self.get_component_path(component_name)
        return component_path.exists() and component_path.is_dir()

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary.

        Returns:
            Dictionary representation of the configuration.
        """
        return {
            "root_dir": str(self.root_dir),
            "submodules_dir": str(self.submodules_dir),
            "log_level": self.log_level,
            "log_file": str(self.log_file) if self.log_file else None,
            "components": {
                name: {
                    "name": comp.name,
                    "path": comp.path,
                    "url": comp.url,
                    "enabled": comp.enabled
                }
                for name, comp in self.components.items()
            }
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FactoryAIConfig":
        """Create configuration from dictionary.

        Args:
            data: Dictionary containing configuration data.

        Returns:
            FactoryAIConfig instance.
        """
        components = {}
        if "components" in data:
            for name, comp_data in data["components"].items():
                components[name] = SubmoduleConfig(**comp_data)

        return cls(
            root_dir=Path(data["root_dir"]),
            submodules_dir=Path(data.get("submodules_dir", "src/platfom")),
            log_level=data.get("log_level", "INFO"),
            log_file=Path(data["log_file"]) if data.get("log_file") else None,
            components=components
        )

    def save(self, path: Path) -> None:
        """Save configuration to JSON file.

        Args:
            path: Path to save the configuration file.
        """
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.to_dict(), f, indent=2)
            logger.info(f"Configuration saved to {path}")
        except Exception as e:
            raise ConfigurationError(f"Failed to save configuration: {e}")

    @classmethod
    def load(cls, path: Path) -> "FactoryAIConfig":
        """Load configuration from JSON file.

        Args:
            path: Path to the configuration file.

        Returns:
            FactoryAIConfig instance.

        Raises:
            ConfigurationError: If loading fails.
        """
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return cls.from_dict(data)
        except FileNotFoundError:
            raise ConfigurationError(f"Configuration file not found: {path}")
        except json.JSONDecodeError as e:
            raise ConfigurationError(f"Invalid JSON in configuration: {e}")
        except Exception as e:
            raise ConfigurationError(f"Failed to load configuration: {e}")


def get_default_config() -> FactoryAIConfig:
    """Get default configuration based on environment.

    Returns:
        Default FactoryAIConfig instance.
    """
    # Try to detect root directory
    current_dir = Path.cwd()

    # Check if we're in the FactoryAI directory
    if (current_dir / ".git").exists() and (current_dir / "sync.sh").exists():
        root_dir = current_dir
    else:
        # Default to current directory
        root_dir = current_dir

    config = FactoryAIConfig(root_dir=root_dir)

    # Check for environment variables
    if "FACTORYAI_LOG_LEVEL" in os.environ:
        config.log_level = os.environ["FACTORYAI_LOG_LEVEL"]

    if "FACTORYAI_LOG_FILE" in os.environ:
        config.log_file = Path(os.environ["FACTORYAI_LOG_FILE"])

    return config


def setup_logging(config: FactoryAIConfig) -> None:
    """Setup logging based on configuration.

    Args:
        config: FactoryAI configuration.
    """
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    handlers = [logging.StreamHandler()]

    if config.log_file:
        handlers.append(logging.FileHandler(config.log_file))

    logging.basicConfig(
        level=getattr(logging, config.log_level.upper()),
        format=log_format,
        handlers=handlers
    )
