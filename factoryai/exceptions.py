"""Custom exceptions for FactoryAI Suite.

This module defines custom exception classes used throughout the FactoryAI
suite for better error handling and debugging.

Author: Ruslan Magana
Website: https://ruslanmv.com
License: Apache 2.0
"""

from typing import Optional


class FactoryAIError(Exception):
    """Base exception class for all FactoryAI errors.

    All custom exceptions in the FactoryAI suite should inherit from this class.
    """

    def __init__(self, message: str, details: Optional[str] = None) -> None:
        """Initialize the FactoryAIError.

        Args:
            message: The error message.
            details: Optional additional details about the error.
        """
        self.message = message
        self.details = details
        super().__init__(self.message)

    def __str__(self) -> str:
        """Return string representation of the error.

        Returns:
            Formatted error message with optional details.
        """
        if self.details:
            return f"{self.message}\nDetails: {self.details}"
        return self.message


class SubmoduleNotFoundError(FactoryAIError):
    """Raised when a required submodule is not found or initialized."""

    def __init__(self, submodule_name: str) -> None:
        """Initialize SubmoduleNotFoundError.

        Args:
            submodule_name: Name of the missing submodule.
        """
        message = f"Submodule '{submodule_name}' not found or not initialized."
        details = "Run 'factoryai sync' or 'make sync' to initialize submodules."
        super().__init__(message, details)


class ConfigurationError(FactoryAIError):
    """Raised when there is a configuration-related error."""

    pass


class ComponentError(FactoryAIError):
    """Raised when a FactoryAI component fails to execute."""

    def __init__(self, component: str, message: str) -> None:
        """Initialize ComponentError.

        Args:
            component: Name of the component that failed.
            message: Description of the error.
        """
        super().__init__(
            message=f"Component '{component}' failed: {message}",
            details=None
        )


class ValidationError(FactoryAIError):
    """Raised when input validation fails."""

    pass
