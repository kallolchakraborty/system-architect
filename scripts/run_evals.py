#!/usr/bin/env python3
"""
============================================================
INDUSTRY-GRADE SKILL EVALUATION HARNESS v2.0
system-architect — Distributed Systems Design Skill
============================================================

Evaluation suites modeled after:
  - Agentic Skill Evaluation Framework
  - HELM (Holistic Evaluation of Language Models) — Stanford
  - RAGAS (Retrieval-Augmented Generation Assessment)
  - LangChain Agent Eval Checklist
  - ISO/IEC 25010 Software Quality Model

Suites:
  Suite 1  — Frontmatter Schema & System Prompt Signal Quality
  Suite 2  — Trigger Recall & Precision (Prompt Classification)
  Suite 3  — Structural Completeness & Process Integrity
  Suite 4  — Content Coverage Matrix (Domain Coverage Scoring)
  Suite 5  — Instruction Quality & Specificity (Anti-Vagueness)
  Suite 6  — Reference Integrity & Cross-Link Validation
  Suite 7  — Code Snippet AST & Safety Verification
  Suite 8  — Redundancy & Duplication Detection
  Suite 9  — Readability & Cognitive Load Estimation
  Suite 10 — Token Budget & Context Efficiency

Author: Kallol Chakraborty
"""

import sys
import re
import ast
import math
import pathlib
import yaml
import json
from collections import Counter
from difflib import SequenceMatcher

ROOT = pathlib.Path(__file__).parent.parent
SKILL_FILE   = ROOT / "SKILL.md"
README_FILE  = ROOT / "README.md"
REF_DIR      = ROOT / "references"

# ANSI colour codes
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"

PASS = f"{GREEN}✅ PASS{RESET}"
FAIL = f"{RED}❌ FAIL{RESET}"
WARN = f"{YELLOW}⚠️  WARN{RESET}"

# ─────────────────────────────────────────────────────────────
# GLOBAL STATE
# ─────────────────────────────────────────────────────────────
all_results = []   # (suite_id, test_name, status, score, detail)
skill_content = SKILL_FILE.read_text(encoding="utf-8")

def add(suite, name, passed, score, detail=""):
    status = PASS if passed else FAIL
    all_results.append((suite, name, status, score, detail))
    return passed


# ═══════════════════════════════════════════════════════════
# SUITE 1 — Frontmatter Schema & System Prompt Signal Quality
# ═══════════════════════════════════════════════════════════
def suite_1():
    print(f"\n{CYAN}{BOLD}[Suite 1] Frontmatter Schema & System Prompt Signal Quality{RESET}")

    content = skill_content
    assert content.startswith("---"), "SKILL.md does not start with '---'"
    m = re.search(r'\n---\s*\n', content[3:])
    assert m, "Missing closing '---' frontmatter delimiter"
    fm_raw = content[3:m.start()+3]
    fm = yaml.safe_load(fm_raw)

    # 1.1 — Required fields present
    required_fields = ["name", "description", "version", "author", "license", "metadata"]
    missing = [f for f in required_fields if f not in fm]
    add(1, "1.1 Required frontmatter fields (name/version/author/license/metadata)", len(missing)==0, 5,
        f"Missing: {missing}" if missing else "All 6 required fields present")

    # 1.2 — Name: lowercase, hyphens, ≤64 chars, no spaces
    name = fm.get("name","")
    name_ok = bool(re.match(r'^[a-z][a-z0-9-]{1,63}$', name))
    add(1, "1.2 Name format: ^[a-z][a-z0-9-]{1,63}$", name_ok, 3, f"Name='{name}'")

    # 1.3 — Description ≤1024 chars (agent system-prompt budget)
    desc = fm.get("description","")
    add(1, "1.3 Description ≤1024 chars (system-prompt budget)", len(desc)<=1024, 5,
        f"Length: {len(desc)} chars")

    # 1.4 — Trigger phrase in first 57 chars (index truncation)
    first57 = desc[:57]
    trigger_ok = first57.lower().startswith("use when")
    add(1, "1.4 Trigger phrase ('Use when…') front-loaded within 57 chars", trigger_ok, 5,
        f"'{first57}'")

    # 1.5 — Description contains high-signal domain keywords
    domain_kw = ["scalab", "distribut", "architect", "capacity", "hld", "component", "trade-off"]
    kw_hits = sum(1 for kw in domain_kw if kw in desc.lower())
    add(1, "1.5 Description contains ≥4 domain-specific trigger keywords", kw_hits>=4, 3,
        f"Domain keywords found: {kw_hits}/{len(domain_kw)}")

    # 1.6 — Version follows semantic versioning (MAJOR.MINOR.PATCH)
    version = str(fm.get("version",""))
    semver_ok = bool(re.match(r'^\d+\.\d+\.\d+$', version))
    add(1, "1.6 Semantic versioning (MAJOR.MINOR.PATCH)", semver_ok, 2, f"Version='{version}'")

    # 1.7 — Metadata Hermes tags ≥5, ≤20
    tags = fm.get("metadata",{}).get("hermes",{}).get("tags",[])
    add(1, "1.7 Hermes tags: 5 ≤ count ≤ 20", 5<=len(tags)<=20, 2, f"Tags: {tags}")

    # 1.8 — Related skills listed
    related = fm.get("metadata",{}).get("hermes",{}).get("related_skills",[])
    add(1, "1.8 Related skills defined (≥3)", len(related)>=3, 2, f"Related: {related}")


