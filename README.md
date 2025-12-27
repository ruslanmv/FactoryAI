# FactoryAI Suite

![FactoryAI Logo](./assets/logo-small.jpg)

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**FactoryAI** is a cutting-edge suite of AI-powered tools designed to revolutionize software development. Unlike traditional code generation assistants, FactoryAI provides a comprehensive, end-to-end solution for creating, enhancing, and debugging software projects autonomously.

The suite consists of three core components, each addressing a distinct phase of the software development lifecycle:

1. **[Factory-App-AI](https://github.com/ruslanmv/Factory-App-AI)** - Dynamic project generation
2. **[Factory-Feature](https://github.com/ruslanmv/Factory-Feature)** - Intelligent feature integration
3. **[Factory-Debug](https://github.com/ruslanmv/Factory-Debug)** - AI-powered debugging (Coming Soon)

---

## 🚀 Features

### Complete Development Automation
- **End-to-End Pipeline**: From initial project scaffolding to production-ready deployment
- **AI-Powered Intelligence**: Leverages state-of-the-art models (OpenAI ChatGPT, IBM WatsonX.ai)
- **Modular Architecture**: Use components independently or as an integrated suite
- **Production-Ready**: Industry-standard code quality, type hints, comprehensive documentation

### Component Highlights

#### Factory-App-AI
- Dynamic project structure generation
- Automated file creation with dependency handling
- Built-in validation and containerization
- Interactive Gradio interface
- **Based on**: [arXiv:2411.10861](https://arxiv.org/abs/2411.10861) - Standard Method

#### Factory-Feature
- Context-aware feature integration
- Vector database for efficient code retrieval
- Framework and language agnostic
- Seamless project enhancement workflow
- **Based on**: [arXiv:2411.18226](https://arxiv.org/abs/2411.18226) - Feature-Factory Algorithm

#### Factory-Debug
- Autonomous bug detection and fixing
- Iterative debugging workflow
- AI-powered code analysis
- Customizable solution refinement

---

## 📋 Table of Contents

- [About](#about)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Components](#components)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

---

## 🎯 About

FactoryAI Suite is designed for developers, scientists, and businesses who want to:

- **Accelerate Development**: Automate repetitive tasks and focus on innovation
- **Maintain Quality**: Generate production-ready code with best practices
- **Scale Efficiently**: Handle projects of any size with AI-powered assistance
- **Reduce Errors**: Leverage AI for debugging and code analysis

Built on cutting-edge research and industry best practices, FactoryAI represents the future of software development automation.

---

## 🔧 Installation

### Prerequisites

- **Python**: 3.9 or higher
- **Git**: For submodule management
- **uv**: Fast Python package installer ([Install uv](https://github.com/astral-sh/uv))

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Installation Methods

#### Method 1: Using Make (Recommended)

```bash
# Clone the repository
git clone --recurse-submodules https://github.com/ruslanmv/FactoryAI.git
cd FactoryAI

# Install FactoryAI
make install

# Synchronize submodules
make sync

# Validate installation
make validate
```

#### Method 2: Using uv directly

```bash
# Clone the repository
git clone https://github.com/ruslanmv/FactoryAI.git
cd FactoryAI

# Install with uv
uv pip install -e .

# Synchronize submodules
chmod +x sync.sh
./sync.sh

# Validate installation
factoryai validate
```

#### Method 3: Development Installation

```bash
# Clone the repository
git clone https://github.com/ruslanmv/FactoryAI.git
cd FactoryAI

# Complete development setup
make dev-setup

# Or manually:
uv pip install -e ".[dev]"
./sync.sh
```

---

## ⚡ Quick Start

After installation, verify everything is working:

```bash
# Check FactoryAI status
factoryai status

# View available components
factoryai list

# Get installation info
factoryai info
```

Run a component:

```bash
# Run Factory-App-AI
factoryai run app

# Run Factory-Feature
factoryai run feature

# Or use Make shortcuts
make run-app
make run-feature
```

---

## 📖 Usage

### Command-Line Interface

FactoryAI provides a unified CLI for all operations:

```bash
factoryai [command] [options]
```

#### Available Commands



---

## 🧩 Components

### 1. Factory-App-AI

**Dynamic Project Generation with Generative AI**

Factory-App-AI enables rapid project scaffolding using AI models. It generates complete project structures, files, and configurations based on user requirements.

**Key Features:**
- AI-powered project tree generation
- Automatic dependency resolution
- File validation and verification
- Docker containerization support
- Interactive Gradio web interface

**Usage:**
```bash
factoryai run app
# or
make run-app
```

**Repository**: [Factory-App-AI](https://github.com/ruslanmv/Factory-App-AI)

---

### 2. Factory-Feature

**Intelligent Feature Integration for Existing Projects**

Factory-Feature analyzes your existing codebase and seamlessly integrates new features while maintaining project coherence and style.

**Key Features:**
- Context-aware code analysis
- Vector database for efficient retrieval
- Framework and language agnostic
- Automated project updates
- Maintains code consistency

**Workflow:**
```
project_old/ → Analysis → Feature Integration → project_new/
```

**Usage:**
```bash
factoryai run feature
# or
make run-feature
```

**Repository**: [Factory-Feature](https://github.com/ruslanmv/Factory-Feature)

---

### 3. Factory-Debug

**AI-Powered Debugging and Auto-Fixing** *(Coming Soon)*

Factory-Debug automatically detects bugs, analyzes code logic, and provides or applies fixes autonomously.

**Planned Features:**
- Autonomous bug detection
- AI-powered code analysis
- Iterative debugging workflow
- Customizable fix suggestions
- Developer-friendly interface

**Repository**: [Factory-Debug](https://github.com/ruslanmv/Factory-Debug)

---

## 🛠️ Development

### Setting Up Development Environment

```bash
# Clone repository
git clone https://github.com/ruslanmv/FactoryAI.git
cd FactoryAI

# Setup development environment
make dev-setup

# Or manually:
uv pip install -e ".[dev]"
./sync.sh
```

### Code Quality Standards

FactoryAI adheres to strict code quality standards:

- **PEP 8**: Python code style guide compliance
- **Type Hints**: Full type annotation coverage
- **Docstrings**: Comprehensive documentation for all modules, classes, and functions
- **Testing**: Comprehensive test coverage with pytest
- **Linting**: Automated checks with ruff and mypy
- **Formatting**: Consistent code style with black and isort

### Running Quality Checks

```bash
# Format code
make format

# Run linters
make lint

# Run tests
make test

# Run tests with coverage
make test-cov

# Run all checks
make check
```

### Project Structure

```
FactoryAI/
├── factoryai/              # Main package
│   ├── __init__.py         # Package initialization
│   ├── cli.py              # Command-line interface
│   ├── config.py           # Configuration management
│   ├── core.py             # Core orchestration logic
│   ├── exceptions.py       # Custom exceptions
│   └── utils.py            # Utility functions
├── tests/                  # Test suite
│   ├── __init__.py
│   ├── test_cli.py
│   ├── test_config.py
│   ├── test_core.py
│   └── test_utils.py
├── src/platfom/            # Submodules directory
│   ├── Factory-App-AI/     # Factory-App-AI submodule
│   ├── Factory-Feature/    # Factory-Feature submodule
│   └── Factory-Debug/      # Factory-Debug submodule
├── assets/                 # Assets (logos, images)
├── pyproject.toml          # Project configuration (uv standard)
├── Makefile                # Build automation
├── README.md               # This file
├── LICENSE                 # Apache 2.0 License
├── .gitignore              # Git ignore rules
└── sync.sh                 # Submodule sync script
```

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with proper tests and documentation
4. Run quality checks (`make check`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Contribution Guidelines

- Follow PEP 8 style guidelines
- Add type hints to all functions
- Write comprehensive docstrings
- Include tests for new features
- Update documentation as needed

---

## 📄 License

This project is licensed under the **Apache License 2.0** - see the [LICENSE](LICENSE) file for details.

```
Copyright 2024 Ruslan Magana

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

---

## 👤 Author

**Ruslan Magana**

- Website: [ruslanmv.com](https://ruslanmv.com)
- GitHub: [@ruslanmv](https://github.com/ruslanmv)
- Email: contact@ruslanmv.com

---

## 🌟 Acknowledgments

- OpenAI for ChatGPT API
- IBM for WatsonX.ai platform
- Research papers:
  - [arXiv:2411.10861](https://arxiv.org/abs/2411.10861) - Standard Method for Factory-App-AI
  - [arXiv:2411.18226](https://arxiv.org/abs/2411.18226) - Feature-Factory Algorithm for Factory-Feature

---

## 📊 Project Status

- **Factory-App-AI**: ✅ Active Development
- **Factory-Feature**: ✅ Active Development
- **Factory-Debug**: 🚧 Coming Soon

---

## 🔗 Links

- [Documentation](https://github.com/ruslanmv/FactoryAI#readme)
- [Issue Tracker](https://github.com/ruslanmv/FactoryAI/issues)
- [Changelog](https://github.com/ruslanmv/FactoryAI/blob/main/CHANGELOG.md)
- [Website](https://ruslanmv.com)

---

<div align="center">

**Built with ❤️ by [Ruslan Magana](https://ruslanmv.com)**

*Empowering developers with AI-driven automation*

This project is licensed under the [Apache 2.0 License](LICENSE).
