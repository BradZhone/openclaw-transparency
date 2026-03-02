"""Simple multi-agent orchestration example with transparency checkpoints."""

from multi_agent_transparency import MultiAgentTransparency


def run_multi_agent_workflow(task: str) -> dict:
    mat = MultiAgentTransparency(project_name="orchestration-demo")

    mat.register_agent("Planner", "planner", ["decomposition", "routing"])
    mat.register_agent("Executor", "developer", ["implementation", "testing"])

    mat.track_interaction("Planner", "Executor", "delegation", f"Implement task: {task}")
    mat.track_interaction("Executor", "Planner", "response", "Implementation completed with tests")

    html_report = mat.generate_html_report()
    summary = mat.end_session()
    return {"summary": summary, "html_report_length": len(html_report)}
