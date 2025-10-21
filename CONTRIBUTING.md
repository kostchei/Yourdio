# Contributing to Yourdio

Thank you for your interest in contributing to Yourdio! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Code Style](#code-style)
- [Submitting Changes](#submitting-changes)

## Code of Conduct

This project welcomes contributions from everyone. Please be respectful and constructive in all interactions.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/Yourdio.git
   cd Yourdio
   ```

3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/kostchei/Yourdio.git
   ```

## Development Setup

### Prerequisites

- Python 3.9 or higher
- Git

### Install Development Dependencies

```bash
# Create a virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install the package in editable mode with dev dependencies
pip install -e ".[dev]"
```

### Install Pre-commit Hooks (Optional but Recommended)

```bash
pip install pre-commit
pre-commit install
```

This will automatically run code formatters and linters before each commit.

## Making Changes

### Creating a Branch

Create a new branch for your changes:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

Use descriptive branch names:
- `feature/` for new features
- `fix/` for bug fixes
- `docs/` for documentation changes
- `refactor/` for code refactoring

### Code Organization

- **yourdio.py** - Core 6-hour composition generator
- **yourdio_gui.py** - Windows GUI application
- **event_generator.py** - Short event soundscape generator
- **theme_loader.py** - YAML theme loading and validation
- **themes/** - Pre-configured YAML theme files
- **tests/** - Test suite

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov

# Run specific test file
pytest tests/test_theme_loader.py

# Run specific test
pytest tests/test_theme_loader.py::TestThemeLoader::test_default_theme_exists
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files `test_*.py`
- Name test functions `test_*`
- Use descriptive test names that explain what is being tested
- Include docstrings explaining the test purpose

Example:

```python
def test_theme_loading_with_valid_file():
    """Test that a valid theme YAML file loads successfully"""
    # Test implementation
```

### Test Coverage

Aim for high test coverage, especially for:
- Theme loading and validation
- MIDI generation core logic
- Event configuration processing

## Code Style

### Python Style Guide

We follow PEP 8 with some modifications:

- **Line length**: 100 characters (not 79)
- **Formatter**: Black
- **Linter**: Flake8
- **Type checker**: mypy (optional but encouraged)

### Running Code Quality Tools

```bash
# Format code with Black
black .

# Check code style with Flake8
flake8 .

# Type check with mypy
mypy yourdio.py theme_loader.py event_generator.py
```

### Pre-commit Hook

If you installed pre-commit hooks, these tools run automatically on commit.

### Code Conventions

- Use descriptive variable names
- Add docstrings to all public functions and classes
- Use type hints where appropriate
- Keep functions focused and concise
- Comment complex algorithms (especially chaos theory math)

Example:

```python
def calculate_intensity_arc(chapter: int, total_chapters: int, arc_type: str) -> float:
    """
    Calculate the intensity value for a chapter based on the structural arc.

    Args:
        chapter: Current chapter number (0-indexed)
        total_chapters: Total number of chapters
        arc_type: Type of arc ('parabolic', 'slow_burn', etc.)

    Returns:
        Intensity value between 0.0 and 1.0
    """
    # Implementation
```

## Submitting Changes

### Commit Messages

Write clear, descriptive commit messages:

```
Short summary (50 chars or less)

More detailed explanation if needed. Wrap at 72 characters.
Explain what changed and why, not just what was done.

- Bullet points are fine
- Use present tense ("Add feature" not "Added feature")
```

### Pull Request Process

1. **Update your branch** with the latest upstream changes:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Push your changes** to your fork:
   ```bash
   git push origin your-branch-name
   ```

3. **Create a Pull Request** on GitHub:
   - Provide a clear description of the changes
   - Reference any related issues
   - Include screenshots for UI changes
   - Ensure all tests pass

4. **Respond to feedback** from reviewers

5. **Update your PR** as needed:
   ```bash
   # Make changes
   git add .
   git commit -m "Address review feedback"
   git push origin your-branch-name
   ```

### Pull Request Checklist

- [ ] Tests pass locally (`pytest`)
- [ ] Code follows style guidelines (`black`, `flake8`)
- [ ] New code has tests
- [ ] Documentation updated if needed
- [ ] CHANGELOG.md updated for user-facing changes
- [ ] Commit messages are clear and descriptive

## Types of Contributions

### Bug Reports

- Use the GitHub issue tracker
- Include Python version, OS, and error messages
- Provide steps to reproduce
- Include YAML theme files if relevant

### Feature Requests

- Describe the use case
- Explain why it would be useful
- Consider implementation complexity

### Code Contributions

Areas where contributions are especially welcome:

- **New themes** - Additional YAML theme configurations
- **Tests** - Expand test coverage
- **Documentation** - Improve or clarify existing docs
- **Performance** - Optimize MIDI generation
- **Features** - New musical algorithms or chaos theory applications
- **Cross-platform** - macOS/Linux support improvements

### Documentation

- Fix typos or unclear explanations
- Add examples
- Improve API documentation
- Create tutorials or guides

## Questions?

If you have questions about contributing, feel free to:
- Open an issue on GitHub
- Check existing documentation
- Review closed issues and PRs for examples

Thank you for contributing to Yourdio!
