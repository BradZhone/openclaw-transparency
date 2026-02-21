"""
LangChain Integration Example
Demonstrates how to add transparency to LangChain agents

This is the #1 requested integration - shows how easy it is to make
LangChain agents transparent and auditable.
"""

from openclaw_transparency import TransparencyLayer
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool

# Initialize Transparency Layer
transparency = TransparencyLayer(
    api_key="your-api-key",
    project_name="langchain-agent-demo"
)

# Create LangChain LLM
llm = ChatOpenAI(
    model="gpt-4",
    temperature=0
)

# Define tools
@transparency.track()
def search_tool(query: str) -> str:
    """Search for information"""
    # Simulated search
    return f"Search results for: {query}"

@transparency.track()
def calculator_tool(expression: str) -> str:
    """Calculate mathematical expressions"""
    try:
        result = eval(expression)
        transparency.checkpoint(f"calculation_result: {result}")
        return str(result)
    except Exception as e:
        return f"Error: {e}"

# Create LangChain tools
tools = [
    Tool(
        name="Search",
        func=search_tool,
        description="Search for information"
    ),
    Tool(
        name="Calculator",
        func=calculator_tool,
        description="Calculate mathematical expressions"
    )
]

# Initialize agent with transparency
@transparency.track()
def run_agent(user_input: str):
    """Run LangChain agent with full transparency tracking"""
    
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    
    # Create checkpoint before agent execution
    transparency.checkpoint(f"agent_start: {user_input}")
    
    result = agent.run(user_input)
    
    # Create checkpoint after agent execution
    transparency.checkpoint(f"agent_result: {result}")
    
    return result

# Example usage
if __name__ == "__main__":
    print("🔍 LangChain Agent with Transparency Layer\n")
    
    # Run agent
    result = run_agent("What is 25 * 4 + 10?")
    print(f"\n✅ Result: {result}")
    
    # Get audit trail
    audit_trail = transparency.get_audit_trail()
    print(f"\n📊 Audit Trail:")
    for event in audit_trail:
        print(f"  - {event['timestamp']}: {event['action']} -> {event['result']}")
    
    # Generate compliance report
    report = transparency.generate_report(format="gdpr")
    print(f"\n📄 GDPR Compliance Report generated")
    print(f"   Report ID: {report['report_id']}")
    print(f"   Total actions tracked: {report['total_actions']}")
    print(f"   Checkpoints created: {report['checkpoints']}")