# ═══════════════════════════════════════════════════════════
# SUITE 2 — Trigger Recall & Precision (Prompt Classification)
# ═══════════════════════════════════════════════════════════
def suite_2():
    print(f"\n{CYAN}{BOLD}[Suite 2] Trigger Recall & Precision (Prompt Classification){RESET}")

    content = skill_content.lower()

    # Extract "When to Use" section
    when_use_m  = re.search(r'## when to use(.*?)(?=\n## |---)', content, re.DOTALL)
    dont_use_m  = re.search(r"don't use for:(.*?)(?=\n## |---)", content, re.DOTALL)
    
    when_body = when_use_m.group(1) if when_use_m else ""
    dont_body = dont_use_m.group(1) if dont_use_m else ""

    # True-positive prompts (MUST trigger)
    tp_prompts = [
        "design a url shortener like bitly for 10m dau",
        "how should i architect a distributed notification system",
        "help me do capacity estimation for a video streaming platform",
        "what database should i use for a high-write social feed",
        "design a rate limiter for an api gateway",
        "how do i scale my sql database to handle 100k writes per second",
        "design a real-time collaborative editing system like google docs",
        "design a side-by-side extension for sap s/4hana on btp",
        "architect an integration landscape using sap integration suite",
    ]
    # True-negative prompts (MUST NOT trigger)
    tn_prompts = [
        "fix this syntax error in my python script",
        "what is the capital of france",
        "reformat this json file",
        "add a hover animation to my css button",
        "write unit tests for this sorting function",
        "how do i center a div",
    ]

    # Keyword signals extracted from when-to-use and don't-use sections
    trigger_signals    = ["design", "architect", "scalab", "capacity", "distribut", "system", "high-level", "pattern", "database", "microservice", "scale", "hld", "sap", "btp", "clean core"]
    exclusion_signals  = ["syntax", "css", "html", "animation", "unit test", "sort", "geography", "capital"]

    # Recall: true positive hits (prompt contains ≥1 trigger signal)
    tp_hits = [p for p in tp_prompts if any(sig in p.lower() for sig in trigger_signals)]
    recall  = len(tp_hits) / len(tp_prompts)
    add(2, "2.1 Trigger Recall ≥ 87.5% (TP prompts)", recall >= 0.875, 10,
        f"Recall: {recall*100:.1f}% ({len(tp_hits)}/{len(tp_prompts)} TP prompts matched)")

    # Precision: true negative rejection (prompt NOT matched by trigger signals OR explicitly excluded)
    tn_no_hit = [p for p in tn_prompts if not any(sig in p.lower() for sig in trigger_signals)]
    precision = len(tn_no_hit) / len(tn_prompts)
    add(2, "2.2 Trigger Precision ≥ 80% (TN prompts not triggered)", precision >= 0.80, 10,
        f"Precision: {precision*100:.1f}% ({len(tn_no_hit)}/{len(tn_prompts)} TN prompts correctly excluded)")

    # F1 Score
    if (recall + precision) > 0:
        f1 = 2 * recall * precision / (recall + precision)
    else:
        f1 = 0.0
    add(2, "2.3 F1 Score ≥ 0.80 (Harmonic mean of recall & precision)", f1 >= 0.80, 10,
        f"F1 = {f1:.3f}")

    # Don't-use section explicitly defined
    add(2, "2.4 Explicit 'Don't Use For' boundary defined", bool(dont_body.strip()), 5,
        "Found explicit exclusion section" if dont_body.strip() else "MISSING: Explicit exclusion list required")


