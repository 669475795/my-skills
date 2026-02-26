---
name: idea-incubator
description: A collaborative multi-agent workflow for incubating AI ideas. Uses three specialized agents—Harper (Research), Benjamin (Logic), and Lucas (Creative)—to research, debate, and refine concepts into structured projects. Trigger when message starts with "💡", "想法：", "孵化", or "incubate".
---

# Idea Incubator

This skill facilitates a structured incubation process for AI ideas using a specialized team of three agents: Harper (Research), Benjamin (Logic), and Lucas (Creative).

## The Team

- **Harper 🔍 (Research / Deep Analysis Expert)**: Objective, data-driven, thorough. Focused on real-time search, competitor landscape, API availability, technical stacks, fact-checking, and feasibility. Provides the factual foundation.
- **Benjamin ⚖️ (Logic / Debate Expert)**: Skeptical, rigorous, direct. Focused on edge cases, potential failure points, resource efficiency, logical consistency, and code/math verification. Stress-tests the idea.
- **Lucas 🎨 (Creative / Consensus Expert)**: Enthusiastic, empathetic, visionary. Focused on divergent thinking, user experience, creative pivots, naming, and balancing conflicting viewpoints. Finds the path forward.

## How to Trigger

Detect when a message starts with any of:
- `💡`
- `想法：`
- `孵化`
- `incubate`

## Workflow

### 1. Research Phase (Harper)
Harper conducts initial deep research on the idea:
- Search for existing competitors and similar products
- Assess technical feasibility and available building blocks
- Identify market signals and academic findings
- Summarize key facts, risks, and opportunities

### 2. Debate Phase (Harper + Benjamin + Lucas)
All three agents engage in **free-form debate** (3-5 rounds). Each agent contributes from their perspective, challenging and building on each other's arguments. The debate is **not rigidly structured** — let the conversation flow naturally and cover whatever dimensions the idea demands (feasibility, UX, ethics, monetization, tech stack, etc.).

### 3. Integration & Report
After the debate concludes:
- Synthesize a final verdict (GO / NO-GO / Conditional)
- Output the full report to `./ideal/reports/<idea-name>-incubation.md`
- Update `./ideal/selected_ideas.md` with the verdict summary

> **Note**: All paths are relative to this skill's directory.

## Execution Modes

This skill can operate in two modes depending on the platform's capabilities:

### Mode A: Multi-Agent (platforms with sub-agent support)
When the platform supports spawning independent sub-agents (e.g., Claude Code `Task()`, Codex `spawn_agent`, OpenClaw `sessions_spawn`):
- Spawn each agent (Harper, Benjamin, Lucas) as a **separate sub-agent** with isolated context
- Each agent receives its role description + the idea + previous round's output
- This produces **genuinely independent perspectives** that avoid confirmation bias

### Mode B: Single-Agent Simulation (default fallback)
When the platform does **not** support sub-agents (e.g., Antigravity):
- The main agent simulates all three roles within a single context
- Use distinct voice, tone, and reasoning style for each agent
- Be transparent in the report: note that this was single-agent simulation
- **Mitigation**: To reduce convergence bias, deliberately adopt each role's persona before generating their arguments — Harper should cite data, Benjamin should actively challenge, Lucas should defend

> **Always prefer Mode A when available.** Mode B is acceptable but should be clearly labeled.

## Output Structure

```
./ideal/
├── reports/          # Full incubation reports per idea
│   └── <idea-name>-incubation.md
├── prd/              # PRDs for approved ideas (optional, post-incubation)
│   └── <idea-name>-prd.md
└── selected_ideas.md # Master index of all incubated ideas with verdicts
```

## Integration Guidelines

- Keep the output focused on being **actionable** — what to build, what to avoid, what to validate
- Ensure all findings are stored in `./ideal/`
- Reference `./references/agents.md` for detailed agent persona definitions
