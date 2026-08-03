# Data Engineering & Modern Architecture Reference

Modern system design often intersects with data engineering (handling massive analytical workloads) and cloud-native patterns.

---

## 1. Data Engineering Pipelines

### Batch Processing
- **Characteristics**: Processes large, bounded datasets at scheduled intervals (e.g., nightly). High latency, high throughput.
- **Tools**: Apache Hadoop (MapReduce), Apache Spark, AWS EMR.
- **Use Case**: Generating daily reports, training machine learning models on historical data, monthly billing calculations.

### Stream Processing
- **Characteristics**: Processes continuous, unbounded data streams in real-time or near real-time. Low latency.
- **Tools**: Apache Kafka Streams, Apache Flink, Apache Spark Streaming, AWS Kinesis.
- **Use Case**: Real-time fraud detection, live dashboards, instant recommendations based on current user activity.

### Architectures
- **Lambda Architecture**: Runs both batch and stream processing in parallel. Batch layer provides accurate historical views; speed layer provides real-time approximate views. Serving layer merges them. (Drawback: requires maintaining two separate codebases/frameworks).
- **Kappa Architecture**: Stream-first. Treats everything as a stream. Batch processing is just stream processing over a historical log (like Kafka). Single unified codebase.

---

## 2. Storage Systems for Analytics

### Data Warehouse
- **Structure**: Highly structured, schema-on-write, relational.
- **Use Case**: Business Intelligence (BI), reporting, structured analytics.
- **Tools**: Amazon Redshift, Google BigQuery, Snowflake.
- **Data modeling**: Star schema, Snowflake schema.

### Data Lake
- **Structure**: Raw, unstructured, semi-structured, and structured data. Schema-on-read.
- **Use Case**: Machine learning, data exploration, storing massive volumes of logs cheaply.
- **Tools**: Amazon S3, Google Cloud Storage + query engines like Amazon Athena or Presto/Trino.

### Data Lakehouse
- Combines the structured query performance of a warehouse with the cheap, scalable storage of a data lake. Uses open table formats.
- **Tools**: Databricks (Delta Lake), Apache Iceberg, Apache Hudi.

---

## 3. Change Data Capture (CDC)

**Problem**: How do you keep a search index (Elasticsearch) or a data warehouse in sync with your primary transactional database (PostgreSQL/MySQL) without modifying the application code to write to both places (which risks dual-write inconsistencies)?

**Solution: CDC**
- CDC tools tail the database's transaction log (e.g., MySQL binlog, Postgres WAL) and stream every insert/update/delete as an event into a message broker (like Kafka).
- **Tools**: Debezium (most common open-source tool).
- **Pros**: Zero impact on primary application logic; guarantees eventual consistency; enables real-time materialized views and search indexing.

---

## 4. Modern Cloud-Native Compute

### Virtual Machines (IaaS)
- **Examples**: AWS EC2, GCP Compute Engine.
- **Pros**: Full control over OS, kernel tuning, easy migration of legacy apps.
- **Cons**: Slow startup time, overhead of managing OS patching and security.

### Containers (CaaS)
- **Examples**: Docker, Kubernetes (K8s), Amazon ECS, AWS Eargate.
- **Pros**: Consistent environments across dev/prod, fast startup, high resource utilization, orchestrators handle auto-healing and scaling.
- **Cons**: Learning curve (especially Kubernetes), cluster management overhead.

### Serverless (FaaS)
- **Examples**: AWS Lambda, Google Cloud Functions, Azure Functions.
- **Pros**: Pay only for execution time (no idle cost), auto-scales to zero and to thousands of concurrent requests instantly, zero infrastructure management.
- **Cons**: Cold starts (latency on first request after idle), vendor lock-in, limited execution duration, harder to debug locally.

### Compute Decision Matrix
- **Use Serverless when**: Event-driven workloads, highly variable traffic (spikes to zero), simple stateless glue code.
- **Use Containers (K8s) when**: Always-on services, microservices architecture, need control over runtime environment, avoiding vendor lock-in.
- **Use VMs when**: Legacy software, databases that require specific OS/disk tuning, predictable massive CPU/RAM workloads where reserved instances are cheaper.
