# Contributing to Garuda: Mimpi Dunia yang Tertunda

Thank you for your interest in contributing to this sentiment analysis project! This document provides guidelines for contributing.

## 🤝 How to Contribute

### 1. Fork the Repository

```bash
# Fork via GitHub UI, then clone your fork
git clone https://github.com/YOUR_USERNAME/Analisis-Sentiment-Data_Mining.git
cd Analisis-Sentiment-Data_Mining
```

### 2. Create a Branch

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/bug-description
```

### 3. Make Your Changes

Follow the coding standards and best practices outlined below.

### 4. Test Your Changes

```bash
# Run tests
pytest tests/

# Test the dashboard
cd dashboard-next
npm run dev
```

### 5. Commit Your Changes

```bash
# Stage your changes
git add .

# Commit with descriptive message
git commit -m "feat: add new feature description"
```

**Commit Message Format:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting)
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

### 6. Push and Create Pull Request

```bash
# Push to your fork
git push origin feature/your-feature-name

# Create Pull Request via GitHub UI
```

---

## 📋 Contribution Guidelines

### Code Style

**Python:**
- Follow PEP 8 style guide
- Use type hints where applicable
- Add docstrings to functions and classes
- Maximum line length: 100 characters

```python
def process_text(text: str, remove_stopwords: bool = True) -> str:
    """
    Process and clean Indonesian text.
    
    Args:
        text: Input text to process
        remove_stopwords: Whether to remove stopwords
        
    Returns:
        Cleaned text string
    """
    # Implementation
    pass
```

**JavaScript/TypeScript:**
- Use ESLint and Prettier
- Follow React best practices
- Use TypeScript for type safety
- Functional components with hooks

```typescript
interface CommentProps {
  text: string;
  sentiment: 'positive' | 'negative' | 'neutral';
}

export const Comment: React.FC<CommentProps> = ({ text, sentiment }) => {
  // Implementation
};
```

### Documentation

- Update README.md if adding new features
- Add inline comments for complex logic
- Update relevant documentation in `/docs`
- Include examples in docstrings

### Testing

- Write unit tests for new functions
- Ensure existing tests pass
- Test edge cases
- Aim for >80% code coverage

---

## 🐛 Reporting Bugs

### Before Submitting

1. Check existing issues
2. Verify it's reproducible
3. Collect relevant information

### Bug Report Template

```markdown
**Description:**
Clear description of the bug

**Steps to Reproduce:**
1. Step one
2. Step two
3. ...

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happens

**Environment:**
- OS: [e.g., Ubuntu 22.04]
- Python version: [e.g., 3.12]
- Node.js version: [e.g., 18.17]

**Screenshots:**
If applicable
```

---

## 💡 Feature Requests

### Feature Request Template

```markdown
**Feature Description:**
Clear description of the proposed feature

**Use Case:**
Why is this feature needed?

**Proposed Solution:**
How should it work?

**Alternatives Considered:**
Other approaches you've thought about

**Additional Context:**
Any other relevant information
```

---

## 🔍 Code Review Process

1. **Automated Checks**: All PRs must pass automated tests
2. **Code Review**: At least one maintainer review required
3. **Documentation**: Ensure documentation is updated
4. **Testing**: New features must include tests
5. **Approval**: Maintainer approval before merge

---

## 📚 Development Setup

### Prerequisites

- Python 3.12+
- Node.js 18+
- Git
- Virtual environment tool

### Setup Steps

```bash
# 1. Clone repository
git clone https://github.com/Fahri-Hilm/Analisis-Sentiment-Data_Mining.git
cd Analisis-Sentiment-Data_Mining

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Install Node.js dependencies
cd dashboard-next
npm install

# 5. Run tests
cd ..
pytest tests/

# 6. Start development
cd dashboard-next
npm run dev
```

---

## 🎯 Areas for Contribution

### High Priority
- [ ] Model optimization and performance improvements
- [ ] Additional visualization features
- [ ] API endpoint development
- [ ] Mobile responsive improvements
- [ ] Documentation enhancements

### Medium Priority
- [ ] Additional ML models (BERT, IndoBERT)
- [ ] Real-time data streaming
- [ ] Advanced filtering options
- [ ] Export functionality improvements
- [ ] Internationalization (i18n)

### Good First Issues
- [ ] UI/UX improvements
- [ ] Documentation fixes
- [ ] Code refactoring
- [ ] Adding unit tests
- [ ] Bug fixes

---

## 📞 Contact

- **GitHub Issues**: [Report bugs or request features](https://github.com/Fahri-Hilm/Analisis-Sentiment-Data_Mining/issues)
- **Discussions**: [Ask questions or discuss ideas](https://github.com/Fahri-Hilm/Analisis-Sentiment-Data_Mining/discussions)
- **Email**: Contact project maintainer

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing! 🙏**

*Built with ❤️ for Indonesian Football Fans*
