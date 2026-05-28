# Querying And Responses

## Pagination

- Do not return large collections in one response by default.
- Support one pagination style consistently per endpoint family.
- Prefer cursor pagination for feeds or high-write datasets.
- Use page-based or limit-offset pagination only when their tradeoffs are acceptable.
- Return pagination metadata that lets clients continue safely.

Examples:

- `GET /events?cursor=evt_200&limit=50`
- `GET /users?page=2&pageSize=25`

## Filtering, Sorting, And Search

- Put filters in the query string with clear parameter names.
- Support sorting with explicit field and direction formats.
- Add search only when it solves a real retrieval need, and document how it behaves.
- Keep naming consistent across endpoints: if one collection uses `limit`, do not switch another to `pageSize` without a reason.

Examples:

- `GET /users?status=active&role=admin`
- `GET /orders?sort=-createdAt`
- `GET /articles?search=rate+limiting`

## Response Efficiency

- Keep responses focused on what clients actually need.
- Support field selection when resources are large and clients routinely need subsets of data.
- Avoid deeply nested structures that mirror internal models instead of client use cases.
- Prefer stable, predictable field names over clever compression.

Example:

- `GET /users/usr_123?fields=id,email,status`

## Content Types

- Use `application/json` as the primary content type for REST APIs.
- Document both `Content-Type` and `Accept` expectations.
- Support alternative representations only when there is a clear consumer need.

Example headers:

```http
Accept: application/json
Content-Type: application/json
```

## CORS

- Configure `Access-Control-Allow-Origin` deliberately instead of defaulting to overly broad access.
- For private APIs, allow only known origins.
- For public APIs, document the chosen CORS policy and allowed methods and headers.

## Practical Checks

- Can clients page through large result sets without duplicates or missing items?
- Are filtering and sorting parameters obvious from their names alone?
- Does each response include enough data to be useful, but not unnecessary payload?