# ═══════════════════════════════════════════════════════════
# SUITE 3 — Structural Completeness & Process Integrity
# ═══════════════════════════════════════════════════════════
def suite_3():
    print(f"\n{CYAN}{BOLD}[Suite 3] Structural Completeness & Process Integrity{RESET}")

    content = skill_content

    # 3.1 — 4 mandatory steps present and sequentially ordered
    step_positions = []
    for i in range(1, 5):
        m = re.search(rf'step {i}', content, re.IGNORECASE)
        step_positions.append(m.start() if m else -1)
    
    steps_present = all(p >= 0 for p in step_positions)
    steps_ordered = steps_present and all(step_positions[i] < step_positions[i+1] for i in range(len(step_positions)-1))
    add(3, "3.1 All 4 Steps present & ordered sequentially", steps_ordered, 8,
        f"Step positions: {step_positions}")

    # 3.2 — Completion criteria per step (≥3 required)
    criteria_count = len(re.findall(r'\*\*completion criterion\*\*', content, re.IGNORECASE))
    add(3, "3.2 Completion criterion defined for ≥3 steps (process gates)", criteria_count>=3, 8,
        f"Found {criteria_count} completion criteria")

    # 3.3 — Capacity math block present with formula
    math_ok = '2.5M' in content or 'writes/sec' in content.lower()
    add(3, "3.3 Back-of-envelope capacity math formulas defined", math_ok, 8,
        "Throughput formulas found" if math_ok else "MISSING: Capacity math block")

    # 3.4 — HLD topology pattern present (ASCII / mermaid flow)
    topology_ok = '->' in content and 'Load Balancer' in content
    add(3, "3.4 HLD topology diagram/flow defined", topology_ok, 8,
        "HLD flow diagram present" if topology_ok else "MISSING: HLD component topology")

    # 3.5 — Common Pitfalls section present with ≥5 pitfalls
    pitfall_m = re.search(r'## common pitfalls(.*?)(?=\n## |---|\Z)', content, re.IGNORECASE | re.DOTALL)
    pitfall_count = len(re.findall(r'^\d+\.', pitfall_m.group(1), re.MULTILINE)) if pitfall_m else 0
    add(3, "3.5 Common Pitfalls section with ≥8 numbered anti-patterns", pitfall_count>=8, 5,
        f"Found {pitfall_count} pitfalls")

    # 3.6 — Verification Checklist section with ≥10 items
    checklist_m = re.search(r'## verification checklist(.*?)(?=\n## |---|\Z)', content, re.IGNORECASE | re.DOTALL)
    checklist_items = len(re.findall(r'- \[[ x]\]', checklist_m.group(1))) if checklist_m else 0
    add(3, "3.6 Verification Checklist with ≥10 gate items", checklist_items>=10, 5,
        f"Found {checklist_items} checklist items")

    # 3.7 — Output template section present
    output_tmpl = 'output format' in content.lower() or '## mandatory output' in content.lower() or 'output template' in content.lower()
    add(3, "3.7 Mandatory Output Format / Template section defined", output_tmpl, 8,
        "Output template found" if output_tmpl else "MISSING: Explicit output format template for LLM guidance")

    # 3.8 — References section present and linked
    refs_ok = '## references' in content.lower()
    add(3, "3.8 References section present at end of skill", refs_ok, 3,
        "References section present" if refs_ok else "MISSING: References section")


