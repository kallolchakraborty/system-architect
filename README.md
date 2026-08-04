<div align="center">

# 🏗️ System Architect
**Enterprise Distributed Systems & Architectural Skill Engine for Autonomous AI**

[![Author](https://img.shields.io/badge/Author-Kallol%20Chakraborty-blue.svg?style=for-the-badge&logo=github)](https://github.com/kallolchakraborty)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production--Ready-brightgreen.svg?style=for-the-badge)]()
[![Type](https://img.shields.io/badge/Type-AI%20Agent%20Skill%20Engine-purple.svg?style=for-the-badge)]()
[![Eval Score](https://img.shields.io/badge/Eval%20Score-300%2F300%20%28100%25%29-brightgreen.svg?style=for-the-badge)]()

*A standardized, mathematically rigorous methodology for designing scalable, fault-tolerant, high-throughput software architectures.*

</div>

---

## 📖 Overview

The **System Architect** framework is an enterprise-grade distributed systems design engine engineered specifically for Large Language Models (LLMs), Principal Software Architects, and Autonomous AI Coding Agents. 

It transcends generic advice like "use a cache" or "scale horizontally" by providing a structured, mathematically-backed blueprint for designing architectures—from high-level cloud topologies down to low-level object-oriented design patterns, database sharding strategies, API contracts, and data pipelines.

---

## ✨ Key Features & Value Proposition

- **⚖️ Trade-off Primacy**: Every architectural design decision explicitly defines what is gained (e.g., lower latency) and what is sacrificed (e.g., strong consistency).
- **🧮 Mathematical Foundation**: Before any topology is drawn, rigorous capacity calculations (RPS, Storage, Bandwidth) dictate the selection of database engines, cache sizes, and queue topologies.
- **🛡️ Zero Single Points of Failure (SPOF)**: Strict enforcement of Active-Active or Active-Passive failover topologies across every application layer.
- **🏗️ Resilience Engineering**: Mandatory inclusion of circuit breakers, rate limiters, retries with exponential backoff, and queue back-pressure handling.
- **✅ Guaranteed Quality**: Benchmarked and evaluated to achieve a **300/300 (100%)** score against a 60-assertion evaluation harness modeling Stanford HELM, RAGAS, and LangChain standards.

---

## 🎯 Target Audience & Use Cases

| Audience | Primary Use Case | Benefit |
| :--- | :--- | :--- |
| **🤖 Autonomous AI Agents** | Skill augmentation for coding agents. | Empowers agents with a structured methodology to *plan rigorously before they build*. |
| **📐 Principal Architects** | Drafting High-Level Designs (HLDs). | Accelerates the creation of comprehensive trade-off matrices and capacity models. |
| **👨‍💼 Engineering Managers** | Standardizing architectural reviews. | Provides a unified framework for cross-team architectural review boards (ARBs). |
| **💻 System Design Candidates** | Interview preparation. | Simulates the most rigorous, industry-grade methodology for FAANG-level design interviews. |

---

## 🚀 Quickstart & Installation

The skill is built for seamless integration with major AI agent platforms including **Google Gemini, Google Antigravity SDK, Hermes Agent Framework, OpenCode,** and popular IDEs like **Cursor and Windsurf**.

### Global Agent Installation (Host Environment)
Install the skill globally so all your agent workflows can access it:

```bash
# For Gemini / Antigravity Agent Environments
mkdir -p ~/.gemini/config/skills
ln -s "$(pwd)" ~/.gemini/config/skills/system-architect

# For Hermes Agent Environments
mkdir -p ~/.hermes/skills/software-development
ln -s "$(pwd)" ~/.hermes/skills/software-development/system-architect
```

### Project-Local Integration (Repository Level)
Embed the skill engine directly into a specific Git repository for localized agent execution:

```bash
mkdir -p .agents/skills/system-architect
cp -r "/path/to/System Design Skill/"* .agents/skills/system-architect/
```

---

## 🧠 The 4-Step Production Methodology

The skill enforces a strict pipeline for architectural design:

```mermaid
graph TD
    subgraph Step 1: Requirements & SLAs
        Req1[Scale Targets: DAU, RPS]
        Req2[Latency SLA: p50, p99]
        Req3[Availability: 99.99%]
        Req4[Consistency Model]
    end

    subgraph Step 2: Capacity Estimation
        Math1[Writes/sec & Reads/sec]
        Math2[Storage & Bandwidth]
        Math3[Cache RAM Sizing]
    end

    subgraph Step 3: High-Level Topology
        Client[Clients] --> Edge[Edge / CDN]
        Edge --> API[API Gateway / LB]
        API --> App[Stateless App Tier]
        App --> Cache[(Distributed Cache)]
        App --> MsgQueue[[Async Event Queue]]
        MsgQueue --> Workers[Background Workers]
        App --> DB[(Durable DB Tier)]
    end

    subgraph Step 4: Deep Dives & Trade-offs
        Deep1[Database Selection via CAP]
        Deep2[Cache Eviction & TTL]
        Deep3[Trade-off Matrix]
    end

    Step 1 --> Step 2
    Step 2 --> Step 3
    Step 3 --> Step 4
```

### 1️⃣ Requirements Formulation & SLA Boundaries
Establish concrete functional scope and non-functional targets:
* **Scale Targets:** DAU, average RPS, and peak RPS.
* **Latency SLA:** p50 and p99 targets (e.g., `< 200ms`).
* **Availability Target:** 99.9% up to 99.999% uptime.
* **Consistency Model:** Strong vs. Eventual vs. Read-your-writes.

### 2️⃣ Capacity Estimation & Mathematical Modeling
Execute back-of-the-envelope estimations before drafting component topologies:
* **Writes/sec** = `(Monthly Writes) / 2,500,000`
* **Reads/sec** = `(Monthly Reads) / 2,500,000`
* **3-Year Storage** = `(Record Size) * (Monthly Writes) * 36`
* **Cache RAM** = `0.20 * (Daily Active Dataset Size)`

### 3️⃣ High-Level Topology Design
Construct a structured component diagram traversing client-to-storage layers. *Every component's existence must be explicitly justified based on the SLA.*

### 4️⃣ Core Component Deep Dives
Dive into critical bottlenecks. Define SQL vs NoSQL choices via the CAP theorem, detail cache invalidation policies, set queue back-pressure limits, and produce a complete **Trade-off Summary Matrix**.

---

## 📚 Knowledge Base Reference Modules

The engine delegates technical specialization to modular reference documents, allowing it to remain lightweight while providing immense depth.

| Reference Module | Core Technical Subject | Key Contents |
| :--- | :--- | :--- |
| 🗄️ [`core-components.md`](references/core-components.md) | **Infrastructure & DB Scaling** | Replication, sharding, CRDTs, service mesh, observability. |
| 🧮 [`capacity-cheatsheet.md`](references/capacity-cheatsheet.md) | **Capacity & Latency** | Hardware latency tables, power-of-two math, throughput formulas. |
| 🏙️ [`worked-examples.md`](references/worked-examples.md) | **Canonical Systems** | 8 end-to-end architectures (Twitter, Bit.ly, Ride-Sharing). |
| 🏗️ [`object-oriented-design.md`](references/object-oriented-design.md) | **LLD & OOP Patterns** | SOLID principles, Thread-Safe LRU Cache, Parking Lot System. |
| 🌐 [`api-design-and-protocols.md`](references/api-design-and-protocols.md) | **API & Gateway Design** | REST/gRPC/GraphQL, Idempotency, Cursor Pagination, BFF. |
| 🌊 [`data-engineering-and-modern-arch.md`](references/data-engineering-and-modern-arch.md) | **Data Engineering** | Batch vs Stream, CDC (Debezium), Data Lakes, Serverless. |
| 🏢 [`sap-architecture-guidelines.md`](references/sap-architecture-guidelines.md) | **SAP BTP & Clean Core** | SAP CAP/RAP, Event Mesh, ISA-M, Multi-cloud integration. |

---

## 🛡️ Behavioral & Quality Guardrails

Agents utilizing this skill are subject to **strict enforcement guardrails** to prevent hallucinations or superficial design outputs:

* 🚫 **No Brand-Name Dropping:** Cannot recommend technologies (e.g., "Use Kafka") without matching them to specific access patterns and scale targets.
* 🚫 **No Vague Caching:** "Use a cache" is prohibited. Agents must specify the strategy (write-through/read-through), eviction policy (LRU/LFU), TTL, and invalidation owner.
* 🚫 **No Unaddressed SPOFs:** Single points of failure must be identified and paired with a concrete failover path.
* 🚫 **No Missing Mathematics:** Deep dives cannot proceed without prior quantitative capacity calculations.
* ✅ **Internal Audits:** Agents automatically run a 10-point self-audit before finalizing their output to ensure compliance with the methodology.

---

## 📊 Evaluation Engine & Benchmark

The repository includes a v2.0 Industry-Grade Evaluation Harness (`scripts/run_evals.py`) modeling standards from Stanford HELM, RAGAS, LangChain, and ISO/IEC 25010.

```bash
# Execute the full 10-suite evaluation harness locally
python3 scripts/run_evals.py
```

| Suite | Category | Benchmark Standard | Tested Metric | Score |
| :--- | :--- | :--- | :--- | :--- |
| **1-4** | Execution & Coverage | Agentic Spec / RAGAS | Frontmatter, completeness, 15/15 domains | ✅ 160/160 |
| **5-7** | Quality & Safety | ISO/IEC / OWASP | Low vagueness, valid AST, safe execution | ✅ 75/75 |
| **8-10** | Readability & Budget | HELM / UX | Zero redundancy, high density, budget compliance | ✅ 65/65 |
| **TOTAL** | **Overall Quality** | **Production Standard** | **All 60 test assertions passed** | **🏆 300/300** |

---

## 🤖 Agent Prompt Blueprints

To get the most out of the System Architect skill, use highly specific prompts that trigger its deep-dive capabilities.

### Blueprint 1: High-Scale Architecture Design
> *"Act as a Principal System Architect. Design a real-time Collaborative Document Editing Platform (like Google Docs) supporting 10M DAU and 100k concurrent active documents. Follow the 4-Step System Design process. Execute full capacity math, define WebSocket sync, operational transformation / CRDTs, storage layers, and provide a full trade-off matrix."*

### Blueprint 2: Refactoring & Bottleneck Audit
> *"Review our current architecture: Single PostgreSQL primary database with 3 replicas, Node.js monolith, and Redis cache. We are experiencing query latency spikes during flash sales (50k writes/sec). Perform a bottleneck analysis and design a migration path to a sharded / event-driven architecture using the Strangler Fig pattern."*

---

## 🤝 Contribution & License

### License
This project is licensed under the terms of the **MIT License**. See [LICENSE](LICENSE) for details.

### Contribution Governance
We welcome contributions to expand the knowledge base and architectural patterns! Please adhere to the following governance model:
1. **Format Compliance**: All reference documents added to `references/` must strictly adhere to the technical depth and formatting standards of the repository.
2. **Quality Gate Requirement**: Any modifications to `SKILL.md` or reference files must achieve a **100% score (300/300 pts)** on the evaluation harness (`python3 scripts/run_evals.py`).
3. **Budget Guardrails**: `SKILL.md` frontmatter descriptions must remain $\le 1024$ characters, with trigger phrases front-loaded in the first 57 characters.
