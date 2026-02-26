# Idea Incubator

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Workflow: Multi-Agent](https://img.shields.io/badge/Workflow-Multi--Agent-1f6feb.svg)
![Execution: Mode_A_Prefer](https://img.shields.io/badge/Execution-Mode_A_Prefer-2da44e.svg)
![Fallback: Mode_B_Simulation](https://img.shields.io/badge/Fallback-Mode_B_Simulation-f59e0b.svg)
![Language: CN/EN](https://img.shields.io/badge/Language-CN%20%2F%20EN-6f42c1.svg)
![Status: Active](https://img.shields.io/badge/Status-Active-22c55e.svg)

Idea Incubator 是一个面向 AI 产品与技术方案的想法孵化 Skill。  
它通过三位专家 Agent 的协同研究与辩论，将早期想法转化为可执行的结论和文档输出。

## 核心能力

- 多视角评估：研究、逻辑、创意三线并行
- 结构化流程：研究 -> 辩论 -> 结论 -> 归档
- 可审计产出：统一写入 `ideal/` 目录，便于追踪与复盘

## 角色分工

| Agent | 职责 | 风格 |
|---|---|---|
| **Harper 🔍** | 研究与深度分析（竞品、可行性、技术路径） | 客观、数据驱动、严谨 |
| **Benjamin ⚖️** | 逻辑检验与压力测试（风险、边界条件、一致性） | 怀疑、直接、结构化 |
| **Lucas 🎨** | 创意拓展与共识整合（用户体验、方案重构、命名） | 热情、共情、有远见 |

参考定义见 `references/agents.md`。

## 触发方式

当用户消息以以下任一前缀开头时触发：

- `💡`
- `想法：`
- `孵化`
- `incubate`

## 标准流程

1. **研究阶段（Harper）**：建立事实基础，识别机会与约束。
2. **辩论阶段（Harper + Benjamin + Lucas）**：进行 3-5 轮自由辩论，覆盖技术、业务、体验、风险等关键维度。
3. **整合阶段（Manager）**：输出最终裁决（`GO` / `NO-GO` / `Conditional`），并写入归档文件。

## 执行模式

Skill 按平台能力在两种模式间切换：

### Mode A: Multi-Agent（首选）

适用于支持子 Agent 的平台（如 Claude Code `Task()`、Codex `spawn_agent`、OpenClaw `sessions_spawn`）：

- 三位角色以**独立子 Agent**运行，上下文隔离
- 每轮输入包含：角色定义 + 想法描述 + 上轮关键信息
- 可显著降低同质化推理和确认偏差

### Mode B: Single-Agent Simulation（回退）

适用于不支持子 Agent 的平台（如 Antigravity）：

- 由主 Agent 在单上下文中模拟三位角色
- 必须显式区分角色语气与推理路径
- 报告中必须注明为“单 Agent 模拟”
- 偏差缓解要求：
  - Harper 以事实与数据为主
  - Benjamin 主动提出反例与失败路径
  - Lucas 提供重构方案并推动收敛

> 原则：**优先 Mode A**；使用 Mode B 时必须透明标注。

## 输出规范

产出统一落盘到 `ideal/`：

```text
ideal/
├── reports/              # 各想法的完整孵化报告
│   └── <idea-name>-incubation.md
├── prd/                  # 通过孵化后的 PRD（可选）
│   └── <idea-name>-prd.md
└── selected_ideas.md     # 想法索引与裁决摘要
```

## 安装

```bash
ln -s /path/to/idea-incubator /your/project/.agent/skills/idea-incubator
```

## License

MIT
