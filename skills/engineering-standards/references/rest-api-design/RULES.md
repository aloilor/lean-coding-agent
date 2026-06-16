# REST API Design Rules

Load this file only for REST API creation or changes, in addition to the normal engineering baseline.

## Rules

| Rule | Summary | Details |
|------|---------|---------|
| Model Resources First | URLs should describe domain resources; HTTP methods should describe actions. | [resource-modeling.md](./resource-modeling.md) |
| Use Nouns In URLs | Prefer plural resource names and stable identifiers over action endpoints. | [resource-modeling.md](./resource-modeling.md) |
| Keep URLs Short And Consistent | Use hierarchy only for strong ownership relationships and avoid deep nesting. | [resource-modeling.md](./resource-modeling.md) |
| Shape Payloads For Clients | Expose predictable client-facing fields, not database or framework internals. | [resource-modeling.md](./resource-modeling.md) |
| Use HTTP Methods Semantically | Use GET, POST, PUT, PATCH, and DELETE according to their intended behavior. | [http-semantics.md](./http-semantics.md) |
| Use Helpful Status Codes | Return codes that let clients react without special-case guessing. | [http-semantics.md](./http-semantics.md) |
| Design Idempotency Explicitly | Make retries safe where appropriate and use idempotency keys for critical retryable POSTs. | [http-semantics.md](./http-semantics.md) |
| Keep Endpoint Semantics Consistent | Similar endpoints should use similar methods, statuses, and edge-case behavior. | [http-semantics.md](./http-semantics.md) |
| Validate At The Boundary | Validate shape, types, ranges, and business constraints before work begins. | [validation-and-errors.md](./validation-and-errors.md) |
| Return Stable Error Formats | Use a consistent error shape with stable machine-readable codes and trace IDs. | [validation-and-errors.md](./validation-and-errors.md) |
| Hide Internal Failure Details | Do not expose stack traces, SQL errors, vendor internals, or infrastructure details. | [validation-and-errors.md](./validation-and-errors.md) |
| Return Practical Validation Details | Return useful field-level errors instead of forcing fix-one-at-a-time loops. | [validation-and-errors.md](./validation-and-errors.md) |
| Keep Response Shapes Consistent | Field names, enum values, nullability, and success shapes should be predictable. | [validation-and-errors.md](./validation-and-errors.md) |
| Page Large Collections | Do not return unbounded collections by default. | [querying-and-responses.md](./querying-and-responses.md) |
| Use Consistent Query Parameters | Filtering, sorting, and search parameters should have clear stable names. | [querying-and-responses.md](./querying-and-responses.md) |
| Return Efficient Responses | Include useful client data without leaking every internal field. | [querying-and-responses.md](./querying-and-responses.md) |
| Declare Content Types | Use JSON as the default unless there is a strong consumer need otherwise. | [querying-and-responses.md](./querying-and-responses.md) |
| Configure CORS Deliberately | Allow only intended origins, methods, and headers. | [querying-and-responses.md](./querying-and-responses.md) |
| Version Only When Needed | Prefer backward-compatible evolution before introducing a new version. | [versioning-and-security.md](./versioning-and-security.md) |
| Version Public Long-Lived APIs Early | Start with a version when external or long-lived clients need stable contracts. | [versioning-and-security.md](./versioning-and-security.md) |
| Preserve Backward Compatibility | Add fields safely and never change existing meaning without a migration plan. | [versioning-and-security.md](./versioning-and-security.md) |
| Define Auth As Contract | Authentication and authorization are part of API design, not implementation details. | [versioning-and-security.md](./versioning-and-security.md) |
| Authorize Per Sensitive Resource | Validate permissions against the specific resource, not only the endpoint. | [versioning-and-security.md](./versioning-and-security.md) |
| Use Security Basics | Use HTTPS, rate limits, payload limits, safe logging, and enumeration-resistant identifiers where needed. | [versioning-and-security.md](./versioning-and-security.md) |
| Make Security Traceable | Propagate request or correlation IDs and log enough context to investigate safely. | [versioning-and-security.md](./versioning-and-security.md) |
| Document Every Endpoint Contract | Document method, URL, parameters, bodies, statuses, auth, and errors. | [documentation-and-operations.md](./documentation-and-operations.md) |
| Keep Examples Aligned | Request and response examples should stay true to implementation. | [documentation-and-operations.md](./documentation-and-operations.md) |
| Provide Operational Observability | Log method, endpoint, status, latency, request ID, and useful metrics. | [documentation-and-operations.md](./documentation-and-operations.md) |
| Manage Deprecation Deliberately | Announce breaking changes, provide migration guidance, and support overlap when possible. | [documentation-and-operations.md](./documentation-and-operations.md) |
| Test API Contracts | Cover auth failures, validation, conflicts, rate limits, retries, and documented examples. | [documentation-and-operations.md](./documentation-and-operations.md) |
