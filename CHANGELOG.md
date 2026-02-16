# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-02-16

### Added
- **Multi-Agent Interaction Tracking** - Track interactions between multiple AI agents
  - Register multiple agents with capabilities
  - Track agent-to-agent interactions (delegation, request, response, collaboration, handoff)
  - Track coordination events (task distribution, conflict resolution, workflow orchestration)
  - Detect conflicts (resource contention, contradictory decisions)
  - Generate text-based visualization of interaction graphs
  - Auto-summarization for multi-agent sessions
  
- **New module**: `multi_agent_transparency.py`
  - `MultiAgentTransparency` class for managing multi-agent systems
  - Support for 4+ concurrent agents
  - Interaction type classification
  - Conflict detection engine
  - Visualization dashboard (text-based)

### Changed
- Better timezone handling (using `datetime.now(timezone.utc)`)
- Improved documentation structure

### Examples
- Added comprehensive multi-agent demo
- Web application development workflow example
- 4-agent system demo (Architect, Backend, Frontend, QA)

## [0.1.0] - 2026-02-16

### Added
- **Core Transparency Layer** - Basic session recording for AI agents
  - Session recording (capture prompts, tool calls, decisions)
  - Checkpoint system (create save points)
  - Auto-summarization
  - File-based storage (no database required)
  - Easy integration (2 lines of code)
  
- **Initial Release**
  - Single-file MVP (`transparency.py`)
  - MIT License
  - Basic documentation (README, QUICKSTART)
  - Setup.py for PyPI distribution

### Features
- Zero dependencies (Python stdlib only)
- Works with any AI agent (OpenAI, Claude, Gemini, etc.)
- Lightweight and simple API
- Auto-save functionality
- Session summary generation

## [Unreleased]

### Planned
- Web-based visualization dashboard
- Git integration (automatic commits)
- Export to PDF/JSON
- Cloud sync
- Enterprise features (SSO, compliance reports)
- Plugin system

---

[0.2.0]: https://github.com/BradZhone/openclaw-transparency/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/BradZhone/openclaw-transparency/releases/tag/v0.2.0
