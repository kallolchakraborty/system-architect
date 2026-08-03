#!/usr/bin/env python3
"""
Comprehensive Evaluation Engine for system-architect skill.
Runs 5 Eval Suites:
  Suite 1: Frontmatter & System Prompt Truncation Eval
  Suite 2: Link Integrity & Reference Coverage Eval
  Suite 3: Python Code Snippet Syntax Eval (OOD / Worked Examples)
  Suite 4: Structural Quality & Step Completion Criteria Eval
  Suite 5: Size & Context Budget Efficiency Eval
"""

import sys
import re
import ast
import pathlib
import yaml

def run_evals():
    root = pathlib.Path(__file__).parent.parent
    skill_file = root / "SKILL.md"
    readme_file = root / "README.md"
    ref_dir = root / "references"
    
    results = []
    
    print("=" * 60)
    print(" 🧪 RUNNING SKILL EVALUATION SUITE: system-architect")
    print("=" * 60)
    
    # -------------------------------------------------------------
    # SUITE 1: Frontmatter & System Prompt Truncation Eval
    # -------------------------------------------------------------
    print("\n[Suite 1] Frontmatter & System Prompt Truncation Eval")
    content = skill_file.read_text(encoding="utf-8")
    
    m = re.search(r'\n---\s*\n', content[3:])
    if not m:
        results.append(("Suite 1: YAML Delimiters", False, "Missing closing '---'"))
    else:
        fm = yaml.safe_load(content[3:m.start()+3])
        desc = fm.get("description", "")
        
        # Test 1.1: Name format
        name_ok = bool(re.match(r'^[a-z0-9-]+$', fm.get("name", ""))) and len(fm.get("name", "")) <= 64
        results.append(("Suite 1: Name Format (lowercase, hyphens <=64ch)", name_ok, f"Name: {fm.get('name')}"))
        
        # Test 1.2: Description length
        desc_len_ok = len(desc) <= 1024
        results.append(("Suite 1: Description Length <= 1024", desc_len_ok, f"Length: {len(desc)} chars"))
        
        # Test 1.3: Trigger phrase in first 57 chars
        first_57 = desc[:57]
        trigger_ok = first_57.startswith("Use when")
        results.append(("Suite 1: Trigger Phrase Front-loaded (first 57 chars)", trigger_ok, f"First 57 chars: '{first_57}'"))
        
        # Test 1.4: Required metadata fields
        meta = fm.get("metadata", {}).get("hermes", {})
        tags_ok = bool(meta.get("tags"))
        rel_ok = bool(meta.get("related_skills"))
        results.append(("Suite 1: Metadata Tags & Related Skills Present", tags_ok and rel_ok, f"Tags: {len(meta.get('tags', []))}, Related: {len(meta.get('related_skills', []))}"))

    # -------------------------------------------------------------
    # SUITE 2: Link Integrity & Reference Coverage Eval
    # -------------------------------------------------------------
    print("\n[Suite 2] Link Integrity & Reference Coverage Eval")
    ref_links = re.findall(r'`(references/[a-zA-Z0-9_-]+\.md)`', content)
    missing_refs = []
    for rl in set(ref_links):
        if not (root / rl).exists():
            missing_refs.append(rl)
            
    results.append(("Suite 2: SKILL.md Reference Links Exist", len(missing_refs) == 0, f"Missing: {missing_refs}" if missing_refs else "All links valid"))
    
    # Check all reference files in directory are linked in SKILL.md
    dir_refs = {f"references/{f.name}" for f in ref_dir.glob("*.md")}
    unlinked = dir_refs - set(ref_links)
    results.append(("Suite 2: All Directory References Linked in SKILL.md", len(unlinked) == 0, f"Unlinked: {unlinked}" if unlinked else "100% referenced"))

    # -------------------------------------------------------------
    # SUITE 3: Code Snippet Syntax Verification Eval
    # -------------------------------------------------------------
    print("\n[Suite 3] Code Snippet Syntax Verification Eval")
    code_files = [skill_file] + list(ref_dir.glob("*.md")) + [readme_file]
    syntax_errors = []
    total_python_blocks = 0
    
    for cf in code_files:
        cf_text = cf.read_text(encoding="utf-8")
        # Extract python code blocks
        py_blocks = re.findall(r'```python\n(.*?)```', cf_text, re.DOTALL)
        for idx, block in enumerate(py_blocks):
            total_python_blocks += 1
            try:
                ast.parse(block)
            except SyntaxError as se:
                syntax_errors.append(f"{cf.name} block #{idx+1}: {se}")
                
    results.append(("Suite 3: Python Code Blocks Syntax Valid", len(syntax_errors) == 0, f"Validated {total_python_blocks} blocks. Errors: {syntax_errors}"))

    # -------------------------------------------------------------
    # SUITE 4: Structural Quality & Step Completion Criteria Eval
    # -------------------------------------------------------------
    print("\n[Suite 4] Structural Quality & Step Completion Criteria Eval")
    has_step1 = "Step 1" in content
    has_step2 = "Step 2" in content
    has_step3 = "Step 3" in content
    has_step4 = "Step 4" in content
    has_pitfalls = "Common Pitfalls" in content
    has_checklist = "Verification Checklist" in content
    
    steps_ok = has_step1 and has_step2 and has_step3 and has_step4 and has_pitfalls and has_checklist
    results.append(("Suite 4: Mandatory Architectural Sections Present", steps_ok, "Steps 1-4 + Pitfalls + Checklist verified"))
    
    # Check completion criteria presence
    completion_criteria_count = len(re.findall(r'Completion criterion', content, re.IGNORECASE))
    results.append(("Suite 4: Explicit Completion Criteria Defined", completion_criteria_count >= 3, f"Found {completion_criteria_count} explicit criteria"))

    # -------------------------------------------------------------
    # SUITE 5: Size & Context Budget Efficiency Eval
    # -------------------------------------------------------------
    print("\n[Suite 5] Size & Context Budget Efficiency Eval")
    total_skill_size = len(content)
    size_ok = total_skill_size <= 100000 and total_skill_size >= 5000
    results.append(("Suite 5: SKILL.md Character Budget (5k - 100k chars)", size_ok, f"Size: {total_skill_size:,} chars"))

    # -------------------------------------------------------------
    # EVAL SUMMARY & SCORE CARD
    # -------------------------------------------------------------
    print("\n" + "=" * 60)
    print(" 📊 EVALUATION SUMMARY SCORECARD")
    print("=" * 60)
    
    passed_count = sum(1 for _, ok, _ in results if ok)
    total_count = len(results)
    score_pct = (passed_count / total_count) * 100
    
    for name, ok, details in results:
        status = "✅ PASS" if ok else "❌ FAIL"
        print(f"{status:<8} | {name:<50} | {details}")
        
    print("-" * 60)
    print(f"OVERALL EVAL SCORE: {passed_count}/{total_count} ({score_pct:.1f}%)\n")
    
    if passed_count < total_count:
        sys.exit(1)

if __name__ == "__main__":
    run_evals()
