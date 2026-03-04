---
name: ai-briefing
description: 获取AI圈最新信息简报。根据用户指定的时间范围（默认最近7天）从多个权威源获取并筛选AI技术进展、模型发布、行业动态。
---

# AI Briefing

根据用户要求的时间范围获取并展示AI圈最新信息，默认最近7天。

## 一、资源配置（Reference）

### 1. 数据源总览地图

| 板块 | 数据源 | 方法 |
|------|--------|------|
| 实时热点 | Hacker News API | `scripts/fetch_hn.py` |
| 社区讨论 | Reddit | WebSearch |
| 模型热度趋势 | HuggingFace API `sort=trendingScore`（主） | curl |
| 重大事件 | WebSearch + 官方博客 WebFetch | 综合 |
| GitHub 仓库更新 | `gh api` 监控核心仓库 | gh cli |
| arXiv 论文 | arXiv API（通用/Agent/RAG/人格四类） | `scripts/fetch_arxiv.py` |
| 行业动态补充 | WebSearch | 关键词搜索 |

### 2. 重点监控的 GitHub 仓库

**【底层架构与推理】**
- `huggingface/transformers` - 模型支持（新模型架构发布的信号）
- `vllm-project/vllm` - 服务端高性能推理引擎
- `ollama/ollama` - 本地端侧推理与体验（新趋势）
- `ggerganov/llama.cpp` - 底层推理与硬件边界探索

**【应用框架与 Agent】**
- `langchain-ai/langchain` - 全栈应用框架
- `langchain-ai/langgraph` - 复杂 Agent 原生工作流

**【数据与存储】**
- `run-llama/llama_index` - RAG 框架与数据管道
- `microsoft/graphrag` - 知识图谱 + RAG 前沿实践
- `mem0ai/mem0` - LLM 长期记忆

**【系统与可视化 (DevOps & LLMOps)】**
- `langfuse/langfuse` - 大模型可观测性与评估工具
- `open-webui/open-webui` - 暴露 AI 交互体验的前瞻趋势

### 3. arXiv 监控方向

你可以根据报告需要灵活获取论文：

**选项 1：一键获取预定义的底层基础方向（推荐）**
当前我们重点关注以下研究方向：
- 通用 AI 进展：大语言模型基础能力、Scaling、训练方法、评测等
- AI Agent：自主 Agent、工具调用、规划、多 Agent 协作
- RAG / 知识图谱：检索增强生成、知识库构建、图谱推理
- AI 数字分身 / 人格建模：个性化 LLM、角色扮演、AI 人格、记忆系统
脚本内置了以上四个基础关注方向，你可以一键抓取它们

**选项 2：自定义抓取任意你感兴趣的前沿方向（高级功能）**

如果你想查阅某个特定的突破性技术（如 `machine learning`, `diffusion models`, `mamba` 等），你可以自主决定查询词

> **查询词构造规则**（arXiv API 格式）：
> - 类别过滤：`cat:cs.AI`、`cat:cs.CL`、`cat:cs.MA`
> - 关键词搜索：`all:%22关键词%22`（引号用 `%22`，空格用 `+`）
> - 组合：`(cat:cs.AI+OR+cat:cs.CL)+AND+all:%22machine+learning%22`


## 二、执行流程（Step-by-step）

### 第零步：建立执行 CheckList（强制！）

由于上下文可能较长，为了防止你遗漏关键数据源和核心格式要求，**在开始执行任何抓取之前**，必须先清理临时数据并向用户输出包含以下内容的 TODO List，后续严格对照执行：

**待办清单 (TODO List)：**
- [ ] 0. **清理旧数据**：运行 `rm -rf ~/.claude/skills/ai-briefing/workspace/temp/*`
- [ ] 1. 并行获取 7 大数据源（须涵盖 HN, Reddit, HF, Web+官网事件, GitHub, arXiv, 行业搜索）
- [ ] 2. HN：分析并筛选真正与 AI/前沿技术相关的文章
- [ ] 3. Reddit：从核心 subreddits 提取最热前沿讨论
- [ ] 4. arXiv：获取 4 大通用标签 + 自行决策的额外方向（如机器/强化学习等）
- [ ] 5. 合并前沿信息：去重并确定优先级（重大事件🔴 / 值得关注🟡 / 一般进展🟢）
- [ ] 6. 拼装报告：确保模板中的 7 大板块**全部存在**，必须在各处**标注数据来源**
- [ ] 7. 提炼洞察：在报告末尾输出 3-5 条具有深度判断倾向的"行业趋势信号"

