window.SITE_CONTENT = [
  {
    "id": "system-design-methodology",
    "title": "System Architect — Industry-Grade 4-Step Methodology",
    "phase": 1,
    "phaseName": "Core Framework",
    "category": "Core Framework",
    "description": "Enterprise-grade distributed systems design methodology with 4 explicit stages.",
    "sections": [
      {
        "title": "Overview & Axioms",
        "description": "<div class=\"p-6 bg-slate-50 dark:bg-slate-800/50 rounded-xl border border-slate-200 dark:border-slate-800 mb-6\"><h3 class=\"text-lg font-bold text-slate-900 dark:text-white mb-2\">Core Architectural Axiom</h3><p class=\"text-slate-700 dark:text-slate-300 leading-relaxed\"><strong class=\"text-indigo-600 dark:text-indigo-400\">Everything is a trade-off.</strong> Every single system decision must explicitly document what you gain and what you sacrifice. Premature optimization kills clarity — execute all 4 design steps in sequence.</p></div>"
      },
      {
        "title": "Step 1 — Requirements & Scope (MANDATORY)",
        "description": "<div class=\"space-y-4 mb-6\"><div class=\"p-4 rounded-lg bg-indigo-50/50 dark:bg-indigo-950/30 border border-indigo-100 dark:border-indigo-900/40\"><h4 class=\"font-semibold text-indigo-700 dark:text-indigo-300 mb-2\">Functional Requirements</h4><ul class=\"list-disc ml-5 space-y-1 text-slate-700 dark:text-slate-300 text-sm\"><li>Core user actions (read, write, search, stream, notify)</li><li>Data inputs and outputs</li><li>Explicit out-of-scope boundaries (what you are NOT building)</li></ul></div><div class=\"p-4 rounded-lg bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-800\"><h4 class=\"font-semibold text-slate-900 dark:text-white mb-2\">Non-Functional Requirements</h4><ul class=\"list-disc ml-5 space-y-1 text-slate-700 dark:text-slate-300 text-sm\"><li><strong>Scale targets</strong>: DAU, MAU, peak RPS (reads/sec vs writes/sec)</li><li><strong>Latency SLAs</strong>: p50 and p99 targets (e.g. timeline load &lt; 200ms)</li><li><strong>Availability SLA</strong>: 99.9% vs 99.99% vs 99.999%</li><li><strong>Consistency model</strong>: Strong ACID vs Eventual consistency</li></ul></div></div>"
      },
      {
        "title": "Step 2 — Capacity Estimation (Back-of-Envelope)",
        "description": "<div class=\"overflow-x-auto my-4\"><table class=\"min-w-full border border-slate-200 dark:border-slate-800 text-sm rounded-lg overflow-hidden\"><thead class=\"bg-slate-100 dark:bg-slate-800\"><tr><th class=\"px-4 py-2 text-left font-semibold text-slate-900 dark:text-white\">Metric</th><th class=\"px-4 py-2 text-left font-semibold text-slate-900 dark:text-white\">Formula</th><th class=\"px-4 py-2 text-left font-semibold text-slate-900 dark:text-white\">Example / Note</th></tr></thead><tbody class=\"divide-y divide-slate-200 dark:divide-slate-800\"><tr class=\"bg-white dark:bg-slate-900\"><td class=\"px-4 py-2 font-medium text-slate-900 dark:text-white\">Writes / sec</td><td class=\"px-4 py-2 font-mono text-indigo-600 dark:text-indigo-400\">(writes/month) / 2.5M</td><td class=\"px-4 py-2 text-slate-600 dark:text-slate-400\">Average write throughput</td></tr><tr class=\"bg-slate-50 dark:bg-slate-800/40\"><td class=\"px-4 py-2 font-medium text-slate-900 dark:text-white\">Reads / sec</td><td class=\"px-4 py-2 font-mono text-indigo-600 dark:text-indigo-400\">(reads/month) / 2.5M</td><td class=\"px-4 py-2 text-slate-600 dark:text-slate-400\">Average read throughput</td></tr><tr class=\"bg-white dark:bg-slate-900\"><td class=\"px-4 py-2 font-medium text-slate-900 dark:text-white\">Peak RPS</td><td class=\"px-4 py-2 font-mono text-indigo-600 dark:text-indigo-400\">Average RPS × 2-3</td><td class=\"px-4 py-2 text-slate-600 dark:text-slate-400\">Account for traffic spikes</td></tr><tr class=\"bg-slate-50 dark:bg-slate-800/40\"><td class=\"px-4 py-2 font-medium text-slate-900 dark:text-white\">Cache RAM</td><td class=\"px-4 py-2 font-mono text-indigo-600 dark:text-indigo-400\">0.20 × Total Data Size</td><td class=\"px-4 py-2 text-slate-600 dark:text-slate-400\">80/20 Pareto rule for hot data</td></tr></tbody></table></div>"
      },
      {
        "title": "Step 3 — High-Level Design (HLD)",
        "description": "<div class=\"p-4 bg-slate-900 text-slate-100 rounded-xl font-mono text-sm leading-relaxed overflow-x-auto border border-slate-800 my-4\"><div class=\"text-indigo-400 mb-2\"># Standard Layered Architecture Topology</div><div>[Client] ➔ [DNS / CDN] ➔ [Load Balancer] ➔ [API Gateway]</div><div class=\"pl-8\">➔ [Application Microservices]</div><div class=\"pl-12\">➔ [Cache Layer (Redis)] ➔ [Primary DB / Replicas]</div><div class=\"pl-12\">➔ [Object Storage (S3)] ➔ [Message Queue (Kafka)] ➔ [Async Workers]</div></div>"
      },
      {
        "title": "Step 4 — Deep Dive & Trade-off Matrix",
        "description": "<div class=\"p-5 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl shadow-sm mb-4\"><p class=\"text-slate-700 dark:text-slate-300 leading-relaxed mb-3\">Deep dive into the 2-3 most critical components. Detail your data schemas, database selection rationale, API contracts, rate limiting, and failover recovery mechanisms.</p><div class=\"flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-indigo-600 dark:text-indigo-400\"><span class=\"material-symbols-outlined text-sm\">check_circle</span><span>Completion Gate: Schema + API Contract + Failover + Trade-off Matrix</span></div></div>"
      }
    ]
  },
  {
    "id": "capacity-cheatsheet",
    "title": "Capacity Estimation & Latency Cheatsheet",
    "category": "Capacity & Metrics",
    "description": "Latency numbers every programmer should know, storage conversion factors, and throughput calculation reference.",
    "sections": [
      {
        "title": "Latency Numbers Every Programmer Should Know",
        "description": "<div class=\"overflow-x-auto my-4\"><table class=\"min-w-full border border-slate-200 dark:border-slate-800 text-sm rounded-lg overflow-hidden\"><thead class=\"bg-slate-100 dark:bg-slate-800\"><tr><th class=\"px-4 py-2.5 text-left font-semibold text-slate-900 dark:text-white\">Operation</th><th class=\"px-4 py-2.5 text-left font-semibold text-slate-900 dark:text-white\">Time</th><th class=\"px-4 py-2.5 text-left font-semibold text-slate-900 dark:text-white\">Human Scale Equivalent</th></tr></thead><tbody class=\"divide-y divide-slate-200 dark:divide-slate-800\"><tr class=\"bg-white dark:bg-slate-900\"><td class=\"px-4 py-2 font-medium text-slate-900 dark:text-white\">L1 cache reference</td><td class=\"px-4 py-2 font-mono text-indigo-600 dark:text-indigo-400\">0.5 ns</td><td class=\"px-4 py-2 text-slate-600 dark:text-slate-400\">1 heart beat</td></tr><tr class=\"bg-slate-50 dark:bg-slate-800/40\"><td class=\"px-4 py-2 font-medium text-slate-900 dark:text-white\">Branch mispredict</td><td class=\"px-4 py-2 font-mono text-indigo-600 dark:text-indigo-400\">5 ns</td><td class=\"px-4 py-2 text-slate-600 dark:text-slate-400\">10 heart beats</td></tr><tr class=\"bg-white dark:bg-slate-900\"><td class=\"px-4 py-2 font-medium text-slate-900 dark:text-white\">Main memory reference (RAM)</td><td class=\"px-4 py-2 font-mono text-indigo-600 dark:text-indigo-400\">100 ns</td><td class=\"px-4 py-2 text-slate-600 dark:text-slate-400\">3.3 minutes</td></tr><tr class=\"bg-slate-50 dark:bg-slate-800/40\"><td class=\"px-4 py-2 font-medium text-slate-900 dark:text-white\">SSD random read</td><td class=\"px-4 py-2 font-mono text-indigo-600 dark:text-indigo-400\">150 µs</td><td class=\"px-4 py-2 text-slate-600 dark:text-slate-400\">3.5 months</td></tr><tr class=\"bg-white dark:bg-slate-900\"><td class=\"px-4 py-2 font-medium text-slate-900 dark:text-white\">Same Datacenter RTT</td><td class=\"px-4 py-2 font-mono text-indigo-600 dark:text-indigo-400\">500 µs (0.5 ms)</td><td class=\"px-4 py-2 text-slate-600 dark:text-slate-400\">1 year</td></tr><tr class=\"bg-slate-50 dark:bg-slate-800/40\"><td class=\"px-4 py-2 font-medium text-slate-900 dark:text-white\">Cross-Continent Packet (CA ➔ EU)</td><td class=\"px-4 py-2 font-mono text-indigo-600 dark:text-indigo-400\">150 ms</td><td class=\"px-4 py-2 text-slate-600 dark:text-slate-400\">300 years</td></tr></tbody></table></div>"
      }
    ]
  },
  {
    "id": "distributed-systems-and-db",
    "title": "Distributed Systems & Database Architecture",
    "category": "Architecture Modules",
    "description": "Deep dive into SQL vs NoSQL, CAP theorem, replication topologies, sharding strategies, and transactions.",
    "sections": [
      {
        "title": "Relational vs. NoSQL Matrix",
        "description": "<div class=\"overflow-x-auto my-4\"><table class=\"min-w-full border border-slate-200 dark:border-slate-800 text-sm rounded-lg overflow-hidden\"><thead class=\"bg-slate-100 dark:bg-slate-800\"><tr><th class=\"px-4 py-2.5 text-left font-semibold text-slate-900 dark:text-white\">Attribute</th><th class=\"px-4 py-2.5 text-left font-semibold text-slate-900 dark:text-white\">Relational (RDBMS)</th><th class=\"px-4 py-2.5 text-left font-semibold text-slate-900 dark:text-white\">NoSQL Systems</th></tr></thead><tbody class=\"divide-y divide-slate-200 dark:divide-slate-800\"><tr class=\"bg-white dark:bg-slate-900\"><td class=\"px-4 py-2 font-medium text-slate-900 dark:text-white\">Data Model</td><td class=\"px-4 py-2 text-slate-600 dark:text-slate-400\">Normalized tables with defined schemas</td><td class=\"px-4 py-2 text-slate-600 dark:text-slate-400\">Key-Value, Document, Wide-Column, Graph</td></tr><tr class=\"bg-slate-50 dark:bg-slate-800/40\"><td class=\"px-4 py-2 font-medium text-slate-900 dark:text-white\">Transactions</td><td class=\"px-4 py-2 text-slate-600 dark:text-slate-400\">Full ACID guarantees</td><td class=\"px-4 py-2 text-slate-600 dark:text-slate-400\">BASE / Eventual consistency</td></tr><tr class=\"bg-white dark:bg-slate-900\"><td class=\"px-4 py-2 font-medium text-slate-900 dark:text-white\">Scaling</td><td class=\"px-4 py-2 text-slate-600 dark:text-slate-400\">Vertical scale-up, Primary-Replica, Sharding</td><td class=\"px-4 py-2 text-slate-600 dark:text-slate-400\">Built-in horizontal auto-sharding</td></tr></tbody></table></div>"
      }
    ]
  },
  {
    "id": "scalability-patterns",
    "title": "Scalability Patterns & Caching Strategies",
    "category": "Architecture Modules",
    "description": "Caching topologies, invalidate patterns, load balancing algorithms, rate limiting, and asynchronous processing.",
    "sections": [
      {
        "title": "Caching Topologies & Invalidation",
        "description": "<div class=\"overflow-x-auto my-4\"><table class=\"min-w-full border border-slate-200 dark:border-slate-800 text-sm rounded-lg overflow-hidden\"><thead class=\"bg-slate-100 dark:bg-slate-800\"><tr><th class=\"px-4 py-2.5 text-left font-semibold text-slate-900 dark:text-white\">Strategy</th><th class=\"px-4 py-2.5 text-left font-semibold text-slate-900 dark:text-white\">Mechanism</th><th class=\"px-4 py-2.5 text-left font-semibold text-slate-900 dark:text-white\">Best For</th></tr></thead><tbody class=\"divide-y divide-slate-200 dark:divide-slate-800\"><tr class=\"bg-white dark:bg-slate-900\"><td class=\"px-4 py-2 font-medium text-slate-900 dark:text-white\">Cache-Aside (Lazy)</td><td class=\"px-4 py-2 text-slate-600 dark:text-slate-400\">App checks cache; on miss, loads from DB &amp; updates cache</td><td class=\"px-4 py-2 text-slate-600 dark:text-slate-400\">Read-heavy workloads</td></tr><tr class=\"bg-slate-50 dark:bg-slate-800/40\"><td class=\"px-4 py-2 font-medium text-slate-900 dark:text-white\">Write-Through</td><td class=\"px-4 py-2 text-slate-600 dark:text-slate-400\">App writes to cache; cache synchronously writes DB</td><td class=\"px-4 py-2 text-slate-600 dark:text-slate-400\">Strong consistency needs</td></tr><tr class=\"bg-white dark:bg-slate-900\"><td class=\"px-4 py-2 font-medium text-slate-900 dark:text-white\">Write-Behind</td><td class=\"px-4 py-2 text-slate-600 dark:text-slate-400\">App writes cache; cache asynchronously flushes DB</td><td class=\"px-4 py-2 text-slate-600 dark:text-slate-400\">High throughput write spikes</td></tr></tbody></table></div>"
      }
    ]
  },
  {
    "id": "resilience-security-operability",
    "title": "Resilience, Security & Operability",
    "category": "Architecture Modules",
    "description": "Circuit breakers, rate limiting, token buckets, TLS termination, zero-trust security, and observability stacks.",
    "sections": [
      {
        "title": "Fault Tolerance & Resilience Patterns",
        "description": "<div class=\"grid grid-cols-1 md:grid-cols-2 gap-4 my-4\"><div class=\"p-4 bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-800 rounded-xl\"><h4 class=\"font-bold text-slate-900 dark:text-white mb-1\">Circuit Breaker</h4><p class=\"text-xs text-slate-600 dark:text-slate-400 leading-relaxed\">Prevents cascading failures by opening circuit when error thresholds exceed limit (Closed ➔ Open ➔ Half-Open).</p></div><div class=\"p-4 bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-800 rounded-xl\"><h4 class=\"font-bold text-slate-900 dark:text-white mb-1\">Bulkheading</h4><p class=\"text-xs text-slate-600 dark:text-slate-400 leading-relaxed\">Isolates thread/connection pools so failures in one downstream service do not drain total application capacity.</p></div></div>"
      }
    ]
  }
];
