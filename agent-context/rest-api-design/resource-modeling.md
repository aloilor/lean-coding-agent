# Resource Modeling

## Overview

Model the API around domain resources. The URL should describe what the client is working with; the HTTP method should describe the action.

## Resource First

### Problem It Solves

Action URLs make APIs inconsistent and hard to predict.

### How to Apply

Use plural nouns for collections and stable identifiers for individual resources.

```http
GET /users
GET /users/{userId}
POST /orders
GET /orders/{orderId}/items
```

Avoid verbs in URLs when the method already expresses the action.

```http
GET /getUsers
POST /createOrder
POST /users/{userId}/delete
```

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

Keep URLs short, readable, and consistent. Use hierarchy only when there is a strong relationship, such as `/orders/{orderId}/items`.

Avoid nesting deeper than two levels. If nesting keeps growing, a standalone resource is probably missing.

## Payload Shape

Keep request and response fields predictable. Use consistent naming, UTC ISO 8601 timestamps, and client-facing fields instead of database or framework internals.

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
- Are internal IDs, table names, or framework details leaking into the contract?
