# Skill packs

Packs are thin routing manifests over canonical skills. They do not duplicate `SKILL.md` bodies.

Each `packs/*.json` file declares:

- `entrypoint` - the most useful first capability for that pack;
- `skills` - the complete canonical skill set exposed by the pack;
- `default_flow` - an evidence-aware suggested route, not an unconditional execution chain.

Validate packs and dependency references with:

```bash
python scripts/validate_graph.py
python scripts/build_graph.py
python scripts/build_graph.py --check
```
