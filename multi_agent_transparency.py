#!/usr/bin/env python3
"""
OpenClaw Transparency Layer v0.2.0
Multi-Agent Interaction Tracking System

This extends v0.1.0 to support tracking interactions between multiple AI agents.
"""

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
import uuid
from collections import defaultdict


class MultiAgentTransparency:
    """
    Tracks interactions between multiple AI agents.
    
    Extends the basic TransparencyLayer to support:
    - Multiple concurrent agents
    - Agent-to-agent interactions
    - Coordination tracking
    - Conflict detection
    """
    
    def __init__(self, project_name: str, storage_path: str = "./multi-agent-sessions"):
        self.project_name = project_name
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # Multi-agent session
        self.session_id = self._generate_session_id()
        self.agents = {}  # agent_name -> agent_info
        self.interactions = []  # List of interactions
        self.coordinations = []  # Coordination events
        self.conflicts = []  # Detected conflicts
        
        print(f"✅ Multi-Agent Transparency Layer initialized")
        print(f"📋 Session ID: {self.session_id}")
        print(f"📁 Project: {project_name}")
    
    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        unique_id = str(uuid.uuid4())[:8]
        return f"{today}-{unique_id}"
    
    def register_agent(
        self,
        agent_name: str,
        agent_type: str,
        capabilities: Optional[List[str]] = None,
        metadata: Optional[Dict] = None
    ):
        """Register an agent in the multi-agent system"""
        if agent_name in self.agents:
            print(f"⚠️  Agent '{agent_name}' already registered")
            return
        
        agent_info = {
            "agent_name": agent_name,
            "agent_type": agent_type,
            "capabilities": capabilities or [],
            "metadata": metadata or {},
            "registered_at": datetime.now(timezone.utc).isoformat(),
            "actions_count": 0,
            "interactions_count": 0
        }
        
        self.agents[agent_name] = agent_info
        print(f"✅ Agent registered: {agent_name} ({agent_type})")
        if capabilities:
            print(f"   Capabilities: {', '.join(capabilities)}")
    
    def track_agent_action(
        self,
        agent_name: str,
        action_type: str,
        input_data: Any,
        output_data: Any,
        metadata: Optional[Dict] = None
    ):
        """Track an action performed by an agent"""
        if agent_name not in self.agents:
            print(f"❌ Agent '{agent_name}' not registered. Call register_agent() first.")
            return
        
        action_record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "agent_name": agent_name,
            "action_type": action_type,
            "input": input_data,
            "output": output_data,
            "metadata": metadata or {}
        }
        
        # Update agent stats
        self.agents[agent_name]["actions_count"] += 1
        self.agents[agent_name]["last_action"] = action_record
        
        # Store action (in agent-specific log)
        self._save_agent_action(agent_name, action_record)
        
        print(f"📝 [{agent_name}] Action: {action_type}")
        return action_record
    
    def track_interaction(
        self,
        from_agent: str,
        to_agent: str,
        interaction_type: str,
        content: Any,
        metadata: Optional[Dict] = None
    ):
        """
        Track an interaction between two agents.
        
        Interaction types:
        - "delegation": from_agent delegates task to to_agent
        - "request": from_agent requests information from to_agent
        - "response": from_agent responds to to_agent
        - "collaboration": both agents working together
        - "handoff": from_agent hands off task to to_agent
        """
        if from_agent not in self.agents or to_agent not in self.agents:
            print(f"❌ Both agents must be registered")
            return
        
        interaction = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "from_agent": from_agent,
            "to_agent": to_agent,
            "interaction_type": interaction_type,
            "content": content,
            "metadata": metadata or {},
            "interaction_id": str(uuid.uuid4())[:12]
        }
        
        self.interactions.append(interaction)
        
        # Update agent stats
        self.agents[from_agent]["interactions_count"] += 1
        self.agents[to_agent]["interactions_count"] += 1
        
        # Auto-save
        self._save_interaction(interaction)
        
        print(f"🤝 Interaction: {from_agent} → {to_agent} ({interaction_type})")
        return interaction
    
    def track_coordination(
        self,
        coordinating_agent: str,
        coordinated_agents: List[str],
        coordination_type: str,
        description: str
    ):
        """
        Track a coordination event (one agent coordinating others).
        
        Coordination types:
        - "task_distribution": distributing tasks among agents
        - "conflict_resolution": resolving conflicts between agents
        - "workflow_orchestration": orchestrating a multi-step workflow
        """
        coordination = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "coordinating_agent": coordinating_agent,
            "coordinated_agents": coordinated_agents,
            "coordination_type": coordination_type,
            "description": description,
            "coordination_id": str(uuid.uuid4())[:12]
        }
        
        self.coordinations.append(coordination)
        self._save_coordination(coordination)
        
        print(f"🎯 Coordination: {coordinating_agent} coordinates {len(coordinated_agents)} agents")
        return coordination
    
    def detect_conflicts(self):
        """
        Detect potential conflicts between agents.
        
        Conflict types:
        - Resource contention (same file/resource)
        - Contradictory decisions
        - Deadlock (circular dependencies)
        """
        conflicts = []
        
        # Check for file conflicts
        file_usage = defaultdict(list)
        for agent_name, agent_info in self.agents.items():
            if "last_action" in agent_info:
                last_action = agent_info["last_action"]
                if "files_modified" in last_action.get("metadata", {}):
                    for file in last_action["metadata"]["files_modified"]:
                        file_usage[file].append(agent_name)
        
        for file, agents in file_usage.items():
            if len(agents) > 1:
                conflict = {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "conflict_type": "resource_contention",
                    "resource": file,
                    "agents_involved": agents,
                    "description": f"Multiple agents modifying same file: {file}"
                }
                conflicts.append(conflict)
                self.conflicts.append(conflict)
                print(f"⚠️  Conflict detected: {file} (agents: {', '.join(agents)})")
        
        return conflicts
    
    def generate_visualization(self):
        """
        Generate a text-based visualization of the multi-agent interaction graph.
        
        Returns a simple ASCII diagram showing agents and their interactions.
        """
        print("\n" + "="*80)
        print("📊 Multi-Agent Interaction Visualization")
        print("="*80)
        
        # Agent summary
        print("\n🤖 Agents:")
        for agent_name, agent_info in self.agents.items():
            print(f"  • {agent_name} ({agent_info['agent_type']})")
            print(f"    Actions: {agent_info['actions_count']}, Interactions: {agent_info['interactions_count']}")
            if agent_info['capabilities']:
                print(f"    Capabilities: {', '.join(agent_info['capabilities'])}")
        
        # Interaction flow
        print("\n🤝 Interaction Flow:")
        for interaction in self.interactions[-10:]:  # Show last 10
            arrow = "→"
            print(f"  {interaction['from_agent']} {arrow} {interaction['to_agent']}")
            print(f"    Type: {interaction['interaction_type']}")
            print(f"    Time: {interaction['timestamp']}")
        
        # Coordination events
        if self.coordinations:
            print("\n🎯 Coordination Events:")
            for coord in self.coordinations[-5:]:
                print(f"  {coord['coordinating_agent']} coordinates {len(coord['coordinated_agents'])} agents")
                print(f"    Type: {coord['coordination_type']}")
                print(f"    Description: {coord['description']}")
        
        # Conflicts
        if self.conflicts:
            print("\n⚠️  Detected Conflicts:")
            for conflict in self.conflicts:
                print(f"  {conflict['conflict_type']}: {conflict['description']}")
                print(f"    Agents: {', '.join(conflict['agents_involved'])}")
        
        print("\n" + "="*80)
    
    def _save_agent_action(self, agent_name: str, action: Dict):
        """Save agent action to file"""
        agent_log = self.storage_path / f"{agent_name}-actions.jsonl"
        with open(agent_log, 'a') as f:
            f.write(json.dumps(action) + "\n")
    
    def _save_interaction(self, interaction: Dict):
        """Save interaction to file"""
        interactions_file = self.storage_path / "interactions.jsonl"
        with open(interactions_file, 'a') as f:
            f.write(json.dumps(interaction) + "\n")
    
    def _save_coordination(self, coordination: Dict):
        """Save coordination to file"""
        coordinations_file = self.storage_path / "coordinations.jsonl"
        with open(coordinations_file, 'a') as f:
            f.write(json.dumps(coordination) + "\n")
    
    def generate_summary(self) -> Dict:
        """Generate comprehensive session summary"""
        summary = {
            "session_id": self.session_id,
            "project_name": self.project_name,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "agents": {
                name: {
                    "type": info["agent_type"],
                    "actions": info["actions_count"],
                    "interactions": info["interactions_count"]
                }
                for name, info in self.agents.items()
            },
            "statistics": {
                "total_agents": len(self.agents),
                "total_interactions": len(self.interactions),
                "total_coordinations": len(self.coordinations),
                "detected_conflicts": len(self.conflicts)
            },
            "interaction_types": self._get_interaction_type_breakdown(),
            "most_active_agents": self._get_most_active_agents(),
            "conflict_summary": [c["description"] for c in self.conflicts]
        }
        
        return summary
    
    def _get_interaction_type_breakdown(self) -> Dict[str, int]:
        """Get breakdown of interaction types"""
        breakdown = defaultdict(int)
        for interaction in self.interactions:
            breakdown[interaction["interaction_type"]] += 1
        return dict(breakdown)
    
    def _get_most_active_agents(self) -> List[str]:
        """Get most active agents by action count"""
        sorted_agents = sorted(
            self.agents.items(),
            key=lambda x: x[1]["actions_count"],
            reverse=True
        )
        return [name for name, _ in sorted_agents[:3]]
    
    def generate_html_report(self, output_path: Optional[str] = None) -> str:
        """
        Generate an interactive HTML report with visualizations.
        
        Args:
            output_path: Where to save the HTML report. If None, uses default path.
        
        Returns:
            HTML content as string
        """
        from html_report_generator import HTMLReportGenerator
        
        # Generate summary first
        summary = self.generate_summary()
        
        # Determine output path
        if output_path is None:
            output_path = self.storage_path / f"{self.session_id}-report.html"
        else:
            output_path = Path(output_path)
        
        # Generate HTML report
        generator = HTMLReportGenerator()
        html_content = generator.generate_report(
            summary=summary,
            interactions=self.interactions,
            agents=self.agents,
            conflicts=self.conflicts,
            coordinations=self.coordinations,
            output_path=str(output_path)
        )
        
        print(f"\n📊 HTML report generated: {output_path}")
        return html_content
    
    def end_session(self) -> Dict:
        """End the session and generate final summary"""
        # Detect any remaining conflicts
        self.detect_conflicts()
        
        # Generate summary
        summary = self.generate_summary()
        
        # Save summary
        summary_file = self.storage_path / f"{self.session_id}-summary.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        # Print summary
        print("\n" + "="*80)
        print("📊 Multi-Agent Session Summary")
        print("="*80)
        print(f"Session ID: {self.session_id}")
        print(f"Project: {self.project_name}")
        print(f"\n🤖 Agents: {summary['statistics']['total_agents']}")
        print(f"🤝 Interactions: {summary['statistics']['total_interactions']}")
        print(f"🎯 Coordinations: {summary['statistics']['total_coordinations']}")
        print(f"⚠️  Conflicts: {summary['statistics']['detected_conflicts']}")
        print(f"\n🏆 Most Active: {', '.join(summary['most_active_agents'])}")
        print(f"\n💾 Session data saved to: {self.storage_path}")
        print("="*80 + "\n")
        
        return summary


