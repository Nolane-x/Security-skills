# Security Skills

[![CI](https://github.com/Nolane-x/Security-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/Nolane-x/Security-skills/actions/workflows/validate.yml)

[English](README.md) · **Tiếng Việt** · [简体中文](README-CN.md)

Một **đồ thị kỹ năng bảo mật theo nguyên tắc verification-first và framework đánh giá cross-agent mang tính xác định dành cho AI agent**.

Security Skills cung cấp cho coding agent, research agent và các hệ thống bảo mật tự động một tập kỹ năng lập luận bảo mật có thể tái sử dụng và mang theo giữa nhiều host — đi kèm evidence gate, routing logic, benchmark và công cụ đánh giá cross-agent để kiểm tra chính những kỹ năng đó có được sử dụng đúng hay không.

> **Baseline ổn định: Wave 6** — 83 kỹ năng canonical, 20 pack, 36 benchmark fixture xác định và một cross-agent evaluation harness độc lập vendor.

## Vì sao dự án này tồn tại

Một security agent không nên nhảy thẳng từ cảnh báo scanner, crash, static-analysis warning hay giả thuyết của model sang kết luận “đã xác nhận lỗ hổng”. Nghiên cứu bảo mật tốt cần scope rõ ràng, bằng chứng, control, quan hệ nhân quả, khả năng tái lập và xác minh hồi quy.

Repository này biến kỷ luật đó thành một hệ thống portable và machine-readable.

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

Kết quả không chỉ là một bộ prompt. Đây là một **security intelligence system có khả năng tự kiểm tra routing của chính nó và đánh giá cách các AI agent bên ngoài tuân thủ cùng một security contract**.

## Dự án này là gì — và không phải là gì

**Security Skills là:**

- đồ thị lập luận bảo mật portable dành cho AI agent;
- tập Agent Skills tái sử dụng với applicability và evidence contract rõ ràng;
- deterministic router có hiểu prerequisite;
- research-case model và evidence-state model machine-readable;
- benchmark cho routing, authorization, evidence, false-positive control và remediation;
- harness độc lập vendor để so sánh normalized agent runs;
- framework nghiên cứu phòng thủ cho mục tiêu local, owned, sandboxed, CTF, benchmark hoặc được ủy quyền rõ ràng.

**Security Skills không phải là:**

- kho payload hay exploit;
- thứ thay thế authorization hoặc phán đoán chuyên môn của con người;
- cơ chế tuyên bố lỗ hổng chỉ từ output của tool;
- prompt pack riêng cho một vendor;
- benchmark “trí thông minh tổng quát”. Điểm cross-agent chỉ đo mức độ tuân thủ security contract đã được review của repository này.

## Snapshot hiện tại

| Năng lực | Baseline hiện tại |
| --- | ---: |
| Canonical skills | **83** |
| Validated packs | **20** |
| Benchmark fixtures | **36** |
| Benchmark categories | **6** |
| Cross-agent portability fixtures | **12** |
| Evidence states | **4** |
| CI environments | **6** |
| Python dependencies | **0 third-party packages** |

CI kiểm tra Linux, macOS và Windows trên Python 3.11 và 3.13.

## Kiến trúc ba tầng

### 1. Security intelligence graph

Mỗi capability canonical chỉ tồn tại một lần tại:

```text
skills/<skill-name>/
├── SKILL.md
└── skill.meta.json
```

`SKILL.md` tuân theo mô hình Agent Skills mở. `skill.meta.json` bổ sung metadata của đồ thị Nolane như domain, prerequisite, composition edge, maturity và evidence stage mà không làm ô nhiễm portable skill frontmatter.

Các pack trong `packs/` chỉ tham chiếu canonical skills thay vì sao chép nội dung.

### 2. Deterministic benchmark authority

Wave 5 đánh giá production case validator và router bằng các synthetic fixture đã được review. Các lỗi cứng như chấp nhận case không được ủy quyền, promote evidence sai, domain leakage hoặc phá prerequisite ordering không thể bị “trung bình hóa” bởi một tổng điểm cao.

### 3. Cross-agent evaluation

Wave 6 chuyển benchmark fixture đã review thành **oracle-free agent tasks**, nhận normalized `agent-run` artifact từ wrapper bên ngoài và chấm bằng deterministic repository code.

Core không hard-code model vendor hay proprietary CLI. Bất kỳ agent host nào cũng có thể tích hợp thông qua cùng một normalized artifact contract.

## Evidence model

Mọi investigation đi qua các trạng thái rõ ràng:

```text
hypothesis
    ↓
observed
    ↓
validated
    ↓
regression-verified
```

Một finding không được promote chỉ vì tool, fuzzer, model hay analyzer nói như vậy.

Một case ở trạng thái `validated` tối thiểu cần các dạng bằng chứng như:

- environment hoặc target revision được pin;
- observation có thể tái lập;
- causal root cause;
- bounded security consequence;
- positive và negative controls;
- reproducer steps và fixture identity.

`regression-verified` còn yêu cầu bằng chứng rằng revision đã sửa không còn tái hiện issue trong khi controls vẫn hoạt động đúng.

Xem [docs/research-case-contract.md](docs/research-case-contract.md).

## Phạm vi năng lực

Đồ thị hiện bao phủ sâu các workflow về:

- scope, authorization, research routing, attack-surface mapping và hypothesis generation;
- fuzz harness design, corpus engineering, coverage-guided, grammar-aware và stateful fuzzing;
- crash triage, minimization, sanitizer-guided analysis, root-cause analysis và exploitability triage;
- static/dataflow analysis, symbolic execution, differential testing, binary reconnaissance và variant hunting;
- memory lifetime, bounds/integer safety, type confusion và concurrency/race analysis;
- parser/protocol state machine, canonicalization, deserialization boundary và namespace confusion;
- authorization, confused deputy, cache identity, secret/token flow và tenant isolation;
- kernel, driver/IOCTL, sandbox, browser process và JIT invariant analysis;
- container, cloud IAM, supply-chain review và dependency trust;
- Android/iOS security, mobile trust boundary và local storage/keystore analysis;
- firmware, update trust chain, secure boot và embedded debug surface;
- virtualization guest-host boundary, virtual device và shared memory;
- web routing, SSRF boundary, upload, template và multi-tenant internals;
- cryptographic protocol misuse, randomness lifecycle, certificate và hostname validation;
- smart-contract invariant, reentrancy, upgradeability và oracle trust;
- prompt-injection boundary, tool confirmation, RAG/memory isolation, connector/plugin trust;
- controlled experiment, evidence ledger, false-positive elimination, static/dynamic correlation, remediation, regression validation và reporting.

## Bắt đầu nhanh

Clone repository và chạy toàn bộ deterministic validation stack:

```bash
git clone https://github.com/Nolane-x/Security-skills.git
cd Security-skills

python scripts/validate_skills.py
python scripts/validate_graph.py
python scripts/validate_benchmarks.py
python -m unittest discover -s tests -v
```

Sinh human/machine indexes khi cần:

```bash
python scripts/build_catalog.py
python scripts/build_graph.py
```

Các artifact catalog/graph được sinh ra cố ý không commit. Nguồn sự thật canonical vẫn là `SKILL.md`, `skill.meta.json` và pack manifest.

## Research-case engine

Validate và route một research case machine-readable:

```bash
python scripts/validate_case.py examples/research-case.example.json
python scripts/route_skills.py examples/research-case.example.json --limit 12
```

Router chỉ mang tính advisory. Nó kiểm authorization và case state trước, đóng transitive prerequisites, áp dụng domain/context filtering rồi trả về thứ tự skill mang tính xác định.

Một memory-safety route điển hình có thể là:

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

Wave 5 có 36 deterministic fixture thuộc sáu nhóm:

1. authorization;
2. domain isolation;
3. evidence-state conformance;
4. false-positive control;
5. remediation/regression routing;
6. representative routing correctness.

Chạy portability suite hoặc full core suite:

```bash
python scripts/run_benchmarks.py benchmarks/suites/portability.json
python scripts/run_benchmarks.py benchmarks/suites/core.json
```

Sinh machine report và human report:

```bash
python scripts/run_benchmarks.py benchmarks/suites/core.json \
  --json /tmp/security-skills-benchmark.json \
  --report /tmp/security-skills-benchmark.md
```

Xem [docs/benchmark-contract.md](docs/benchmark-contract.md).

## Cross-agent evaluation

Wave 6 cho phép đánh giá AI agent bên ngoài bằng cùng một security authority đã review mà không làm lộ fixture oracle trong task artifact.

Chuẩn bị oracle-free tasks:

```bash
python scripts/prepare_agent_tasks.py benchmarks/suites/portability.json --out /tmp/agent-tasks
```

Sinh deterministic reference replay profile:

```bash
python scripts/prepare_replay_runs.py benchmarks/suites/portability.json \
  --profile reference \
  --out /tmp/reference-runs
```

Validate và chấm normalized runs:

```bash
python scripts/validate_agent_runs.py /tmp/reference-runs
python scripts/evaluate_agent_runs.py benchmarks/suites/portability.json /tmp/reference-runs \
  --json /tmp/agent-evaluation.json \
  --report /tmp/agent-evaluation.md
```

Các replay profile được commit gồm:

- `reference` — baseline deterministic và conforming;
- `cautious` — hành vi `needs-evidence` an toàn nhưng cố ý chưa hoàn chỉnh;
- `faulty` — negative control xác định và bắt buộc phải fail.

Xem [agent-eval/README.md](agent-eval/README.md).

## Safe adapter boundary

External agent wrapper có thể dùng `scripts/run_agent_adapter.py` với explicit argv vector.

Adapter boundary được thiết kế phòng thủ:

- `shell=False`;
- explicit argv, không shell interpolation;
- timeout enforcement;
- streaming stdout/stderr byte caps;
- kill child process khi overflow;
- sanitize environment mặc định;
- credential-like variable chỉ được truyền qua explicit allowlist;
- untrusted agent output chỉ được parse như data;
- subprocess pipes được đóng deterministic;
- không yêu cầu hay lưu hidden reasoning / chain-of-thought.

## Portability

`skills/` là nguồn canonical duy nhất. Không fork prose của skill theo từng vendor.

Một project layout có khả năng interoperable rộng:

```text
<project>/
└── .agents/
    └── skills/
        └── <skill-name>/
            ├── SKILL.md
            └── ...optional local resources...
```

Repository được thiết kế cho các coding/agent host hiện đại hiểu Agent Skills hoặc có thể sử dụng explicit repository context. Vendor-specific discovery path có thể cùng trỏ tới canonical skill content.

Xem [docs/compatibility.md](docs/compatibility.md).

## Packs

Pack là curated routing manifest trong `packs/`. Các pack lớn gồm:

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

Xem [packs/README.md](packs/README.md) để xem toàn bộ danh sách.

## Cấu trúc repository

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

## Full validation

Không cần cài third-party Python package.

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

CI lặp lại các gate quan trọng trên Ubuntu, macOS và Windows với Python 3.11/3.13, sau đó chạy riêng deterministic `benchmark-core` và `agent-eval-core`.

## Thêm một skill mới

Đọc [CONTRIBUTING.md](CONTRIBUTING.md) trước khi thêm capability.

Một canonical skill phải mô tả một **decision process có thể tái sử dụng**, không phải wrapper mỏng quanh một lệnh tool. Nó cần có rõ:

- applicability;
- preconditions;
- workflow;
- evidence contract;
- stop conditions;
- output contract;
- graph metadata.

## Security boundary

Intrusive technique chỉ được dùng với mục tiêu local, owned, sandboxed, benchmark/CTF hoặc được ủy quyền rõ ràng.

Proof nên ưu tiên evidence có kiểm soát và không phá hoại như assertion, sanitizer report, minimized crash, synthetic resource, marker file, policy simulation và regression test thay vì persistence, stealth, destructive impact, credential theft hay indiscriminate exploitation.

Xem [SECURITY.md](SECURITY.md).

## Nguồn nghiên cứu

Security Skills tổng hợp các workflow nguyên bản từ reproducible vulnerability research, autonomous Cyber Reasoning Systems, fuzzing infrastructure, program analysis, reverse engineering, web/mobile/firmware/cloud security, smart-contract analysis và nghiên cứu AI-agent security hiện đại.

Repository **không** vendor third-party exploit code và không sao chép third-party prompt.

Xem [docs/sources.md](docs/sources.md) và [sources/research-systems.json](sources/research-systems.json).

## Tài liệu

- [English README](README.md)
- [简体中文 README](README-CN.md)
- [Compatibility](docs/compatibility.md)
- [Research-case contract](docs/research-case-contract.md)
- [Benchmark contract](docs/benchmark-contract.md)
- [Cross-agent evaluation](agent-eval/README.md)
- [Packs](packs/README.md)
- [Research sources](docs/sources.md)
- [Security policy](SECURITY.md)
- [Contributing](CONTRIBUTING.md)

---

**Security Skills** được xây dựng quanh một nguyên tắc đơn giản: **một security claim chỉ mạnh bằng chất lượng bằng chứng, controls và khả năng tái lập đứng phía sau nó.**
