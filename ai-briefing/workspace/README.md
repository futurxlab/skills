# AI Briefing Workspace

这个目录是 ai-briefing skill 的独立工作空间。

## 目录结构

```
workspace/
├── temp/       # 临时文件（arXiv XML等）
├── cache/      # 缓存数据
└── output/     # 输出结果（生成的报告）
```

## 安全说明

- 此目录下的操作会被自动批准（通过 hooks/hooks.json 配置）
- skill 的所有文件操作都应该在这个目录内进行
- 不会影响系统其他文件
