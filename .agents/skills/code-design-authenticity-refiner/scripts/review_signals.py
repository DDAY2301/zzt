#!/usr/bin/env python3
"""Read-only static review signals, NOT an AI origin detector.

Outputs rule/filename/line only to avoid leaking secrets or source code.
Never modifies scanned files. Review each hit manually.
"""
import argparse
import json
from pathlib import Path
import re
from collections import Counter
import os

EXTENSIONS = {'.html', '.htm', '.js', '.jsx', '.ts', '.tsx', '.css', '.scss', '.vue', '.svelte', '.md', '.json'}
EXCLUDED = {'.git', 'node_modules', 'dist', 'build', '.next', '.nuxt', 'coverage', '.venv', 'venv', '__pycache__'}
RULES = {
    'placeholder-copy': re.compile(r'\b(?:lorem ipsum|your (?:headline|tagline|company name) here|insert (?:text|image|copy) here)\b', re.I),
    'dummy-link': re.compile(r'\bhref\s*=\s*[\"\']\s*#\s*[\"\']', re.I),
    'stub-implementation': re.compile(r'\b(?:TODO|FIXME)\b\s*[:\-]', re.I),
    'empty-handler': re.compile(r'(?:onClick|onSubmit)\s*=\s*\{\s*\(\s*\)\s*=>\s*\{\s*\}\s*\}', re.I),
}

def scan(root: Path, max_size: int = 400_000, limit: int = 500):
    findings = []
    files = 0
    # Prune dependency directories *before* traversing their contents.
    for current, dirs, names in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in EXCLUDED and not (Path(current) / d).is_symlink())
        for filename in sorted(names):
            path = Path(current) / filename
            if path.suffix.lower() not in EXTENSIONS or path.is_symlink():
                continue
            try:
                if path.stat().st_size > max_size:
                    continue
                content = path.read_text(encoding='utf-8', errors='replace')
            except OSError:
                continue
            files += 1
            for lineno, line in enumerate(content.splitlines(), 1):
                for name, regex in RULES.items():
                    if regex.search(line):
                        findings.append({'rule': name, 'file': str(path.relative_to(root)), 'line': lineno})
                        if len(findings) >= limit:
                            return {'files_scanned': files, 'truncated': True, 'findings': findings}
    return {'files_scanned': files, 'truncated': False, 'findings': findings}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', nargs='?', default='.')
    parser.add_argument('--format', choices=('json','text'), default='text')
    parser.add_argument('--limit', type=int, default=500)
    args = parser.parse_args()
    path = Path(args.path).resolve()
    if not path.is_dir():
        parser.error('Path must be an existing directory')
    result = scan(path, limit=max(1, args.limit))
    if args.format == 'json':
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        counts = Counter(f['rule'] for f in result['findings'])
        print(f"Reviewed {result['files_scanned']} files; {len(result['findings'])} possible review signals; truncated={result['truncated']}")
        for name, count in counts.most_common(): print(f'  {name}: {count}')
        for f in result['findings'][:50]: print(f"  {f['file']}:{f['line']}  {f['rule']}")
        print('Review hints only: no AI-origin or design-quality inference.')

if __name__ == '__main__':
    main()
