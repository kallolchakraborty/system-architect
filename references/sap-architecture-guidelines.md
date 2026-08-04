# SAP Reference Architecture Guidelines

This document codifies the core architecture and design guidelines from the **SAP Architecture Center** (`https://architecture.learning.sap.com/docs/ref-arch`) and the **SAP Discovery Center**. It serves as the definitive reference when the `system-architect` skill is invoked for SAP BTP, S/4HANA extensions, or SAP Integration Suite scenarios.

---

## 1. Core Principles & Philosophy

### 1.1 The "Clean Core" Paradigm
When extending SAP S/4HANA or other SAP core systems, the strict directive is to keep the core clean of custom modifications.
- **In-App Extensibility**: Minor UI tweaks, custom fields, and business logic using Key User Extensibility. Used for tight coupling.
- **Side-by-Side Extensibility**: Deployed on SAP BTP (Business Technology Platform). Used for decoupled, scalable applications, complex integrations, and partner solutions. **This is the preferred pattern for system design.**

### 1.2 Composable Architecture
Design systems as independent, loosely coupled building blocks leveraging SAP BTP services rather than building monolithic extensions. Use established SAP Discovery Center missions/reference architectures before designing custom patterns.

---

## 2. Technology Domains

### 2.1 AI & Machine Learning
SAP promotes the **AI-native North Star Architecture** and the **AI Golden Path**.
- **Generative AI Hub**: Centralized access point for LLMs on BTP. Use it for text generation, embeddings, and summarization instead of calling external LLMs directly. Ensures compliance and trust.
- **Agentic AI Standards**: When designing multi-agent AI solutions on SAP, align with SAP's global standards for Agentic AI, ensuring agents are governed, secure, and interoperable with business data.
- **SAP AI Core**: For deploying and operating custom machine learning models at scale.

### 2.2 Application Development & Automation
When designing side-by-side applications on BTP, use standard programming models:
- **SAP CAP (Cloud Application Programming Model)**: The recommended framework for building enterprise-grade apps (Node.js or Java). Features built-in OData support, CDS (Core Data Services) for schema definition, and automatic out-of-the-box multi-tenancy support.
- **SAP RAP (RESTful ABAP Programming Model)**: The recommended approach if the development team is ABAP-centric and building tightly integrated extensions on S/4HANA or SAP BTP ABAP Environment.
- **SAP Build**: For low-code/no-code application composition, process automation (Build Process Automation), and business sites (Build Work Zone). Use when business users need to rapidly compose solutions without professional developers.

### 2.3 Data & Analytics
Data gravity dictates that moving ERP data is expensive. Follow these guidelines:
- **SAP Datasphere**: The foundation of the business data fabric. Use Datasphere to semantically connect data across SAP and non-SAP landscapes.
- **Data Federation vs. Replication**: **Federate** data whenever possible to avoid replication costs and staleness (using SAP Datasphere virtual tables). **Replicate** only when latency/performance dictates it (e.g., using SAP Landscape Transformation Replication Server (SLT) or SAP Event Mesh for CDC).
- **SAP Analytics Cloud (SAC)**: The primary tool for BI, planning, and predictive analytics.

### 2.4 Integration (ISA-M)
SAP Integration Solution Advisory Methodology (ISA-M) provides standard integration patterns:
- **A2A / B2B Integration**: Use **SAP Integration Suite** (specifically Cloud Integration) as the central ESB/middleware.
- **Event-Driven Architecture (EDA)**: Use **SAP Event Mesh** or **SAP Advanced Event Mesh** for asynchronous, high-volume event publishing (e.g., Business Events from S/4HANA like `BusinessPartner.Created`).
- **API Management**: Front all exposed microservices and OData endpoints with **SAP API Management** for rate limiting, threat protection, and monetization.

### 2.5 Operation & Security
- **Identity & Access**: Always delegate authentication to **SAP Cloud Identity Services** (Identity Authentication Service - IAS for user login, and Identity Provisioning Service - IPS for sync).
- **Observability**: Use **SAP Cloud ALM** (Application Lifecycle Management) for monitoring health, performance, and integrations of BTP apps. Do not build custom monitoring dashboards unless specifically integrating into a corporate standard (e.g., Datadog/Dynatrace).

---

## 3. Technology Partners (Multi-Cloud Interoperability)

SAP BTP runs on top of hyperscalers. When designing hybrid architectures leveraging partner technologies (AWS, Azure, GCP, Datadog, Snowflake), observe the following interoperability guidelines:
1. **AWS / Azure / GCP**: Use SAP Private Link service to securely connect SAP BTP applications to native hyperscaler services (e.g., S3 buckets, Azure Blob, Google BigQuery) without traversing the public internet.
2. **IBM**: Leverage the SAP and IBM partnership for AI and infrastructure, often utilizing IBM Watsonx for enterprise AI capabilities integrated with SAP.
3. **Data Partners (Databricks, Snowflake)**: Use SAP Datasphere's native outbound integrations for analytics workflows, ensuring SAP business semantics are preserved when data leaves the SAP ecosystem.
4. **Nvidia**: Leverage SAP's strategic partnership with Nvidia for accelerated computing and GenAI by accessing Nvidia foundation models through the SAP Generative AI Hub.

---

## 4. Architectural Decision Records (ADRs) for SAP

When delivering an SAP-based system design, the Trade-off Summary (Step 6) must explicitly address these common SAP dilemmas:
- **CAP vs RAP**: Node.js/Java cloud-native vs. ABAP-native.
- **Cloud Integration vs Event Mesh**: Request/Reply (sync) vs. Fire/Forget (async).
- **Datasphere vs Hyperscaler Data Lake**: Preserving business context vs. raw compute scale.
- **In-App vs Side-by-Side**: Maintenance overhead vs. architectural flexibility.
