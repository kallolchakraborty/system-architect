<div align="center">

# 🏗️ System Architect Skill Engine
**The Enterprise-Grade Distributed Systems & Architectural Skill for Autonomous AI**

[![Author](https://img.shields.io/badge/Author-Kallol%20Chakraborty-blue.svg?style=for-the-badge&logo=github)](https://github.com/kallolchakraborty)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production--Ready-brightgreen.svg?style=for-the-badge)]()
[![Type](https://img.shields.io/badge/Type-AI%20Agent%20Skill%20Engine-purple.svg?style=for-the-badge)]()
[![Eval Score](https://img.shields.io/badge/Eval%20Score-300%2F300%20%28100%25%29-brightgreen.svg?style=for-the-badge)]()

*A standardized, mathematically rigorous methodology for designing scalable, fault-tolerant, high-throughput software architectures, tailored for autonomous AI agents and Principal Engineers.*

</div>

---

## 📑 Table of Contents

1. [📖 Overview & Mission](#-overview--mission)
2. [✨ Key Features & Value Proposition](#-key-features--value-proposition)
3. [🎯 Target Audience & Use Cases](#-target-audience--use-cases)
4. [🧠 The 4-Step Production Methodology](#-the-4-step-production-methodology)
5. [🗂️ Knowledge Base Reference Modules](#-knowledge-base-reference-modules)
6. [🛡️ Behavioral & Quality Guardrails](#️-behavioral--quality-guardrails)
7. [🚀 Installation & Integration Guide](#-installation--integration-guide)
8. [📊 Evaluation Engine & Benchmarks](#-evaluation-engine--benchmarks)
9. [🤖 Agent Prompt Blueprints](#-agent-prompt-blueprints)
10. [🤝 Contribution Governance](#-contribution-governance)
11. [📝 License](#-license)

---

## 📖 Overview & Mission

The **System Architect** framework is a premier, enterprise-grade distributed systems design engine. It is specifically engineered to augment Large Language Models (LLMs), Autonomous AI Coding Agents, and Principal Software Architects with a structured, rigorous methodology for system design.

Generic AI models often default to superficial advice (e.g., "use a cache," "scale horizontally," or "use Kafka for events"). The **System Architect Skill Engine** intercepts these generic responses and enforces a mathematically-backed blueprint. From defining strict Service Level Agreements (SLAs) and high-level cloud topologies to low-level object-oriented design patterns, database sharding strategies, API contracts, and data pipelines—this skill ensures that every design decision is justifiable, quantitative, and production-ready.

---

## ✨ Key Features & Value Proposition

- **⚖️ Trade-off Primacy (CAP & PACELC Theorem)**: No component is introduced without explicit acknowledgment of trade-offs. The skill mandates a detailed analysis of what is gained (e.g., lower latency) versus what is sacrificed (e.g., strong consistency).
- **🧮 Mathematical Foundation**: Rigorous capacity calculations (Requests Per Second (RPS), Storage, Bandwidth, Memory Sizing) dictate the selection of database engines, cache sizes, and queue topologies before a single diagram is drawn.
- **🛡️ Zero Single Points of Failure (SPOF)**: Strict enforcement of Active-Active or Active-Passive failover topologies across every application and infrastructure layer.
- **🏗️ Resilience Engineering**: Mandatory inclusion of circuit breakers, rate limiters, retries with exponential backoff, jitter, and queue back-pressure handling for distributed systems stability.
- **✅ Guaranteed Quality & Benchmarking**: The engine is heavily tested and benchmarked, consistently achieving a **300/300 (100%)** score against a 60-assertion evaluation harness modeling Stanford HELM, RAGAS, ISO/IEC 25010, and LangChain standards.
- **📚 Modular Knowledge Architecture**: The skill utilizes an extensible reference system (7+ modular domains) ensuring context windows remain optimized while providing immense technical depth when triggered.

---

## 🎯 Target Audience & Use Cases

| Audience | Primary Use Case | Core Benefit |
| :--- | :--- | :--- |
| **🤖 Autonomous AI Agents** | Capability augmentation for multi-agent frameworks. | Empowers agents with a structured methodology to *plan rigorously before they build*, preventing costly refactors. |
| **📐 Principal / Staff Architects** | Drafting High-Level Designs (HLDs) & RFCs. | Accelerates the creation of comprehensive trade-off matrices, sequence diagrams, and capacity models for executive review. |
| **👨‍💼 Engineering Managers** | Standardizing Architectural Review Boards (ARBs). | Provides a unified, objective framework for cross-team design reviews, ensuring security and compliance standards are met. |
| **💻 System Design Candidates** | FAANG/MAANG Interview preparation. | Simulates the most rigorous, industry-grade methodology expected in L5+ system design interviews. |

---

## 🧠 The 4-Step Production Methodology

The skill enforces a strict, linear pipeline for architectural design to prevent hallucinations and ensure logical consistency:

```mermaid
graph TD
    subgraph Step 1: Requirements & SLAs
        Req1[Scope: Functional & Non-Functional]
        Req2[Scale Targets: DAU, MAU, RPS]
        Req3[Latency SLA: p50, p99, p99.9]
        Req4[Availability & Consistency Model]
    end

    subgraph Step 2: Capacity Estimation
        Math1[Throughput: Writes/sec & Reads/sec]
        Math2[Storage: 3-5 Year Projections]
        Math3[Bandwidth: Ingress & Egress]
        Math4[Cache: Working Set RAM Sizing]
    end

    subgraph Step 3: High-Level Topology
        Client[Clients / Mobile / Web] --> Edge[Edge / CDN / WAF]
        Edge --> API[API Gateway / Load Balancer]
        API --> App[Stateless Application Tier]
        App --> Cache[(Distributed Cache Cluster)]
        App --> MsgQueue[[Async Event Queue / Broker]]
        MsgQueue --> Workers[Background Worker Pool]
        App --> DB[(Durable Database Tier / Shards)]
    end

    subgraph Step 4: Deep Dives & Trade-offs
        Deep1[Data Partitioning & Sharding Strategy]
        Deep2[Cache Eviction & Invalidation TTLs]
        Deep3[API Contracts & Protocol Selection]
        Deep4[Comprehensive Trade-off Matrix]
    end

    Step 1 -->|Establishes Baselines| Step 2
    Step 2 -->|Dictates Scale| Step 3
    Step 3 -->|Identifies Bottlenecks| Step 4
```

### 1️⃣ Phase 1: Requirements Formulation & SLA Boundaries
Establish concrete functional scope and non-functional targets before any design work begins.
* **Functional Requirements:** What must the system do? (e.g., "Users can upload 50MB videos", "Real-time chat delivery").
* **Scale Targets:** Daily Active Users (DAU), average Request Per Second (RPS), and peak load multipliers (e.g., flash sales).
* **Latency SLA:** Explicit p50, p99, and p99.9 targets (e.g., `< 200ms at p99`).
* **Availability Target:** 99.9% (3 nines) up to 99.999% (5 nines) uptime requirements.
* **Consistency Model:** Explicit declaration of Strong Consistency vs. Eventual Consistency vs. Read-Your-Writes.

### 2️⃣ Phase 2: Capacity Estimation & Mathematical Modeling
Execute back-of-the-envelope estimations to determine hardware constraints and storage paradigms.
* **Writes/sec** = `(Monthly Writes) / (30 days * 24 hours * 3600 seconds) ≈ (Monthly Writes) / 2.5M`
* **Reads/sec** = `(Monthly Reads) / 2.5M`
* **3-Year Storage** = `(Average Record Size) * (Monthly Writes) * 36 months`
* **Cache RAM** = `0.20 * (Daily Active Dataset Size) * (Metadata Overhead)`
* **Bandwidth (Ingress/Egress)** = `(RPS) * (Average Payload Size)`

### 3️⃣ Phase 3: High-Level Topology Design
Construct a structured component diagram traversing client-to-storage layers. *Every component's existence must be explicitly justified based on the math from Phase 2.* Includes Load Balancers, API Gateways, Stateless Application Nodes, Distributed Caches, Asynchronous Message Brokers, and Database Clusters (Primary/Replica).

### 4️⃣ Phase 4: Core Component Deep Dives & Resolution
Dive into critical system bottlenecks and operational edge cases.
* **Database Selection:** SQL vs NoSQL choices justified via the CAP/PACELC theorems.
* **Caching Strategies:** Write-through, Read-through, or Cache-aside policies, including Cache Eviction (LRU/LFU) and Invalidation rules.
* **Data Partitioning:** Sharding keys, consistent hashing, and hot-partition mitigation.
* **Trade-off Summary Matrix:** A required artifact comparing rejected designs against the proposed architecture.

---

## 🗂️ Knowledge Base Reference Modules

To maintain a lightweight core while offering unparalleled depth, the engine delegates technical specialization to modular markdown reference documents located in the `references/` directory.

| Reference Module | Domain / Subject | Deep Dive Contents |
| :--- | :--- | :--- |
| 🗄️ [`core-components.md`](references/core-components.md) | **Infrastructure & DB Scaling** | Replication topologies, sharding, CRDTs, Service Mesh, consensus algorithms (Raft/Paxos). |
| 🧮 [`capacity-cheatsheet.md`](references/capacity-cheatsheet.md) | **Capacity & Latency Math** | Hardware latency tables (L1/L2, SSD, Network), power-of-two math, throughput estimation formulas. |
| 🏙️ [`worked-examples.md`](references/worked-examples.md) | **Canonical Systems** | 8 complete end-to-end architectures (Twitter/X, Bit.ly, Uber/Ride-Sharing, WhatsApp, Netflix). |
| 🏗️ [`object-oriented-design.md`](references/object-oriented-design.md) | **LLD & OOP Patterns** | SOLID principles, Gang of Four patterns, Thread-Safe LRU Cache implementation, Parking Lot System. |
| 🌐 [`api-design-and-protocols.md`](references/api-design-and-protocols.md) | **API & Gateway Design** | RESTful standards, gRPC/Protobufs, GraphQL, Idempotency keys, Cursor Pagination, BFF pattern. |
| 🌊 [`data-engineering-and-modern-arch.md`](references/data-engineering-and-modern-arch.md)| **Data Engineering & Analytics**| Batch vs Stream processing (Hadoop/Spark vs Flink), CDC (Debezium), Data Lakes, Serverless Event-Driven flows. |
| 🏢 [`sap-architecture-guidelines.md`](references/sap-architecture-guidelines.md) | **SAP BTP & Clean Core** | SAP CAP/RAP frameworks, SAP Event Mesh, ISA-M methodology, Multi-cloud integration patterns. |

---

## 🛡️ Behavioral & Quality Guardrails

Agents executing the System Architect skill are constrained by rigorous rules of engagement to eliminate hallucination, bias, and superficiality:

* 🚫 **No Brand-Name Dropping Without Justification:** Agents cannot blindly recommend technologies (e.g., "Use Kafka") without mapping them directly to specific access patterns, scale targets, and payload sizes.
* 🚫 **No Vague Caching Directives:** "Use a cache" is prohibited. Agents must specify the layer, the pattern (cache-aside/write-through), eviction policy (LRU/LFU), TTL strategies, and the invalidation owner.
* 🚫 **No Unaddressed Single Points of Failure (SPOFs):** Every SPOF must be identified and paired with a concrete Active-Passive or Active-Active failover path.
* 🚫 **No Missing Mathematics:** Deep dives cannot proceed without quantitative capacity calculations establishing the baseline.
* ✅ **Mandatory Internal Audits:** Before finalizing output, the agent automatically executes a 10-point self-audit to guarantee compliance with the 4-step methodology.

---

## 🚀 Installation & Integration Guide

The skill is built as a standard, markdown-based Agent Skill, ensuring seamless integration with major AI agent platforms, CLI tools, and IDEs including **Google Gemini**, **Google Antigravity SDK**, **Hermes Agent Framework**, **OpenCode**, **Cursor**, and **Windsurf**.

### Option A: Global Agent Installation (Host Environment)
Install the skill globally so all your agent workflows and CLI interactions can access it automatically.

```bash
# 1. Clone the repository
git clone https://github.com/kallolchakraborty/system-architect-skill.git
cd system-architect-skill

# 2. Link for Gemini / Antigravity Agent Environments
mkdir -p ~/.gemini/config/skills
ln -s "$(pwd)" ~/.gemini/config/skills/system-architect

# 3. Link for Hermes Agent Environments
mkdir -p ~/.hermes/skills/software-development
ln -s "$(pwd)" ~/.hermes/skills/software-development/system-architect
```

### Option B: Project-Local Integration (Repository Level)
Embed the skill engine directly into a specific Git repository for localized, context-aware agent execution. This ensures the skill travels with your codebase.

```bash
# In your target repository's root directory:
mkdir -p .agents/skills/system-architect
cp -r "/path/to/system-architect-skill/"* .agents/skills/system-architect/
```

### Option C: IDE Integration (Cursor / Windsurf)
1. Copy the contents of `SKILL.md` into your `.cursorrules` or `.windsurfrules` file.
2. Place the `references/` directory in a `.system-design/` folder at the root of your project.
3. Update the file paths in the prompt rules to point to the local reference documents.

---

## 📊 Evaluation Engine & Benchmarks

We believe in measurable, objective quality. This repository includes a bespoke v2.0 Industry-Grade Evaluation Harness (`scripts/run_evals.py`) that scores the agent's output against a strict 60-assertion matrix. The evaluation framework models standards from **Stanford HELM**, **RAGAS**, **LangChain**, and **ISO/IEC 25010**.

### Running the Evaluation Suite
```bash
# Execute the full 10-suite evaluation harness locally
python3 scripts/run_evals.py
```

### Benchmark Results

| Test Suite | Assessment Category | Modeled Benchmark Standard | Tested Metrics | Score |
| :--- | :--- | :--- | :--- | :--- |
| **Suites 1-4** | Execution & Coverage | Agentic Spec / RAGAS | Frontmatter parsing, methodology completeness, 15/15 architectural domains covered | ✅ 160/160 |
| **Suites 5-7** | Quality & Safety | ISO/IEC 25010 / OWASP | Low vagueness penalty, valid AST generation, safe execution sandboxing | ✅ 75/75 |
| **Suites 8-10**| Readability & Budget | Stanford HELM / UX | Zero redundancy, high information density, token budget compliance | ✅ 65/65 |
| **TOTAL** | **Overall Quality** | **Production Grade Standard** | **All 60/60 test assertions passed flawlessly** | **🏆 300/300** |

---

## 🤖 Agent Prompt Blueprints

To maximize the efficacy of the System Architect skill, utilize highly specific prompts that act as rigorous inputs for the 4-step pipeline.

### Blueprint 1: High-Scale Consumer Architecture (e.g., Google Docs)
> *"Trigger the System Architect Skill. Act as a Principal System Architect. Design a real-time Collaborative Document Editing Platform supporting 10M DAU and 100k concurrent active documents. Follow the 4-Step System Design process explicitly. Execute full capacity math, define WebSocket sync, detail the Operational Transformation (OT) or CRDT strategy, map out the storage layers, and provide a full trade-off matrix."*

### Blueprint 2: Enterprise Refactoring & Bottleneck Audit (e.g., E-Commerce)
> *"Trigger the System Architect Skill. Review our current architecture: A single PostgreSQL primary database with 3 read replicas, a Node.js monolith, and a Redis cache. We are experiencing severe query latency spikes and lock contention during flash sales (targeting 50k writes/sec). Perform a bottleneck analysis. Design a migration path to a sharded, event-driven architecture using the Strangler Fig pattern, and justify your database engine choice via the PACELC theorem."*

### Blueprint 3: Low-Level Object-Oriented Design (LLD)
> *"Trigger the System Architect Skill. Design the LLD for a multi-level Parking Lot system. Apply SOLID principles and Gang of Four design patterns. Provide the class diagrams, define the API contracts for `enterVehicle()` and `exitVehicle()`, and handle concurrency for when two vehicles attempt to claim the last spot simultaneously."*

---

## 🤝 Contribution Governance

We actively welcome contributions from the community to expand our knowledge base, add new canonical examples, and refine architectural patterns! To ensure the highest standard of quality, please adhere to the following governance model:

1. **Format Compliance**: All new reference documents added to the `references/` directory must strictly adhere to the technical depth, density, and formatting standards of the existing repository.
2. **Quality Gate Requirement**: Any modifications to `SKILL.md` or reference files must achieve a flawless **100% score (300/300 pts)** on the evaluation harness (`python3 scripts/run_evals.py`). Pull requests with failing evaluations will not be merged.
3. **Token Budget Guardrails**: `SKILL.md` frontmatter descriptions must remain concise ($\le 1024$ characters), with trigger phrases front-loaded in the first 57 characters to optimize LLM context window attention mechanisms.
4. **Pull Request Process**: Please open an issue to discuss proposed changes before submitting a PR. Use conventional commits for your commit messages.

---

## 📝 License

This project is licensed under the terms of the **MIT License**. 

*You are free to use, modify, and distribute this skill in both open-source and commercial enterprise environments. See the [LICENSE](LICENSE) file for complete details.*

<div align="center">
  <br>
  <i>"Architecture is about the important stuff. Whatever that is." — Ralph Johnson</i>
</div>
