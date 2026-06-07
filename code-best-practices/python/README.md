# Python

This folder collects reusable Python best practices for readable style, maintainable module design, clear typing, and safe everyday coding habits.

## Sources

- Python, [PEP 8 - Style Guide for Python Code](https://peps.python.org/pep-0008/)
- Python, [PEP 257 - Docstring Conventions](https://peps.python.org/pep-0257/)
- Python, [typing - Support for type hints](https://docs.python.org/3/library/typing.html)

## Contents

- [Style And Maintainability](./style-and-maintainability.md): how to keep Python code readable, typed where it matters, and easy to change without unnecessary abstraction.

## Core Rules

- Follow the project formatter and import style instead of hand-tuning layout.
- Keep functions small, side effects explicit, and modules focused on one area of behavior.
- Add type hints where they clarify public contracts or complex data flow.
- Raise precise exceptions and avoid hiding failures behind broad `except` blocks.
- Document public APIs and behavior constraints, not obvious line-by-line mechanics.
