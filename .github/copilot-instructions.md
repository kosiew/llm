# GitHub Copilot Instructions for LLM

This document provides instructions for GitHub Copilot to help with development in the LLM (Large Language Model) CLI tool project.

## Project Overview

LLM is a command-line tool for accessing large language models from OpenAI, Anthropic, and other providers. The project is written in Python and uses Click for the CLI interface, SQLite for logging, and a plugin system for extensibility.

## Code Style Guidelines

### Python Style

Follow these guidelines when generating Python code:

1. **PEP 8 Compliance**: Follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
2. **Ruff Compatibility**: Code must pass Ruff linting with the project's configuration
3. **String Literals**: Use double quotes for string literals
4. **Imports**: Use explicit relative imports (e.g., `from .module import Class`)
5. **Line Length**: Limit lines to 88 characters (Black formatter standard)
6. **Type Hints**: Include type hints for function parameters and return values
7. **String Formatting**: Use f-strings instead of `.format()` or `%` formatting
8. **Exception Handling**: Assign exception messages to variables before raising:

   ```python
   # Correct:
   msg = "Invalid input value"
   raise ValueError(msg)

   # Incorrect:
   raise ValueError("Invalid input value")
   ```

### Documentation

1. **Docstrings**: Use Google-style docstrings for all modules, classes, and functions
2. **Type Information**: Include Args, Returns, and Raises sections where applicable
3. **Meaningful Comments**: Add comments for complex logic, avoiding obvious statements
4. **Comment Style**: Start inline comments with a capital letter

### Code Organization

1. **Function Size**: Keep functions under 40-50 lines when possible
2. **Single Responsibility**: Functions should focus on a single task
3. **Reuse**: Check for existing utility functions before creating new ones
4. **Consistency**: Follow established patterns in the codebase
5. **Avoid Over-engineering**: Don't create unnecessary abstractions

## Project Structure

### Key Modules

- `llm/cli.py`: Main CLI interface using Click
- `llm/models.py`: Model abstractions and conversation handling
- `llm/__init__.py`: Public API exports
- `llm/plugins.py`: Plugin system implementation
- `llm/utils.py`: Utility functions
- `llm/tools.py`: Tool system for function calling
- `llm/templates.py`: Template system for prompts
- `llm/embeddings.py`: Text embedding functionality

### Key Concepts

1. **Models**: Abstraction for different LLM providers (OpenAI, Anthropic, etc.)
2. **Conversations**: Stateful chat sessions with models
3. **Fragments**: Reusable text snippets that can be referenced in prompts
4. **Attachments**: Files, URLs, or other media attached to prompts
5. **Tools**: Functions that models can call during conversations
6. **Templates**: Reusable prompt templates with parameters
7. **Plugins**: Extension system for adding new models and functionality

### CLI Command Structure

- `llm prompt`: Execute a single prompt
- `llm chat`: Start an interactive chat session
- `llm models`: Manage and list available models
- `llm keys`: Manage API keys
- `llm logs`: View conversation logs
- `llm embed`: Generate text embeddings
- `llm install`: Install plugins

## Common Patterns

### Error Handling

Use Click exceptions for CLI errors:

```python
try:
    result = some_operation()
except SomeError as ex:
    raise click.ClickException(str(ex))
```

### Database Operations

Use sqlite-utils for database operations:

```python
import sqlite_utils

db = sqlite_utils.Database(path)
db.executescript(sql)
```

### Plugin System

When working with plugins, use the hookspec pattern:

```python
from llm.plugins import pm

@pm.hook
def register_models(register):
    register("model-name", ModelClass)
```

### Model Implementation

Models should inherit from appropriate base classes:

```python
from llm.models import Model, Chat

class MyModel(Model):
    model_id = "my-model"

    def prompt(self, prompt, **options):
        # Implementation
        pass
```

### Testing

1. Use pytest for all tests
2. Use meaningful test function names that describe what's being tested
3. Group related tests in classes
4. Use pytest-style assertions
5. Mock external API calls using cassettes or fixtures

## Dependencies

Key dependencies to be aware of:

- `click`: CLI framework
- `sqlite-utils`: Database operations
- `httpx`: HTTP client
- `pydantic`: Data validation
- `yaml`: Configuration parsing
- `pytest`: Testing framework
- `ruff`: Linting
- `black`: Code formatting
- `mypy`: Type checking

## Development Workflow

1. Install development dependencies: `pip install -e '.[test]'`
2. Run tests: `pytest`
3. Lint code: `ruff check .`
4. Check types: `mypy llm`
5. Format code: `black . --check`

## When Contributing

1. **Backward Compatibility**: Maintain backward compatibility in public APIs
2. **Documentation**: Update relevant documentation for new features
3. **Tests**: Add tests for new functionality
4. **Plugin Compatibility**: Consider impact on existing plugins
5. **Performance**: Be mindful of startup time and memory usage

## Security Considerations

1. **API Keys**: Never log or expose API keys
2. **File Access**: Validate file paths and permissions
3. **URL Handling**: Sanitize and validate URLs
4. **SQL Injection**: Use parameterized queries
5. **Plugin Security**: Be cautious with plugin execution

## Common Gotchas

1. **Model Loading**: Models are loaded lazily; check for availability before use
2. **Async Support**: Some models support async operations; handle both sync and async
3. **Unicode Handling**: Properly handle Unicode in prompts and responses
4. **Error Messages**: Provide helpful error messages with context
5. **Configuration**: Check for environment variables and config files
