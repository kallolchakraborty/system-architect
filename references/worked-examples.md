# Worked System Design Examples

Full step-by-step solutions following the 4-step methodology from SKILL.md.

---

## Example 1: Design a URL Shortener (Bit.ly / Pastebin)

### Step 1 — Requirements

**Functional:**
- User submits a long URL, receives a short URL (e.g., bit.ly/xK4mPq)
- Short URL redirects to original URL
- Optional: custom aliases, URL expiration, analytics (click counts)
- Out of scope: user accounts, paid tiers, spam detection

**Non-functional:**
- 100M URLs created/month
- 10B redirects/month (100:1 read:write)
- Redirect latency: < 10ms p99
- Availability: 99.99%
- URL data retention: 5 years

### Step 2 — Capacity

```
Writes: 100M / 2.5M = 40 writes/sec (peak: ~120 writes/sec)
Reads:  10B  / 2.5M = 4,000 reads/sec (peak: ~12,000 reads/sec)

Storage per URL record:
  short_code: 7 bytes
  long_url:   ~200 bytes (average)
  user_id:    8 bytes
  created_at: 8 bytes
  expires_at: 8 bytes
  click_count: 8 bytes
  Total: ~500 bytes

Storage: 500 bytes x 100M URLs/month x 60 months = 3 TB over 5 years

Cache (20% hot data): 100M URLs x 500 bytes x 0.20 = 10 GB Redis RAM
```

### Step 3 — High-Level Design

```
[User] -> [DNS (Route 53)] -> [Load Balancer (L7, Nginx/ALB)]
       -> [URL Service API] -> [Cache (Redis)] -> [URL DB (MySQL primary)]
                           -> [Analytics Service] -> [Analytics DB (Cassandra)]
                           <- [Object Store for optional file pastes (S3)]
```

**Component justifications:**
- **Redis cache**: 4K reads/sec with < 10ms SLA; cache hot URLs by short_code; LRU eviction; single node (10 GB) is sufficient
- **MySQL**: ACID for URL creation; master-replica for read scale; single primary for writes (40/sec easily within MySQL single-node limits)
- **Analytics Service**: decoupled from read path; Kafka for click events; Cassandra for time-series click counts
- **Load Balancer**: eliminates SPOF on API tier; active-active pair

### Step 4 — Core Component Deep Dives

**Short code generation:**
```
Option A: MD5(long_url) -> take first 7 chars (Base62)
  Problem: collisions likely at 100M URLs (birthday paradox)
  Collision handling: append counter suffix and rehash

Option B: Globally unique ID (snowflake) -> encode as Base62
  Snowflake ID: [41-bit timestamp | 10-bit machine_id | 12-bit sequence]
  Base62 encode 64-bit int -> 7 char string (62^7 = 3.5 trillion combinations)
  No collisions; monotonically increasing; sortable

CHOSEN: Option B (Snowflake + Base62)
  Reason: no collision detection round-trips; predictable; URL-safe
```

**Redirect flow:**
```
1. Client GET /xK4mPq
2. API server: check Redis cache by key 'xK4mPq'
3. Cache HIT (90%+): return HTTP 301 (permanent) or 302 (track analytics) redirect
4. Cache MISS: query MySQL WHERE short_code = 'xK4mPq'
5. Populate Redis cache with TTL = 24h
6. Return redirect; fire async click event to Kafka -> Analytics Service
```

**DB Schema:**
```sql
CREATE TABLE urls (
  id         BIGINT PRIMARY KEY,      -- Snowflake ID
  short_code VARCHAR(10) NOT NULL,
  long_url   TEXT NOT NULL,
  user_id    BIGINT,
  created_at TIMESTAMP DEFAULT NOW(),
  expires_at TIMESTAMP,
  INDEX idx_short_code (short_code)   -- critical: all reads use this
);
```

### Step 5 — Bottleneck Analysis

| Bottleneck | Trigger | Mitigation | Trade-off |
|---|---|---|---|
| Cache becomes hot (too much RAM) | >100M active URLs | Scale Redis with consistent hashing | Resharding complexity |
| MySQL write bottleneck | >10K writes/sec | Shard by short_code prefix | Cross-shard analytics harder |
| Redirect latency spikes | Cache eviction of viral URLs | Tiered cache (local in-process LRU + Redis) | Memory per app server |

### Step 6 — Trade-offs

| Decision | Chosen | Alternative | Why |
|---|---|---|---|
| Code generation | Snowflake + Base62 | MD5 hash | No collisions; no DB round-trips |
| Redirect type | HTTP 302 | HTTP 301 | 302 allows analytics tracking (301 cached by browser forever) |
| Primary DB | MySQL | Cassandra | URL creation is ACID; read scale via replicas is sufficient |
| Cache strategy | Cache-aside | Write-through | Write-through wastes cache for rare URLs; lazy is better |

---

