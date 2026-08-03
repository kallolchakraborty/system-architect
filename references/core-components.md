# Core Components — Deep Reference

## Database Scaling Patterns

### 1. Master-Slave (Primary-Replica) Replication

```
[Write] -> [Primary DB]
                |-- async replication --> [Replica 1] <-- [Read]
                |-- async replication --> [Replica 2] <-- [Read]
                |-- async replication --> [Replica 3] <-- [Read]
```

**Pros**: Scales read-heavy workloads; replicas double as backups; hot failover.
**Cons**: Replication lag (replicas may serve stale data); if primary fails before replication, data loss; all writes still hit single primary.

**When to use**: Read:write ratio > 3:1; reporting/analytics queries on replicas.

---

### 2. Master-Master Replication

```
[Write] -> [Primary A] <-> [Primary B] <- [Write]
                |                |
           [Replicas]       [Replicas]
```

**Pros**: Both nodes handle writes; active-active failover.
**Cons**: Conflict resolution required on concurrent writes; increased write latency; added complexity.

**Conflict resolution strategies**: Last-write-wins (timestamp), application-level merge, vector clocks.

---

### 3. Federation (Functional Partitioning)

Split database by domain/function rather than by row:

```
[App] -> [Users DB]    (user accounts, auth)
      -> [Orders DB]   (purchase history, carts)
      -> [Products DB] (catalog, inventory)
      -> [Analytics DB](events, metrics)
```

**Pros**: Smaller databases (more cache-friendly); independent scaling per domain; teams own their DB.
**Cons**: Cross-domain joins require application logic; transactions across DBs need 2PC or Saga; schema coordination harder.

---

### 4. Sharding (Horizontal Partitioning)

Distribute rows across multiple database shards by a shard key:

```
shard = hash(user_id) mod num_shards

[Shard 0] -- user_id 0..1M
[Shard 1] -- user_id 1M..2M
[Shard 2] -- user_id 2M..3M
...
```

**Shard key selection** (critical):
- High cardinality (many distinct values)
- Even distribution (no hotspots)
- Aligned with access pattern (queries use shard key in WHERE)
- Avoid shard key that creates celebrities (e.g., user_id of a very popular user)

**Resharding**: Adding shards requires migrating keys. Use consistent hashing to minimize migration.

**Pros**: Eliminates single-node throughput ceiling; independent I/O per shard.
**Cons**: Cross-shard queries require scatter-gather (expensive); transactions across shards need distributed coordination; resharding is operationally complex.

---

### 5. Consistent Hashing

Distribute keys across nodes such that when a node is added or removed, only K/N keys are remapped:

```
Virtual ring (0..2^32):

[Node A: 0-90]  [Node B: 91-180]  [Node C: 181-270]
Key hash -> falls into node's range -> served by that node
```

**Virtual nodes**: Each physical node owns multiple virtual nodes on the ring. Improves load balance when nodes have different capacities or when nodes join/leave.

**Used by**: Amazon DynamoDB, Apache Cassandra, Chord DHT, Memcached clusters.

---

### 6. SQL Tuning Checklist

```sql
-- 1. Use EXPLAIN to see query plan
EXPLAIN SELECT * FROM users WHERE email = 'x@y.com';

-- 2. Index hot filter columns
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_user_id_created ON orders(user_id, created_at);

-- 3. Avoid SELECT * in production
SELECT id, name, email FROM users WHERE id = ?;

-- 4. Use covering indexes for query + sort columns
CREATE INDEX idx_posts_author_ts ON posts(author_id, created_at DESC);

-- 5. Partition large tables
PARTITION BY RANGE (YEAR(created_at)) (
  PARTITION p2022 VALUES LESS THAN (2023),
  PARTITION p2023 VALUES LESS THAN (2024)
);

-- 6. Connection pooling
-- PgBouncer (PostgreSQL), ProxySQL (MySQL)
-- Pool size = (core_count * 2) + effective_spindle_count
```

---

## Consistency Patterns

### Weak Consistency
After a write, reads **may not** see it immediately. Best-effort delivery.
- Used by: VoIP, video chat, real-time multiplayer games, memcached
- Tradeoff: lowest latency, best availability; stale reads acceptable

### Eventual Consistency
After a write, reads **will eventually** see it (typically within milliseconds to seconds). Data replicated asynchronously.
- Used by: DNS, email, Amazon S3, Cassandra, DynamoDB in AP mode
- Tradeoff: high availability; stale reads for a bounded time window

### Read-Your-Writes Consistency
After a write, the same client **always** reads its own writes. Other clients may still see stale data.
- Implementation: route all reads from a client to the same replica; or use session tokens to pin reads
- Used by: user profile updates, post creation (author immediately sees their post)

### Monotonic Read Consistency
After reading a value, subsequent reads return that value or a newer one (never older).
- Implementation: route all reads from a client to the same replica
- Prevents "time travel" anomalies in distributed systems

