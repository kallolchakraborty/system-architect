---
name: system-architect
description: "Use when designing scalable systems, distributed architectures, or complex software solutions. Full industry-grade methodology: requirements -> capacity -> HLD -> component design -> scale."
version: 1.0.0
author: Antigravity (based on donnemartin/system-design-primer)
license: MIT
metadata:
  hermes:
    tags: [system-design, architecture, scalability, distributed-systems, databases, caching, microservices]
    related_skills: [architecture-diagram, spike, plan, requesting-code-review, excalidraw]
---

# System Design — Industry-Grade Methodology

## Overview

This skill encodes the complete system design methodology from the [System Design Primer](https://github.com/donnemartin/system-design-primer) — the definitive open-source reference (250k+ stars). Use it to produce **production-quality architectural blueprints** with explicit trade-off reasoning, capacity math, and component-level detail.

**Core axiom**: *Everything is a trade-off.* Every decision must name what you gain and what you sacrifice.

---

## When to Use

- User asks to "design a system for X" (URL shortener, social feed, search engine, ride-sharing, etc.)
- User needs a scalability review of an existing architecture
- User wants to choose between architectural patterns (microservices vs monolith, SQL vs NoSQL, etc.)
- User is preparing for a system design interview or architectural review board
- User is building a greenfield complex application and needs architectural guidance

**Don't use for:** Pure coding questions, single-function debugging, UI/CSS design, or simple CRUD app scaffolding with no scale requirements.

---

## The 4-Step Design Process

Execute all four steps in sequence. Do NOT skip to component design without completing requirements and capacity first — premature optimization kills clarity.

### Step 1 — Requirements & Scope (MANDATORY)

Ask or state the following before drawing anything:

**Functional requirements** (what the system does):
- Core user actions (read, write, search, stream, notify)
- Data inputs and outputs
- Core features (enumerate them explicitly)
- Out-of-scope items (state what you're NOT building)

**Non-functional requirements** (quality attributes):
- Scale targets: DAU, MAU, RPS (reads + writes separately)
- Latency SLA: p50/p99 targets (e.g., "timeline loads < 200ms p99")
- Availability SLA: 99.9%, 99.99%, 99.999%?
- Consistency model: strong, eventual, or read-your-writes?
- Data volume: storage growth per month/year
- Read/write ratio (e.g., Twitter is ~100:1 read-heavy)
- Geographic distribution: single-region or multi-region?

**Completion criterion**: You can fill in every row of the capacity table below.

---

### Step 2 — Capacity Estimation (Back-of-Envelope)

Run these calculations BEFORE designing. They expose which tier will bottleneck first.

```text
--- Throughput ---
Writes/sec  = (writes/month) / 2.5M
Reads/sec   = (reads/month)  / 2.5M
Peak factor = 2-3x average (traffic spikes)

--- Storage ---
Storage/month = record_size_bytes x writes/month
3-year total  = storage/month x 36

--- Bandwidth ---
Inbound  = write_payload_KB x writes/sec
Outbound = read_payload_KB  x reads/sec

--- Cache memory ---
Cache_RAM = hot_data_fraction x total_dataset_size
            (20% of data serves 80% of traffic -- Pareto)
```

> **Latency & capacity quick reference**: See `references/capacity-cheatsheet.md` for the complete latency numbers table (L1 cache → cross-continent), power-of-two storage reference, and throughput conversion constants.

**Completion criterion**: You have explicit numbers for writes/sec, reads/sec, storage/year, peak RPS, and bandwidth before proceeding.

---

### Step 3 — High-Level Design (HLD)

Produce a component diagram covering these layers in order:

```text
[Client] -> [DNS/CDN] -> [Load Balancer] -> [API Gateway / Web Server]
         -> [Application Services] -> [Cache Layer] -> [Database Layer]
         -> [Object Storage] -> [Message Queue] -> [Async Workers]
         -> [Monitoring / Alerting]
```

For each component, justify its presence. If you include a cache, say WHY (read-heavy, latency SLA). If you exclude a message queue, say WHY (write volume too low).

**HLD checklist:**
- [ ] Entry point: DNS routing strategy (round-robin, geo, latency-based)
- [ ] CDN placement for static assets
- [ ] Load balancer type and algorithm
- [ ] API gateway / reverse proxy (rate limiting, auth, SSL termination)
- [ ] Application tier: monolith vs microservices decision (with rationale)
- [ ] Caching tier: where (client, CDN, app, DB) and what strategy
- [ ] Primary database choice (relational vs NoSQL -- which type)
- [ ] Async processing: message queue if any write fan-out > 10x
- [ ] Storage: object store for media/blobs
- [ ] Observability: metrics, logs, traces

**Completion criterion**: A non-expert could draw this from your description, with every component labeled and every connection explained.

---

### Step 4 — Deep Dive: Core Components

After HLD, dive into the most critical 2-3 components. Use the component reference below.

**Completion criterion**: Deep-dives cover database schemas, API contracts, failover recovery mechanisms, and a complete trade-off matrix contrasting chosen technologies with rejected alternatives.

---

## Component Reference

### Load Balancer

**When to use**: 2+ application servers, need to eliminate SPOF, or need SSL termination.

| Algorithm | Best for |
|---|---|
| Round robin | Stateless, homogeneous servers |
| Weighted round robin | Heterogeneous server capacity |
| Least connections | Long-lived connections (WebSockets) |
| IP hash / sticky sessions | Session-stateful apps (legacy) |
| Layer 4 (transport) | Low overhead, no content inspection |
| Layer 7 (application) | Content-based routing (API vs static) |

**HA setup**: Active-active (both handle traffic) or active-passive (heartbeat failover).
**Disadvantage**: Load balancer itself can become SPOF -> use multiple LBs with DNS failover.

---

### Databases -- Relational (RDBMS)

**Use SQL when**: ACID transactions required, complex joins, well-defined schema, reporting.

**Scaling techniques (apply in order):**
1. **Primary-Replica Replication** -- writes to primary, reads from replicas. Risk: replication lag.
2. **Federation** -- split by domain (users DB, orders DB). Reduces per-DB load; joins require app logic.
3. **Sharding** -- split rows across shards by shard key (user_id mod N). Eliminates single-node bottleneck; adds resharding complexity.
4. **Denormalization** -- duplicate data to avoid expensive JOINs. Trade storage for query speed.
5. **SQL Tuning** -- index hot query columns; EXPLAIN; connection pooling (PgBouncer).

---

### Databases -- NoSQL

| Type | Examples | Use when |
|---|---|---|
| Key-Value | Redis, DynamoDB, Memcached | Session storage, caching, leaderboards, counters |
| Document | MongoDB, CouchDB, Firestore | Semi-structured data, flexible schema, catalogs |
| Wide-Column | Cassandra, HBase, BigTable | Time-series, write-heavy, IoT, event logs |
| Graph | Neo4j, Amazon Neptune | Social graphs, recommendations, fraud detection |

**CAP theorem decision guide:**
- **CP** (Consistency + Partition Tolerance) -> HBase, MongoDB, Redis cluster. Choose for: financial transactions, inventory, atomic reads/writes.
- **AP** (Availability + Partition Tolerance) -> Cassandra, CouchDB, DynamoDB. Choose for: social feeds, metrics, stale reads OK.

**SQL vs NoSQL decision matrix:**

| Factor | Choose SQL | Choose NoSQL |
|---|---|---|
| Data model | Relational, normalized | Flexible, semi-structured |
| Consistency | Strong ACID required | Eventual OK |
| Query patterns | Complex JOINs, aggregations | Key-based lookups |
| Scale | Moderate, vertical first | Massive horizontal scale |
| Schema | Stable | Rapidly evolving |

---

## Component Reference — Caching, Queues & Network

### Caching

**Golden rule**: Cache data that is read frequently and changes infrequently.

**Cache update strategies:**

| Strategy | How it works | Best for | Drawback |
|---|---|---|---|
| Cache-aside (lazy) | App checks cache first; on miss, fetches DB and populates cache | Read-heavy, tolerates stale | Cache miss penalty; thundering herd risk |
| Write-through | Write to cache AND DB synchronously | Strong consistency, low read latency | Write penalty; cache holds rarely-read data |
| Write-behind (write-back) | Write to cache immediately; async flush to DB | Write-heavy, high throughput | Risk of data loss on cache crash |
| Refresh-ahead | Pre-emptively refresh cache before expiry | Predictable access patterns | May cache unnecessary data |

**Eviction policies**: LRU (most common), LFU (frequency-based), FIFO.
**Cache invalidation**: Prefer TTL + event-driven invalidation. State: WHO owns invalidation, WHEN it fires, WHAT the failure mode is.

---

### Asynchronism & Message Queues

**Use a message queue when:**
- Write fan-out > 10x (e.g., post triggers notifications to many followers)
- Operations are too slow for sync request/response (email, video processing)
- Decouple producers from consumers for independent scaling

| System | Model | Best for |
|---|---|---|
| RabbitMQ | Push-based, AMQP | Task queues, RPC, low-latency jobs |
| Apache Kafka | Pull-based, log | Event streaming, audit logs, high-throughput pipelines |
| Amazon SQS | Managed pull | Simple task queues, AWS-native |
| Redis Pub/Sub | Pub/sub, in-memory | Ephemeral real-time fan-out |

**Back pressure**: Bounded queues + circuit breakers. Signal producers to slow down rather than letting queue grow unbounded.

---

### CDN

| Type | How it works | Best for |
|---|---|---|
| Push CDN | You upload content to CDN on change | Small, infrequently updated sites |
| Pull CDN | CDN fetches from origin on first request | High-traffic sites with large asset libraries |

---

## Component Reference — Networking, Availability & Architecture

### Networking & Communication

| Protocol | Properties | Use when |
|---|---|---|
| HTTP/REST | Stateless, text, wide support | Public APIs, CRUD services |
| gRPC / Protobuf | Binary, strongly typed, streaming | Internal microservice-to-microservice |
| GraphQL | Client-driven queries | Complex UI with variable data needs |
| WebSocket | Full-duplex, persistent | Chat, live scores, collaborative editing |
| TCP | Reliable, ordered | Data correctness matters |
| UDP | Unreliable, low-latency | Video streaming, gaming, DNS |

---

### Availability

| SLA | Downtime/year | Downtime/month |
|---|---|---|
| 99% (two 9s) | 3.65 days | 7.2 hours |
| 99.9% (three 9s) | 8.76 hours | 43.8 minutes |
| 99.99% (four 9s) | 52.6 minutes | 4.4 minutes |
| 99.999% (five 9s) | 5.26 minutes | 26.3 seconds |

**Availability in parallel (redundancy):**
```text
Overall = 1 - (1 - A_foo) * (1 - A_bar)
Two 99.9% components in parallel -> 99.9999% combined
```

**Fail-over modes:**
- **Active-passive**: standby takes over on heartbeat failure. Simple; wastes standby capacity.
- **Active-active**: both serve traffic; DNS/LB distributes. No waste; conflict resolution required.

---

### Microservices vs Monolith

**Start monolith, migrate to microservices when:**
- Team > 10 engineers on same codebase
- Independent deployment needed per service domain
- Different scaling requirements per service
- Polyglot persistence needed

**Microservices challenges**: distributed tracing, eventual consistency, network failures, service discovery, complex deployments.

**Service discovery**: Consul, etcd, Eureka, AWS Service Discovery, Kubernetes DNS.

---

### Security Principles

- Least privilege: every service/user gets only permissions it needs
- Encrypt in transit: TLS everywhere (mutual TLS for internal services)
- Encrypt at rest: AES-256 for sensitive fields; KMS for key management
- Input validation: sanitize at every boundary; parameterized queries
- Rate limiting: per-user, per-IP, per-API-key at gateway
- Auth: JWT or OAuth2 for stateless auth; RBAC for access control
- DDoS: CDN edge filtering, rate limiting, anycast routing
- Secrets management: Vault, AWS Secrets Manager, never hardcode

---

## Proven System Design Patterns

### Fan-out on Write (Precomputed timelines)
Twitter home timelines. On post, write to every follower's timeline cache. Fast reads (O(1)); expensive writes for celebrities -> hybrid push-pull.

### CQRS (Command Query Responsibility Segregation)
Separate write model (commands -> event store) from read model (queries -> read replica). Independent scaling of reads vs writes. Adds eventual consistency.

### Event Sourcing
Store state as immutable log of events. Current state = replay of all events. Enables audit log, time travel. Drawback: query complexity, snapshot management.

### Saga Pattern (Distributed Transactions)
Coordinate multi-service transactions via local transactions + compensating actions on failure. Avoids 2PC locks. Flavors: choreography (event-driven) and orchestration (central coordinator).

### Circuit Breaker
Wrap downstream calls; after N consecutive failures, open the circuit (fail fast). After timeout, half-open: allow one probe. Prevents cascading failures. Tools: Hystrix, Resilience4j.

### Consistent Hashing
Distribute data across nodes. When a node joins or leaves, only K/N keys are remapped (K=keys, N=nodes). Essential for distributed caches and database sharding.

### Strangler Fig
Incrementally migrate monolith to microservices: route new traffic to new services at reverse proxy; legacy handles the rest. Eliminates big-bang rewrite risk.

---

## Canonical System Design Examples

### URL Shortener (Pastebin / Bit.ly)
- Core challenge: unique short codes, efficient redirect
- Key decisions: Base62 encoding; separate read service (100:1 read-heavy); Redis cache hot URLs; SQL for metadata
- Scale: 100M URLs = ~10 GB; 10K reads/sec -> Redis with LRU

### Social Feed / Timeline (Twitter / Instagram)
- Core challenge: fan-out delivery at scale
- Key decisions: Cassandra for tweet storage; Redis timeline cache; Kafka for async fan-out workers; hybrid push-pull for celebrities (>1M followers)
- Scale: 500M tweets/day; 6K writes/sec; 100K reads/sec

### Web Crawler
- Core challenge: politeness, deduplication, crawl prioritization
- Key decisions: URL frontier as priority queue (Redis); DNS cache; consistent hashing for distributed crawlers; Bloom filter for deduplication

### Ride-Sharing (Uber/Lyft)
- Core challenge: real-time geo-matching, location tracking
- Key decisions: geospatial index (S2 cells / geohash); WebSockets for driver location; Kafka for trip events; separate matching service

### Video Streaming (YouTube/Netflix)
- Core challenge: encoding pipeline, adaptive bitrate, global delivery
- Key decisions: S3 for raw/transcoded video; FFmpeg workers via job queue; CDN for edge delivery; HLS/DASH adaptive bitrate; ML service for recommendations

### Rate Limiter
- Algorithms: Token bucket (burst-friendly), leaky bucket (smooth), fixed window counter, sliding window
- Distributed: Redis atomic INCR + EXPIRE with Lua scripts

### Distributed Cache
- Consistent hashing for shard-to-node mapping
- Redis Sentinel for HA; Redis Cluster for horizontal sharding + HA

### Search Engine / Query Cache
- Inverted index in Elasticsearch; write-through cache for hot queries; async index refresh

---

## Output Format

Structure every system design response as:

```text
## System: [Name]

### 1. Requirements
  - Functional: [list]
  - Non-functional: [list with numbers]

### 2. Capacity Estimation
  - Writes: X/sec (Y/month)
  - Reads: X/sec (Y/month)
  - Storage: X GB/month -> Y TB in 3 years
  - Peak RPS: Z (3x average)
  - Bandwidth: A MB/s in, B MB/s out

### 3. High-Level Design
  [Component diagram description; justify each component]

### 4. Core Component Deep Dives
  [2-3 most critical components, with schema / API / algorithm detail]

### 5. Bottleneck Analysis & Scale Plan
  [Top 3 bottlenecks: current state -> mitigation -> trade-off]

### 6. Trade-off Summary
  | Decision | Chosen | Alternative | Why chosen |
```

---

## Common Pitfalls

1. **Never jump to components before requirements.** Without explicit scale numbers, every technology choice is a guess. Do NOT draw architecture until capacity math is complete.
2. **Do not over-engineer for day-1 scale.** Start with the simplest architecture that meets the SLA; identify bottlenecks; evolve iteratively. Avoid distributed systems complexity until proven necessary.
3. **Never skip the SPOF audit.** Walk every component: what happens when it fails? Do NOT ship a design where a single component failure violates the availability SLA without a documented failover plan.
4. **Never pick a database for brand-name reasons.** Access pattern + consistency requirement + scale target → then pick technology. Do not reverse this order.
5. **Never hand-wave the consistency model.** State explicitly which operations are eventually consistent and which must be strongly consistent. Do NOT leave consistency unspecified.
6. **Do not hand-wave cache invalidation.** State precisely: when does a cache entry get invalidated? Who owns the invalidation? What is the failure mode on cache miss thundering herd?
7. **Never omit back-pressure in async pipelines.** Define queue depth limits and producer throttling behaviour. An unbounded queue is a ticking time bomb under load.
8. **Avoid microservices as default.** A modular monolith is often the correct choice until you have proven scale and team-size justification. Do NOT adopt microservices for social proof.
9. **Never ship a design without an observability plan.** Every production system needs metrics (Prometheus/Grafana), structured logs (ELK), and distributed traces (Jaeger). Name them explicitly.
10. **Never underestimate data gravity.** Data is hard to move once written at scale. State the data model and access patterns before committing to a data store; do NOT change storage engines post-production lightly.

---

## Verification Checklist

- [ ] Requirements stated with explicit scale numbers (RPS, storage, latency SLA)
- [ ] Capacity calculations completed before any component is selected
- [ ] Every component has a stated technical justification (not just listed)
- [ ] Every component failure mode addressed (SPOF eliminated or tolerated with rationale)
- [ ] Database choice matches consistency requirement, access pattern, and scale target
- [ ] Cache strategy named (cache-aside / write-through / write-behind) with explicit invalidation plan
- [ ] Async queues have back-pressure mechanism and bounded depth defined
- [ ] Security layers named at each boundary (auth, TLS, encryption at rest, rate limiting)
- [ ] CAP theorem position stated explicitly for each data store
- [ ] Trade-off table produced for each major design decision
- [ ] Bottleneck analysis covers at least 3 future scaling issues with mitigation plans
- [ ] Observability plan named explicitly (metrics tool, logging tool, tracing tool)

---

## References

- `references/core-components.md` -- Deep-dive component reference: replication, sharding, federation, consistency, CRDT patterns
- `references/capacity-cheatsheet.md` -- Capacity estimation formulas, latency numbers, and storage conversions
- `references/worked-examples.md` -- Step-by-step worked examples for 8 canonical system design problems
- `references/object-oriented-design.md` -- Low-level object-oriented design patterns & code examples (LRU Cache, Parking Lot, Hash Map)
- `references/api-design-and-protocols.md` -- API design best practices, pagination, idempotency, REST/GraphQL/gRPC
- `references/data-engineering-and-modern-arch.md` -- Stream vs Batch, Data Lakes, CDC (Debezium), Serverless vs Containers
- Source: https://github.com/donnemartin/system-design-primer (donnemartin, MIT License)
