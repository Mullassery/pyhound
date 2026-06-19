# Contributing to PyHound

Thank you for considering contributing to PyHound! We welcome contributions of all kinds.

## Getting Started

### Prerequisites
- Python 3.8+
- Rust 1.70+
- pip or uv

### Development Setup

```bash
# Clone the repository
git clone https://github.com/Mullassery/pyhound.git
cd pyhound

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[all]"

# Install pre-commit hooks (optional but recommended)
pip install pre-commit
pre-commit install
```

### Building from Source

```bash
# Build Rust extension
maturin develop

# Run tests
pytest tests/

# Run linting
black pyhound/ tests/
ruff check pyhound/ tests/
mypy pyhound/
```

## Code Style

We follow:
- **Python:** PEP 8 via Black (line length: 100)
- **Rust:** Standard Rust conventions via rustfmt
- **Type hints:** Full type annotations for Python

```bash
# Format code
black pyhound/ tests/
cargo fmt

# Check types
mypy pyhound/

# Lint
ruff check pyhound/ tests/
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pyhound

# Run specific test file
pytest tests/test_diagnosis.py

# Run specific test
pytest tests/test_diagnosis.py::test_basic_diagnosis
```

Write tests for new features:
```python
# tests/test_feature.py
def test_new_feature():
    """Test description."""
    hound = Hound(db="mock")
    result = hound.new_feature()
    assert result is not None
```

## Commit Messages

Follow conventional commits:
```
feat: Add new feature
fix: Fix a bug
docs: Update documentation
refactor: Refactor code
test: Add tests
chore: Update dependencies
```

Example:
```
feat: Add embedding quality scorer with isotropy metric

- Implement isotropy calculation in Rust core
- Add QualityScorer Python API
- Add tests for edge cases
- Update documentation
```

## Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Make your changes
4. Write/update tests
5. Update documentation if needed
6. Run linting and tests: `pytest && black . && ruff check .`
7. Push to your fork
8. Submit a pull request

### PR Guidelines
- Keep PRs focused on a single feature/fix
- Include test coverage (aim for >90%)
- Update docs if applicable
- Add entry to CHANGELOG.md
- Link related issues

## Documentation

Documentation lives in `docs/` directory:
- `docs/guide.md` — User guide
- `docs/api.md` — API reference
- `docs/architecture.md` — Architecture overview
- `docs/development.md` — Developer guide

Update docs when:
- Adding new features
- Changing APIs
- Improving explanations

## Areas for Contribution

### High Priority
- [ ] Core diagnostic engine (Rust)
- [ ] Database adapters (Qdrant, Chroma, Pinecone, etc.)
- [ ] Python wrapper completeness
- [ ] Test coverage

### Medium Priority
- [ ] Additional embedding metrics
- [ ] Performance optimizations
- [ ] Integration examples
- [ ] Documentation improvements

### Nice to Have
- [ ] CLI interface
- [ ] Web dashboard
- [ ] IDE plugins
- [ ] Language bindings (Node.js, Go, etc.)

## Reporting Issues

Report bugs with:
- Clear title and description
- Steps to reproduce
- Expected vs actual behavior
- Python/Rust version
- Traceback if applicable

Use the issue template on GitHub.

## Questions?

- Open a GitHub Discussion
- Check existing issues/discussions
- Email: mullassery@gmail.com

## Code of Conduct

Be respectful and constructive. We welcome all backgrounds and experience levels.

---

**Thank you for contributing to PyHound!** 🐕