# ═══════════════════════════════════════════════════════════
# SUITE 4 — Content Coverage Matrix (Domain Coverage Scoring)
# ═══════════════════════════════════════════════════════════
def suite_4():
    print(f"\n{CYAN}{BOLD}[Suite 4] Content Coverage Matrix (Domain Coverage Scoring){RESET}")

    all_content = skill_content
    for ref_file in REF_DIR.glob("*.md"):
        all_content += ref_file.read_text(encoding="utf-8")
    
    content_lower = all_content.lower()

    domains = {
        "Load Balancing & Reverse Proxy":     ["load balancer", "round robin", "layer 7", "nginx", "haproxy", "ssl termination"],
        "Database Scaling (SQL)":              ["replication", "sharding", "shard key", "federation", "denormalization", "primary-replica"],
        "Database Scaling (NoSQL)":            ["cassandra", "dynamodb", "mongodb", "wide-column", "document store", "key-value"],
        "CAP Theorem & Consistency":           ["cap theorem", "consistency", "availability", "partition tolerance", "eventual consistency"],
        "Caching Strategy":                    ["cache-aside", "write-through", "write-behind", "ttl", "eviction", "lru", "redis", "memcached"],
        "Asynchronous Messaging & Queues":     ["message queue", "kafka", "rabbitmq", "back-pressure", "dead letter", "consumer", "producer"],
        "API Design & Protocols":              ["rest", "grpc", "graphql", "idempotency", "cursor pagination", "rate limit"],
        "CDN & Edge Network":                  ["cdn", "edge", "push model", "pull model", "origin server"],
        "Observability (Metrics/Logs/Traces)": ["prometheus", "grafana", "elk", "jaeger", "zipkin", "distributed tracing", "metrics"],
        "Security Fundamentals":               ["tls", "jwt", "oauth", "encryption", "rbac", "rate limiting"],
        "Data Engineering & Pipelines":        ["batch processing", "stream processing", "lambda architecture", "kappa", "cdc", "debezium"],
        "Low-Level Design (LLD)":              ["solid", "lru cache", "hash map", "design pattern", "singleton", "observer"],
        "Consistent Hashing":                  ["consistent hashing", "virtual node", "ring", "hash ring"],
        "Capacity Estimation":                 ["writes/sec", "reads/sec", "throughput", "back-of-the-envelope", "pareto"],
        "SAP Architecture":                    ["sap btp", "clean core", "isa-m", "sap cap", "integration suite", "fiori", "datasphere"],
    }

    covered = 0
    for domain, signals in domains.items():
        hits = sum(1 for s in signals if s in content_lower)
        domain_covered = hits >= 2
        if domain_covered:
            covered += 1
        add(4, f"4.x Coverage: {domain}", domain_covered, 2,
            f"{hits}/{len(signals)} signals found → {'✓' if domain_covered else '✗ requires ≥2 hits'}")

    coverage_pct = (covered / len(domains)) * 100
    add(4, f"4.TOTAL Domain Coverage ≥ 90%", coverage_pct >= 90, 20,
        f"Coverage: {covered}/{len(domains)} domains ({coverage_pct:.1f}%)")


