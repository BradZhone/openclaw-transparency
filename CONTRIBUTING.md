# Contributing to OpenClaw Transparency Layer

First off, thank you for considering contributing to OpenClaw Transparency Layer! 🎉

## Ways to Contribute

### 🐛 Report Bugs

Found a bug? Please [open an issue](https://github.com/BradZhone/openclaw-transparency/issues/new) with:
- Clear description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Your environment (Python version, OS)

### 💡 Suggest Features

Have an idea? [Start a discussion](https://github.com/BradZhone/openclaw-transparency/discussions) with:
- Clear description of the feature
- Use case (why is this useful?)
- Possible implementation (optional)

### 📝 Improve Documentation

Documentation improvements are always welcome:
- Fix typos or unclear sections
- Add examples or use cases
- Improve code comments

### 🔧 Submit Code

Ready to submit code? Here's how:

#### 1. Fork and Clone

```bash
# Fork on GitHub, then:
git clone https://github.com/YOUR-USERNAME/openclaw-transparency.git
cd openclaw-transparency
```

#### 2. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

#### 3. Make Changes

- Write clean, readable code
- Follow PEP 8 style guide
- Add tests if applicable
- Update documentation

#### 4. Test Your Changes

```bash
# Run tests
python -m pytest

# Or run manual tests
python transparency.py
python multi_agent_transparency.py
```

#### 5. Commit and Push

```bash
git add .
git commit -m "feat: Add your feature description"
git push origin feature/your-feature-name
```

#### 6. Create Pull Request

- Go to your fork on GitHub
- Click "Create Pull Request"
- Describe your changes clearly
- Reference any related issues

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git

### Installation

```bash
# Clone the repo
git clone https://github.com/BradZhone/openclaw-transparency.git
cd openclaw-transparency

# No dependencies required! (uses stdlib only)
```

### Project Structure

```
openclaw-transparency/
├── transparency.py              # Core single-agent module
├── multi_agent_transparency.py  # Multi-agent tracking
├── html_report_generator.py     # HTML visualization
├── test_html_report.py          # Tests
├── examples/                    # Usage examples
├── docs/                        # Documentation
└── README.md                    # This file
```

## Coding Standards

### Python Style

- Follow [PEP 8](https://pep8.org/)
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused (single responsibility)

### Documentation

- Update README.md if needed
- Add inline comments for complex logic
- Update CHANGELOG.md with your changes

## Roadmap

### v0.3.0 (Next)
- [ ] Real-time dashboard (WebSocket)
- [ ] Git integration (auto-commit checkpoints)
- [ ] Enterprise compliance reports
- [ ] PDF export

### v1.0.0 (Future)
- [ ] Cloud sync
- [ ] AI-powered insights
- [ ] Enterprise features (SSO, RBAC)

## Questions?

- 💬 [Start a discussion](https://github.com/BradZhone/openclaw-transparency/discussions)
- 🐛 [Open an issue](https://github.com/BradZhone/openclaw-transparency/issues/new)
- 📧 Email: brad@example.com

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for making AI agents more transparent! 🙏**
