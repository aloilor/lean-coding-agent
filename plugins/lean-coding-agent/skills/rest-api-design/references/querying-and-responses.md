# Querying And Responses

## Overview

Collection endpoints should be predictable, bounded, and efficient. Clients need clear ways to page, filter, sort, search, and request useful response shapes.

## Pagination

Do not return large collections in one response by default.

Use one pagination style consistently per endpoint family. Prefer cursor pagination for feeds or high-write datasets. Use page-based or limit-offset pagination only when their tradeoffs are acceptable.

Examples:

- `GET /events?cursor=evt_200&limit=50`
- `GET /users?page=2&pageSize=25`

## Filtering, Sorting, And Search

Put filters in query parameters with clear names. Support sorting with explicit field and direction formats.

Add search only when it solves a real retrieval need, and document how it behaves.

Examples:

- `GET /users?status=active&role=admin`
- `GET /orders?sort=-createdAt`
- `GET /articles?search=rate+limiting`

## Response Efficiency

Return enough data to be useful, but not every internal field.

Support field selection when resources are large and clients routinely need subsets. Avoid deeply nested structures that mirror internal models instead of client use cases.

Example:

- `GET /users/usr_123?fields=id,email,status`

## Content Types

Use `application/json` as the primary content type for REST APIs. Document both `Content-Type` and `Accept` expectations.

```http
Accept: application/json
Content-Type: application/json
```

Support alternative representations only when there is a clear consumer need.

## CORS

Configure `Access-Control-Allow-Origin` deliberately.

For private APIs, allow only known origins. For public APIs, document the CORS policy, allowed methods, and allowed headers.

## Practical Checks

- Can clients page through large result sets without duplicates or missing items?
- Are filtering and sorting parameters obvious from their names alone?
- Does each response include enough data to be useful without unnecessary payload?
- Is CORS deliberate rather than a broad default?
