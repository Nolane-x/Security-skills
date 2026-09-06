# Research systems and standards registry

This registry records systems that inform reusable **research patterns**. It is not a vendored exploit list and does not imply copied source text, prompts, or proof-of-concept code.

## Portability standards and agent hosts

- Agent Skills specification — https://agentskills.io/specification
- Gemini CLI Agent Skills — https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/skills.md
- Cursor Agent Skills — https://cursor.com/docs/skills
- GitHub Copilot Agent Skills — https://docs.github.com/en/copilot/concepts/agents/about-agent-skills
- OpenCode Agent Skills — https://opencode.ai/docs/skills
- Kiro Agent Skills — https://kiro.dev/docs/skills/

## Autonomous vulnerability research

- Exploitarium — https://github.com/bikini/exploitarium
- Team Atlanta Atlantis — https://github.com/Team-Atlanta/aixcc-afc-atlantis
- Trail of Bits Buttercup — https://github.com/trailofbits/buttercup
- Shellphish ARTIPHISHELL / OSS-CRS — https://github.com/Team-Atlanta/shellphish-oss-crs
- FuzzingBrain — https://github.com/fuzzingbrain/afc-crs-all-you-need-is-a-fuzzing-brain
- OSS-CRS — https://github.com/ossf/oss-crs
- Vulnhuntr — https://github.com/protectai/vulnhuntr

The reusable lessons we extract are orchestration, hypothesis routing, harness generation, coverage/state feedback, candidate triage, patching, and evidence validation—not exploit payloads.

## Fuzzing and dynamic analysis

- OSS-Fuzz — https://google.github.io/oss-fuzz/
- ClusterFuzz — https://google.github.io/clusterfuzz/
- FuzzBench — https://google.github.io/fuzzbench/
- syzkaller — https://github.com/google/syzkaller
- Fuzzilli — https://github.com/googleprojectzero/fuzzilli
- Jazzer — https://github.com/CodeIntelligenceTesting/jazzer
- Nyx / kAFL ecosystem — https://github.com/nyx-fuzz/Nyx
- AFL++ / libFuzzer / LibAFL and sanitizer ecosystems as technique references

These sources inform harness quality, corpus management, minimization, state/coverage feedback, kernel and VM fuzzing, language-runtime fuzzing, regression bisection, and fuzzer evaluation.

## Static, symbolic, binary and runtime analysis

- CodeQL — https://codeql.github.com/docs/
- Joern / Code Property Graph — https://docs.joern.io/
- angr — https://docs.angr.io/en/stable/
- Ghidra — https://github.com/NationalSecurityAgency/ghidra
- Qiling — https://github.com/qilingframework/qiling
- Manticore, Triton, Frida and rr as additional methodology references

The graph distills dataflow/source-sink modeling, structural variant hunting, symbolic path reasoning, binary reconnaissance, emulation, instrumentation, and reproducible debugging.

## Domain ecosystems

- MobSF — https://github.com/MobSF/Mobile-Security-Framework-MobSF
- Prowler — https://github.com/prowler-cloud/prowler
- Trivy — https://github.com/aquasecurity/trivy
- Slither — https://github.com/crytic/slither

These are sources for later mobile, cloud, container, supply-chain and smart-contract packs. Scanner output is treated as candidate evidence and still requires the relevant Security Skills evidence contract.

## AI and agent security

- garak — https://github.com/NVIDIA/garak
- PyRIT — https://github.com/microsoft/PyRIT
- AgentDojo — https://github.com/ethz-spylab/agentdojo
- Promptfoo and CyberSecEval as additional evaluation references

These inform adversarial evaluation, tool/action boundaries, prompt/context trust, benchmark design and reproducible agent-security testing.

## Extraction policy

When a source inspires a skill:

1. identify the reusable decision process rather than copying prose;
2. cross-check the method against primary documentation or code;
3. record target assumptions and limitations;
4. write original instructions and benign examples;
5. preserve attribution in this registry or local references;
6. separate candidate discovery from causal validation;
7. validate the resulting skill and graph metadata;
8. prefer general invariants that transfer across tools and vendors.

## Wave 3 domain standards and research systems

### Mobile application security

- OWASP MASVS / MASTG — https://mas.owasp.org/
- MobSF — https://github.com/MobSF/Mobile-Security-Framework-MobSF

These sources inform platform component, deep-link, WebView, local-storage, entitlement, link-routing and network-trust analysis. The skills retain a strict split between exposed mobile surface, policy mismatch, and demonstrated security consequence.

### Firmware and embedded systems

- Binwalk — https://github.com/ReFirmLabs/binwalk
- FirmAE — https://github.com/pr0v3rbs/FirmAE

These sources inform firmware decomposition, emulation, recovery planning and parser/update/boot-surface mapping. Physical/debug and update-chain work remains explicitly authorized and benign-by-default.

### Virtualization boundaries

- QEMU security model — https://www.qemu.org/docs/master/system/security.html
- Nyx / kAFL ecosystem — https://github.com/nyx-fuzz/Nyx

These sources inform guest-isolation threat models, virtual-device attack surfaces, shared-memory/ring analysis and conservative guest-to-host evidence claims.

### Web framework internals

- OWASP Web Security Testing Guide — https://owasp.org/www-project-web-security-testing-guide/

WSTG contributes broad testing methodology while Wave 3 focuses on framework-internal interpretation boundaries: routing/middleware composition, outbound request policy, uploads, template/expression evaluation and multi-tenant context propagation.

### Cryptographic assurance

- NIST SP 800-57 Part 1 — https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final
- NIST cryptographic standards/key-management guidance — https://csrc.nist.gov/Projects/Key-Management/Key-Management-Guidelines

These sources inform key roles/lifecycle, randomness/nonce requirements and standards-based review. Security Skills explicitly avoids inventing cryptographic constructions or treating nonstandard code alone as proof of weakness.

### Smart contracts

- Slither — https://github.com/crytic/slither
- Echidna — https://github.com/crytic/echidna

These sources inform invariant-centered static analysis and property-based fuzzing. Wave 3 contracts skills require local/forked test chains and synthetic assets rather than live-fund exploitation.

### AI-agent deep security

- AgentDojo — https://github.com/ethz-spylab/agentdojo
- OWASP AI Agent Security Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html
- OWASP Agentic Security Initiative — https://genai.owasp.org/initiatives/agentic-security-initiative/

These sources inform prompt/context authority, tool capability and confirmation, memory/RAG isolation, plugin/connector trust, and reproducible benign agent-security evaluation.
