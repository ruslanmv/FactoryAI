"""FactoryAI Suite - AI-Powered Software Development Automation.

This package provides an orchestrated suite of AI-powered tools for
end-to-end software development automation, including:
- Factory-App-AI: Dynamic project generation
- Factory-Feature: Intelligent feature integration
- Factory-Debug: AI-powered debugging and fixing

Author: Ruslan Magana
Website: https://ruslanmv.com
License: Apache 2.0
"""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("factoryai")
except PackageNotFoundError:
    __version__ = "0.1.0"

__author__ = "Ruslan Magana"
__email__ = "contact@ruslanmv.com"
__license__ = "Apache 2.0"
__all__ = ["__version__", "__author__", "__email__", "__license__"]