## Example 2: Design a Social Feed (Twitter Timeline)

### Step 1 — Requirements

**Functional:**
- User posts a tweet (text, media)
- User views home timeline (tweets from accounts they follow)
- User views user timeline (tweets from a single account)
- User searches tweets by keyword
- Push notifications to followers
- Out of scope: ads, moments, DMs, live video

**Non-functional:**
- 100M DAU; 500M tweets/day
- Home timeline load: < 200ms p99
- Availability: 99.99%
- Tweets are immutable after posting (no edit initially)

### Step 2 — Capacity

```
Tweet writes: 500M / 86400 = ~6,000 tweets/sec (peak: 18K)
Timeline reads: 250B / 2.5M = 100,000 reads/sec (peak: 300K)
Search: 10B / 2.5M = 4,000 searches/sec

Fan-out:
  Average follower count: 10
  5B fan-out events/day -> 60,000 fan-out ops/sec

Tweet storage: 10 KB/tweet x 500M/day x 365 x 3 = 5.47 PB
Active timeline cache: 100M users x 100 tweets x 10 KB = 100 TB (hot 20% = 20 TB Redis)
```

### Step 3 — High-Level Design

```
[Client] -> [CDN (media)] -> [Load Balancer] -> [API Gateway (auth, rate limit)]
  -> [Tweet Service] -> [Kafka (tweet events)] -> [Fan-out Workers]
                     -> [Tweet Store (Cassandra)]
                     -> [Media Store (S3)]
  -> [Timeline Service] -> [Timeline Cache (Redis, 20 TB)]
  -> [Search Service] -> [Elasticsearch cluster]
  -> [Notification Service] -> [APNs / FCM]
  -> [User Graph Service] -> [Graph DB (followers/following)]
  [Monitoring: Prometheus + Grafana + Jaeger]
```

### Step 4 — Core Component Deep Dives

**Fan-out on Write (Push model):**
```
When user posts tweet:
1. Write tweet to Cassandra (durable storage)
2. Publish tweet_id + author_id to Kafka topic 'new_tweets'
3. Fan-out workers consume from Kafka
4. For each follower: prepend tweet_id to their Redis timeline list
   LPUSH timeline:<user_id> <tweet_id>
   LTRIM timeline:<user_id> 0 999  (keep only latest 1000 tweets)
5. Timeline read: LRANGE timeline:<user_id> 0 99 -> fetch tweet details from Cassandra

Celebrity problem (>1M followers):
  Fan-out 1M writes to Redis takes too long (minutes)
  SOLUTION: Hybrid push-pull
  - Regular users: fan-out on write (push)
  - Celebrity accounts (>1M followers): fan-out on read (pull)
  - Timeline service merges: Redis list (push tweets) + fetch celebrity tweets on demand
```

**Tweet Schema (Cassandra wide-column):**
```
CREATE TABLE tweets (
  tweet_id     UUID,
  author_id    UUID,
  content      TEXT,
  media_ids    LIST<UUID>,
  created_at   TIMESTAMP,
  PRIMARY KEY (tweet_id)
);

CREATE TABLE user_timeline (
  user_id      UUID,
  tweet_id     UUID,
  created_at   TIMESTAMP,
  PRIMARY KEY (user_id, created_at)  -- partition by user, cluster by time
) WITH CLUSTERING ORDER BY (created_at DESC);
```

**Search (Elasticsearch):**
```
On tweet creation -> async worker indexes tweet content to Elasticsearch
Index mapping:
  tweet_id, author_id, content (analyzed, English), hashtags (keyword), created_at
Query: match phrase on content, filter by date range, sort by relevance or recency
```

### Step 5 — Bottleneck Analysis

| Bottleneck | Trigger | Mitigation |
|---|---|---|
| Redis OOM | Timeline cache grows beyond RAM | Shard Redis cluster; evict old timelines; compress tweet IDs |
| Fan-out lag for celebrities | 1M+ followers | Hybrid push-pull; batch fan-out with low priority |
| Cassandra hot partitions | Viral tweet read | Cache hot tweets in Redis separately |
| Elasticsearch lag | Indexing 6K tweets/sec | Async indexing via Kafka; bulk index batches |

---

## Example 3: Design a Distributed Rate Limiter

### Step 1 — Requirements

**Functional:**
- Limit API calls per user, per IP, and per API key
- Return HTTP 429 when limit exceeded
- Configurable: different limits per endpoint or customer tier
- Out of scope: billing, analytics dashboards, DDoS scrubbing

**Non-functional:**
- < 5ms overhead per request check
- Limits accurate within 1% across distributed nodes
- Availability: 99.99% (rate limiter failure = allow traffic, not block all)

### Step 2 — Capacity

```
10,000 API servers x 1,000 RPS each = 10M RPS total
Redis rate limit checks: 10M check ops/sec

Redis throughput: ~1M ops/sec per node
  -> Need Redis Cluster with 10+ shards
  -> OR: local in-process rate limiter + Redis for cross-node sync
```

