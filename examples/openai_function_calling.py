"""OpenAI function-calling style integration example for Transparency Layer."""

from transparency import TransparencyLayer


def call_openai_function(user_input: str) -> dict:
    transparency = TransparencyLayer(agent_name="openai-function-agent")

    transparency.track_action(
        action_type="prompt",
        input_data=user_input,
        output_data="Preparing function-calling request",
        metadata={"provider": "openai", "mode": "function_calling"},
    )

    # Pseudocode placeholder for external SDK call:
    # response = client.responses.create(...)
    response = {
        "model": "gpt-4.1",
        "tool_call": "search_docs",
        "arguments": {"query": user_input},
    }

    transparency.track_action(
        action_type="tool_call",
        input_data={"tool": "search_docs", "query": user_input},
        output_data=response,
    )

    transparency.end_session()
    return response
