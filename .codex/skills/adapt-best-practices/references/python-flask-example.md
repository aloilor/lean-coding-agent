# Python Flask Example

Use this file when the target stack is Python plus Flask, or when you need a concrete example of the expected adaptation quality.

## Suggested Output Location

If the repository keeps agent-facing context together, a clean default is:

```text
agent-context/best-practices/python-flask/clean-code/
```

## How Generic Clean-Code Rules Usually Adapt

### Naming And Clarity

- Keep the underlying rule: names should explain intent.
- Adapt the form to Python conventions:
  - functions and variables in `snake_case`
  - classes in `CapWords`
  - module names in short lowercase form
- Use endpoint, blueprint, and helper names that match what the code actually serves.

Example:

```python
from flask import Blueprint

users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.get("/<int:user_id>")
def get_user(user_id: int):
    ...
```

Prefer `get_user` over vague names like `handle_data` or `do_request`.

### Functions And Control Flow

- Keep route functions thin.
- Move business rules into helpers or service functions when the route starts mixing parsing, validation, persistence, and response shaping.
- Use early returns for invalid input so the main path stays easy to scan.

Example:

```python
from flask import Blueprint, jsonify, request

users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.post("/")
def create_user():
    payload = request.get_json(silent=True) or {}
    email = payload.get("email")
    if not email:
        return {"error": "email is required"}, 400

    user = create_user_service(email=email)
    return jsonify({"id": user.id, "email": user.email}), 201
```

```python
def create_user_service(*, email: str) -> User:
    normalized_email = email.strip().lower()
    if not normalized_email:
        raise ValueError("email cannot be blank")

    user = User(email=normalized_email)
    db.session.add(user)
    db.session.commit()
    return user
```

### Comments And Documentation

- Keep the generic rule: comment intent, not obvious code.
- Prefer docstrings for public helpers, extension points, and non-obvious behavior.
- Document request and response constraints when they are part of the public contract.

Example:

```python
def create_user_service(*, email: str) -> User:
    """Create a user with normalized email and persist it in one transaction."""
    ...
```

Avoid comments like `# get email from payload` right above `email = payload.get("email")`.

### Duplication And Refactoring

- Keep the generic rule: refactor repeated logic carefully.
- In Flask, common duplication often shows up in request parsing, error shaping, and repeated route setup.
- Replace copy-pasted route logic with shared helpers, blueprints, or application-factory wiring when repetition is real.

Example:

```python
from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(users_bp)
    app.register_blueprint(admin_bp)
    return app
```

When several modules need the same initialization pattern, the application factory is often a clearer reuse point than hidden global setup.

## Sources To Prefer

- Flask blueprints: <https://flask.palletsprojects.com/en/stable/blueprints/>
- Flask application factories: <https://flask.palletsprojects.com/en/stable/patterns/appfactories/>
- Flask request context: <https://flask.palletsprojects.com/en/stable/reqcontext/>
- PEP 8 naming and style: <https://peps.python.org/pep-0008/>
