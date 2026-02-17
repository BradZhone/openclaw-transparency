# OpenClaw Transparency Skill

AI Agent 透明度记录和审计工具

## 🎯 功能

### 🆓 Free Tier
- ✅ **自动记录** - 记录所有 AI agent 操作
- ✅ **检查点** - 在关键时刻创建保存点
- ✅ **会话总结** - 自动生成执行摘要
- ✅ **数据持久化** - JSON 格式存储
- ✅ **会话管理** - 完整的会话生命周期

### ⭐ Pro Tier ($9/月)
- ✅ **多 Agent 追踪** - 同时追踪多个 agent 的活动
- ✅ **可视化报告** - 生成 ASCII 和 HTML 格式的可视化报告
- ✅ **会话搜索** - 搜索历史会话中的内容
- ✅ **优先支持** - 工单优先处理

### 🏢 Enterprise Tier ($49/月)
- ✅ **合规报告模板** - SOC2, GDPR, HIPAA 合规报告
- ✅ **导出功能** - CSV, PDF 导出
- ✅ **会话合并/对比** - 合并和对比多个会话
- ✅ **优先支持** - 专属技术支持

## 🚀 快速开始

### 安装

```bash
# 复制到 OpenClaw skills 目录
cp -r transparency ~/.openclaw/skills/
```

### 使用

在 OpenClaw 配置中启用：

```python
# config.py
skills = [
    'transparency',
    # ... 其他 skills
]
```

### 命令

```
/transparency status      # 查看当前会话状态
/transparency checkpoint  # 创建检查点
/transparency summary     # 生成会话总结
/transparency report      # 生成审计报告
```

## 📊 示例

### 示例 1：基础使用 (Free)

```python
from openclaw_transparency_mvp import TransparencyLayer

# 初始化
t = TransparencyLayer("MyAgent", tier="free")

# 追踪操作
t.track_action("file_read", "config.py", "content loaded")

# 创建检查点
t.create_checkpoint("完成初始化", ["config.py"], [])

# 结束会话
summary = t.end_session()
```

### 示例 2：多 Agent 追踪 (Pro)

```python
from openclaw_transparency_mvp import MultiAgentTracker

# 初始化多 agent 追踪器
tracker = MultiAgentTracker()

# 注册多个 agent
agent1 = tracker.register_agent("CodeAgent")
agent2 = tracker.register_agent("TestAgent")

# 追踪所有 agent
tracker.track_all("system_start", "init", "ok")

# 生成多 agent 报告
report = tracker.generate_multi_report()
```

### 示例 3：可视化报告 (Pro)

```python
from openclaw_transparency_mvp import generate_visual_report

# 生成 ASCII 报告
ascii_report = generate_visual_report(output_format="ascii")

# 生成 HTML 报告
html_report = generate_visual_report(output_format="html")
```

### 示例 4：会话搜索 (Pro)

```python
from openclaw_transparency_mvp import search_sessions

# 搜索包含 "database" 的会话
results = search_sessions("database")

# 搜索检查点
results = search_sessions("migration", search_type="checkpoints")
```

### 示例 5：合规报告 (Enterprise)

```python
from openclaw_transparency_mvp import generate_compliance_report

# 生成 SOC2 报告
soc2_report = generate_compliance_report(
    template="SOC2",
    organization="Acme Corp"
)

# 生成 GDPR 报告
gdpr_report = generate_compliance_report(
    template="GDPR",
    organization="EU Company"
)

# 生成 HIPAA 报告
hipaa_report = generate_compliance_report(
    template="HIPAA",
    organization="Healthcare Inc"
)
```

### 示例 6：导出功能 (Enterprise)

```python
from openclaw_transparency_mvp import export_sessions

# 导出为 CSV
csv_path = export_sessions(format="CSV")

# 导出为 PDF-ready HTML
pdf_path = export_sessions(format="PDF")
```

### 示例 7：会话合并/对比 (Enterprise)

```python
from openclaw_transparency_mvp import merge_sessions, compare_sessions

# 合并多个会话
merged = merge_sessions(
    session_ids=["session-1", "session-2"],
    merged_name="Combined Session"
)

# 对比两个会话
comparison = compare_sessions("session-1", "session-2")
print(f"Similarity: {comparison['similarity_score']}%")
```

## 💰 定价

### 🆓 Free
**$0/月 - 适合个人开发者**

- ✅ 基础透明度记录
- ✅ 检查点功能
- ✅ 会话总结
- ✅ JSON 数据存储
- ✅ 社区支持

### ⭐ Pro
**$9/月 - 适合小团队**

包含 Free 所有功能，加上：
- ✅ 多 agent 追踪
- ✅ 可视化报告 (ASCII + HTML)
- ✅ 会话搜索功能
- ✅ 优先工单支持

### 🏢 Enterprise
**$49/月 - 适合企业客户**

包含 Pro 所有功能，加上：
- ✅ 合规报告模板 (SOC2, GDPR, HIPAA)
- ✅ 导出功能 (CSV, PDF)
- ✅ 会话合并/对比
- ✅ 专属技术支持
- ✅ SLA 保障

## 📁 文件结构

```
transparency/
├── skill.py                        # OpenClaw skill 集成
├── openclaw_transparency_mvp.py   # 核心透明度层（所有层级）
├── README.md                       # 本文件
├── examples/                       # 使用示例
│   ├── basic_usage.py
│   └── enterprise_integration.py
└── tests/                          # 测试
    ├── test_all_tiers.py          # 完整测试套件
    └── test_comprehensive.py      # 综合测试
```

## 🔧 开发

### 运行测试

```bash
# 运行完整测试套件（所有层级）
python test_all_tiers.py

# 运行基础测试
python test_comprehensive.py
```

### 添加新功能

编辑 `openclaw_transparency_mvp.py` 并添加新方法：

```python
# Free 功能
class TransparencyLayer:
    def new_free_feature(self):
        pass

# Pro 功能
def new_pro_feature():
    pass

# Enterprise 功能
def new_enterprise_feature():
    pass
```

## 📝 更新日志

### v1.0.0 (2026-02-17)
- ✅ 完整的三层级功能实现
- ✅ Free: 基础透明度记录
- ✅ Pro: 多 agent 追踪 + 可视化 + 搜索
- ✅ Enterprise: 合规报告 + 导出 + 合并/对比
- ✅ 14 个测试全部通过
- ✅ 跨层级兼容性

### v0.1.0 (2026-02-16)
- ✅ 基础透明度记录
- ✅ 检查点功能
- ✅ 会话总结
- ✅ OpenClaw 集成

## 🧪 测试覆盖

| 层级 | 测试数量 | 状态 |
|------|---------|------|
| Free | 5 | ✅ 全部通过 |
| Pro | 4 | ✅ 全部通过 |
| Enterprise | 4 | ✅ 全部通过 |
| 跨层级 | 1 | ✅ 全部通过 |
| **总计** | **14** | **✅ 100%** |

## 🤝 贡献

基于 Entire Checkpoints ($60M seed) 开发

## 📄 License

MIT

## 🔗 相关链接

- GitHub: https://github.com/BradZhone/openclaw-transparency
- Entire Checkpoints: https://github.com/entire/checkpoints
- OpenClaw: https://openclaw.ai

---

**让你的 AI Agent 更透明、更可信！** 🚀
