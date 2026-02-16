# Quick Start Guide

## 5-Minute Tutorial

### Step 1: Download

```bash
# Option A: Clone the repository
git clone https://github.com/openclaw/transparency-layer.git
cd transparency-layer

# Option B: Download single file
curl -O https://raw.githubusercontent.com/openclaw/transparency-layer/main/transparency.py
```

### Step 2: Try the Demo

```bash
python3 transparency.py
```

You'll see output like:

```
✅ Transparency Layer enabled for agent: CodeGeneratorAgent
📋 Session ID: 2026-02-16-5f57cc46
📝 Tracked action: prompt
📝 Tracked action: tool_call
...
✅ Demo completed successfully!
```

### Step 3: Use in Your Project

```python
from transparency import TransparencyLayer

# Initialize
transparency = TransparencyLayer(agent_name="my-agent")

# Track an action
transparency.track_action(
    action_type="prompt",
    input_data="Create a REST API",
    output_data="I'll create a FastAPI endpoint",
    metadata={"user": "brad"}
)

# Create checkpoint
transparency.create_checkpoint(
    description="API design complete",
    files_modified=["api.py"]
)

# End session
summary = transparency.end_session()
print(summary)
```

### Step 4: Explore Session Data

```bash
ls transparency-sessions/
# You'll see:
# - 2026-02-16-5f57cc46.json (full session)
# - 2026-02-16-5f57cc46-summary.json (summary)
```

## Common Use Cases

### Use Case 1: Debug AI Agent

```python
# When agent goes wrong, check session log
transparency.track_action(
    action_type="error",
    input_data="...",
    output_data="Error: ...",
    metadata={"error_type": "tool_failure"}
)
```

### Use Case 2: Share with Team

```bash
# Share session file with teammate
git add transparency-sessions/2026-02-16-*.json
git commit -m "Add session log for review"
git push
```

### Use Case 3: Generate Report

```python
# Auto-summary gives you key insights
summary = transparency.end_session()
# Use summary for reports, documentation, etc.
```

## Next Steps

- Read the [README.md](README.md) for full documentation
- Check out [examples/](examples/) for more use cases
- Star the repo on GitHub if this helps you!

## Questions?

- Open a [GitHub Issue](https://github.com/openclaw/transparency-layer/issues)
- Join our [Discord](https://discord.gg/your-invite)

**Happy transparent coding! 🎉**
