# Contributing to Credit Scoring Engine

## Development Setup

```bash
# Clone repository
git clone https://github.com/ananyaapoorva/tvs-credit-engine.git
cd tvs-credit-engine

# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. pytest tests/ -v

# Frontend
cd ../frontend
npm install
npm run dev
```

## Commit Guidelines

Use conventional commits:
- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation changes
- `test:` adding or updating tests
- `refactor:` code refactoring
- `style:` formatting changes
- `ci:` CI/CD changes
- `chore:` build process or tooling changes

## Pull Request Process

1. Create a feature branch from `main`
2. Make changes with tests
3. Ensure all tests pass (`pytest` and `npm run build`)
4. Update documentation if needed
5. Submit PR against `main`
6. Wait for CI/CD checks to pass
7. Merge after review

## Code Style

- **Python:** Follow PEP 8 conventions. All functions must have docstrings.
- **JavaScript:** Use ES6+ syntax. Prefer functional components with hooks.
- **Constants:** Never hardcode magic numbers. Use `app/utils/constants.py` for backend values.

## Testing

- Backend tests: `cd backend && PYTHONPATH=. pytest tests/ -v --cov=app`
- Frontend build: `cd frontend && npm run build`
- All tests must pass before merging.