### Step 3 — High-Level Design

```
[Client] -> [API Gateway]
              -> [Rate Limiter Middleware]
                    -> [Local Token Bucket (in-process, per node)]
                    -> [Redis Cluster (distributed sync, sliding window)]
              -> [Upstream Service]
```

### Step 4 — Algorithm Comparison

**Token Bucket:**
```python
# Redis implementation
def is_allowed(user_id, limit, window_sec):
    key = f"rate:{user_id}"
    now = time.time()
    pipe = redis.pipeline()
    # Remove tokens older than window
    pipe.zremrangebyscore(key, 0, now - window_sec)
    # Count current tokens
    pipe.zcard(key)
    # Add current request
    pipe.zadd(key, {str(uuid4()): now})
    # Set expiry
    pipe.expire(key, window_sec)
    _, count, _, _ = pipe.execute()
    return count < limit
```

**Fixed Window Counter:**
```python
def is_allowed(user_id, limit, window_sec):
    key = f"rate:{user_id}:{int(time.time() // window_sec)}"
    count = redis.incr(key)
    if count == 1:
        redis.expire(key, window_sec)
    return count <= limit
# Problem: burst at window boundary (up to 2x limit)
```

**Sliding Window Log**: Most accurate; stores all timestamps; high memory at scale.
**Sliding Window Counter**: Hybrid of fixed windows; approximates sliding window; low memory.

**CHOSEN**: Sliding window counter (accuracy vs memory trade-off).

### Step 5 — Trade-offs

| Decision | Chosen | Alternative | Why |
|---|---|---|---|
| Algorithm | Sliding window counter | Token bucket | Better burst control; lower memory than sliding log |
| Sync mode | Local + async Redis sync | Fully centralized Redis | Local check = 0ms overhead; async = eventual accuracy |
| Failure mode | Fail open (allow traffic) | Fail closed (block all) | Rate limiter failure should not block legitimate traffic |

---

## Example 4: Design a Notification System

### Step 1 — Requirements

**Functional:**
- Send push notifications (iOS APNs, Android FCM), SMS (Twilio), and email (SendGrid)
- Support one-off and scheduled notifications
- User opt-out preferences respected
- Retry failed deliveries
- Out of scope: in-app notification center

**Non-functional:**
- 10M notifications/day across channels
- Delivery latency: push < 5 sec, email < 30 sec
- At-least-once delivery guarantee
- Availability: 99.9%

### Step 2 — Capacity

```
Total: 10M notifications/day = 116 notifications/sec average
Peak: 3x = 350 notifications/sec

Breakdown (assumed):
  Push: 70% = 245/sec
  Email: 20% = 70/sec
  SMS: 10% = 35/sec

Kafka: 350 msgs/sec (trivial; Kafka handles 1M/sec)
```

### Step 3 — High-Level Design

```
[API / Service Events] -> [Notification Service API]
  -> [Kafka 'notifications' topic]
    -> [Push Worker] -> [APNs / FCM]
    -> [Email Worker] -> [SendGrid / SES]
    -> [SMS Worker]  -> [Twilio]
  -> [User Preference Service] (opt-out check before enqueue)
  -> [Retry Queue (Redis or Kafka DLQ)] (failed delivery retry with backoff)
  -> [Delivery Log (Cassandra)] (audit trail, deduplication)
```

**Deduplication**: Each notification gets idempotency key. Workers check delivery log before sending. Prevents double-send on retry.

**Retry strategy**: Exponential backoff (1s, 2s, 4s, 8s, max 5 retries). After 5 failures, move to dead letter queue (DLQ) and alert.

---

## Summary: Design Process Reference Card

```
1. REQUIREMENTS (5-10 min)
   - Enumerate functional features (what the system DOES)
   - State non-functional targets with NUMBERS (RPS, latency SLA, availability)
   - Explicitly list what is OUT OF SCOPE

2. CAPACITY (5 min)
   - writes/sec = monthly_writes / 2.5M
   - reads/sec  = monthly_reads  / 2.5M
   - peak = 2-3x average
   - storage/year, bandwidth in/out
   - cache size needed (20% of hot data)

3. HIGH-LEVEL DESIGN (10-15 min)
   - Draw layers: DNS -> CDN -> LB -> API -> Cache -> DB -> Queue -> Workers
   - JUSTIFY each component (why it's there, what it prevents)
   - Call out SPOF and how redundancy addresses them

4. DEEP DIVES (15-20 min)
   - Pick 2-3 most complex or critical components
   - Schema, API contract, algorithm choice
   - Failure modes and recovery

5. SCALE & TRADE-OFFS (5 min)
   - Top 3 bottlenecks at 10x scale: what breaks first and how to fix it
   - Trade-off table: decision | chosen | alternative | rationale
```