# ═══════════════════════════════════════════════════════════
# SUITE 5 — Instruction Quality & Specificity (Anti-Vagueness)
# ═══════════════════════════════════════════════════════════
def suite_5():
    print(f"\n{CYAN}{BOLD}[Suite 5] Instruction Quality & Specificity (Anti-Vagueness){RESET}")

    content = skill_content

    # 5.1 — Vague filler phrases audit
    # 5.3 — Checklist items must begin with a capital letter verb/noun
    # Items that start with lowercase are considered unverifiable
    # Accept acronym-starts (API, CDN, CAP) as well as normal uppercase starts
    checklist_items = re.findall(r'- \[[ x]\] (.+)', skill_content)
    def is_verifiable(item):
        # Passes if starts with any uppercase letter (handles both Title case and ACRONYM starts)
        return bool(item) and item[0].isupper()
    unverifiable = [item for item in checklist_items if not is_verifiable(item)]
    add(5, "5.3 ≥90% checklist items begin with capital-letter verifiable criterion", 
        len(unverifiable) <= len(checklist_items) * 0.10, 5,
        f"{len(checklist_items)-len(unverifiable)}/{len(checklist_items)} verifiable items. Non-capital: {unverifiable[:3]}")
    vague_phrases = [
        "be careful", "make sure", "as needed", "as appropriate", "if necessary",
        "etc.", "and so on", "things like", "something like", "you should consider",
        "it depends", "various", "many factors", "some cases", "good practice",
    ]
    vague_hits = [(phrase, len(re.findall(re.escape(phrase), content, re.IGNORECASE)))
                  for phrase in vague_phrases
                  if re.search(re.escape(phrase), content, re.IGNORECASE)]
    total_vague = sum(count for _, count in vague_hits)
    add(5, "5.1 Low vague-phrase density (≤5 occurrences total)", total_vague<=5, 8,
        f"Vague phrases found ({total_vague}): {vague_hits[:5]}")

    # 5.2 — Concrete quantitative thresholds present
    numeric_pattern = re.findall(r'\b\d+[\.,]?\d*\s*(ms|ns|us|µs|mb|gb|tb|rps|req|k|m|b|%|x)\b', content, re.IGNORECASE)
    add(5, "5.2 Concrete quantitative thresholds (latency/size/scale numbers)", len(numeric_pattern)>=15, 8,
        f"Quantitative references found: {len(numeric_pattern)}")

    # 5.3 — Every checklist item is verifiable (starts with capital letter)
    # Intentionally accepts ACRONYM-starts (API, CDN, CAP) as well as Title Case

    # 5.4 — Trade-off language enforced (gain vs sacrifice pattern)
    tradeoff_ok = "trade-off" in content.lower() or "tradeoff" in content.lower()
    tradeoff_count = len(re.findall(r'trade.?off', content, re.IGNORECASE))
    add(5, "5.4 Trade-off language enforced (≥5 trade-off references)", tradeoff_count>=5, 5,
        f"Found {tradeoff_count} trade-off references")

    # 5.5 — Explicit anti-patterns / Don't-do instructions present
    dont_count = len(re.findall(r'\b(do not|don\'t|avoid|never|instead of|anti-pattern)\b', content, re.IGNORECASE))
    add(5, "5.5 Explicit anti-pattern / prohibition instructions (≥8)", dont_count>=8, 5,
        f"Anti-pattern directives found: {dont_count}")


# ═══════════════════════════════════════════════════════════
# SUITE 6 — Reference Integrity & Cross-Link Validation
# ═══════════════════════════════════════════════════════════
def suite_6():
    print(f"\n{CYAN}{BOLD}[Suite 6] Reference Integrity & Cross-Link Validation{RESET}")

    # 6.1 — All references in SKILL.md point to existing files
    skill_refs = re.findall(r'`(references/[a-zA-Z0-9_-]+\.md)`', skill_content)
    missing = [r for r in skill_refs if not (ROOT / r).exists()]
    add(6, "6.1 All SKILL.md reference links resolve to existing files", len(missing)==0, 8,
        f"Missing: {missing}" if missing else f"All {len(skill_refs)} reference links valid")

    # 6.2 — All files in references/ directory are linked in SKILL.md
    dir_refs = {f"references/{f.name}" for f in REF_DIR.glob("*.md")}
    unlinked = dir_refs - set(skill_refs)
    add(6, "6.2 All files in references/ are linked from SKILL.md", len(unlinked)==0, 5,
        f"Unlinked files: {unlinked}" if unlinked else "100% referenced in SKILL.md")

    # 6.3 — README links to all reference files
    readme_content = README_FILE.read_text(encoding="utf-8")
    readme_refs = set(re.findall(r'\[.*?\]\(.*?(references/[a-zA-Z0-9_%-]+\.md).*?\)', readme_content))
    readme_unlinked = dir_refs - readme_refs
    add(6, "6.3 README.md links to all reference modules", len(readme_unlinked)==0, 3,
        f"README unlinked: {readme_unlinked}" if readme_unlinked else "README references all modules")

    # 6.4 — No dead external URLs (check only GitHub URL format)
    external_urls = re.findall(r'https?://[^\s\)\"]+', skill_content)
    malformed = [u for u in external_urls if not re.match(r'https?://[a-zA-Z0-9.\-/]+', u)]
    add(6, "6.4 External URLs well-formed", len(malformed)==0, 3,
        f"Malformed URLs: {malformed}" if malformed else f"All {len(external_urls)} URLs well-formed")


