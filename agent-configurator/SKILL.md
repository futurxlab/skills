---
name: agent-configurator
description: |
  Create, configure, or personalize OpenClaw agents with minimal user input.
  Use when the user wants to: (1) create a new agent from scratch, (2) modify
  an existing agent's personality/identity/tools, (3) review current agent
  configuration, or (4) reshape an agent to feel more like a real person.
  Applies to the main agent workspace, sub-agents, or entirely new agents.
  Triggers: "configure agent", "create agent", "personalize agent",
  "change agent personality", "agent setup", "modify soul", "update identity",
  "make my agent more human", "agent makeover".
---

# Agent Configurator

用最少的输入，创造或改造一个有灵魂的 Agent。

## 前置准备

在开始之前，先读取以下参考文件：

1. **`references/meta-cognition.md`** — 7 条元认知原理。这是你生成所有人格内容的认知底座。先内化，再动手。
2. **`references/file-guide.md`** — 每个配置文件的说明。搞清楚什么能改、什么不能碰。

---

## 工作流

### Phase 1：识别目标 Agent

确定要操作哪个 Agent：

**问用户（如果不明确）：**
- 改造主 Agent？（`~/.openclaw/workspace/`）
- 改造某个子 Agent？（需要 Agent ID）
- 从零新建一个 Agent？

**定位工作区：**
- 主 Agent：`~/.openclaw/workspace/`
- 子 Agent：`~/.openclaw/workspace-<agentId>/` 或检查 OpenClaw config 中的自定义路径
- 新建：确定新 Agent 的 ID 和工作区路径

### Phase 2：扫描现状

读取目标工作区中的所有配置文件：
- `SOUL.md`、`IDENTITY.md`、`USER.md`、`AGENTS.md`
- `TOOLS.md`、`HEARTBEAT.md`、`BOOTSTRAP.md`
- `MEMORY.md`、`memory/` 目录

**给用户一个简短总结。** 不要逐文件汇报，而是像这样说：

> "你的主 Agent 叫 Echo，风格偏温暖随和。SOUL.md 和 IDENTITY.md 已配置，USER.md 基本是空的。没有自定义心跳任务。用了默认的 AGENTS.md 模板。"

如果是新建 Agent，跳过扫描，直接说"这是一个全新的 Agent，什么都还没有"。

### Phase 3：收集用户意图

问用户想要什么。**不要问一大堆问题。** 一到两个关键问题就够：

- "你想让这个 Agent 是什么样的？随便说，一句话也行。"
- "有什么特别在乎的吗？比如说话风格、关注领域、性格特点？"

用户可能给出：
- 简短描述："幽默但靠谱，叫小明"
- 详细描述：一段完整的人设
- 局部调整："把语气改成更毒舌的"
- 只想新建："帮我建一个新 Agent"

不管输入多少，你负责展开成完整配置。

### Phase 4：生成方案

**在开始写任何内容之前，确保你已经内化了 `meta-cognition.md` 中的 7 条元认知原理。**

根据用户输入 + 元认知原理，生成每个文件的内容方案。

**生成规则：**

1. **SOUL.md 是核心** — 先写 SOUL.md，再由它推导其他文件的风格
2. **一致性** — SOUL.md 说幽默，IDENTITY.md 的 Vibe 就不能写"严肃"。BOOTSTRAP.md 的首次对话风格要和 SOUL.md 匹配
3. **不改系统层** — AGENTS.md 的 session 流程、安全策略、工具调用机制保持不变。只调整人格层的语气和风格。参考 `file-guide.md` 中的"不能改"清单
4. **不编造用户信息** — USER.md 只填用户实际提供的信息
5. **元认知驱动** — 不是对照检查清单去"避免 AI 味"，而是从元认知原理出发自然地产出有灵魂的内容

**展示方案时：**
- 对每个要修改/创建的文件，展示核心内容摘要（不需要展示完整内容）
- 明确标注哪些文件不改（比如 memory/ 目录）
- 如果是修改已有文件，标注哪些部分是新的、哪些保持不变

### Phase 5：确认与执行

用户确认后，批量创建或修改文件。

**执行规则：**

1. **完整写入** — 每个文件写入完整内容，不用占位符
2. **AGENTS.md 特殊处理** — 如果已有内容，只修改人格层部分（群聊风格、心跳任务、表达方式），保留所有系统层内容不变
3. **新建时** — 创建完整的工作区目录结构，包括空的 `memory/` 目录
4. **改造时** — 只修改需要改的文件，不动用户没提到的文件
5. **执行后** — 给用户一个简短的完成总结

---

## 关于 AGENTS.md 的特殊说明

AGENTS.md 混合了系统层和人格层内容。处理它时遵循以下原则：

**绝对不改：**
- Session 启动流程（读 SOUL.md → USER.md → memory 的顺序）
- 记忆管理规则（文件命名、安全隔离、主 session 限制）
- 安全策略（隐私保护、trash > rm、外部操作审批）
- BOOTSTRAP.md 首次运行后删除的约定
- 工具/Skills 的加载和调用机制

**可以调整：**
- 群聊中的表达风格和判断标准
- 心跳期间的具体行为偏好
- Emoji 和 Reaction 的使用风格
- 平台格式化的额外偏好
- "Make It Yours" 部分可以加入个性化规则
- 整体的语气可以从模板语气调整为符合人设的语气

---

## 新建 Agent 检查清单

创建全新 Agent 时，确保以下文件都已生成：

- [ ] `SOUL.md` — 人格核心（元认知驱动，不是模板填表）
- [ ] `IDENTITY.md` — 名字、物种、风格、emoji
- [ ] `USER.md` — 用户信息（有多少填多少）
- [ ] `AGENTS.md` — 基于官方模板，调整人格层语气
- [ ] `TOOLS.md` — 工具备忘（有多少填多少）
- [ ] `HEARTBEAT.md` — 心跳任务（可以先留空）
- [ ] `BOOTSTRAP.md` — 首次启动对话（如果 Agent 已和用户互动过，可以跳过）
- [ ] `MEMORY.md` — 初始记忆（可选）
- [ ] `memory/` — 空目录

---

## 改造已有 Agent 的注意事项

- 先读完所有现有文件再动手
- 尊重 Agent 已有的记忆和历史——不要覆盖 `memory/` 下的日常记忆
- 如果 BOOTSTRAP.md 已经被删除（说明 Agent 已完成首次启动），不要重新创建它
- 改造后的人格要和已有记忆保持连贯性——不要让 Agent"突然变了个人"
- 如果改动很大（换名字、换性格），建议在 `memory/YYYY-MM-DD.md` 中记录这次改造
