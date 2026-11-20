#!/usr/bin/env python3
"""Validate the JoyStack catalog, module metadata, links, and public boundary."""
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', '__pycache__', 'node_modules', '.next'}
PRIVATE = re.compile(r'/(?:Users|home)/[^/\s]+/|\b(?:[\w-]+\.)*(?:alibaba-inc|aliway|fliggy)\.com\b')


def validate():
    errors = []
    catalog = json.loads((ROOT / 'catalog.json').read_text())
    names, paths = set(), set()
    for item in catalog:
        name, path = item['name'], item['path']
        if name in names or path in paths:
            errors.append(f'duplicate catalog entry: {name}')
        names.add(name)
        paths.add(path)
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name):
            errors.append(f'invalid name: {name}')
        if path != f"skills/{item['category']}/{name}":
            errors.append(f'category/path mismatch: {path}')
        skill = ROOT / path / 'SKILL.md'
        if not skill.is_file():
            errors.append(f'missing skill: {path}')
            continue
        text = skill.read_text()
        front = re.match(r'\A---\n(.*?)\n---\n', text, re.S)
        if not front or not re.search(r'^name:\s*' + re.escape(name) + r'\s*$', front[1], re.M):
            errors.append(f'frontmatter name mismatch: {path}')
        if not front or not re.search(r'^description:\s*\S', front[1], re.M):
            errors.append(f'missing description: {path}')
        for target in re.findall(r'\]\(([^\s)]+)\)', text):
            if target.startswith(('#', '/', '~')) or '://' in target:
                continue
            if not (skill.parent / unquote(target.split('#')[0])).resolve().exists():
                errors.append(f'broken link: {path}: {target}')
    found = {str(path.parent.relative_to(ROOT)) for path in (ROOT / 'skills').glob('*/*/SKILL.md')}
    if found != paths:
        errors.append(f'catalog mismatch: {sorted(found ^ paths)}')
    readme = (ROOT / 'README.md').read_text()
    for path in paths:
        if path + '/SKILL.md' not in readme:
            errors.append(f'README missing: {path}')
    for path in ROOT.rglob('*'):
        if any(part in SKIP for part in path.relative_to(ROOT).parts) or not path.is_file():
            continue
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            continue
        if PRIVATE.search(text):
            errors.append(f'private reference: {path.relative_to(ROOT)}')
    return errors


if __name__ == '__main__':
    problems = validate()
    if problems:
        print('\n'.join(problems), file=sys.stderr)
        sys.exit(1)
    print('Validated JoyStack modules, catalog, links, and public boundary.')
