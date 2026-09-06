# Research systems and standards registry

This file records systems that inform the *research patterns* we plan to distill. It is not a vendored code list and does not imply that third-party source text or exploit code is copied into this repository.

## Portability standards and agent hosts

- Agent Skills specification — https://agentskills.io/specification
- Gemini CLI Agent Skills — https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/skills.md
- Cursor Agent Skills — https://cursor.com/docs/skills
- GitHub Copilot Agent Skills — https://docs.github.com/en/copilot/concepts/agents/about-agent-skills
- OpenCode Agent Skills — https://opencode.ai/docs/skills
- Kiro Agent Skills — https://kiro.dev/docs/skills/

## Autonomous vulnerability research and reproducible research

- Exploitarium — https://github.com/bikini/exploitarium
- AIxCC — DARPA AI Cyber Challenge public materials and open-sourced Cyber Reasoning Systems
- Team Atlanta Atlantis — https://github.com/Team-Atlanta/aixcc-afc-atlantis
- Trail of Bits Buttercup — https://github.com/trailofbits/buttercup
- Shellphish ARTIPHISHELL / OSS-CRS work — https://github.com/Team-Atlanta/shellphish-oss-crs
- FuzzingBrain — https://github.com/fuzzingbrain/afc-crs-all-you-need-is-a-fuzzing-brain
- OSS-CRS — https://github.com/ossf/oss-crs
- Vulnhuntr — https://github.com/protectai/vulnhuntr

## Fuzzing and dynamic analysis

- OSS-Fuzz / ClusterFuzz
- AFL++
- libFuzzer
- LibAFL
- syzkaller
- FuzzBench
- sanitizer ecosystems (ASan, UBSan, MSan, TSan)

## Static, symbolic, binary, and runtime analysis

- CodeQL
- Joern
- angr
- Manticore
- Triton
- Ghidra
- Qiling
- Frida
- rr

## Domain/security ecosystems for future packs

- Nuclei and template ecosystems
- MobSF
- Prowler
- Trivy
- Slither
- garak
- PyRIT
- Promptfoo
- CyberSecEval
- AgentDojo

## Extraction policy

When a source inspires a skill:

1. identify the reusable decision process rather than copying prose;
2. cross-check the method against primary documentation or code;
3. record assumptions and limitations;
4. write original instructions and examples;
5. preserve attribution in references;
6. validate the resulting skill against the repository contract.
