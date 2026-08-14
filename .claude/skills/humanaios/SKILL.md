```markdown
# humanaios Development Patterns

> Auto-generated skill from repository analysis

## Overview
This skill teaches the core development patterns and conventions used in the `humanaios` Python codebase. You'll learn how to structure files, write imports and exports, and follow the repository's conventions for naming, testing, and commit messages. This guide also provides suggested commands for common workflows to ensure consistency and efficiency.

## Coding Conventions

### File Naming
- **Style:** snake_case
- **Example:**  
  ```python
  # Good
  user_profile.py

  # Bad
  UserProfile.py
  userProfile.py
  ```

### Import Style
- **Style:** Relative imports are preferred.
- **Example:**  
  ```python
  # Good
  from .utils import parse_data

  # Bad
  import utils
  from utils import parse_data
  ```

### Export Style
- **Style:** Named exports (explicitly define what is exported).
- **Example:**  
  ```python
  # In module.py
  def foo(): ...
  def bar(): ...

  __all__ = ['foo', 'bar']
  ```

### Commit Messages
- **Type:** Freeform, no strict prefixes.
- **Average Length:** ~56 characters.
- **Example:**  
  ```
  Fix bug in data parsing for edge cases
  Add support for new user roles
  ```

## Workflows

### Adding a New Module
**Trigger:** When implementing new functionality.
**Command:** `/add-module`

1. Create a new Python file using snake_case naming.
2. Implement the functionality.
3. Use relative imports for any internal dependencies.
4. Define `__all__` to specify exports.
5. Write corresponding tests in a `*.test.*` file.

### Writing Tests
**Trigger:** When adding or updating features.
**Command:** `/write-test`

1. Create a test file matching the pattern `*.test.*` (e.g., `user_profile.test.py`).
2. Write test cases for all public functions.
3. Use the project's preferred (currently unknown) test framework.
4. Run tests to ensure correctness.

### Making Commits
**Trigger:** When saving progress or completing a feature/fix.
**Command:** `/commit`

1. Write a clear, concise commit message (~56 characters).
2. No strict prefix required.
3. Commit related changes together.

## Testing Patterns

- **File Pattern:** Test files are named with the pattern `*.test.*` (e.g., `module.test.py`).
- **Framework:** Not explicitly specified; use standard Python testing frameworks (e.g., `unittest`, `pytest`) unless otherwise indicated.
- **Test Coverage:** Ensure all exported functions/classes are tested.

**Example:**
```python
# user_profile.test.py

from .user_profile import get_user_info

def test_get_user_info():
    assert get_user_info(1) == {'name': 'Alice'}
```

## Commands
| Command        | Purpose                                      |
|----------------|----------------------------------------------|
| /add-module    | Scaffold and implement a new module          |
| /write-test    | Add or update tests for a module             |
| /commit        | Make a commit following repository patterns   |
```
