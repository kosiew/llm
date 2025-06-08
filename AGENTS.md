# AGENTS.md

This project uses a Python environment for development, testing, and documentation.

## Setting up a development environment

1. Install the project with its test dependencies:
   ```bash
   pip install -e '.[test]'
   ```
2. Run the tests:
   ```bash
   pytest
   ```
3. Lint the codebase:
   ```bash
   ruff check .
   ```
4. Check type hints:
   ```bash
   mypy llm
   ```
5. Ensure formatting:
   ```bash
   black . --check
   ```

## Building the documentation

Run the following commands if you want to build the docs locally:

```bash
cd docs
pip install -r requirements.txt
make html
```