### Strong Consistency
After a write, all reads **immediately** see it. Data replicated synchronously before write returns.
- Used by: RDBMS with sync replication, Google Spanner (TrueTime), ZooKeeper
- Tradeoff: lowest availability; higher write latency; cannot tolerate partition (CP in CAP)

---

## CRDT (Conflict-free Replicated Data Types)

CRDTs allow concurrent updates to replicated data without coordination, with automatic conflict resolution:

| CRDT Type | Example | Use case |
|---|---|---|
| G-Counter | Increment-only counter | View counts, likes |
| PN-Counter | Inc/Dec counter | Inventory (can go negative) |
| G-Set | Add-only set | User tags, unique visitors |
| OR-Set | Add/remove set | Shopping cart (handles concurrent add/remove) |
| LWW-Register | Last-Write-Wins | User preferences, profile fields |
| MV-Register | Multi-Value Register | Concurrent edits (show conflict to user) |

Used by: Amazon DynamoDB, Riak, Redis CRDT extension (Redis Enterprise).

---

## Distributed Coordination

### ZooKeeper / etcd
Strongly consistent distributed key-value stores used for:
- Leader election (exactly one node is leader at a time)
- Distributed locks (advisory locking)
- Service registry (who is alive and at what address)
- Distributed configuration

**Leader election pattern**:
```
Each node tries to create ephemeral node /election/node_N
Lowest numbered node is leader
If leader dies, ephemeral node deleted, next watches and takes over
```

---

## DNS Deep Dive

**Record types:**
- **A record**: hostname -> IPv4 address
- **AAAA record**: hostname -> IPv6 address
- **CNAME**: hostname -> hostname (alias)
- **MX**: mail exchange server for domain
- **NS**: authoritative name server for domain
- **TXT**: arbitrary text (used for SPF, DKIM, domain verification)
- **SRV**: service location (host + port + priority + weight)

**DNS routing policies (Route 53):**
- **Weighted**: send X% to service A, Y% to service B (A/B testing, canary)
- **Latency-based**: route to region with lowest latency for client
- **Geolocation**: route based on client's geographic location
- **Failover**: health-check-based primary/secondary failover
- **Multivalue**: return multiple IPs (basic load distribution)

**TTL strategy**: Low TTL (30-60s) during migrations; high TTL (86400s=24h) for stable prod (reduces DNS lookup load).

---

## Service Mesh

For microservices at scale, a service mesh provides:
- **mTLS**: mutual TLS for all service-to-service communication
- **Traffic management**: canary deployments, circuit breaking, retries, timeouts
- **Observability**: distributed tracing, metrics, access logs per service pair
- **Service discovery**: sidecar proxies handle routing without app changes

**Tools**: Istio (Envoy sidecar), Linkerd, AWS App Mesh, Consul Connect.

**Sidecar pattern**: Deploy a proxy (Envoy) alongside each service instance. All traffic goes through the sidecar. App code has zero networking logic.

---

## Storage Tier Reference

| Storage Type | Examples | Characteristics | Use when |
|---|---|---|---|
| Block storage | AWS EBS, Google Persistent Disk | Low-latency, raw disk, OS-mountable | Databases, boot volumes |
| File storage | NFS, AWS EFS | Shared filesystem, POSIX | Legacy apps, shared configs |
| Object storage | S3, GCS, Azure Blob | Flat namespace, HTTP API, unlimited scale | Media, backups, data lake |
| In-memory | Redis, Memcached | Microsecond latency, volatile | Cache, session store, pub/sub |
| Data warehouse | Redshift, BigQuery, Snowflake | Columnar, analytical queries | BI, reporting, ML features |
| Time-series DB | InfluxDB, TimescaleDB, Prometheus | Optimized for time-indexed data | Metrics, IoT, monitoring |
| Search engine | Elasticsearch, Solr, OpenSearch | Inverted index, full-text | Search, log analytics |

---

## Observability Stack

### The Three Pillars

**Metrics (quantitative)**:
- Tools: Prometheus (collection) + Grafana (visualization)
- Key metrics: RPS, error rate, p50/p95/p99 latency, saturation (CPU/mem/disk)
- Alerting: PagerDuty, OpsGenie on threshold breaches

**Logs (events)**:
- Tools: ELK stack (Elasticsearch + Logstash + Kibana), Datadog Logs, Loki
- Structure: JSON logs with trace_id, span_id, user_id, request_id
- Retention: hot (7 days), warm (30 days), cold (1 year) tiering

**Traces (distributed request flow)**:
- Tools: Jaeger, Zipkin, AWS X-Ray, Datadog APM
- Every request gets a unique trace_id propagated via HTTP headers (W3C TraceContext)
- Identifies which service/query is the latency bottleneck

### SLO / SLA / SLI

- **SLI** (Service Level Indicator): the measurement (e.g., % requests < 200ms)
- **SLO** (Service Level Objective): the target (e.g., 99.9% of requests < 200ms)
- **SLA** (Service Level Agreement): contractual commitment with penalties
- **Error budget**: 100% - SLO = allowed failure budget. When exhausted, freeze releases.
