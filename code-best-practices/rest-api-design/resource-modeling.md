# Resource Modeling

## Resource First

- Design endpoints around clear domain nouns: `/users`, `/orders`, `/invoices`.
- Use plural names for collections and stable identifiers for single resources: `/users/{userId}`.
- Avoid verbs in URLs when the HTTP method already expresses the action.

## Examples

Good:

- `GET /users`
- `GET /users/{userId}`
- `POST /orders`
- `GET /orders/{orderId}/items`

Avoid:

- `GET /getUsers`
- `POST /createOrder`
- `POST /users/{userId}/delete`

## URL Design

- Keep URLs short, readable, and consistent across services.
- Use hierarchy only when there is a strong relationship: `/orders/{orderId}/items`.
- Avoid nesting deeper than 2 levels; if it grows further, a standalone resource is probably missing.

## Payload Shape

- Keep fields predictable and naming consistent across requests and responses.
- Prefer ISO 8601 timestamps in UTC.
- Do not expose internal database or framework details.
- Avoid deep response nesting when flatter structures are easier for clients to consume.

Example response:

```json
{
  "id": "usr_123",
  "email": "alex@example.com",
  "status": "active",
  "createdAt": "2026-05-28T18:30:00Z"
}
```

## Practical Checks

- Can a consumer understand the domain by looking at the endpoints?
- Is the same naming rule applied everywhere?
- Could a new resource follow the same pattern without exceptions?
