# Security Skills

[![CI](https://github.com/Nolane-x/Security-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/Nolane-x/Security-skills/actions/workflows/validate.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

[English](README.md) · [Tiếng Việt](README-VN.md) · **简体中文**

**Security Skills** 是一个面向 AI Agent 的 **verification-first 安全技能图谱与确定性评估框架**。

它提供可移植的安全推理技能、明确的证据契约、理解 prerequisite 的确定性路由、可复现 benchmark、选择性 operator-depth 方法，以及 vendor-neutral 的 Agent 评估。目标不是更快地下漏洞结论，而是让结论**更可复现、更可审查、边界更明确，也更难被夸大**。

> **稳定基线：Wave 10 已关闭** — **83 个 canonical skills**、**20 个 packs**、**40 个由 CI 强制执行的 operator-depth profiles**、**36 个确定性 benchmark fixtures**、**12 个 portability fixtures**、**6 个 CI environments**、**0 个必需的第三方 Python packages**，采用 **Apache-2.0** 许可证。

## 为什么需要这个项目

安全 Agent 不应从 scanner alert、crash、可疑 trace、static-analysis warning 或模型假设直接跳到“已确认漏洞”。

可靠的安全研究需要一条证据链：

```text
scope + authorization
        ↓
hypothesis
        ↓
observation
        ↓
causal validation
        ↓
false-positive controls
        ↓
bounded security consequence
        ↓
remediation
        ↓
regression verification
```

Security Skills 把这种纪律转化为可移植 Agent Skills 与机器可检查的 contract。

## 当前架构

```text
                         ┌─────────────────────────────┐
                         │ 83 canonical Agent Skills   │
                         └──────────────┬──────────────┘
                                        │
                         ┌──────────────▼──────────────┐
                         │ 20 curated routing packs    │
                         └──────────────┬──────────────┘
                                        │
                 ┌──────────────────────▼──────────────────────┐
                 │ deterministic case validation + routing     │
                 └──────────────────────┬──────────────────────┘
                                        │
                 ┌──────────────────────▼──────────────────────┐
                 │ 40 selective operator-depth profiles        │
                 │ runbooks + machine-readable safe cases      │
                 └──────────────────────┬──────────────────────┘
                                        │
        ┌───────────────────────────────▼───────────────────────────────┐
        │ benchmarks · cross-agent evaluation · regression authorities │
        └───────────────────────────────────────────────────────────────┘
```

Canonical skill prose 只在 `skills/` 中存在一份。Packs、operator-depth profiles、benchmarks 与 evaluation 层引用同一 canonical authority，而不是为不同 vendor 复制内容。

## 项目提供什么

### 1. Canonical 安全推理图谱

每个 canonical capability 的结构为：

```text
skills/<skill-name>/
├── SKILL.md
├── skill.meta.json
└── references/        # 可选的更深层本地资源
```

一个 skill 编码可复用的 decision process：何时适用、prerequisite、workflow、evidence requirements、stop conditions 与 expected output。

`skill.meta.json` 增加 domain、prerequisite、composition edge、maturity 与 evidence stage 等图谱元数据。

### 2. 确定性 research routing

Research case 在路由前先验证。Router 会闭包 transitive prerequisites、应用 domain/context filtering、保持 evidence-state 约束，并返回确定性的 skill 顺序。

```bash
python scripts/validate_case.py examples/research-case.example.json
python scripts/route_skills.py examples/research-case.example.json --limit 12
```

Routing 仅提供 advisory 结果。Authorization 与 evidence requirements 仍然具有 authority。

### 3. Evidence-state 模型

Security claim 按明确状态推进：

```text
hypothesis
    ↓
observed
    ↓
validated
    ↓
regression-verified
```

单个工具结果不能自动升级 finding。

一个 `validated` finding 至少需要固定 target/environment、可复现 observation、causal root cause、bounded consequence、positive/negative controls 以及 reproducer identity。`regression-verified` 还要求修复 revision 不再复现问题，同时 controls 继续正常工作。

参见 [docs/research-case-contract.md](docs/research-case-contract.md)。

### 4. Operator depth

Wave 10 以 **40 个 CI-enforced operator-depth profiles** 正式关闭。

Operator depth 是选择性的：并非每个 canonical skill 都需要大型 runbook。只有当更深的 causal methodology 能显著提升可靠性时，才注册 profile。

每个已注册 profile 组合：

- 已审查的 operator runbook；
- machine-readable synthetic/controlled scenarios 或 review cases；
- 明确的 safe oracle；
- evidence ladder；
- counterfactual 与 false-positive controls；
- stop conditions；
- remediation 与 regression checks；
- 专用 deterministic tests。

覆盖范围包括 authorization/identity、parser/protocol boundaries、memory/runtime、sandbox/browser/driver、firmware/virtualization、crypto/external-data trust、AI-agent security、web internals，以及 smart-contract invariant/reentrancy/upgradeability。

参见 [docs/operator-depth-contract.md](docs/operator-depth-contract.md)、[operator-depth/profiles.json](operator-depth/profiles.json) 与 [Wave 10 closure audit](docs/wave10-closure-audit.md)。

### 5. Deterministic benchmarks

Wave 5 建立 **36 个 deterministic fixtures**，分为六类：

1. authorization；
2. domain isolation；
3. evidence-state conformance；
4. false-positive control；
5. remediation/regression routing；
6. representative routing correctness。

```bash
python scripts/validate_benchmarks.py
python scripts/run_benchmarks.py benchmarks/suites/portability.json
python scripts/run_benchmarks.py benchmarks/suites/core.json
```

未授权 case 被接受、evidence-state 被破坏或 domain leakage 等硬错误，不能被高平均分掩盖。

参见 [docs/benchmark-contract.md](docs/benchmark-contract.md)。

### 6. Cross-agent evaluation

Evaluation 层把已审查 benchmark fixtures 转换成不包含 oracle 的 task，并使用 repository 内确定性代码评分 normalized `agent-run` artifacts。

Core 不 hard-code model vendor 或 proprietary CLI。外部 Agent host 通过统一 artifact contract 接入。

```bash
python scripts/prepare_agent_tasks.py benchmarks/suites/portability.json --out /tmp/agent-tasks
python scripts/prepare_replay_runs.py benchmarks/suites/portability.json --profile reference --out /tmp/reference-runs
python scripts/validate_agent_runs.py /tmp/reference-runs
python scripts/evaluate_agent_runs.py benchmarks/suites/portability.json /tmp/reference-runs
```

Repository 内置一个 conforming reference baseline 与 deterministic negative controls。

参见 [agent-eval/README.md](agent-eval/README.md)。

### 7. 受控 comparative regression

Repository 还包含一个 deterministic “superiority-court” harness，用于受控内部 contestant view 的 regression test。它是 engineering test authority，**不是外部模型排行榜，也不是通用 superiority 的证据**。

任何与其他系统的实证比较都需要匹配 task、受控条件、明确限制以及直接证据。

## Security coverage

Canonical graph 深入覆盖：

- scope、authorization、attack-surface mapping 与 hypothesis generation；
- fuzz harness、corpus、coverage-guided、grammar-aware 与 stateful fuzzing；
- crash triage、minimization、sanitizer evidence 与 exploitability triage；
- static/dataflow analysis、symbolic execution、differential testing 与 variant hunting；
- memory lifetime、bounds/integer safety、type confusion、concurrency 与 JIT invariants；
- parser/protocol state machines、canonicalization、deserialization 与 namespace confusion；
- authorization、confused deputy、cache identity、secrets/tokens 与 tenant isolation；
- kernel、driver/IOCTL、sandbox、browser process boundaries 与 virtualization；
- container、cloud IAM、supply-chain、firmware、secure boot 与 update chains；
- Android/iOS security 与 local-storage/keystore boundaries；
- web routing、server-side request boundaries、upload、template 与 multi-tenant internals；
- cryptographic protocol、randomness lifecycle、certificate 与 hostname validation；
- smart-contract invariant、reentrancy、upgradeability 与 oracle trust；
- prompt injection、RAG/memory isolation、tool confirmation、connector/plugin 与 AI-agent assessment；
- evidence ledger、false-positive elimination、remediation、regression validation 与 reporting。

## Quick start

Core validation 不需要第三方 Python package。

```bash
git clone https://github.com/Nolane-x/Security-skills.git
cd Security-skills

python scripts/validate_skills.py
python scripts/validate_operator_depth.py
python scripts/validate_graph.py
python scripts/validate_benchmarks.py
python -m unittest discover -s tests -v
```

生成并检查 index：

```bash
python scripts/build_catalog.py
python scripts/build_graph.py
python scripts/build_catalog.py --check
python scripts/build_graph.py --check
```

## Full validation

```bash
python scripts/validate_skills.py
python scripts/validate_operator_depth.py
python scripts/validate_graph.py
python scripts/build_catalog.py
python scripts/build_graph.py
python scripts/build_catalog.py --check
python scripts/build_graph.py --check
python scripts/validate_case.py examples/research-case.example.json
python scripts/route_skills.py examples/research-case.example.json --limit 12
python scripts/validate_benchmarks.py
python scripts/run_benchmarks.py benchmarks/suites/portability.json
python scripts/run_benchmarks.py benchmarks/suites/core.json
python scripts/prepare_agent_tasks.py benchmarks/suites/portability.json --out /tmp/agent-tasks
python scripts/prepare_replay_runs.py benchmarks/suites/portability.json --profile reference --out /tmp/agent-runs
python scripts/validate_agent_runs.py /tmp/agent-runs
python scripts/evaluate_agent_runs.py benchmarks/suites/portability.json /tmp/agent-runs
python -m unittest discover -s tests -v
```

CI 在 Ubuntu、macOS 与 Windows × Python 3.11/3.13 上重复关键 gate，然后运行专用 benchmark、cross-agent 与 comparative regression jobs。

## Portability

`skills/` 是 canonical source。不要为不同 vendor 复制 skill prose。

一个 host layout 可以直接指向同一内容：

```text
<project>/
└── .agents/
    └── skills/
        └── <skill-name>/
            ├── SKILL.md
            └── ...optional local resources...
```

任何理解 Agent Skills 或可以读取 explicit repository context 的 Agent host 都可以集成，而无需改变底层 security authority。

参见 [docs/compatibility.md](docs/compatibility.md)。

## Safe adapter boundary

Local adapter 采用防御性设计：

- `shell=False`；
- 显式 argv vectors；
- timeout enforcement；
- stdout/stderr byte caps；
- overflow 时终止 child；
- 默认 sanitize environment；
- credential-like variables 仅通过 explicit allowlist；
- untrusted agent output 只作为 data 解析；
- deterministic pipe cleanup；
- 不请求也不保存 hidden reasoning / chain-of-thought。

## Repository 结构

```text
Security-skills/
├── skills/              # 83 canonical Agent Skills
├── operator-depth/      # 40 selective deep profiles 的 registry
├── packs/               # 20 curated routing manifests
├── benchmarks/          # deterministic routing/evidence fixtures
├── agent-eval/          # vendor-neutral cross-agent contracts
├── superiority/         # controlled comparative regression authority
├── schemas/             # machine-readable schemas
├── scripts/             # validators, routers, evaluators, builders
├── tests/               # deterministic regression tests
├── examples/            # research-case examples
├── docs/                # contracts 与 architecture documentation
├── sources/             # research-system lineage metadata
├── AGENTS.md             # repository-level agent guidance
├── SECURITY.md           # authorization 与 responsible-use boundary
├── CONTRIBUTING.md       # contribution requirements
└── LICENSE               # Apache License 2.0
```

## Safety boundary

Intrusive techniques 仅限 local、owned、sandboxed、benchmark/CTF 或明确授权目标。

Proof 应优先使用足以证明 claim 的最小风险 evidence：assertion、sanitizer report、minimized crash、synthetic resource、marker file、policy simulation、mock service、read-only snapshot、synthetic canary 与 regression test。

参见 [SECURITY.md](SECURITY.md)。

## Wave 10 closure

Wave 10 被有意**关闭在 40 个 operator-depth profiles**。项目不把 repository size、skill count、profile count 或 line count 当作 quality metric。

后续工作默认应集中于：

- correctness 与 maintenance；
- 更强的 evidence 与 controls；
- 更安全的 oracle；
- 更好的 benchmark；
- portability；
- research-lineage 更新；
- targeted defect fixes；
- documentation 与 onboarding。

任何超出 83 / 20 / 40 baseline 的扩张都应要求真实未覆盖的 mechanism、非重复设计以及明确的 architecture decision。

参见 [docs/wave10-closure-audit.md](docs/wave10-closure-audit.md)。

## Contributing

修改 canonical skills、graph metadata、packs、operator-depth contracts、benchmarks 或 agent-evaluation authority 前，请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

强 contribution 应增加可复用 decision process 或强化已有 contract。弱 contribution 只是增加另一个 tool wrapper、payload list 或重复 prompt。

## Research lineage

Security Skills 从 reproducible vulnerability research、autonomous cyber-reasoning systems、fuzzing infrastructure、program analysis、reverse engineering、web/mobile/firmware/cloud security、smart-contract analysis 与现代 AI-agent security research 中提炼原创 workflow。

Repository **不会** vendor third-party offensive code，也不会复制 third-party prompts。

参见 [docs/sources.md](docs/sources.md) 与 [sources/research-systems.json](sources/research-systems.json)。

## Documentation

- [English README](README.md)
- [Tiếng Việt README](README-VN.md)
- [Wave 10 closure audit](docs/wave10-closure-audit.md)
- [Compatibility](docs/compatibility.md)
- [Research-case contract](docs/research-case-contract.md)
- [Operator-depth contract](docs/operator-depth-contract.md)
- [Benchmark contract](docs/benchmark-contract.md)
- [Cross-agent evaluation](agent-eval/README.md)
- [Packs](packs/README.md)
- [Research sources](docs/sources.md)
- [Security policy](SECURITY.md)
- [Contributing](CONTRIBUTING.md)

## License

采用 [Apache License 2.0](LICENSE)。

---

**Security Skills 遵循一个原则：一个 security claim 的可信度，不会超过支撑它的 evidence、controls 与可复现性。**