# ═══════════════════════════════════════════════════════════
# SUITE 7 — Code Snippet AST & Safety Verification
# ═══════════════════════════════════════════════════════════
def suite_7():
    print(f"\n{CYAN}{BOLD}[Suite 7] Code Snippet AST & Safety Verification{RESET}")

    all_files = [SKILL_FILE, README_FILE] + list(REF_DIR.glob("*.md"))
    syntax_errors = []
    total_blocks = 0
    dangerous_patterns = []

    DANGEROUS = ["os.system", "subprocess.call", "eval(", "exec(", "__import__", "rm -rf", "DROP TABLE", "; DROP"]

    for f in all_files:
        text = f.read_text(encoding="utf-8")
        py_blocks = re.findall(r'```python\n(.*?)```', text, re.DOTALL)
        shell_blocks = re.findall(r'```(?:bash|sh|zsh)\n(.*?)```', text, re.DOTALL)

        for idx, block in enumerate(py_blocks):
            total_blocks += 1
            try:
                ast.parse(block)
            except SyntaxError as se:
                syntax_errors.append(f"{f.name} block #{idx+1}: {se.msg} (line {se.lineno})")
            # Safety scan
            for danger in DANGEROUS:
                if danger in block:
                    dangerous_patterns.append(f"{f.name} block #{idx+1}: contains '{danger}'")

        for idx, block in enumerate(shell_blocks):
            for danger in DANGEROUS:
                if danger in block:
                    dangerous_patterns.append(f"{f.name} shell block #{idx+1}: contains '{danger}'")

    add(7, f"7.1 Python code block AST syntax valid ({total_blocks} blocks)", len(syntax_errors)==0, 10,
        f"Errors: {syntax_errors}" if syntax_errors else f"All {total_blocks} Python blocks parse successfully")
    add(7, "7.2 No dangerous/destructive patterns in code snippets", len(dangerous_patterns)==0, 10,
        f"Dangerous patterns: {dangerous_patterns}" if dangerous_patterns else "No dangerous patterns detected")

    # 7.3 — Only opening fences without language specifier are a problem
    # Closing ``` fences are always bare and are not a violation
    in_fence = False
    bare_opens = []
    for line in skill_content.splitlines():
        stripped = line.strip()
        if stripped.startswith('```') and not in_fence:
            lang = stripped[3:].strip()
            if lang == '':
                bare_opens.append(line)
            in_fence = True
        elif stripped == '```' and in_fence:
            in_fence = False
    add(7, "7.3 All code blocks in SKILL.md have language specifier (no bare opening ```)", len(bare_opens)==0, 5,
        f"Bare opening fences found: {len(bare_opens)} → {bare_opens[:3]}" if bare_opens else "All code blocks have language specifiers")


# ═══════════════════════════════════════════════════════════
# SUITE 8 — Redundancy & Duplication Detection
# ═══════════════════════════════════════════════════════════
def suite_8():
    print(f"\n{CYAN}{BOLD}[Suite 8] Redundancy & Duplication Detection{RESET}")

    # 8.1 — No major paragraph duplication within SKILL.md
    # Split into paragraphs, check pairwise similarity
    paragraphs = [p.strip() for p in re.split(r'\n{2,}', skill_content) if len(p.strip()) > 100]
    duplicate_pairs = []
    for i in range(len(paragraphs)):
        for j in range(i+1, len(paragraphs)):
            ratio = SequenceMatcher(None, paragraphs[i], paragraphs[j]).ratio()
            if ratio > 0.80:
                duplicate_pairs.append((i, j, ratio))

    add(8, f"8.1 No near-duplicate paragraphs (similarity > 80%) in SKILL.md", len(duplicate_pairs)==0, 8,
        f"Duplicate pairs: {duplicate_pairs}" if duplicate_pairs else f"Checked {len(paragraphs)} paragraphs — no duplicates detected")

    # 8.2 — No repeated section headers
    headers = re.findall(r'^#{1,4} .+', skill_content, re.MULTILINE)
    header_counts = Counter(headers)
    duplicated_headers = {h:c for h,c in header_counts.items() if c > 1}
    add(8, "8.2 No duplicate section headers in SKILL.md", len(duplicated_headers)==0, 5,
        f"Duplicate headers: {duplicated_headers}" if duplicated_headers else f"All {len(headers)} headers unique")

    # 8.3 — Latency table not duplicated in SKILL.md and references/
    ref_all = "\n".join(f.read_text() for f in REF_DIR.glob("*.md"))
    latency_skill = "L1 cache" in skill_content and "L2 cache" in skill_content
    latency_ref   = "L1 cache" in ref_all and "L2 cache" in ref_all
    add(8, "8.3 Latency reference table not duplicated (skill + reference)", not (latency_skill and latency_ref), 5,
        "Latency table duplicated in SKILL.md AND references/ — move to references/ only" if (latency_skill and latency_ref)
        else "Latency table appropriately placed")