### 第一步：获取数据（并行执行所有数据获取）

同时发起以下所有请求：

**1. GitHub 核心仓库 releases**

```bash
curl -s "https://api.github.com/repos/{owner}/{repo}/releases/latest" | jq '{name: .name, published_at: .published_at, url: .html_url, body: (.body // "")[0:400]}'
```
*(注：未登录的 curl 每小时有 60 次请求上限。如触发拉取报错，请等待或在 curl 后补充 `-H "Authorization: Bearer YOUR_TOKEN"`)*

**2. HuggingFace 热门模型**

```bash
curl -s "https://huggingface.co/api/models?sort=trendingScore&direction=-1&limit=15" | python3 -c "
import json,sys
data = json.loads(sys.stdin.read())
if isinstance(data, list):
    for m in data:
        print(f'{m.get(\"id\",\"N/A\")}  |  likes: {m.get(\"likes\",0)}  |  downloads: {m.get(\"downloads\",0)}  |  {m.get(\"pipeline_tag\",\"\")}')
"
```

**3. arXiv 论文（灵活获取）**

一次性抓取全部 4 个预定义主题：
```bash
python3 ~/.claude/skills/ai-briefing/scripts/fetch_arxiv.py --category all --days {天数}
```
结合当前的 AI 圈热点，你还可以追加一到两个**自定义查询**获取特定主题（此步骤可选且鼓励多角度）：
```bash
python3 ~/.claude/skills/ai-briefing/scripts/fetch_arxiv.py --query "all:%22machine+learning%22" --label "机器学习" --days {天数}
```

**4. 官方博客（WebFetch）**

- Anthropic: `https://www.anthropic.com/news`
- DeepMind: `https://deepmind.google/discover/blog/`

**5. 行业新闻补充（WebSearch）**

搜索:
- `AI news this week {当前月份} {当前年份}`
- `new AI models released {当前月份} {当前年份}`

**6. Hacker News 综合热点（靠你自主筛选）**

> **🚨 注意**：Hacker News API脚本将极速获取该时间段内**所有类别的 Top 50 热榜内容**，所以需要你判别哪些是AI相关的。

```bash
python3 ~/.claude/skills/ai-briefing/scripts/fetch_hn.py --days {天数} --limit 50
```

你（作为 Agent）获取到这 50 条原始数据后，**必须凭借你的认知和专业知识，仔细甄别**出到底哪些和 AI / 前沿技术相关（比如可能并未包含 AI 字眼而是隐晦地指代模型或芯片的），再将它们编入报告。
只有**你选中的**帖子，才需要输出为简报中的格式（标题、分数、时间、资源链接）。

**7. Reddit AI 社区热帖（靠你自主解析）**

当前我们重点关注以下社区（Subreddits），执行时**针对重点社区分别调用** RSS 获取数据，并从中挑选有价值的前沿讨论：

**重点监控社区：**
- `LocalLLaMA` - 开源模型、本地部署、硬件评测（最核心硬核的底层讨论）
- `MachineLearning` - 机器学习学术研究、论文讨论、工程技术
- `singularity` - AGI 前沿进展、大模型能力边界评测、科技大事件讨论
- `ArtificialIntelligence` - 综合类 AI 行业新闻与大众趋势
- `ClaudeAI` / `ChatGPT` / `OpenAI` - 闭源大模型更新与应用实践（可选，按需查看）

**首选方案：通过 RSS 获取**（⚠️有时会被 Reddit 反爬拦截）

```bash
# 通用调用格式，替换 {社区名} ，参数 t=week 表示本周最热
curl -s -L -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" "https://www.reddit.com/r/{社区名}/top/.rss?t=week"
```
你（作为 Agent）获取 XML 后，需要自行解析里面的 `<entry>` 和 `<title>` 内容，挑选最具深度的帖子。

**备用方案：如果 RSS 获取失败、为空或访问超时**

请立即使用自带的 WebSearch 工具进行搜索，结构范例如下：
- `reddit LocalLLaMA top posts this week`
- `reddit singularity AI news this week`

如遇特定突发事件，可针对性搜索：
- `Anthropic distillation attacks DeepSeek reddit discussion`

### 第二步：解析和筛选（交叉验证）

1. **去重**：同一事件可能出现在多个信息源，合并为一条
2. **按重要性排序**：
   - 🔴 重大事件：同一事件出现在多个源（HN + Reddit + 官方博客等），如新旗舰模型发布、重大架构突破等
   - 🟡 值得关注：框架核心更新、有价值的前沿论文、核心研究者观点
   - 🟢 一般信息：小版本更新、常规论文拓展
