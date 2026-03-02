"""LangChain integration example for OpenClaw Transparency Layer."""

from transparency import TransparencyLayer


def run_langchain_agent(query: str) -> str:
    """Pseudo-example showing how to wrap a LangChain call with transparency."""
    transparency = TransparencyLayer(agent_name="langchain-agent")

    transparency.track_action(
        action_type="prompt",
        input_data=query,
        output_data="Dispatching query to LangChain agent",
        metadata={"framework": "langchain"},
    )

    # Pseudocode to avoid adding a hard dependency in example docs:
    # from langchain.agents import initialize_agent
    # agent = initialize_agent(tools, llm, agent="zero-shot-react-description")
    # response = agent.run(query)
    response = f"[demo] handled by LangChain agent: {query}"

    transparency.create_checkpoint(
        description="LangChain request handled",
        files_modified=[],
        decisions=["Used zero-shot-react-description style agent"],
    )

    transparency.end_session()
    return response
