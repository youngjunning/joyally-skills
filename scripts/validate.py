#!/usr/bin/env python3
"""Check the public catalog, references, CI paths, and disclosure boundaries."""
import ast
import glob
import json
from pathlib import Path
import re
import shlex
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', '.next', '__pycache__', '.venv', 'node_modules'}
PATTERNS = {
    'personal absolute path': re.compile('/' + r'Users/[^/\s]+/'),
    'internal host': re.compile(r'\b(?:[\w-]+\.)*(?:alibaba-inc|aliway|fliggy)\.com\b'),
    'credential': re.compile(r'\b(?:sk-[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9_]{30,})\b'),
    'private key': re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    'live ad account': re.compile(r'ca-pub-\d{10,}|div-gpt-ad-\d{10,}'),
    'live pixel config': re.compile(r"(?:fbq\(['\"]init['\"],\s*['\"]|Pixel\s+[`'\"]?)\d{12,}"),
}
WORKFLOW_PATH_PREFIXES = ('scripts/', 'skills/', 'tests/', 'docs/', '.github/')


def workflow_commands(path):
    """Yield (line number, shell command) pairs without requiring a YAML package."""
    lines = path.read_text().splitlines()
    index = 0
    while index < len(lines):
        match = re.match(r'^(\s*)(?:-\s+)?run:\s*(.*)$', lines[index])
        if not match:
            index += 1
            continue
        line_number = index + 1
        value = match.group(2).strip()
        if value not in {'|', '>', '|-', '>-', '|+', '>+'}:
            yield line_number, value
            index += 1
            continue
        indentation = len(match.group(1))
        command_lines = []
        index += 1
        while index < len(lines):
            line = lines[index]
            if line.strip() and len(line) - len(line.lstrip()) <= indentation:
                break
            command_lines.append(line.strip())
            index += 1
        yield line_number, ' '.join(command_lines)


def validate_workflow_paths(root):
    """Catch stale repository paths in CI commands before GitHub Actions runs them."""
    errors = []
    workflows = root / '.github/workflows'
    if not workflows.is_dir():
        return errors
    for workflow in sorted((*workflows.glob('*.yml'), *workflows.glob('*.yaml'))):
        for line_number, command in workflow_commands(workflow):
            try:
                tokens = shlex.split(command, comments=True)
            except ValueError:
                continue
            for token in tokens:
                candidate = token.split('=', 1)[-1].removeprefix('./').rstrip(';,')
                if '$' in candidate or not candidate.startswith(WORKFLOW_PATH_PREFIXES):
                    continue
                target = root / candidate
                exists = (
                    bool(glob.glob(str(target), recursive=True))
                    if glob.has_magic(candidate)
                    else target.exists()
                )
                if not exists:
                    relative_workflow = workflow.relative_to(root)
                    errors.append(
                        'workflow command path does not exist: '
                        f'{relative_workflow}:{line_number}: {candidate}'
                    )
    return errors


def validate(root=ROOT):
    errors = []
    catalog = json.loads((root / 'catalog.json').read_text())
    names, paths = set(), set()
    for item in catalog:
        name, path = item['name'], item['path']
        if name in names or path in paths:
            errors.append(f'duplicate catalog entry: {name}')
        names.add(name)
        paths.add(path)
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name):
            errors.append(f'invalid skill name: {name}')
        if path != f"skills/{item['category']}/{name}":
            errors.append(f'category/path mismatch: {path}')
        entry = root / path / 'SKILL.md'
        if not entry.is_file():
            errors.append(f'missing entry: {entry}')
            continue
        text = entry.read_text()
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
        for target in re.findall(r'\]\(([^\s)]+)\)', text):
            if target.startswith(('#', '~', '/')) or '://' in target or '<' in target:
                continue
            local = (entry.parent / unquote(target.split('#')[0])).resolve()
            if not local.exists():
                errors.append(f'broken entry link: {path}: {target}')
    found = {str(p.parent.relative_to(root)) for p in (root / 'skills').glob('*/*/SKILL.md')}
    if paths != found:
        errors.append(f'catalog differs from skill tree: {sorted(paths ^ found)}')
    readme = (root / 'README.md').read_text()
    for path in paths:
        if path + '/SKILL.md' not in readme:
            errors.append(f'missing README catalog link: {path}')
    readme_paths = set(re.findall(r'skills/[a-z0-9-]+/[a-z0-9-]+/SKILL\.md', readme))
    stale_paths = readme_paths - {path + '/SKILL.md' for path in paths}
    if stale_paths:
        errors.append(f'stale README skill links: {sorted(stale_paths)}')
    errors.extend(validate_workflow_paths(root))
    for p in root.rglob('*'):
        rel = p.relative_to(root)
        if any(part in SKIP for part in rel.parts):
            continue
        if p.is_symlink():
            errors.append(f'public source contains symlink: {rel}')
            continue
        if not p.is_file():
            continue
        if p.name == '.env' or p.name.startswith('.env.') and p.name != '.env.example':
            errors.append(f'environment file in source: {rel}')
        if '.bak' in p.name:
            errors.append(f'backup in source: {rel}')
        try:
            text = p.read_text()
        except UnicodeError:
            continue
        for label, pattern in PATTERNS.items():
            match = pattern.search(text)
            if match:
                line = text.count('\n', 0, match.start()) + 1
                errors.append(f'{label}: {rel}:{line}')
        if re.search(r'git (?:clone|submodule add) https://github\.com/[^/\s]+/[^/\s]+/tree/', text):
            errors.append(f'Git command uses a web directory URL: {rel}')
        if p.suffix == '.json':
            try:
                json.loads(text)
            except ValueError as error:
                errors.append(f'invalid JSON: {rel}: {error}')
        if p.suffix == '.py':
            try:
                ast.parse(text, filename=str(rel))
            except SyntaxError as error:
                errors.append(f'invalid Python: {rel}: {error}')
    return errors


if __name__ == '__main__':
    problems = validate()
    if problems:
        print('\n'.join(problems), file=sys.stderr)
        sys.exit(1)
    count = len(json.loads((ROOT / 'catalog.json').read_text()))
    print(
        f'Validated {count} public skills, catalog, entry links, CI paths, '
        'Python/JSON, and disclosure patterns.'
    )
