# Rest API Design

This folder collects reusable guidelines for designing and implementing REST APIs.

Source used for this guidance:

- Postman Blog, [REST API Best Practices: A Developer's Guide to Building Reliable APIs](https://blog.postman.com/rest-api-best-practices/)

## Contents

- [Resource Modeling](./resource-modeling.md): how to model resources, URLs, and relationships.
- [HTTP Semantics](./http-semantics.md): how to use HTTP methods, status codes, and idempotency correctly.
- [Validation And Errors](./validation-and-errors.md): how to handle input validation, errors, and response formats.
- [Querying And Responses](./querying-and-responses.md): how to paginate, filter, search, and keep responses efficient.
- [Versioning And Security](./versioning-and-security.md): how to handle API evolution and baseline security requirements.
- [Documentation And Operations](./documentation-and-operations.md): how to document, observe, and test APIs continuously.

## Core Rules

- Model URLs around resources, not actions.
- Use HTTP semantics consistently and predictably.
- Return structured and stable error responses.
- Support pagination, filtering, sorting, and search on collection endpoints where they matter.
- Introduce versioning only when a breaking change is truly necessary.
- Treat authentication, authorization, and observability as part of the API design.
- Keep examples, documentation, and tests aligned with real API behavior.
