# API Design & Communication Protocols Reference

System design requires defining the boundaries between components. This reference covers industry best practices for API design, data contracts, and communication protocols.

---

## 1. REST API Best Practices

- **Resource-Oriented URLs**: Nouns, not verbs. Use hierarchical paths.
  - Good: `GET /users/123/orders`
  - Bad: `GET /getOrdersForUser?id=123`
- **HTTP Methods**:
  - `GET`: Read (idempotent, safe)
  - `POST`: Create (not idempotent)
  - `PUT`: Replace/Update whole resource (idempotent)
  - `PATCH`: Partial update (not strictly idempotent, but often implemented as such)
  - `DELETE`: Delete (idempotent)
- **Status Codes**:
  - `200 OK`, `201 Created`, `202 Accepted` (async processing)
  - `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`, `429 Too Many Requests`
  - `500 Internal Server Error`, `503 Service Unavailable`
- **Versioning**:
  - URI versioning (most common): `/api/v1/users`
  - Header versioning: `Accept: application/vnd.company.v1+json`

---

## 2. API Pagination

When returning lists of data, pagination is required to prevent large payloads and DB performance issues.

### Offset Pagination
- **Format**: `?offset=100&limit=20`
- **SQL**: `LIMIT 20 OFFSET 100`
- **Pros**: Easy to implement, allows jumping to a specific page.
- **Cons**: Poor performance on large offsets (DB must scan and skip rows); inconsistent results if items are added/deleted during pagination.

### Cursor Pagination (Recommended for Scale)
- **Format**: `?cursor=eyJpZCI6MTIzdQ==&limit=20` (cursor is an opaque encoded string of the last item's sort column + ID).
- **SQL**: `WHERE id > 123 LIMIT 20` (assuming sorting by ID).
- **Pros**: O(1) performance regardless of depth (uses index); consistent results even with concurrent writes.
- **Cons**: Cannot jump to a specific page number; harder to implement.

---

## 3. Idempotency

**Problem**: Network failures can cause clients to retry a request that actually succeeded on the server, leading to duplicate actions (e.g., double charging a credit card).

**Solution: Idempotency Keys**
1. Client generates a unique ID (UUID) for the operation: `Idempotency-Key: <uuid>`.
2. Server checks if this key exists in an idempotency store (e.g., Redis or a dedicated DB table).
3. If it exists, server returns the saved response of the previous successful execution.
4. If it doesn't exist, server processes the request, saves the response against the key, and returns it.

- *Crucial for POST requests in payment systems or critical state changes.*

---

## 4. Communication Protocols Comparison

| Protocol / Style | Format | Transport | Best For | Pros | Cons |
|---|---|---|---|---|---|
| **REST** | JSON/XML | HTTP/1.1 or 2 | Public APIs, Web clients | Universal support, cacheable, easy to debug | Over-fetching/under-fetching, lacks strict typing |
| **GraphQL** | JSON | HTTP/1.1 or 2 | Complex web/mobile UIs | Client fetches exactly what it needs in one request | Hard to cache at network level, N+1 query problems |
| **gRPC** | Protobuf (binary) | HTTP/2 | Internal microservices | Extremely fast, strongly typed, bidirectional streaming | Not natively supported in browsers (requires grpc-web) |
| **WebSockets**| Binary/Text | TCP | Real-time apps (chat, gaming) | Full-duplex, persistent connection, low latency | Stateful, harder to load balance and scale |
| **Webhooks** | JSON | HTTP | Server-to-server events | Push model (better than polling) | Requires receiver to have public endpoint |

---

## 5. API Gateway Patterns

An API Gateway sits between clients and backend microservices.

**Responsibilities:**
1. **Routing**: Map `/api/users` -> `UserService`, `/api/orders` -> `OrderService`.
2. **Authentication/Authorization**: Validate JWTs, check scopes before hitting internal services.
3. **Rate Limiting**: Throttling requests to prevent abuse.
4. **Load Balancing**: Distribute traffic among internal service instances.
5. **SSL Termination**: Decrypt HTTPS traffic at the edge.
6. **Protocol Translation**: Convert REST from client into gRPC for internal services.

**BFF (Backend for Frontend) Pattern**:
Instead of one massive API Gateway, create specific gateways for different clients (e.g., Mobile BFF, Web BFF). This allows tailoring the API responses to the specific needs of each client type without bloating a single gateway.
