# Contributing to oss-maintainer-compass

Thank you for considering a contribution to `oss-maintainer-compass`! This project is built by and for open source maintainers, and we welcome improvements from the community.

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/). By participating, you are expected to uphold this code. Please report unacceptable behavior to the maintainers.

## How to Contribute

### Report Bugs

Bug reports help us improve. When reporting a bug, please include:

- **Clear title and description** – Explain what the bug is and when it occurs
- **Steps to reproduce** – Provide specific steps with sample data
- **Expected behavior** – What should happen
- **Actual behavior** – What actually happens
- **Screenshots/logs** – Include error messages or output
- **Environment** – Python version, OS, etc.

Use the [bug report template](.github/ISSUE_TEMPLATE/bug_report.md) when opening an issue.

### Suggest Features

Feature requests are welcome! Please:

- **Explain the use case** – Why is this feature useful?
- **Provide examples** – How would maintainers use it?
- **Consider scope** – Does it fit with the project's philosophy of simplicity?

Use the [feature request template](.github/ISSUE_TEMPLATE/feature_request.md).

### Submit Code Changes

We use a standard GitHub fork + pull request workflow.

#### 1. Set up your development environment

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/oss-maintainer-compass.git
cd oss-maintainer-compass

# Create a feature branch
git checkout -b feature/your-feature-name
```

#### 2. Make your changes

- Follow the existing code style (PEP 8)
- Write tests for new functionality (we use `unittest`)
- Update documentation as needed
- Keep commits focused and descriptive

#### 3. Run tests

```bash
# Run all tests
python3 -m unittest discover -s tests -p "test_*.py" -v

# Run specific test file
python3 -m unittest tests.test_analyzer -v
```

#### 4. Commit and push

```bash
# Write clear commit messages
git commit -m "Add feature: describe what you added"

# Push to your fork
git push origin feature/your-feature-name
```

#### 5. Open a pull request

- Describe what your PR does and why
- Reference any related issues (e.g., "Fixes #42")
- Ensure CI passes (GitHub Actions)
- Be responsive to review feedback

## Development Guidelines

### Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use meaningful variable names
- Add docstrings to functions and classes
- Max line length: 100 characters (preferred), 120 (hard limit)

### Testing

- Write tests for new features and bug fixes
- Aim for >80% code coverage
- Use descriptive test names: `test_function_does_something_when_condition`
- Test both happy path and error cases

Example:

```python
import unittest
from src.oss_maintainer_compass.analyzer import IssueAnalyzer

class TestIssueAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = IssueAnalyzer()
    
    def test_identifies_stale_issues_correctly(self):
        # Test implementation
        pass
    
    def test_handles_empty_issue_list(self):
        # Test edge case
        pass
```

### Documentation

- Update README.md if adding user-facing features
- Add docstrings to new functions/classes
- Include examples for CLI commands
- Update ROADMAP.md if planning future work

### Commits

Write clear, descriptive commit messages:

```
# Good
Add staleness detection for issues without recent activity
Fix typo in reporter output formatting
Refactor analyzer to support custom label filters

# Avoid
Fix bug
Update code
Work in progress
```

## Project Philosophy

Keep these principles in mind when contributing:

1. **Zero runtime dependencies** – Use only Python standard library
2. **Simplicity over features** – Focus on core maintainer workflows
3. **Auditability** – Code should be easy to review and understand
4. **Maintainer-first** – Solutions should serve open source maintainers
5. **Extensibility** – Design for future AI/agent integration

## Review Process

Pull requests will be reviewed by maintainers for:

- Alignment with project goals
- Code quality and test coverage
- Documentation completeness
- Performance impact
- Security considerations

Reviews may take a few days. Please be patient and responsive to feedback!

## Getting Help

- **Questions?** Start a discussion: [GitHub Discussions](https://github.com/Psymath-code/oss-maintainer-compass/discussions)
- **Issues?** See [GitHub Issues](https://github.com/Psymath-code/oss-maintainer-compass/issues)
- **Security concern?** See [SECURITY.md](SECURITY.md)

## Recognition

Contributors are recognized in:

- Release notes
- Git commit history
- Project README (with permission)

Thank you for helping make `oss-maintainer-compass` better!
