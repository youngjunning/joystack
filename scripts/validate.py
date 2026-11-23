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


def markdown_targets(text):
    inline = re.findall(r'\]\(([^\s)]+)\)', text)
    definitions = re.findall(r'^ {0,3}\[[^\]\n]+\]:\s*(<[^>\n]+>|[^\s]+)', text, re.M)
    return [target[1:-1] if target.startswith('<') and target.endswith('>') else target
            for target in inline + definitions]


def validate_skill_bundle(skill_dir):
    """Each independently mounted Skill must carry its own relative resources."""
    root = Path(skill_dir).resolve()
    errors = []
    for document in root.rglob('*.md'):
        if not document.resolve().is_relative_to(root):
            errors.append(f'outside bundled document: {document.relative_to(root)}')
            continue
        for target in markdown_targets(document.read_text()):
            if target.startswith(('#', '/', '~')) or '://' in target:
                continue
            resource = (document.parent / unquote(target.split('#')[0])).resolve()
            if not resource.is_relative_to(root):
                errors.append(f'cross-Skill relative resource: {document.relative_to(root)}: {target}; use Skill-name discovery')
            elif not resource.exists():
                errors.append(f'missing bundled resource: {document.relative_to(root)}: {target}')
    return errors


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
        metadata = re.search(r'^metadata:\s*\n((?:[ \t]+[^\n]*\n?)*)', front[1], re.M) if front else None
        metadata_text = metadata.group(1) if metadata else ''
        if not re.search(r'^  author:\s*杨俊宁\s*$', metadata_text, re.M):
            errors.append(f'missing or invalid author metadata: {path}')
        if not re.search(r'^  email:\s*luozhu2021@gmail\.com\s*$', metadata_text, re.M):
            errors.append(f'missing or invalid author email: {path}')
        errors.extend(f'{path}: {problem}' for problem in validate_skill_bundle(skill.parent))
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
        relative = path.relative_to(ROOT)
        boundary = ROOT / Path(*relative.parts[:3]) if len(relative.parts) >= 4 and relative.parts[0] == 'skills' else ROOT
        if not path.resolve().is_relative_to(boundary.resolve()):
            errors.append(f'outside public scan boundary: {relative}')
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
