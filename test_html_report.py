#!/usr/bin/env python3
"""
Demo: HTML Report Generation
Test the new HTML visualization feature
"""

import sys
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from multi_agent_transparency import MultiAgentTransparency


def main():
    print("🧪 Testing HTML Report Generation")
    print("=" * 80)
    
    # Initialize multi-agent system
    multi_agent = MultiAgentTransparency(
        project_name="HTML Report Test"
    )
    
    print("\n1️⃣  Registering agents...")
    multi_agent.register_agent(
        agent_name="CodeGenerator",
        agent_type="developer",
        capabilities=["code_generation", "refactoring", "debugging"]
    )
    
    multi_agent.register_agent(
        agent_name="Reviewer",
        agent_type="reviewer",
        capabilities=["code_review", "quality_check"]
    )
    
    multi_agent.register_agent(
        agent_name="Deployer",
        agent_type="manager",
        capabilities=["deployment", "monitoring", "rollback"]
    )
    
    time.sleep(1)
    
    print("\n2️⃣  Tracking agent actions...")
    multi_agent.track_agent_action(
        agent_name="CodeGenerator",
        action_type="code_generation",
        input_data="Create authentication module",
        output_data="Generated auth.py with JWT support",
        metadata={"files_modified": ["auth.py"]}
    )
    
    time.sleep(1)
    
    print("\n3️⃣  Tracking interactions...")
    multi_agent.track_interaction(
        from_agent="CodeGenerator",
        to_agent="Reviewer",
        interaction_type="delegation",
        content="Please review the authentication module",
        metadata={"priority": "high"}
    )
    
    time.sleep(1)
    
    multi_agent.track_interaction(
        from_agent="Reviewer",
        to_agent="CodeGenerator",
        interaction_type="response",
        content="Code review completed. Found 2 minor issues.",
        metadata={"issues": 2}
    )
    
    time.sleep(1)
    
    multi_agent.track_interaction(
        from_agent="CodeGenerator",
        to_agent="Deployer",
        interaction_type="handoff",
        content="Authentication module ready for deployment",
        metadata={"version": "1.0.0"}
    )
    
    time.sleep(1)
    
    print("\n4️⃣  Tracking coordination...")
    multi_agent.track_coordination(
        coordinating_agent="Deployer",
        coordinated_agents=["CodeGenerator", "Reviewer"],
        coordination_type="workflow_orchestration",
        description="Coordinating final deployment of authentication system"
    )
    
    time.sleep(1)
    
    print("\n5️⃣  Generating HTML report...")
    html_content = multi_agent.generate_html_report()
    
    time.sleep(1)
    
    print("\n6️⃣  Ending session...")
    summary = multi_agent.end_session()
    
    print("\n" + "=" * 80)
    print("✅ Test complete!")
    print("=" * 80)
    
    print(f"\n📊 Session Summary:")
    print(f"  - Agents: {summary['statistics']['total_agents']}")
    print(f"  - Interactions: {summary['statistics']['total_interactions']}")
    print(f"  - Coordinations: {summary['statistics']['total_coordinations']}")
    print(f"  - Conflicts: {summary['statistics']['detected_conflicts']}")
    
    print(f"\n📁 Files generated:")
    print(f"  - Session data: {multi_agent.storage_path}")
    print(f"  - HTML report: {multi_agent.storage_path}/{multi_agent.session_id}-report.html")
    
    print(f"\n💡 Next steps:")
    print(f"  1. Open the HTML report in a browser")
    print(f"  2. View the interactive visualizations")
    print(f"  3. Check the agent interaction graph")


if __name__ == "__main__":
    main()
