# Module 7: SAP Enterprise Architecture & BTP Cloud Blueprints

> **Context**: Designing for the SAP ecosystem requires adherence to SAP's Clean Core strategy, deep integration with the SAP Business Technology Platform (SAP BTP), and security architectures prioritizing Principal Propagation. This module provides reference patterns directly aligned with the official [SAP Architecture Center](https://architecture.learning.sap.com).

---

## 1. Clean Core Strategy & Extensibility

When extending SAP systems (e.g., S/4HANA), modifications to the core ERP are discouraged (technical debt). Use these patterns instead:

### A. Side-by-Side Extensibility (Preferred)
- **Host**: SAP BTP (Cloud Foundry, Kyma, or Serverless).
- **Tech Stack**: SAP Cloud Application Programming Model (CAP) using Node.js/Java, or SAP RAP (RESTful ABAP Programming Model).
- **Use Case**: Decoupled applications, large-scale custom UIs, SaaS multitenancy, or heavy integrations with third-party systems.
- **Integration**: Communicates with the SAP backend via OData (v2/v4) or Enterprise Messaging (Event Mesh).

### B. In-App (On-Stack) Extensibility
- **Host**: SAP S/4HANA Core (ABAP Cloud).
- **Tech Stack**: ABAP RESTful Application Programming Model (RAP) and Key User Extensibility.
- **Use Case**: Tightly coupled transactional logic, minor UI adjustments (Fiori Elements), custom CDS views, and validation logic requiring immediate synchronous DB access without network hops.

---

## 2. SAP Business Technology Platform (BTP) Services

Map generic architecture components to their SAP BTP equivalents:

| Generic Component | SAP BTP Equivalent | Key Characteristics |
|---|---|---|
| API Gateway | **SAP API Management** | Rate limiting, OAuth/SAML policies, quota management. |
| Message Queue / Broker | **SAP Event Mesh / Advanced Event Mesh** | Pub/Sub, Webhooks, AMQP/MQTT support, S/4HANA event integration. |
| Data Warehouse | **SAP Datasphere** | Semantic layer, virtual data access, federation with hyperscalers. |
| DB / Storage | **SAP HANA Cloud** | In-memory HTAP (Hybrid Transactional/Analytical Processing), Vector Engine. |
| Identity Provider (IdP) | **SAP Cloud Identity Services (IAS/IPS)** | Single Sign-On (SSO), user provisioning, integration with Azure AD. |
| Integration Broker | **SAP Cloud Integration (CPI)** | Out-of-the-box adapters (Ariba, SuccessFactors, Salesforce), mapping. |
| App Platform (PaaS) | **Cloud Foundry / Kyma (K8s)** | Polyglot runtime, buildpacks, container orchestration. |

---

## 3. Enterprise Security & Principal Propagation

**Never hardcode credentials or service users for business transactions.**

- **Pattern**: Principal Propagation.
- **Mechanism**: Passes the logged-in user's identity from the cloud application (BTP) to the on-premise or backend system (S/4HANA).
- **Flow**:
  1. User authenticates via Identity Authentication Service (IAS).
  2. BTP Application exchanges the JWT token for an OAuth2 SAML Bearer Assertion.
  3. The token is passed to the **SAP Cloud Connector** (deployed in the customer's DMZ).
  4. Cloud Connector translates the identity into a short-lived X.509 certificate.
  5. S/4HANA trusts the certificate and maps it to a local ABAP user for authorization.

---

## 4. AI-Native North Star Architecture & Agentic AI

SAP's AI architecture (AI Foundation) emphasizes embedding AI directly into business processes while abstracting away hyperscaler LLM dependencies.

- **SAP Generative AI Hub**: A centralized gateway for interacting with Foundation Models (GPT-4, Claude, Gemini, open-source via Aleph Alpha or Meta). It provides enterprise data privacy, usage metering, and prompt management.
- **Agentic AI Standards (A2A)**: For building autonomous agents on BTP. Agents must:
  - Utilize the **SAP HANA Cloud Vector Engine** for RAG (Retrieval-Augmented Generation) with enterprise context.
  - Implement tool calling against standard SAP APIs (OData/REST) with Principal Propagation to ensure the agent only accesses data the underlying user is authorized to see.
  - Fall back to the "AI Golden Path" pattern for orchestration, keeping logic in CAP and inference in AI Core.

---

## 5. Hyperscaler Integration Topologies (Partners)

SAP architectures often run in a multi-cloud or hybrid context.

- **AWS / Azure / GCP / IBM**: Use SAP BTP on the target hyperscaler to reduce latency. Integrate native services (e.g., Azure Event Grid, AWS EventBridge, GCP Pub/Sub) with SAP Event Mesh for cross-cloud eventing.
- **Databricks / Snowflake**: **Zero-Copy Integration**. Do not build ETL pipelines to extract massive data from SAP Datasphere. Instead, use data federation where Databricks/Snowflake queries Datasphere virtually, or vice versa, preserving semantic context and reducing data gravity issues.
- **Nvidia**: Accelerated training for custom localized models on SAP AI Core utilizing GPU instances.

---

## 6. Architecture Verification (Clean Core Checklist)

When reviewing an SAP architecture, apply these gates:
1. **Is the Core Clean?** Are custom tables and logic moved to BTP or ABAP Cloud, rather than using classic BADIs or user exits?
2. **Is it API First?** Are integrations using standard OData v4 or SOAP APIs documented in the SAP Business Accelerator Hub, rather than direct database RFCs?
3. **Is the Identity Propagated?** Does the architecture use Cloud Connector + Principal Propagation, or is it relying on a technical/system user? (System users are an anti-pattern for business transactions).
4. **Is it Event-Driven?** Is the system using SAP Event Mesh to listen to business object changes, rather than aggressive polling?