3. **过滤噪音**：无情裁减无实物干货的营销内容、标题党、以及与 AI 前沿推进弱相关的帖子

### 第三步：按照模板输出报告

**重要：每个数据板块必须标注来源**

按以下格式输出：

```
# 🧠 AI Briefing | {日期}

## 一、Hacker News 热点（来源: HN API）
| 分数 | 评论 | 日期 | 原文标题 | 中文翻译 | 来源 |
|------|------|------|----------|----------|------|
| 578 | 119 | 2026-02-25 | [Google API keys weren't secrets](https://hn.com/...) | Google API 密钥曾不被视作机密 | [trufflesecurity.com](https://...) |

## 二、Reddit 社区讨论（来源: WebSearch）
### r/LocalLLaMA
1. **标题** - 简短描述（[讨论链接](https://reddit.com/...)）

### r/MachineLearning
（最热的 3 条帖子）

## 三、模型热度趋势（来源: HuggingFace API）
| 排名 | 模型 | 类型 | Likes | Downloads | 趋势点评 |
|------|------|------|-------|-----------|----------|
| 1 | deepseek-ai/DeepSeek-V3 | text-generation | 12.3k | 5.6M | 本周增速最快 |

**关键洞察**：开源模型 vs 闭源模型趋势、中国模型市场份额等

## 四、本周重大事件（来源: WebSearch + 官方博客）

## 五、GitHub 核心仓库更新（来源: GitHub API）
（表格：仓库、最新版本、日期、关键更新内容）

## 六、arXiv 论文精选
### 通用 AI（来源: arXiv API）
### AI Agent（来源: arXiv API）
### RAG / 知识图谱（来源: arXiv API）
### AI 数字分身 / 人格建模（来源: arXiv API）

## 七、行业趋势信号
（从所有数据中提炼 3-5 条趋势判断，每条一句话 + 支撑证据）

---
*数据获取时间：{时间}*
*信息源：HN API, Reddit WebSearch, HuggingFace API, GitHub API, arXiv API, 官方博客*
```

## 三、规则与约束（Rules）

### 1. 数据质量与操作约束

- **时效性与真实性**：根据用户输入判断时间范围，过滤掉超出时间范围的内容；所有数据必须通过获取工具实时获取，**禁止编造**。
- **获取失败降级**：某个数据源获取失败时，必须在对应的板块中保留占位提示，并在报告末尾注明，**严禁直接跳过该板块**。
- **学术摘要要求**：arXiv 论文摘要必须用中文精炼描述：1. 在做什么；2. 解决什么问题；3. 方法和创新点是什么。
- **动态交叉验证**：同一事件若同时在多处出现（如同时上了 HN、Reddit 和官方博客），应上升为“重大事件”。
- **阈值智能过滤**：
  - HN 帖子：分数 > 50 或评论 > 30
  - Reddit 帖子：各 subreddit 只取 top 5 最干货的内容
  - 自动无视明显的营销文章和标题党

### 2. 核心排雷经验（执行避坑）

- **灵活切换方案**：Reddit RSS 若被反爬拦截报错，**切勿死磕重复调用**，请立刻换用 WebSearch 在全网搜索 Reddit 当前时间范围的讨论热门。并行的独立请求能显著提升任务速度。
- **数据源盲点防御**：之前常见错误是“忘记查询 Reddit 社区或漏查 arXiv”，这两种前沿价值最高的数据极易漏传。请严格参照第零步 Checklist 仔细验收所有的 7 个部分。
- **格式规范要求（尤其是 HN）**：HN 板块的生成经常忘记可点击的超链接 URL。必须核对模版格式，表格必须包含对应的【日期】、【中文标题及超链接】、【外部来源】。
- **深度的价值**：如果只是罗列数据，那是爬虫的工作，而你是一个**高级AI Briefing Agent**！必须在总结报告末尾输出深度的**“行业趋势信号”**！

### 3. 文件管理策略

- **工作目录 `workspace/`**
  - **`temp/` 临时文件**：每次运行时需要在第一步被清理释放。
  - **`cache/` 缓存数据** 和 **`output/` 输出结果**：目前可用作保留部分历史报告或临时转存的数据。
- **权限与沙箱防范 (`hooks/hooks.json`)**
  - **白名单工具集**：授权自动批准 `curl`、`python3`、`gh api` 抓取执行。
  - **操作限制**：目前文件体系限制仅限操作 `workspace/**`，不会对用户系统其他部分造成影响。
