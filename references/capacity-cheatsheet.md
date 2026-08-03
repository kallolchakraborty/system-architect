# Capacity Estimation Cheat Sheet

## Core Conversion Table

```
Time conversions:
  1 day   = 86,400 seconds  (~100K)
  1 month = 2,500,000 seconds (~2.5M)
  1 year  = 31,500,000 seconds (~31.5M)

  Shortcut: 1 req/sec = 2.5 million req/month
            40 req/sec = 100 million req/month
            400 req/sec = 1 billion req/month
```

## Storage Size Reference

```
Data sizes:
  1 char = 1 byte
  1 UUID = 16 bytes (128-bit) or 36 chars as string
  1 int  = 4 bytes
  1 long = 8 bytes
  1 float = 4 bytes, double = 8 bytes
  1 timestamp = 8 bytes

Typical record sizes:
  Tweet (text only): ~150 bytes
  Tweet (with metadata): ~500 bytes
  User profile row: ~1 KB
  Session token: ~256 bytes
  URL metadata row: ~500 bytes
  Product listing: ~2 KB
  Image (thumbnail): ~50 KB
  Image (full HD): ~2 MB
  Video (1 min, 1080p): ~100-150 MB
```

## Standard Estimation Templates

### Template A — Write-heavy (IoT, logging, events)

```
Writes/sec = daily_writes / 86400
           = monthly_writes / 2.5M

Peak writes = 3x average (traffic spikes)

Storage/month = record_bytes x monthly_writes
Storage/3yr   = storage/month x 36

Inbound bandwidth = record_KB x writes/sec  [KB/s]
```

### Template B — Read-heavy (social feed, search, catalog)

```
Reads/sec = monthly_reads / 2.5M
Read:write ratio -> state it explicitly (e.g., 100:1)

Cache memory needed:
  Hot data = 20% of working set (Pareto)
  Cache RAM = 0.20 x total_active_dataset_GB

Cache hit rate target: >= 90% for read-heavy systems
  Every 10% drop in hit rate -> 10% more DB load
```

### Template C — Media upload (video, images)

```
Storage/sec = upload_size_MB x uploads/sec  [MB/s]
CDN outbound = avg_file_MB x downloads/sec  [MB/s]

Encoding pipeline:
  Input video: 1 GB raw
  Outputs: 1080p (500 MB), 720p (250 MB), 480p (100 MB), 360p (50 MB)
  Total storage per video: ~1 GB input + 0.9 GB output = ~2 GB
```

## Latency Numbers Every Engineer Should Know

```
Operation                    Latency         Notes
--------------------------   -------------   ----------------------------
L1 cache reference           0.5 ns
L2 cache reference           7 ns            14x L1 cache
Branch misprediction         5 ns
Mutex lock/unlock            25 ns
Main memory reference        100 ns          20x L2 cache, 200x L1 cache
Compress 1K bytes (LZ)       3 us (3000 ns)
Send 1K bytes over 1Gbps     10 us
Read 4K randomly from SSD    150 us          ~1GB/s SSD
Read 1MB sequentially (RAM)  250 us
Round trip within datacenter 500 us
Read 1MB sequentially (SSD)  1 ms            4x RAM
HDD seek                     10 ms           20x SSD seek
Read 1MB sequentially (HDD)  20 ms           80x RAM, 20x SSD
Send packet CA -> Netherlands -> CA  150 ms
```

**Key intuitions from these numbers:**
- RAM is 20x faster than SSD, SSD is 20x faster than HDD
- Network I/O within DC: ~0.5ms; cross-continent: ~150ms
- CPU-bound operations in memory are 1000x faster than disk seeks
- Compression saves bandwidth at the cost of CPU

## Availability Math

```
Availability = uptime / (uptime + downtime)

Components in SERIES (AND): A_total = A1 x A2 x A3 x ...
  99.9% x 99.9% = 99.8%  (slightly worse)

Components in PARALLEL (OR): A_total = 1 - (1-A1) x (1-A2) x ...
  1 - (0.001 x 0.001) = 99.9999%  (much better)

Lesson: add redundancy to eliminate sequential failure paths.
```

## Throughput Capacity Limits (Approximate)

```
Single server (modern, well-tuned):
  Web requests (stateless, small payload):  ~10,000-50,000 RPS
  Database queries (indexed reads):         ~10,000 QPS
  Database writes (with fsync):             ~1,000-5,000 WPS
  Redis operations:                         ~100,000-1M ops/sec
  Kafka throughput:                         ~1M msgs/sec per broker

Network:
  1 Gbps NIC:   ~125 MB/s = ~125,000 KB/s
  10 Gbps NIC:  ~1.25 GB/s
  100 Gbps NIC: ~12.5 GB/s

Disk:
  HDD sequential: 100-200 MB/s
  SSD sequential: 500 MB/s - 3.5 GB/s (NVMe)
  SSD random 4K:  ~100K IOPS (SATA) to ~700K IOPS (NVMe)
```

## Example: Twitter-scale Estimation

```
Given:
  100M active users
  500M tweets/day
  Average fanout: 10 followers per tweet read
  250B read requests/month
  10B searches/month

Calculations:
  Tweets/sec = 500M / 86400 = ~6,000 tweets/sec
  Reads/sec  = 250B / 2.5M  = 100,000 reads/sec
  Search/sec = 10B  / 2.5M  = 4,000 searches/sec
  Fanout/sec = 500M x 10 / 86400 = 60,000 fan-outs/sec

  Storage (tweets, 3 years):
    10 KB/tweet x 500M tweets/day x 365 days/yr x 3 years
    = 10 KB x 547B = 5.47 PB

  Cache (for timelines, hot 20%):
    Active users' timelines: 100M x 100 tweets x 10 KB = ~100 TB
    20% hot = 20 TB of Redis RAM needed (sharded)

Architecture conclusion:
  - Writes: Kafka fan-out pipeline (60K events/sec)
  - Reads: Redis timeline cache (100K reads/sec, 20 TB RAM)
  - Storage: Cassandra for tweet objects (5+ PB, write-optimized)
  - Search: Elasticsearch cluster
```

## Example: URL Shortener Estimation

```
Given:
  100M URLs created/month
  10B URL redirects/month (100:1 read:write)
  URL lifetime: 5 years

Calculations:
  Writes/sec = 100M / 2.5M = 40 writes/sec
  Reads/sec  = 10B  / 2.5M = 4,000 reads/sec (peak: ~12K)

  Storage:
    500 bytes/URL record
    100M URLs/month x 500 bytes = 50 GB/month
    5 years = 50 GB x 60 months = 3 TB total

  Cache:
    Hot URLs: 20% of daily traffic = 0.2 x 4000 reads/sec
    Store top 20% of URLs in Redis
    100M URLs x 500 bytes x 0.20 = 10 GB cache

Architecture conclusion:
  - 4000 reads/sec -> single Redis node handles easily (well under 100K ops/sec limit)
  - 40 writes/sec -> single MySQL node with Master-Replica is fine
  - 3 TB storage over 5 years -> manageable with MySQL sharding later
  - Start simple: 1 web server + 1 MySQL + 1 Redis
```
