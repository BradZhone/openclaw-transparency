# OpenClaw Transparency Layer

<div align="center">

**🔍 Make AI Agents Transparent & Auditable**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**Capture, track, and audit every AI agent action**

[Features](#features) • [Quick Start](#quick-start) • [Real-World Examples](#-real-world-examples) • [Documentation](#documentation) • [Roadmap](#roadmap)

</div>

---

## 🎯 What is OpenClaw Transparency Layer?

OpenClaw Transparency Layer is a lightweight, open-source solution for capturing and auditing AI agent sessions. Inspired by [Entire Checkpoints](https://github.com/entireio/cli), but designed specifically for the OpenClaw ecosystem.

### Why Transparency Matters

- **🔍 Auditability**: Know exactly what your AI agents did and why
- **🐛 Debugging**: Quickly identify where agents went wrong
- **📊 Compliance**: Generate audit trails for enterprise requirements
- **📚 Onboarding**: Help new team members understand AI workflows
- **🔄 Reproducibility**: Recreate agent sessions from any checkpoint

---

## ✨ Features

### Current Features

**v0.1.0 - Single Agent (MVP)**
- ✅ **Session Recording**: Capture every AI agent action (prompts, tool calls, decisions)
- ✅ **Checkpoint System**: Create save points at any time
- ✅ **Auto-Summarization**: Automatically generate session summaries
- ✅ **Lightweight Storage**: File-based, no database required
- ✅ **Easy Integration**: Add transparency to any OpenClaw agent in 2 lines of code

**v0.2.0 - Multi-Agent & HTML Visualization (NEW! 🚀)**
- ✅ **Multi-Agent Tracking**: Track interactions between multiple agents
- ✅ **Interaction Types**: Delegation, request, response, collaboration, handoff
- ✅ **Coordination Tracking**: Monitor agent coordination and orchestration
- ✅ **Conflict Detection**: Automatically detect resource contention and conflicts
- ✅ **HTML Visualization**: Beautiful, interactive HTML reports with Mermaid.js charts
- ✅ **Responsive Design**: Mobile-friendly reports with gradient colors
- ✅ **Timeline Visualization**: Visual timeline of agent interactions
- ✅ **Statistics Dashboard**: At-a-glance metrics with stat cards
- ✅ **4+ Concurrent Agents**: Support for complex multi-agent systems

### Coming Soon (v0.3.0)

- 🔜 **Enterprise Compliance**: HIPAA, SOX, GDPR audit reports
- 🔜 **Real-time Dashboard**: Live monitoring with WebSocket updates
- 🔜 **Git Integration**: Automatic commits on checkpoints
- 🔜 **PDF Export**: Generate PDF reports from sessions

### Future Roadmap

- 🚀 **Cloud Sync**: Sync sessions across team members
- 🚀 **AI-Powered Insights**: Get recommendations from session analysis
- 🚀 **Enterprise Features**: SSO, audit logs, compliance reports

---

## 🚀 Quick Start

### Installation

```bash
pip install openclaw-transparency
```

Or use the standalone module:

```bash
# Download the single-file MVP
curl -O https://raw.githubusercontent.com/your-username/openclaw-transparency/main/transparency.py
```

### Basic Usage

```python
from openclaw import Agent
from openclaw_transparency import TransparencyLayer

# Initialize your OpenClaw agent
agent = Agent("my-agent")

# Add transparency in 2 lines
transparency = TransparencyLayer(agent_name="my-agent")
transparency.enable()

# Now all agent actions are automatically tracked
result = agent.execute("Create a REST API endpoint")

# Create checkpoints at key moments
transparency.create_checkpoint(
    description="Completed API implementation",
    files_modified=["api.py", "test_api.py"]
)

# End session and get summary
summary = transparency.end_session()
```

### Example Output

```
✅ Transparency Layer enabled for agent: my-agent
📋 Session ID: 2026-02-16-abc123

📝 Tracked action: prompt
📝 Tracked action: tool_call
📝 Tracked action: decision
✅ Checkpoint created: a3b2c4d5e6f7

📊 Session Summary:
{
  "session_id": "2026-02-16-abc123",
  "duration_seconds": 45.2,
  "total_actions": 12,
  "total_checkpoints": 3,
  "files_modified": ["api.py", "test_api.py", "README.md"],
  "key_decisions": ["Use FastAPI framework", "Add JWT authentication"]
}
```

### Multi-Agent Usage (v0.2.0)

```python
from multi_agent_transparency import MultiAgentTransparency

# Initialize multi-agent system
multi_agent = MultiAgentTransparency(project_name="Web Application")

# Register agents
multi_agent.register_agent(
    agent_name="CodeGenerator",
    agent_type="developer",
    capabilities=["code_generation", "refactoring"]
)

multi_agent.register_agent(
    agent_name="Reviewer",
    agent_type="reviewer",
    capabilities=["code_review", "quality_check"]
)

# Track agent interactions
multi_agent.track_interaction(
    from_agent="CodeGenerator",
    to_agent="Reviewer",
    interaction_type="delegation",
    content="Please review the authentication module"
)

# Generate HTML report
html_content = multi_agent.generate_html_report()

# End session
summary = multi_agent.end_session()
```

**HTML Report Features:**
- 📊 **Interactive Graph**: Mermaid.js visualization of agent workflows
- ⏱️ **Timeline View**: Visual timeline of all interactions
- 🤖 **Agent Cards**: Beautiful cards showing agent capabilities
- 📈 **Statistics**: At-a-glance metrics (agents, interactions, conflicts)
- 🎨 **Responsive Design**: Works on desktop and mobile
- 🌈 **Modern UI**: Gradient colors, hover effects, smooth transitions

Open the generated HTML file in any browser to see the interactive report!

## 🌍 Real-World Examples

New integration examples are available in [`examples/`](examples):

- [`examples/langchain_integration.py`](examples/langchain_integration.py) — track a LangChain-style agent workflow
- [`examples/openai_function_calling.py`](examples/openai_function_calling.py) — add traceability to OpenAI function/tool calls
- [`examples/multi_agent_orchestration.py`](examples/multi_agent_orchestration.py) — trace delegation and handoffs between multiple agents
- [`examples/fastapi_integration.md`](examples/fastapi_integration.md) — production pattern for FastAPI (middleware, auth/rate-limit notes, persistence)

These examples are intentionally lightweight and dependency-minimal so contributors can adapt them quickly.

---

## 📖 Documentation

### API Reference

#### `TransparencyLayer(agent_name, storage_path, auto_save)`

Initialize transparency layer for an agent.

**Parameters:**
- `agent_name` (str): Name of your AI agent
- `storage_path` (str, optional): Where to store session data (default: `./transparency-sessions`)
- `auto_save` (bool, optional): Auto-save after each action (default: `True`)

#### `track_action(action_type, input_data, output_data, metadata)`

Manually track an agent action.

**Parameters:**
- `action_type` (str): Type of action (e.g., "prompt", "tool_call", "decision")
- `input_data` (any): Input to the action
- `output_data` (any): Output from the action
- `metadata` (dict, optional): Additional context

#### `create_checkpoint(description, files_modified, decisions)`

Create a checkpoint (save point) in the session.

**Parameters:**
- `description` (str): Human-readable description
- `files_modified` (list, optional): List of files modified
- `decisions` (list, optional): List of key decisions

#### `end_session()`

End the session and generate final summary.

**Returns:**
- `dict`: Session summary with statistics and key insights

---

## 🗺️ Roadmap

### v0.1.0 (Current - MVP)
- [x] Basic session recording
- [x] Checkpoint system
- [x] Auto-summarization
- [x] File-based storage

### v0.2.0 (Next - Week 2)
- [ ] Multi-agent interaction tracking
- [ ] Simple visualization dashboard
- [ ] Git integration
- [ ] Better error handling

### v0.3.0 (Week 4)
- [ ] Team collaboration features
- [ ] Export to PDF/JSON
- [ ] Performance optimizations
- [ ] Extended documentation

### v1.0.0 (Month 2)
- [ ] Cloud sync
- [ ] AI-powered insights
- [ ] Enterprise features
- [ ] Plugin system

---

## 💡 Use Cases

### 1. Individual Developers
```python
# Track your personal AI coding assistant
transparency = TransparencyLayer("my-coding-assistant")
# Review sessions later to improve prompts
```

### 2. Teams
```python
# Share session logs with team members
# Understand why certain decisions were made
# Onboard new developers faster
```

### 3. Enterprises
```python
# Generate compliance reports
# Audit AI usage across organization
# Meet regulatory requirements (SOC 2, HIPAA)
```

---

## 🤝 Contributing

We welcome contributions! This is an open-source project aimed at making AI agents more transparent and trustworthy.

**Ways to contribute:**
- 🐛 Report bugs
- 💡 Suggest features
- 📖 Improve documentation
- 🔧 Submit pull requests

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 📊 Comparison with Similar Tools

| Feature | OpenClaw Transparency | Entire Checkpoints | Git LFS |
|---------|----------------------|-------------------|---------|
| **Open Source** | ✅ MIT | ✅ MIT | ✅ |
| **Agent Agnostic** | ✅ | ❌ Claude/Gemini only | ✅ |
| **Multi-Agent** | 🔜 v0.2.0 | ❌ | ❌ |
| **Git Integration** | 🔜 v0.2.0 | ✅ | ✅ |
| **Visualization** | 🔜 v0.2.0 | ❌ | ❌ |
| **Easy Setup** | ✅ 2 lines | ⚠️ Git hooks | ⚠️ Config |
| **File-Based** | ✅ | ❌ Shadow branch | ✅ |

**Our Differentiation:**
- Focus on OpenClaw ecosystem
- Agent-agnostic design
- Multi-agent tracking (coming soon)
- Easier setup (no Git hooks required for basic usage)

---

## 💰 Pricing

### Open Source (Free Forever)
- ✅ Full session recording
- ✅ Checkpoint system
- ✅ Auto-summarization
- ✅ File-based storage
- ✅ Community support

### Pro ($29/month, Coming Soon)
- ✅ Everything in Open Source
- ✅ Multi-agent tracking
- ✅ Visualization dashboard
- ✅ Export to PDF/JSON
- ✅ Priority support

### Enterprise ($299/month, Coming Soon)
- ✅ Everything in Pro
- ✅ Cloud sync
- ✅ Team collaboration
- ✅ Compliance reports
- ✅ SSO integration
- ✅ Dedicated support

---

## 🙏 Acknowledgments

- Inspired by [Entire Checkpoints](https://github.com/entireio/cli) by Thomas Dohmke
- Built for the [OpenClaw](https://github.com/openclaw/openclaw) ecosystem
- Thanks to the open-source community

---

## 📜 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 📞 Contact & Community

- **GitHub Issues**: [Report bugs or request features](https://github.com/your-username/openclaw-transparency/issues)
- **Discord**: [Join our community](https://discord.gg/your-invite)
- **Twitter**: [@OpenClawAI](https://twitter.com/openclawai)

---

<div align="center">

**⭐ If this project helps you, please give it a star! ⭐**

**Made with ❤️ for the OpenClaw community**

</div>
