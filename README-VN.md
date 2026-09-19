# Security Skills

[![CI](https://github.com/Nolane-x/Security-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/Nolane-x/Security-skills/actions/workflows/validate.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

[English](README.md) · **Tiếng Việt** · [简体中文](README-CN.md)

**Security Skills** là đồ thị kỹ năng bảo mật theo hướng **verification-first** cùng framework đánh giá xác định dành cho AI agent.

Repository cung cấp các kỹ năng suy luận bảo mật có thể mang sang nhiều agent host, hợp đồng bằng chứng rõ ràng, router hiểu prerequisite, benchmark tái lập được, operator-depth có chọn lọc và hệ thống đánh giá agent độc lập vendor. Mục tiêu không phải kết luận lỗ hổng nhanh hơn, mà là làm cho kết luận **dễ kiểm chứng hơn, có giới hạn rõ hơn, tái lập được và khó bị thổi phồng hơn**.

> **Baseline ổn định: Wave 10 đã đóng** — **83 canonical skills**, **20 packs**, **40 operator-depth profiles được CI bắt buộc**, **36 benchmark fixtures xác định**, **12 portability fixtures**, **6 môi trường CI**, **0 Python package bên thứ ba bắt buộc**, giấy phép **Apache-2.0**.

## Vì sao repository này tồn tại

Một security agent không nên đi thẳng từ scanner alert, crash, trace đáng ngờ, static-analysis warning hay giả thuyết của model đến kết luận “đã xác nhận lỗ hổng”.

Nghiên cứu bảo mật đáng tin cậy cần một chuỗi bằng chứng:

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

Security Skills biến kỷ luật này thành các Agent Skills có thể tái sử dụng và các contract máy có thể kiểm tra.

## Kiến trúc hiện tại

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

Nội dung canonical của skill chỉ tồn tại một lần dưới `skills/`. Packs, operator-depth profiles, benchmarks và các lớp evaluation tham chiếu cùng nguồn authority đó thay vì nhân bản prose theo từng vendor.

## Repository cung cấp những gì

### 1. Đồ thị suy luận bảo mật canonical

Mỗi capability canonical có cấu trúc:

```text
skills/<skill-name>/
├── SKILL.md
├── skill.meta.json
└── references/        # tài nguyên sâu hơn nếu cần
```

Một skill mô tả decision process có thể tái sử dụng: khi nào áp dụng, prerequisite, workflow, yêu cầu bằng chứng, stop condition và output mong đợi.

`skill.meta.json` bổ sung metadata đồ thị như domain, prerequisite, composition edge, maturity và evidence stage.

### 2. Research routing xác định

Research case được validate trước khi route. Router đóng transitive prerequisites, áp dụng domain/context filtering, giữ các ràng buộc evidence-state và trả về thứ tự skill xác định.

```bash
python scripts/validate_case.py examples/research-case.example.json
python scripts/route_skills.py examples/research-case.example.json --limit 12
```

Routing chỉ mang tính advisory. Authorization và yêu cầu bằng chứng vẫn là authority.

### 3. Mô hình evidence-state

Security claim đi qua các trạng thái rõ ràng:

```text
hypothesis
    ↓
observed
    ↓
validated
    ↓
regression-verified
```

Kết quả từ một tool không tự động nâng trạng thái finding.

Một finding ở mức `validated` cần các loại evidence như target/environment được pin, observation tái lập được, causal root cause, hậu quả bảo mật có giới hạn, positive/negative controls và định danh reproducer. `regression-verified` còn yêu cầu revision đã sửa không tái hiện lỗi trong khi controls vẫn hoạt động đúng.

Xem [docs/research-case-contract.md](docs/research-case-contract.md).

### 4. Operator depth

Wave 10 đóng ở **40 operator-depth profiles có CI enforcement**.

Operator depth được dùng có chọn lọc: không phải canonical skill nào cũng cần một runbook lớn. Profile chỉ được thêm khi causal methodology sâu hơn thực sự làm tăng độ tin cậy.

Mỗi profile đã đăng ký kết hợp:

- operator runbook đã review;
- scenario/review case synthetic hoặc controlled ở dạng machine-readable;
- safe oracle rõ ràng;
- evidence ladder;
- counterfactual và false-positive controls;
- stop conditions;
- remediation và regression checks;
- test xác định riêng.

Coverage trải từ authorization/identity, parser/protocol boundaries, memory/runtime, sandbox/browser/driver, firmware/virtualization, crypto/external-data trust, AI-agent security, web internals đến smart-contract invariant/reentrancy/upgradeability.

Xem [docs/operator-depth-contract.md](docs/operator-depth-contract.md), [operator-depth/profiles.json](operator-depth/profiles.json) và [Wave 10 closure audit](docs/wave10-closure-audit.md).

### 5. Deterministic benchmarks

Wave 5 thiết lập **36 deterministic fixtures** trong sáu nhóm:

1. authorization;
2. domain isolation;
3. evidence-state conformance;
4. false-positive control;
5. remediation/regression routing;
6. representative routing correctness.

```bash
python scripts/validate_benchmarks.py
python scripts/run_benchmarks.py benchmarks/suites/portability.json
python scripts/run_benchmarks.py benchmarks/suites/core.json
```

Các lỗi cứng như chấp nhận case không được ủy quyền, vi phạm evidence-state hay domain leakage không thể bị che bởi điểm trung bình cao.

Xem [docs/benchmark-contract.md](docs/benchmark-contract.md).

### 6. Cross-agent evaluation

Lớp evaluation biến benchmark fixtures đã review thành task không chứa oracle và chấm các `agent-run` artifact đã normalize bằng code xác định trong repository.

Core không hard-code model vendor hay proprietary CLI. Agent host bên ngoài tích hợp qua cùng artifact contract.

```bash
python scripts/prepare_agent_tasks.py benchmarks/suites/portability.json --out /tmp/agent-tasks
python scripts/prepare_replay_runs.py benchmarks/suites/portability.json --profile reference --out /tmp/reference-runs
python scripts/validate_agent_runs.py /tmp/reference-runs
python scripts/evaluate_agent_runs.py benchmarks/suites/portability.json /tmp/reference-runs
```

Repository giữ một reference baseline conforming cùng các deterministic negative controls.

Xem [agent-eval/README.md](agent-eval/README.md).

### 7. Comparative regression có kiểm soát

Repository cũng có “superiority-court” deterministic để regression-test các contestant view nội bộ trong điều kiện được kiểm soát. Đây là engineering test authority, **không phải leaderboard model bên ngoài và không phải bằng chứng cho superiority phổ quát**.

Mọi so sánh thực nghiệm với hệ thống khác phải dùng task tương đồng, điều kiện kiểm soát, nêu rõ giới hạn và có bằng chứng trực tiếp.

## Phạm vi security coverage

Canonical graph bao phủ sâu:

- scope, authorization, attack-surface mapping và hypothesis generation;
- fuzz harness, corpus, coverage-guided, grammar-aware và stateful fuzzing;
- crash triage, minimization, sanitizer evidence và exploitability triage;
- static/dataflow analysis, symbolic execution, differential testing và variant hunting;
- memory lifetime, bounds/integer safety, type confusion, concurrency và JIT invariants;
- parser/protocol state machines, canonicalization, deserialization và namespace confusion;
- authorization, confused deputy, cache identity, secrets/tokens và tenant isolation;
- kernel, driver/IOCTL, sandbox, browser process boundaries và virtualization;
- container, cloud IAM, supply-chain, firmware, secure boot và update chains;
- Android/iOS security cùng local-storage/keystore boundaries;
- web routing, server-side request boundaries, upload, template và multi-tenant internals;
- cryptographic protocol, randomness lifecycle, certificate và hostname validation;
- smart-contract invariant, reentrancy, upgradeability và oracle trust;
- prompt injection, RAG/memory isolation, tool confirmation, connector/plugin và AI-agent assessment;
- evidence ledger, false-positive elimination, remediation, regression validation và reporting.

## Quick start

Core validation không cần cài Python package bên thứ ba.

```bash
git clone https://github.com/Nolane-x/Security-skills.git
cd Security-skills

python scripts/validate_skills.py
python scripts/validate_operator_depth.py
python scripts/validate_graph.py
python scripts/validate_benchmarks.py
python -m unittest discover -s tests -v
```

Sinh và kiểm tra index:

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

CI lặp lại các gate quan trọng trên Ubuntu, macOS và Windows với Python 3.11/3.13, sau đó chạy riêng benchmark, cross-agent và comparative regression jobs.

## Portability

`skills/` là canonical source. Không fork skill prose theo vendor.

Một host layout có thể trỏ trực tiếp về cùng nội dung:

```text
<project>/
└── .agents/
    └── skills/
        └── <skill-name>/
            ├── SKILL.md
            └── ...optional local resources...
```

Agent host hiểu Agent Skills hoặc có thể đọc explicit repository context đều có thể tích hợp mà không thay đổi security authority gốc.

Xem [docs/compatibility.md](docs/compatibility.md).

## Safe adapter boundary

Local adapter được thiết kế phòng thủ:

- `shell=False`;
- argv vector rõ ràng;
- timeout enforcement;
- stdout/stderr byte caps;
- terminate child khi overflow;
- sanitize environment mặc định;
- credential-like variables chỉ qua explicit allowlist;
- parse untrusted agent output như data;
- cleanup pipe xác định;
- không yêu cầu hoặc lưu hidden reasoning / chain-of-thought.

## Cấu trúc repository

```text
Security-skills/
├── skills/              # 83 canonical Agent Skills
├── operator-depth/      # registry cho 40 selective deep profiles
├── packs/               # 20 curated routing manifests
├── benchmarks/          # deterministic routing/evidence fixtures
├── agent-eval/          # vendor-neutral cross-agent contracts
├── superiority/         # controlled comparative regression authority
├── schemas/             # machine-readable schemas
├── scripts/             # validators, routers, evaluators, builders
├── tests/               # deterministic regression tests
├── examples/            # research-case examples
├── docs/                # contracts và architecture documentation
├── sources/             # research-system lineage metadata
├── AGENTS.md             # repository-level agent guidance
├── SECURITY.md           # authorization và responsible-use boundary
├── CONTRIBUTING.md       # contribution requirements
└── LICENSE               # Apache License 2.0
```

## Safety boundary

Intrusive techniques chỉ dành cho target local, owned, sandboxed, benchmark/CTF hoặc được ủy quyền rõ ràng.

Proof nên dùng bằng chứng ít gây hại nhất đủ để chứng minh claim: assertion, sanitizer report, minimized crash, synthetic resource, marker file, policy simulation, mock service, read-only snapshot, synthetic canary và regression test.

Xem [SECURITY.md](SECURITY.md).

## Wave 10 closure

Wave 10 được **đóng có chủ đích tại 40 operator-depth profiles**. Project không coi repository size, skill count, profile count hay line count là quality metric.

Công việc tiếp theo mặc định nên tập trung vào:

- correctness và maintenance;
- bằng chứng và controls mạnh hơn;
- safe oracle tốt hơn;
- benchmark tốt hơn;
- portability;
- cập nhật research lineage;
- targeted defect fixes;
- documentation và onboarding.

Mở rộng vượt baseline 83 / 20 / 40 phải có một mechanism thực sự chưa được bao phủ, không trùng lặp và một quyết định kiến trúc rõ ràng.

Xem [docs/wave10-closure-audit.md](docs/wave10-closure-audit.md).

## Đóng góp

Đọc [CONTRIBUTING.md](CONTRIBUTING.md) trước khi thay đổi canonical skills, graph metadata, packs, operator-depth contracts, benchmarks hoặc agent-evaluation authority.

Một contribution mạnh thêm decision process có thể tái sử dụng hoặc làm contract hiện tại chặt hơn. Một contribution yếu chỉ thêm tool wrapper, payload list hoặc prompt trùng lặp.

## Nguồn nghiên cứu

Security Skills chắt lọc workflow nguyên bản từ reproducible vulnerability research, autonomous cyber-reasoning systems, fuzzing infrastructure, program analysis, reverse engineering, web/mobile/firmware/cloud security, smart-contract analysis và nghiên cứu AI-agent security hiện đại.

Repository **không** vendor third-party offensive code và không sao chép third-party prompt.

Xem [docs/sources.md](docs/sources.md) và [sources/research-systems.json](sources/research-systems.json).

## Tài liệu

- [English README](README.md)
- [简体中文 README](README-CN.md)
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

Phát hành theo [Apache License 2.0](LICENSE).

---

**Security Skills tuân theo một nguyên tắc: một security claim chỉ mạnh bằng chất lượng evidence, controls và khả năng tái lập đứng phía sau nó.**
