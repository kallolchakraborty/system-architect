window.SITE_CONTENT = [
  {
    "id": "system-design-methodology",
    "title": "System Design — Industry-Grade 4-Step Methodology",
    "category": "Core Framework",
    "description": "Enterprise-grade distributed systems design methodology with 4 explicit stages.",
    "content": "# System Design — Industry-Grade Methodology\n\n## Overview\nThis portal encodes an enterprise-grade distributed systems design methodology. Use it to produce **production-quality architectural blueprints** with explicit trade-off reasoning, capacity math, and component-level detail.\n\n**Core axiom**: *Everything is a trade-off.* Every decision must name what you gain and what you sacrifice.\n\n---\n\n## The 4-Step Design Process\n\n### Step 1 — Requirements & Scope (MANDATORY)\n- **Functional Requirements**: Core user actions, data inputs/outputs, explicit out-of-scope boundaries.\n- **Non-Functional Requirements**: Scale targets (DAU/RPS), Latency SLAs (p50/p99), Availability (99.99%), Consistency model (Strong vs Eventual).\n\n### Step 2 — Capacity Estimation (Back-of-Envelope)\n- **Throughput**: `Writes/sec = (writes/month) / 2.5M`\n- **Storage**: `Storage/month = record_size_bytes x writes/month`\n- **Bandwidth**: `Inbound = write_payload_KB x writes/sec`\n- **Cache RAM**: `Cache_RAM = 0.20 x total_dataset_size` (80/20 Pareto rule)\n\n### Step 3 — High-Level Design (HLD)\n```text\n[Client] -> [DNS/CDN] -> [Load Balancer] -> [API Gateway / Web Server]\n         -> [Application Services] -> [Cache Layer] -> [Database Layer]\n         -> [Object Storage] -> [Message Queue] -> [Async Workers]\n```\n\n### Step 4 — Deep Dive & Trade-offs\nDive into core bottlenecks, schema design, failover strategies, and explicit technology comparison matrices."
  },
  {
    "id": "capacity-cheatsheet",
    "title": "Capacity Estimation & Latency Cheatsheet",
    "category": "Capacity & Metrics",
    "description": "Latency numbers every programmer should know, storage conversion factors, and throughput calculation reference.",
    "content": "# Latency & Capacity Quick Reference\n\n## Latency Numbers Every Programmer Should Know\n\n| Operation | Time |\n|---|---|\n| L1 cache reference | 0.5 ns |\n| Branch mispredict | 5 ns |\n| L2 cache reference | 7 ns |\n| Mutex lock/unlock | 25 ns |\n| Main memory reference | 100 ns |\n| Compress 1KB with Zstandard | 3,000 ns (3 µs) |\n| Send 2KB over 1Gbps network | 20,000 ns (20 µs) |\n| SSD random read | 150,000 ns (150 µs) |\n| Read 1MB sequentially from memory | 250,000 ns (250 µs) |\n| Round trip within same datacenter | 500,000 ns (0.5 ms) |\n| Read 1MB sequentially from SSD | 1,000,000 ns (1 ms) |\n| HDD seek | 10,000,000 ns (10 ms) |\n| Read 1MB sequentially from HDD | 20,000,000 ns (20 ms) |\n| Send packet CA -> Europe -> CA | 150,000,000 ns (150 ms) |\n\n## Storage Powers of Two\n\n- **1 KB** = 10^3 bytes (2^10 = 1,024)\n- **1 MB** = 10^6 bytes (2^20 = 1,048,576)\n- **1 GB** = 10^9 bytes (2^30 = 1,073,741,824)\n- **1 TB** = 10^12 bytes (2^40 = 1,099,511,627,776)\n- **1 PB** = 10^15 bytes (2^50 = 1,125,899,906,842,624)\n\n## Time & Throughput Constants\n\n- **1 day** = 86,400 seconds ≈ **100,000 seconds** (useful for quick estimation)\n- **1 month** = 2,592,000 seconds ≈ **2.5 Million seconds**\n- **1 million requests/day** = **12 requests/second**\n- **100 million requests/day** = **1,160 requests/second**"
  },
  {
    "id": "distributed-systems-and-db",
    "title": "Distributed Systems & Database Architecture",
    "category": "Architecture Modules",
    "description": "Deep dive into SQL vs NoSQL, CAP theorem, replication topologies, sharding strategies, and transactions.",
    "content": "# Distributed Systems & Database Architecture\n\n## 1. Relational vs. NoSQL Paradigm Matrix\n\n| Attribute | Relational (RDBMS) | NoSQL (Key-Value, Document, Wide-Column, Graph) |\n|---|---|---|\n| Data Structure | Normalized tables with defined schemas | Unstructured/semi-structured, key-value, BSON, graph nodes |\n| Transactions | Full ACID guarantees | Eventual consistency, BASE (Basically Available, Soft-state, Eventual consistency) |\n| Scaling | Vertical (scale-up); Read replicas, Sharding for horizontal | Built-in horizontal partitioning (sharding) |\n\n## 2. Partitioning & Sharding Strategies\n- **Range-Based Partitioning**: Maps continuous key ranges to nodes. Vulnerable to hot spots.\n- **Hash-Based Partitioning**: Hashes partition key modulo N. Requires full resharding on node addition.\n- **Consistent Hashing**: Hashes keys & nodes onto a 2^32 ring. Virtual nodes ensure uniform key distribution with minimal key movement on cluster topology changes."
  },
  {
    "id": "scalability-patterns",
    "title": "Scalability Patterns & Caching Strategies",
    "category": "Architecture Modules",
    "description": "Caching topologies, invalidate patterns, load balancing algorithms, rate limiting, and asynchronous processing.",
    "content": "# Scalability Patterns & Caching Strategies\n\n## 1. Caching Topologies & Invalidation\n- **Cache-Aside (Lazy Loading)**: Application reads cache; on miss, loads from DB and updates cache.\n- **Write-Through**: Application writes to cache; cache synchronously writes to DB.\n- **Write-Behind (Write-Back)**: Application writes to cache; cache asynchronously flushes to DB in batches.\n- **Refresh-Ahead**: Cache pre-emptively refreshes keys before TTL expiration based on access patterns.\n\n## 2. Load Balancing & Reverse Proxy\n- **Layer 4 (L4) Load Balancing**: Operates at TCP/UDP level. Fast, low overhead.\n- **Layer 7 (L7) Load Balancing**: Operates at HTTP/HTTPS level. Enables URL routing, SSL termination, rate-limiting."
  },
  {
    "id": "resilience-security-operability",
    "title": "Resilience, Security & Operability",
    "category": "Architecture Modules",
    "description": "Circuit breakers, rate limiting, token buckets, TLS termination, zero-trust security, and observability stacks.",
    "content": "# Resilience, Security & Operability\n\n## 1. Resilience & Fault Tolerance\n- **Circuit Breaker Pattern**: Monitors error rates to prevent cascading failure (Closed -> Open -> Half-Open).\n- **Bulkheading**: Isolates resources (thread pools, connection pools) so failures in one service do not drain capacity.\n- **Graceful Degradation**: Fallback to cached or read-only data when upstream services fail.\n\n## 2. Security Fundamentals\n- **Rate Limiting**: Token Bucket, Leaky Bucket, Sliding Window Counter.\n- **Identity & Auth**: OAuth 2.0 / OIDC, JWTs, Mutual TLS (mTLS) for microservices inter-service auth.\n- **Zero-Trust Network Architecture**: Never trust, always verify every request regardless of location."
  }
];
