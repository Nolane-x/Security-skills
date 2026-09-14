from __future__ import annotations

"""Build a deterministic oracle-free Security Skills contestant surface."""

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

INCLUDED_DIRS = (
    'skills',
    'packs',
    'operator-depth',
)
INCLUDED_FILES = (
    'AGENTS.md',
    'SECURITY.md',
    'scripts/research_case.py',
    'scripts/route_skills.py',
    'scripts/security_graph.py',
    'scripts/skilllib.py',
    'scripts/validate_case.py',
)
FORBIDDEN_TOKENS = (
    'private_expected',
    'superiority-core-corpus',
)


def _stable_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + '\n'


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _ensure_empty_destination(out_dir: Path) -> None:
    if out_dir.exists():
        if not out_dir.is_dir():
            raise ValueError(f'contestant view destination is not a directory: {out_dir}')
        if any(out_dir.iterdir()):
            raise ValueError(f'contestant view destination must be empty: {out_dir}')
    else:
        out_dir.mkdir(parents=True)


def _copy_file(root: Path, out_dir: Path, relative: str) -> None:
    source = root / relative
    if not source.is_file():
        raise ValueError(f'missing contestant-view file: {relative}')
    target = out_dir / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)


def _copy_dir(root: Path, out_dir: Path, relative: str) -> None:
    source = root / relative
    if not source.is_dir():
        raise ValueError(f'missing contestant-view directory: {relative}')
    target = out_dir / relative
    for path in sorted(source.rglob('*')):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        destination = out_dir / rel
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, destination)


def _audit_and_manifest(out_dir: Path) -> dict:
    entries = []
    for path in sorted(p for p in out_dir.rglob('*') if p.is_file()):
        relative = path.relative_to(out_dir).as_posix()
        data = path.read_bytes()
        try:
            text = data.decode('utf-8')
        except UnicodeDecodeError as exc:
            raise ValueError(f'contestant view contains non-UTF-8 file: {relative}') from exc
        for token in FORBIDDEN_TOKENS:
            if token in text:
                raise ValueError(f'contestant view leaks judge authority token {token!r}: {relative}')
        entries.append({'path': relative, 'sha256': _sha256_bytes(data)})

    surface_digest = _sha256_bytes(
        json.dumps(entries, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
    )
    return {
        'schema_version': 1,
        'kind': 'security-skills-contestant-view',
        'file_count': len(entries),
        'surface_digest': surface_digest,
        'files': entries,
    }


def build_contestant_view(root: Path, out_dir: Path) -> dict:
    root = Path(root).resolve()
    out_dir = Path(out_dir).resolve()
    if out_dir == root or root in out_dir.parents:
        raise ValueError('contestant view destination must be outside the source repository')

    _ensure_empty_destination(out_dir)
    for relative in INCLUDED_DIRS:
        _copy_dir(root, out_dir, relative)
    for relative in INCLUDED_FILES:
        _copy_file(root, out_dir, relative)

    manifest = _audit_and_manifest(out_dir)
    (out_dir / 'CONTESTANT_VIEW.json').write_text(_stable_json(manifest), encoding='utf-8')
    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description='Build a deterministic Security Skills contestant view without judge/oracle files.'
    )
    parser.add_argument('--out', required=True)
    args = parser.parse_args(argv)
    try:
        manifest = build_contestant_view(ROOT, Path(args.out))
    except (OSError, ValueError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2
    print(
        f"Built contestant view with {manifest['file_count']} file(s); "
        f"surface digest {manifest['surface_digest']}."
    )
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
