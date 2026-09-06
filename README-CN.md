# Security Skills

[![CI](https://github.com/Nolane-x/Security-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/Nolane-x/Security-skills/actions/workflows/validate.yml)

[English](README.md) · [Tiếng Việt](README-VN.md) · **简体中文**

一个面向 AI Agent 的**验证优先（verification-first）安全技能图谱与确定性跨 Agent 评估框架**。

Security Skills 为 coding agent、research agent 和自动化安全系统提供可复用、可移植的安全推理技能，同时提供证据门禁、路由逻辑、基准测试和跨 Agent 一致性评估工具，用于验证这些技能是否被正确使用。

> **稳定基线：Wave 6** — 83 个 canonical skills、20 个 packs、36 个确定性 benchmark fixtures，以及一个 vendor-neutral 的 cross-agent evaluation harness。

## 为什么要做这个项目

安全 Agent 不应该从 scanner alert、crash、static-analysis warning 或模型假设直接跳到“已确认漏洞”。高质量安全研究需要明确授权范围、证据、对照、因果关系、可复现性以及修复后的回归验证。

本仓库把这些原则变成一个可移植、机器可读的系统。

```text
security knowledge
      │
      ▼
83 canonical Agent Skills
      │
      ▼
deterministic research router
      │
      ▼
evidence-state machine
      │
      ▼
Wave 5 benchmark authority
      │
      ▼
Wave 6 cross-agent evaluator
```

因此，它并不是一个简单的 prompt 集合，而是一个**能够验证自身路由逻辑，并评估外部 AI Agent 是否遵守同一安全契约的 security intelligence system**。

## 它是什么 — 以及不是什么

**Security Skills 是：**

- 面向 AI Agent 的可移植安全推理图谱；
- 带有明确 applicability 和 evidence contract 的可复用 Agent Skills；
- 理解 prerequisite 的 deterministic router；
- machine-readable 的 research-case 与 evidence-state 模型；
- 覆盖 routing、authorization、evidence、false-positive control 和 remediation 的 benchmark；
- 用于比较 normalized agent runs 的 vendor-neutral harness；
- 面向 local、owned、sandboxed、CTF、benchmark 或明确授权目标的防御性研究框架。

**Security Skills 不是：**

- payload 或 exploit 仓库；
- authorization 或人工安全判断的替代品；
- 仅凭工具输出就宣称漏洞成立的机制；
- 某一家 vendor 的专用 prompt pack；
- “通用智能”排行榜。Cross-agent 分数只衡量 Agent 对本仓库已审查安全契约的遵循程度。

## 当前快照

| 能力 | 当前基线 |
| --- | ---: |
| Canonical skills | **83** |
| Validated packs | **20** |
| Benchmark fixtures | **36** |
| Benchmark categories | **6** |
| Cross-agent portability fixtures | **12** |
| Evidence states | **4** |
| CI environments | **6** |
| Python dependencies | **0 third-party packages** |

CI 在 Python 3.11 与 3.13 上覆盖 Linux、macOS 和 Windows。

## 三层架构

### 1. Security intelligence graph

每个 canonical capability 只在一个位置存在：

```text
skills/<skill-name>/
├── SKILL.md
└── skill.meta.json
```

`SKILL.md` 遵循开放的 Agent Skills 模型。`skill.meta.json` 增加 Nolane 图谱元数据，例如 domain、prerequisite、composition edge、maturity 和 evidence stage，而不会污染可移植的 skill frontmatter。

`packs/` 中的 pack 引用 canonical skills，而不是复制它们。

### 2. Deterministic benchmark authority

Wave 5 使用已审查的 synthetic fixtures 对 production case validator 和 router 进行评估。未授权 case 被接受、错误 evidence promotion、domain leakage 或 prerequisite ordering 被破坏等硬错误，不能被高平均分掩盖。

### 3. Cross-agent evaluation

Wave 6 将已审查 benchmark fixture 转换为**不包含 oracle 的 agent tasks**，接受外部 wrapper 提交的 normalized `agent-run` artifact，再由仓库内的确定性代码评分。

Core 不 hard-code model vendor 或 proprietary CLI。任何 agent host 都可以通过统一的 normalized artifact contract 接入。

## Evidence model

每项研究都通过明确状态推进：

```text
hypothesis
    ↓
observed
    ↓
validated
    ↓
regression-verified
```

Finding 不会因为 tool、fuzzer、model 或 analyzer 给出结果就自动升级状态。

一个 `validated` case 至少需要以下类型的证据：

- 固定的 environment 或 target revision；
- 可复现 observation；
- causal root cause；
- bounded security consequence；
- positive 与 negative controls；
- reproducer steps 与 fixture identity。

`regression-verified` 还要求证明修复 revision 不再复现问题，同时 controls 仍保持正常。

参见 [docs/research-case-contract.md](docs/research-case-contract.md)。

## 能力覆盖范围

当前图谱深入覆盖：

- scope、authorization、research routing、attack-surface mapping 与 hypothesis generation；
- fuzz harness design、corpus engineering、coverage-guided、grammar-aware 与 stateful fuzzing；
- crash triage、minimization、sanitizer-guided analysis、root-cause analysis 与 exploitability triage；
- static/dataflow analysis、symbolic execution、differential testing、binary reconnaissance 与 variant hunting；
- memory lifetime、bounds/integer safety、type confusion 与 concurrency/race analysis；
- parser/protocol state machine、canonicalization、deserialization boundary 与 namespace confusion；
- authorization、confused deputy、cache identity、secret/token flow 与 tenant isolation；
- kernel、driver/IOCTL、sandbox、browser process 与 JIT invariant analysis；
- container、cloud IAM、supply-chain review 与 dependency trust；
- Android/iOS security、mobile trust boundary 与 local storage/keystore analysis；
- firmware、update trust chain、secure boot 与 embedded debug surface；
- virtualization guest-host boundary、virtual device 与 shared memory；
- web routing、SSRF boundary、upload、template 与 multi-tenant internals；
- cryptographic protocol misuse、randomness lifecycle、certificate 与 hostname validation；
- smart-contract invariant、reentrancy、upgradeability 与 oracle trust；
- prompt-injection boundary、tool confirmation、RAG/memory isolation、connector/plugin trust；
- controlled experiment、evidence ledger、false-positive elimination、static/dynamic correlation、remediation、regression validation 与 reporting。

## 快速开始

Clone 仓库并运行完整 deterministic validation stack：

```bash
git clone https://github.com/Nolane-x/Security-skills.git
cd Security-skills

python scripts/validate_skills.py
python scripts/validate_graph.py
python scripts/validate_benchmarks.py
python -m unittest discover -s tests -v
```

按需生成 human/machine indexes：

```bash
python scripts/build_catalog.py
python scripts/build_graph.py
```

生成的 catalog/graph artifacts 被故意忽略。Canonical truth 仍然只存在于 `SKILL.md`、`skill.meta.json` 与 pack manifests 中。

## Research-case engine

验证并路由一个 machine-readable research case：

```bash
python scripts/validate_case.py examples/research-case.example.json
python scripts/route_skills.py examples/research-case.example.json --limit 12
```

Router 仅提供 advisory 结果。它首先验证 authorization 与 case state，闭包 transitive prerequisites，执行 domain/context filtering，然后返回确定性的 skill 顺序。

一个典型 memory-safety route 可能是：

```text
scope + authorization
  → attack surface
  → fuzzing
  → crash minimization
  → sanitizer evidence
  → lifetime / bounds / type / race analysis
  → evidence validation
  → conservative exploitability triage
  → variant hunt
  → remediation
  → regression verification
```

## Benchmark engine

Wave 5 包含 36 个 deterministic fixtures，分为六类：

1. authorization；
2. domain isolation；
3. evidence-state conformance；
4. false-positive control；
5. remediation/regression routing；
6. representative routing correctness。

运行 portability suite 或 full core suite：

```bash
python scripts/run_benchmarks.py benchmarks/suites/portability.json
python scripts/run_benchmarks.py benchmarks/suites/core.json
```

生成 machine 与 human reports：

```bash
python scripts/run_benchmarks.py benchmarks/suites/core.json \
  --json /tmp/security-skills-benchmark.json \
  --report /tmp/security-skills-benchmark.md
```

参见 [docs/benchmark-contract.md](docs/benchmark-contract.md)。

## Cross-agent evaluation

Wave 6 可以使用同一套已审查 security authority 评估外部 AI Agent，同时不会在 task artifact 中泄露 fixture oracle。

准备 oracle-free tasks：

```bash
python scripts/prepare_agent_tasks.py benchmarks/suites/portability.json --out /tmp/agent-tasks
```

生成 deterministic reference replay profile：

```bash
python scripts/prepare_replay_runs.py benchmarks/suites/portability.json \
  --profile reference \
  --out /tmp/reference-runs
```

验证并评分 normalized runs：

```bash
python scripts/validate_agent_runs.py /tmp/reference-runs
python scripts/evaluate_agent_runs.py benchmarks/suites/portability.json /tmp/reference-runs \
  --json /tmp/agent-evaluation.json \
  --report /tmp/agent-evaluation.md
```

仓库内置 replay profiles：

- `reference` — conforming deterministic baseline；
- `cautious` — 安全但故意不完整的 `needs-evidence` 行为；
- `faulty` — 必须失败的 deterministic negative controls。

参见 [agent-eval/README.md](agent-eval/README.md)。

## 安全的 adapter boundary

外部 agent wrapper 可以通过显式 argv vector 使用 `scripts/run_agent_adapter.py`。

Adapter boundary 采用防御性设计：

- `shell=False`；
- 显式 argv，不进行 shell interpolation；
- timeout enforcement；
- streaming stdout/stderr byte caps；
- overflow 时终止 child process；
- 默认 sanitize environment；
- credential-like variable 只能通过 explicit allowlist 转发；
- untrusted agent output 只作为 data 解析；
- subprocess pipes 确定性关闭；
- 不请求也不保存 hidden reasoning / chain-of-thought。

## Portability

`skills/` 是唯一 canonical source。不要为不同 vendor 复制 skill prose。

一个具有广泛互操作性的 project layout：

```text
<project>/
└── .agents/
    └── skills/
        └── <skill-name>/
            ├── SKILL.md
            └── ...optional local resources...
```

仓库面向支持 Agent Skills 或能够显式消费 repository context 的现代 coding/agent host。Vendor-specific discovery path 可以共同指向同一 canonical skill content。

参见 [docs/compatibility.md](docs/compatibility.md)。

## Packs

Pack 是 `packs/` 下的 curated routing manifests。主要 pack 包括：

- `fuzzing-research`
- `memory-safety`
- `parsers-and-protocols`
- `trust-and-authorization`
- `kernel-sandbox-browser`
- `cloud-and-supply-chain`
- `verification-engineering`
- `mobile-security`
- `firmware-and-boot`
- `virtualization-boundaries`
- `web-framework-internals`
- `cryptographic-assurance`
- `smart-contracts`
- `ai-agent-deep-security`
- `autonomous-research-orchestration`

完整列表参见 [packs/README.md](packs/README.md)。

## Repository 结构

```text
Security-skills/
├── skills/              # canonical Agent Skills
├── packs/               # curated skill routing manifests
├── benchmarks/          # Wave 5 deterministic fixtures and suites
├── agent-eval/          # Wave 6 cross-agent contracts and suites
├── schemas/             # machine-readable schemas
├── scripts/             # validators, routers, evaluators, builders
├── tests/               # deterministic regression tests
├── examples/            # research-case examples
├── docs/                # contracts, compatibility, design documentation
├── sources/             # research-system lineage metadata
├── AGENTS.md             # repository-level agent guidance
├── SECURITY.md           # safety and authorization boundary
└── CONTRIBUTING.md       # contribution requirements
```

## 完整验证

无需安装 third-party Python package。

```bash
python scripts/validate_skills.py
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

CI 会在 Ubuntu、macOS、Windows × Python 3.11/3.13 上重复关键 gate，然后运行专用 deterministic `benchmark-core` 与 `agent-eval-core` jobs。

## 添加新 skill

添加 capability 前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

Canonical skill 应编码一个可复用的**决策过程**，而不是对某个 tool command 的薄封装。它需要明确描述：

- applicability；
- preconditions；
- workflow；
- evidence contract；
- stop conditions；
- output contract；
- graph metadata。

## Security boundary

Intrusive technique 仅限 local、owned、sandboxed、benchmark/CTF 或明确授权的目标。

Proof 应优先使用可控、非破坏性证据，例如 assertion、sanitizer report、minimized crash、synthetic resource、marker file、policy simulation 与 regression test，而不是 persistence、stealth、destructive impact、credential theft 或 indiscriminate exploitation。

参见 [SECURITY.md](SECURITY.md)。

## 研究来源

Security Skills 从 reproducible vulnerability research、autonomous Cyber Reasoning Systems、fuzzing infrastructure、program analysis、reverse engineering、web/mobile/firmware/cloud security、smart-contract analysis 和现代 AI-agent security research 中提炼原创 workflow。

本仓库**不会** vendor third-party exploit code，也不会复制第三方 prompt。

参见 [docs/sources.md](docs/sources.md) 与 [sources/research-systems.json](sources/research-systems.json)。

## 文档

- [English README](README.md)
- [Tiếng Việt README](README-VN.md)
- [Compatibility](docs/compatibility.md)
- [Research-case contract](docs/research-case-contract.md)
- [Benchmark contract](docs/benchmark-contract.md)
- [Cross-agent evaluation](agent-eval/README.md)
- [Packs](packs/README.md)
- [Research sources](docs/sources.md)
- [Security policy](SECURITY.md)
- [Contributing](CONTRIBUTING.md)

---

**Security Skills** 遵循一个简单原则：**一个安全结论的可信度，不会超过支撑它的证据、对照和可复现性。**
