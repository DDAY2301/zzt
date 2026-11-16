#!/usr/bin/env python3
"""Dependency-free structural checks for the SKILL.md package."""
import argparse
import re
import sys
from pathlib import Path

def check(root: Path):
    errors = []
    skill = root/'SKILL.md'
    if not skill.is_file(): return ['Missing SKILL.md']
    body = skill.read_text(encoding='utf-8')
    match = re.match(r'^---\n(.*?)\n---\n', body, re.S)
    if not match: return ['YAML frontmatter missing or malformed']
    front = match.group(1)
    name = re.search(r'^name:\s*(\S+)\s*$', front, re.M)
    description = re.search(r'^description:\s*(.+)$', front, re.M)
    if not name: errors.append('Missing name')
    else:
        val = name.group(1)
        if len(val) > 64 or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', val): errors.append('Invalid name syntax')
        if val != root.name: errors.append('Directory and frontmatter names differ')
    if not description or len(description.group(1).strip()) < 40: errors.append('Description absent or not sufficiently specific')
    for heading in ('Objective','When to activate','Negative triggers','Procedure','Output contract','Error and conflict handling','Examples'):
        if heading.lower() not in body.lower(): errors.append(f'Missing heading: {heading}')
    for ref in re.findall(r'`((?:references|scripts)/[^`]+)`', body):
        if not (root/ref).is_file(): errors.append(f'Broken local reference: {ref}')
    if len(body) > 40000: errors.append('Skill exceeds recommended compact size; move detail to references')
    return errors

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('skill_dir', nargs='?', default=str(Path(__file__).resolve().parents[1]))
    args = parser.parse_args()
    root = Path(args.skill_dir)
    errors = check(root)
    if errors:
        print('FAIL:', '\n'.join(errors)); sys.exit(1)
    print('PASS: SKILL.md structure, references and metadata validated')
