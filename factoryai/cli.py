"""Command-line interface for FactoryAI Suite.

This module provides the CLI entry point for the FactoryAI suite,
allowing users to interact with all components through a unified interface.

Author: Ruslan Magana
Website: https://ruslanmv.com
License: Apache 2.0
"""

import sys
import argparse
import logging
from pathlib import Path
from typing import Optional, List
import json

from factoryai import __version__
from factoryai.config import get_default_config, setup_logging
from factoryai.core import FactoryAIOrchestrator
from factoryai.exceptions import FactoryAIError
from factoryai.utils import format_list


logger = logging.getLogger(__name__)


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser.

    Returns:
        Configured ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(
        prog="factoryai",
        description=(
            "FactoryAI Suite - AI-Powered Software Development Automation\n"
            "An orchestrated suite of AI tools for end-to-end development."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  factoryai sync                    # Sync all submodules\n"
            "  factoryai status                  # Show component status\n"
            "  factoryai run app                 # Run Factory-App-AI\n"
            "  factoryai run feature             # Run Factory-Feature\n"
            "  factoryai validate                # Validate installation\n"
            "\n"
            "For more information, visit: https://ruslanmv.com\n"
        )
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"FactoryAI {__version__}"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    parser.add_argument(
        "--log-file",
        type=Path,
        help="Log file path"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Sync command
    sync_parser = subparsers.add_parser(
        "sync",
        help="Synchronize all git submodules"
    )
    sync_parser.add_argument(
        "--force",
        action="store_true",
        help="Force re-initialization of submodules"
    )

    # Status command
    subparsers.add_parser(
        "status",
        help="Show status of all components"
    )

    # Info command
    subparsers.add_parser(
        "info",
        help="Show FactoryAI installation information"
    )

    # Validate command
    subparsers.add_parser(
        "validate",
        help="Validate FactoryAI installation"
    )

    # Run command
    run_parser = subparsers.add_parser(
        "run",
        help="Run a FactoryAI component"
    )
    run_parser.add_argument(
        "component",
        choices=["app", "feature", "debug"],
        help="Component to run (app=Factory-App-AI, feature=Factory-Feature, debug=Factory-Debug)"
    )
    run_parser.add_argument(
        "args",
        nargs=argparse.REMAINDER,
        help="Arguments to pass to the component"
    )
    run_parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="Run in non-interactive mode"
    )

    # List command
    subparsers.add_parser(
        "list",
        help="List all available components"
    )

    return parser


def cmd_sync(orchestrator: FactoryAIOrchestrator, args: argparse.Namespace) -> int:
    """Handle the sync command.

    Args:
        orchestrator: FactoryAI orchestrator instance.
        args: Parsed command-line arguments.

    Returns:
        Exit code (0 for success, non-zero for failure).
    """
    try:
        print("Synchronizing FactoryAI submodules...")
        orchestrator.sync_submodules(force=args.force)
        print("✓ Submodules synchronized successfully")
        return 0
    except FactoryAIError as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1


def cmd_status(orchestrator: FactoryAIOrchestrator, args: argparse.Namespace) -> int:
    """Handle the status command.

    Args:
        orchestrator: FactoryAI orchestrator instance.
        args: Parsed command-line arguments.

    Returns:
        Exit code (0 for success).
    """
    print("FactoryAI Component Status")
    print("=" * 60)

    status = orchestrator.get_component_status()

    for component_name, component_status in status.items():
        status_icon = "✓" if component_status["available"] else "✗"
        enabled_text = "" if component_status["enabled"] else " (disabled)"

        print(f"\n{status_icon} {component_status['name']}{enabled_text}")
        print(f"  Path: {component_status['path']}")
        print(f"  Available: {component_status['available']}")
        print(f"  URL: {component_status['url']}")

    print("\n" + "=" * 60)

    # Check if sync is needed
    available_count = sum(
        1 for s in status.values()
        if s["available"] and s["enabled"]
    )

    if available_count == 0:
        print("\n⚠ No components are initialized.")
        print("Run 'factoryai sync' or 'make sync' to initialize submodules.")

    return 0


def cmd_info(orchestrator: FactoryAIOrchestrator, args: argparse.Namespace) -> int:
    """Handle the info command.

    Args:
        orchestrator: FactoryAI orchestrator instance.
        args: Parsed command-line arguments.

    Returns:
        Exit code (0 for success).
    """
    info = orchestrator.info()

    print("FactoryAI Installation Information")
    print("=" * 60)
    print(f"Version: {info['version']}")
    print(f"Root Directory: {info['root_dir']}")
    print(f"Submodules Directory: {info['submodules_dir']}")
    print(f"Log Level: {info['log_level']}")
    print("\nComponents:")

    for name, component in info['components'].items():
        status = "Available" if component["available"] else "Not Initialized"
        print(f"  • {component['name']}: {status}")

    print("=" * 60)
    return 0


def cmd_validate(orchestrator: FactoryAIOrchestrator, args: argparse.Namespace) -> int:
    """Handle the validate command.

    Args:
        orchestrator: FactoryAI orchestrator instance.
        args: Parsed command-line arguments.

    Returns:
        Exit code (0 for success, 1 for validation failure).
    """
    print("Validating FactoryAI installation...")
    print("=" * 60)

    results = orchestrator.validate_installation()

    # Check git
    git_status = "✓" if results["git_installed"] else "✗"
    print(f"{git_status} Git installed: {results['git_installed']}")

    # Check repository
    repo_status = "✓" if results["is_git_repo"] else "✗"
    print(f"{repo_status} Git repository: {results['is_git_repo']}")

    # Check submodules
    submodules_status = "✓" if results["submodules_initialized"] else "✗"
    print(f"{submodules_status} Submodules initialized: {results['submodules_initialized']}")

    # Check components
    print("\nComponent Status:")
    for name, status in results["components"].items():
        component_status = "✓" if status["available"] else "✗"
        enabled = "" if status["enabled"] else " (disabled)"
        print(f"  {component_status} {status['name']}{enabled}")

    print("\n" + "=" * 60)

    # Show errors
    if results["errors"]:
        print("\nIssues Found:")
        print(format_list(results["errors"], bullet="✗"))
        print("\nPlease resolve these issues to use FactoryAI.")
        return 1

    print("\n✓ Installation is valid and ready to use!")
    return 0


def cmd_run(orchestrator: FactoryAIOrchestrator, args: argparse.Namespace) -> int:
    """Handle the run command.

    Args:
        orchestrator: FactoryAI orchestrator instance.
        args: Parsed command-line arguments.

    Returns:
        Exit code from the component.
    """
    # Map short names to full component names
    component_map = {
        "app": "factory-app-ai",
        "feature": "factory-feature",
        "debug": "factory-debug"
    }

    component = component_map[args.component]

    try:
        print(f"Running {component}...")
        returncode = orchestrator.run_component(
            component,
            args=args.args if args.args else None,
            interactive=not args.non_interactive
        )
        return returncode

    except FactoryAIError as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        if e.details:
            print(f"Details: {e.details}", file=sys.stderr)
        return 1


def cmd_list(orchestrator: FactoryAIOrchestrator, args: argparse.Namespace) -> int:
    """Handle the list command.

    Args:
        orchestrator: FactoryAI orchestrator instance.
        args: Parsed command-line arguments.

    Returns:
        Exit code (0 for success).
    """
    print("Available FactoryAI Components")
    print("=" * 60)

    components = [
        {
            "name": "app",
            "full_name": "Factory-App-AI",
            "description": "Dynamic project generation using generative AI"
        },
        {
            "name": "feature",
            "full_name": "Factory-Feature",
            "description": "Intelligent feature integration for existing projects"
        },
        {
            "name": "debug",
            "full_name": "Factory-Debug",
            "description": "AI-powered debugging and auto-fixing (Coming Soon)"
        }
    ]

    for component in components:
        print(f"\n{component['name']}: {component['full_name']}")
        print(f"  {component['description']}")
        print(f"  Usage: factoryai run {component['name']}")

    print("\n" + "=" * 60)
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point for the FactoryAI CLI.

    Args:
        argv: Optional command-line arguments. If None, uses sys.argv.

    Returns:
        Exit code (0 for success, non-zero for failure).
    """
    parser = create_parser()
    args = parser.parse_args(argv)

    # Setup configuration
    config = get_default_config()

    if args.verbose:
        config.log_level = "DEBUG"

    if args.log_file:
        config.log_file = args.log_file

    setup_logging(config)

    # Create orchestrator
    try:
        orchestrator = FactoryAIOrchestrator(config)
    except Exception as e:
        print(f"✗ Failed to initialize FactoryAI: {e}", file=sys.stderr)
        return 1

    # Handle commands
    if args.command == "sync":
        return cmd_sync(orchestrator, args)
    elif args.command == "status":
        return cmd_status(orchestrator, args)
    elif args.command == "info":
        return cmd_info(orchestrator, args)
    elif args.command == "validate":
        return cmd_validate(orchestrator, args)
    elif args.command == "run":
        return cmd_run(orchestrator, args)
    elif args.command == "list":
        return cmd_list(orchestrator, args)
    else:
        parser.print_help()
        return 0


def entrypoint() -> None:
    """Entry point wrapper for console scripts."""
    sys.exit(main())


if __name__ == "__main__":
    entrypoint()
