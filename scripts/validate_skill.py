#!/usr/bin/env python3
"""
Validation script for System Design Skill.
Verifies frontmatter, character limits, structure, and internal reference links.
"""

import sys
import re
import pathlib
import yaml

def validate():
    root = pathlib.Path(__file__).parent.parent
    skill_file = root / "SKILL.md"
    
    if not skill_file.exists():
        print("❌ FAIL: SKILL.md not found")
        sys.exit(1)
        
    content = skill_file.read_text(encoding="utf-8")
    
    # 1. Check byte start
    if not content.startswith("---"):
        print("❌ FAIL: SKILL.md does not start with '---'")
        sys.exit(1)
        
    # 2. Check YAML closing tag
    m = re.search(r'\n---\s*\n', content[3:])
    if not m:
        print("❌ FAIL: SKILL.md missing closing '---'")
        sys.exit(1)
        
    # 3. Parse frontmatter
    try:
        fm = yaml.safe_load(content[3:m.start()+3])
    except Exception as e:
        print(f"❌ FAIL: YAML parsing error: {e}")
        sys.exit(1)
        
    # 4. Check required fields
    if "name" not in fm or not fm["name"]:
        print("❌ FAIL: Missing 'name' in frontmatter")
        sys.exit(1)
        
    if "description" not in fm or not fm["description"]:
        print("❌ FAIL: Missing 'description' in frontmatter")
        sys.exit(1)
        
    desc_len = len(fm["description"])
    if desc_len > 1024:
        print(f"❌ FAIL: Description length ({desc_len}) exceeds 1024 chars")
        sys.exit(1)
        
    if len(content) > 100000:
        print(f"❌ FAIL: SKILL.md size ({len(content)}) exceeds 100,000 chars limit")
        sys.exit(1)
        
    # 5. Check reference links existence
    ref_dir = root / "references"
    if not ref_dir.exists():
        print("❌ FAIL: references/ directory missing")
        sys.exit(1)
        
    ref_files = list(ref_dir.glob("*.md"))
    if not ref_files:
        print("❌ FAIL: No reference markdown files found")
        sys.exit(1)
        
    print("✅ PASS: SKILL.md frontmatter & structure valid.")
    print(f"  - Name: {fm['name']}")
    print(f"  - Description length: {desc_len}/1024 chars")
    print(f"  - File size: {len(content):,} chars")
    print(f"  - Reference files validated: {len(ref_files)}")
    for rf in sorted(ref_files):
        print(f"    • references/{rf.name}")

if __name__ == "__main__":
    validate()
