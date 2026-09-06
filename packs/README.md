# Skill Packs

Packs are routing manifests, not copied prompt bundles. A pack references canonical skills under `skills/`, declares routing `domains`, one entrypoint, and an opinionated default flow.

Agents should start with the pack entrypoint when the domain is clear, then follow evidence rather than blindly executing every step. Pack domains are routing constraints used to prevent unrelated packs from surfacing merely because they share a generic primitive. `default_flow` is a common path, not a mandatory pipeline. A skill may appear in several packs because primitives such as authorization, validation, lifetime, and canonicalization cross domain boundaries.

Validate pack references and graph topology with:

```bash
python scripts/validate_graph.py
python scripts/build_graph.py
python scripts/build_graph.py --check
```