# Demo: Multi-Agent Transparency
def demo_multi_agent():
    """Demonstrate multi-agent interaction tracking"""
    
    print("="*80)
    print("🚀 Multi-Agent Transparency Layer v0.2.0 Demo")
    print("="*80)
    print()
    
    # Initialize multi-agent system
    multi_agent = MultiAgentTransparency(
        project_name="Web Application Development"
    )
    
    print("\n--- Step 1: Register Agents ---\n")
    
    # Register agents
    multi_agent.register_agent(
        agent_name="ArchitectAgent",
        agent_type="designer",
        capabilities=["system_design", "architecture_planning", "technology_selection"]
    )
    
    multi_agent.register_agent(
        agent_name="BackendAgent",
        agent_type="developer",
        capabilities=["api_development", "database_design", "authentication"]
    )
    
    multi_agent.register_agent(
        agent_name="FrontendAgent",
        agent_type="developer",
        capabilities=["ui_implementation", "state_management", "api_integration"]
    )
    
    multi_agent.register_agent(
        agent_name="QAAgent",
        agent_type="tester",
        capabilities=["test_planning", "test_automation", "bug_reporting"]
    )
    
    time.sleep(1)
    
    print("\n--- Step 2: Track Agent Actions ---\n")
    
    # Architect designs the system
    multi_agent.track_agent_action(
        agent_name="ArchitectAgent",
        action_type="design",
        input_data="Design REST API architecture",
        output_data={
            "architecture": "Microservices",
            "database": "PostgreSQL",
            "framework": "FastAPI"
        },
        metadata={
            "decisions": ["Use JWT for auth", "Implement rate limiting"],
            "files_modified": ["architecture.md"]
        }
    )
    
    time.sleep(1)
    
    # Backend implements API
    multi_agent.track_agent_action(
        agent_name="BackendAgent",
        action_type="code_generation",
        input_data="Implement authentication endpoints",
        output_data={
            "files_created": ["auth.py", "models.py"],
            "endpoints": ["/login", "/register", "/refresh"]
        },
        metadata={
            "files_modified": ["auth.py", "models.py"]
        }
    )
    
    time.sleep(1)
    
    # Frontend implements UI
    multi_agent.track_agent_action(
        agent_name="FrontendAgent",
        action_type="code_generation",
        input_data="Implement login UI",
        output_data={
            "files_created": ["Login.tsx"],
            "components": ["LoginForm", "AuthContext"]
        },
        metadata={
            "files_modified": ["Login.tsx", "AuthContext.tsx"]
        }
    )
    
    time.sleep(1)
    
    print("\n--- Step 3: Track Agent Interactions ---\n")
    
    # Architect delegates to Backend
    multi_agent.track_interaction(
        from_agent="ArchitectAgent",
        to_agent="BackendAgent",
        interaction_type="delegation",
        content="Implement the authentication system as per design",
        metadata={"priority": "high"}
    )
    
    time.sleep(1)
    
    # Backend requests review from Architect
    multi_agent.track_interaction(
        from_agent="BackendAgent",
        to_agent="ArchitectAgent",
        interaction_type="request",
        content="Review authentication implementation",
        metadata={"request_type": "code_review"}
    )
    
    time.sleep(1)
    
    # Backend hands off to Frontend
    multi_agent.track_interaction(
        from_agent="BackendAgent",
        to_agent="FrontendAgent",
        interaction_type="handoff",
        content="Authentication API ready for integration",
        metadata={
            "api_endpoints": ["/login", "/register"],
            "documentation": "API docs attached"
        }
    )
    
    time.sleep(1)
    
    # Frontend and Backend collaborate
    multi_agent.track_interaction(
        from_agent="FrontendAgent",
        to_agent="BackendAgent",
        interaction_type="collaboration",
        content="Discussing API response format",
        metadata={"issue": "CORS configuration needed"}
    )
    
    time.sleep(1)
    
    print("\n--- Step 4: Track Coordination ---\n")
    
    # QA coordinates testing
    multi_agent.track_coordination(
        coordinating_agent="QAAgent",
        coordinated_agents=["BackendAgent", "FrontendAgent"],
        coordination_type="workflow_orchestration",
        description="Coordinating end-to-end testing of authentication flow"
    )
    
    time.sleep(1)
    
    print("\n--- Step 5: Detect Conflicts ---\n")
    
    # Detect potential conflicts
    conflicts = multi_agent.detect_conflicts()
    if conflicts:
        print(f"⚠️  Found {len(conflicts)} potential conflict(s)")
    else:
        print("✅ No conflicts detected")
    
    time.sleep(1)
    
    print("\n--- Step 6: Generate Visualization ---\n")
    
    # Generate text visualization
    multi_agent.generate_visualization()
    
    print("\n--- Step 7: End Session ---\n")
    
    # End session and get summary
    summary = multi_agent.end_session()
    
    print("\n📊 Full Summary:")
    print(json.dumps(summary, indent=2))
    
    print("\n✅ Demo completed successfully!")
    print(f"📁 Check the ./multi-agent-sessions/ directory for detailed logs")


if __name__ == "__main__":
    demo_multi_agent()
