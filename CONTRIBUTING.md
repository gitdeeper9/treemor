# Contributing to TREEMOR

Thank you for your interest in contributing to TREEMOR! 🎉

## Code of Conduct

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.

## Getting Started

### Prerequisites

- Python 3.9+
- Git
- Basic knowledge of seismology/geophysics (helpful but not required)

### Development Setup

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/treomor.git
cd treomor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Install in development mode
pip install -e .

# Install dev dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

What to Contribute

1. Code Contributions

· FSIN parameter implementations: New or improved models
· Machine learning models: Better detection algorithms
· Dashboard features: New visualizations
· Performance optimizations: Faster data processing

2. Documentation

· API documentation improvements
· Tutorial notebooks
· Translation to other languages
· Example workflows

3. Validation

· New test sites and datasets
· Field validation reports
· Case studies

4. Research

· Extending the theoretical framework
· Publishing validation results
· Collaborations with seismology institutions

Development Workflow

1. Create an Issue

Before starting, create an issue describing:

· What you want to change
· Why it's needed
· How you plan to implement it

2. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

3. Make Changes

Follow coding standards:

· Black: black treomor tests
· isort: isort treomor tests
· flake8: flake8 treomor tests
· mypy: mypy treomor

4. Write Tests

Add tests in tests/ directory:

```python
# tests/test_fsin.py
import pytest
from treomor.fsin import ResonanceCalculator

def test_resonance_frequency():
    calc = ResonanceCalculator(E=13e9, D=1.0, L=50, rho=450)
    f0 = calc.fundamental_frequency()
    assert 0.4 < f0 < 0.6
```

5. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=treomor --cov-report=html

# Run specific test
pytest tests/test_fsin.py -v
```

6. Update Documentation

```bash
# Update docstrings
# Build documentation locally
cd docs
make html
```

7. Commit Changes

```bash
# Conventional commits
git commit -m "feat: add new FSIN parameter for canopy drag"
git commit -m "fix: correct root-soil impedance calculation"
git commit -m "docs: update API reference for FSIN module"
```

Commit types:

· feat: New feature
· fix: Bug fix
· docs: Documentation only
· style: Code style (formatting)
· refactor: Code restructuring
· test: Adding tests
· chore: Maintenance

8. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Create PR on GitHub with:

· Clear description
· Link to issue
· Screenshots (for UI changes)
· Test results

Code Structure

```
treomor/
├── __init__.py
├── cli.py              # Command line interface
├── engine.py           # Core detection engine
├── fsin.py             # FSIN parameter calculations
├── dashboard/
│   ├── app.py          # Dash application
│   ├── layouts.py      # Page layouts
│   └── callbacks.py    # Interactive callbacks
├── utils/
│   ├── io.py           # Data I/O (HDF5, NetCDF)
│   ├── signal.py       # Signal processing
│   └── validation.py   # Validation utilities
├── models/
│   ├── detector.py     # ML event detection
│   └── discriminator.py # Event classification
└── data/
    ├── validation/     # Validation datasets
    └── config/         # Configuration files
```

FSIN Parameter Guidelines

When adding/modifying FSIN parameters:

1. Document thoroughly: Include physical significance, units, typical values
2. Add validation: Test against known data
3. Update equations: Ensure mathematical rigor
4. Consider uncertainty: Include error bounds where possible

```python
def parameter_name(inputs):
    """
    Physical significance of parameter.
    
    Parameters
    ----------
    param1 : float
        Description with units
    param2 : float
        Description with units
    
    Returns
    -------
    float
        Parameter value with units
    
    Notes
    -----
    Mathematical derivation or references.
    Typical values and ranges.
    """
    # Implementation
    pass
```

Testing Standards

Unit Tests

```python
def test_edge_cases():
    """Test extreme values."""
    assert calc.fundamental_frequency(E=0) == 0
    with pytest.raises(ValueError):
        calc.fundamental_frequency(L=0)
```

Integration Tests

```python
def test_end_to_end_detection():
    """Test complete detection pipeline."""
    data = load_test_event()
    result = engine.detect(data)
    assert result.detected is True
    assert result.magnitude > 3.5
```

Performance Tests

```python
@pytest.mark.benchmark
def test_detection_speed(benchmark):
    def detect():
        return engine.detect(test_data)
    result = benchmark(detect)
    assert result.time < 1.0  # < 1 second
```

Documentation Standards

Docstrings (Google Style)

```python
def calculate_tssi(f0, xi, zeta, **kwargs):
    """Calculate Tree Seismic Sensitivity Index.
    
    The TSSI is a composite metric combining all nine FSIN parameters
    into a single sensitivity score.
    
    Args:
        f0 (float): Fundamental resonance frequency (Hz)
        xi (float): Seismic coupling coefficient (0-1)
        zeta (float): Damping ratio (0-1)
        **kwargs: Additional FSIN parameters
    
    Returns:
        float: TSSI value between 0 and 1
    
    Raises:
        ValueError: If any parameter is out of valid range
    
    Example:
        >>> tssi = calculate_tssi(0.48, 0.91, 0.08, EI=1.2e9)
        >>> print(tssi)
        0.82
    """
    pass
```

Review Process

1. Automated checks: CI runs tests, linting, type checking
2. Human review: At least one maintainer reviews
3. Feedback: Address comments and make changes
4. Merge: Squash and merge to main

Release Process

Maintainers handle releases:

```bash
# Update version
bumpversion patch  # or minor/major

# Build and upload to PyPI
python -m build
twine upload dist/*

# Create GitHub release
gh release create v1.0.1 --notes "Bug fixes and improvements"
```

Getting Help

· Discussions: GitHub Discussions
· Issues: Bug reports and feature requests
· Email: gitdeeper@gmail.com

Recognition

Contributors will be:

· Added to AUTHORS.md
· Acknowledged in release notes
· Cited in research papers (if applicable)

Thank you for contributing to open science! 🌍