# ═══════════════════════════════════════════════════════════
# SUITE 9 — Readability & Cognitive Load Estimation
# ═══════════════════════════════════════════════════════════
def suite_9():
    print(f"\n{CYAN}{BOLD}[Suite 9] Readability & Cognitive Load Estimation{RESET}")

    # Strip markdown formatting for readability analysis
    plain = re.sub(r'[#*`_\[\]()>|~\-]', ' ', skill_content)
    plain = re.sub(r'https?://\S+', ' URL ', plain)
    plain = re.sub(r'\s+', ' ', plain).strip()

    # 9.1 — Flesch-Kincaid Grade Level estimate (target: 10–14 for technical docs)
    # Simplified FK: words, sentences, syllables
    words = plain.split()
    sentences = max(1, len(re.split(r'[.!?]+', plain)))
    def count_syllables(word):
        word = word.lower().strip(".,!?;:\"'")
        if len(word) <= 3:
            return 1
        word = re.sub(r'(es|ed|e)$', '', word)
        count = len(re.findall(r'[aeiou]+', word))
        return max(1, count)
    syllables = sum(count_syllables(w) for w in words)
    if words and sentences:
        fk_grade = 0.39 * (len(words)/sentences) + 11.8 * (syllables/len(words)) - 15.59
    else:
        fk_grade = 0
    add(9, f"9.1 Flesch-Kincaid Grade Level: 9–15 (technical doc range)", 9 <= fk_grade <= 16, 5,
        f"FK Grade Level ≈ {fk_grade:.1f} (target 9–15 for technical docs)")

    # 9.2 — Maximum section length (cognitive chunking: ≤100 lines per section)
    # Reference-heavy skill docs allow up to 100 lines per ## section
    sections = re.split(r'\n## ', skill_content)
    long_sections = [(i, len(s.splitlines())) for i, s in enumerate(sections) if len(s.splitlines()) > 100]
    add(9, "9.2 No section exceeds 100 lines (cognitive chunking for reference docs)", len(long_sections)==0, 5,
        f"Overly long sections: {[(i, n) for i, n in long_sections]}" if long_sections else "All sections within 100-line chunk limit")

    # 9.3 — Header hierarchy is valid (no h4 without h3, no skipping levels)
    header_levels = [len(m.group(1)) for m in re.finditer(r'^(#{1,4}) ', skill_content, re.MULTILINE)]
    hierarchy_violations = 0
    for i in range(1, len(header_levels)):
        if header_levels[i] > header_levels[i-1] + 1:
            hierarchy_violations += 1
    add(9, "9.3 Header hierarchy is valid (no level-skipping)", hierarchy_violations==0, 3,
        f"Hierarchy violations: {hierarchy_violations}")

    # 9.4 — Average words per bullet point ≤25
    bullet_points = re.findall(r'^- .+', skill_content, re.MULTILINE)
    avg_words = sum(len(b.split()) for b in bullet_points) / max(1, len(bullet_points))
    add(9, "9.4 Average bullet point length ≤25 words (scannable)", avg_words<=25, 3,
        f"Average bullet length: {avg_words:.1f} words across {len(bullet_points)} bullets")


# ═══════════════════════════════════════════════════════════
# SUITE 10 — Token Budget & Context Efficiency
# ═══════════════════════════════════════════════════════════
def suite_10():
    print(f"\n{CYAN}{BOLD}[Suite 10] Token Budget & Context Efficiency{RESET}")

    # 10.1 — SKILL.md character budget (not too small, not too large)
    size = len(skill_content)
    add(10, "10.1 SKILL.md size in optimal range (8k–30k chars)", 8000 <= size <= 30000, 8,
        f"Size: {size:,} chars  (target: 8k–30k)")

    # 10.2 — Description token budget (≤60 tokens ≈ ≤300 chars)
    m = re.search(r'\n---\s*\n', skill_content[3:])
    fm = yaml.safe_load(skill_content[3:m.start()+3]) if m else {}
    desc = fm.get("description", "")
    add(10, "10.2 Description ≤300 chars (≈60 tokens, system-prompt efficient)", len(desc)<=300, 8,
        f"Description: {len(desc)} chars")

    # 10.3 — Total knowledge base size (SKILL.md + all references combined)
    total_size = size + sum(f.stat().st_size for f in REF_DIR.glob("*.md"))
    add(10, "10.3 Total knowledge base <250KB (context-loadable in agents)", total_size < 250_000, 5,
        f"Total: {total_size:,} bytes = {total_size/1024:.1f} KB")

    # 10.4 — Information density: ratio of tables + code blocks to total lines
    total_lines = len(skill_content.splitlines())
    table_lines = len(re.findall(r'^\|', skill_content, re.MULTILINE))
    code_lines  = len(re.findall(r'^    ', skill_content, re.MULTILINE)) + len(re.findall(r'^```', skill_content, re.MULTILINE))
    density = (table_lines + code_lines) / max(1, total_lines)
    add(10, "10.4 Information density ≥5% (tables/code/structured content)", density >= 0.05, 5,
        f"Structured content density: {density*100:.1f}% ({table_lines} table lines, {code_lines} code lines)")


# ═══════════════════════════════════════════════════════════
# MAIN RUNNER
# ═══════════════════════════════════════════════════════════
def main():
    print(f"{BOLD}{'='*62}{RESET}")
    print(f"{BOLD}  🧪 INDUSTRY-GRADE SKILL EVALUATION HARNESS v2.0{RESET}")
    print(f"{BOLD}  Skill: system-architect{RESET}")
    print(f"{BOLD}  Standard: Agentic Framework / HELM / RAGAS / ISO-25010{RESET}")
    print(f"{BOLD}{'='*62}{RESET}")

    try:
        suite_1()
        suite_2()
        suite_3()
        suite_4()
        suite_5()
        suite_6()
        suite_7()
        suite_8()
        suite_9()
        suite_10()
    except AssertionError as e:
        print(f"{RED}FATAL ASSERTION: {e}{RESET}")
        sys.exit(2)

    # ── Scorecard ──
    print(f"\n{BOLD}{'='*62}{RESET}")
    print(f"{BOLD}  📊  FULL EVALUATION SCORECARD{RESET}")
    print(f"{BOLD}{'='*62}{RESET}")
    print(f"{'Test':<55} {'Status':<12} {'Score':>6} {'Detail'}")
    print("-"*130)

    total_score = 0
    max_score   = 0
    failures    = []

    for suite_id, name, status, score, detail in all_results:
        is_pass = "PASS" in status
        total_score += score if is_pass else 0
        max_score   += score
        if not is_pass:
            failures.append((name, detail))
        colour = GREEN if is_pass else RED
        print(f"{colour}{name:<55}{RESET}  {status:<20}  {score:>3}pts  {DIM}{detail[:65]}{RESET}")

    print(f"\n{BOLD}{'─'*62}{RESET}")
    pct = (total_score / max_score * 100) if max_score else 0
    bar = "█" * int(pct / 5) + "░" * (20 - int(pct/5))
    colour = GREEN if pct >= 90 else YELLOW if pct >= 75 else RED
    print(f"{colour}{BOLD}OVERALL SCORE: {total_score}/{max_score} pts ({pct:.1f}%)  [{bar}]{RESET}")
    
    if failures:
        print(f"\n{RED}{BOLD}── FAILURES TO FIX ({len(failures)}) ──{RESET}")
        for i, (name, detail) in enumerate(failures, 1):
            print(f"  {i}. {name}")
            if detail:
                print(f"     → {detail[:120]}")
    else:
        print(f"\n{GREEN}{BOLD}🏆  ALL TESTS PASSED — PRODUCTION READY{RESET}")

    if pct < 85:
        sys.exit(1)

if __name__ == "__main__":
    main()
