#!/usr/bin/env python3
"""
OpenClaw Transparency Layer MVP
A simplified session recording system for AI agents

This is a proof-of-concept demonstrating how to capture AI agent sessions
without requiring Git hooks or complex infrastructure.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import uuid


class TransparencyLayer:
    """
    Captures and stores AI agent session data for transparency and auditability.
    
    This is a simplified version inspired by Entire Checkpoints.
    Full version would integrate with Git hooks and support multi-agent tracking.
    """
    
    def __init__(
        self,
        agent_name: str,
        storage_path: str = "./transparency-sessions",
        auto_save: bool = True
    ):
        self.agent_name = agent_name
        self.storage_path = Path(storage_path)
        self.auto_save = auto_save
        
        # Create session
        self.session_id = self._generate_session_id()
        self.session_data = {
            "session_id": self.session_id,
            "agent_name": agent_name,
            "start_time": datetime.utcnow().isoformat(),
            "checkpoints": [],
            "actions": [],
            "metadata": {}
        }
        
        # Create storage directory
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        print(f"✅ Transparency Layer enabled for agent: {agent_name}")
        print(f"📋 Session ID: {self.session_id}")
    
    def _generate_session_id(self) -> str:
        """Generate a unique session ID (format: YYYY-MM-DD-<UUID>)"""
        today = datetime.utcnow().strftime("%Y-%m-%d")
        unique_id = str(uuid.uuid4())[:8]
        return f"{today}-{unique_id}"
    
    def track_action(
        self,
        action_type: str,
        input_data: Any,
        output_data: Any,
        metadata: Optional[Dict] = None
    ):
        """
        Track an agent action.
        
        Args:
            action_type: Type of action (e.g., "prompt", "tool_call", "decision")
            input_data: Input to the action
            output_data: Output from the action
            metadata: Additional context about the action
        """
        action_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "action_type": action_type,
            "input": input_data,
            "output": output_data,
            "metadata": metadata or {}
        }
        
        self.session_data["actions"].append(action_record)
        
        if self.auto_save:
            self._save_session()
        
        print(f"📝 Tracked action: {action_type}")
        return action_record
    
    def create_checkpoint(
        self,
        description: str,
        files_modified: Optional[List[str]] = None,
        decisions: Optional[List[Dict]] = None
    ):
        """
        Create a checkpoint (save point) in the session.
        
        Args:
            description: Human-readable description of the checkpoint
            files_modified: List of files modified since last checkpoint
            decisions: List of key decisions made
        """
        checkpoint_id = str(uuid.uuid4())[:12]  # 12-char hex
        
        checkpoint = {
            "checkpoint_id": checkpoint_id,
            "timestamp": datetime.utcnow().isoformat(),
            "description": description,
            "files_modified": files_modified or [],
            "decisions": decisions or [],
            "action_count": len(self.session_data["actions"])
        }
        
        self.session_data["checkpoints"].append(checkpoint)
        
        if self.auto_save:
            self._save_session()
        
        print(f"✅ Checkpoint created: {checkpoint_id}")
        print(f"   Description: {description}")
        return checkpoint
    
    def _save_session(self):
        """Save session data to file"""
        session_file = self.storage_path / f"{self.session_id}.json"
        with open(session_file, 'w') as f:
            json.dump(self.session_data, f, indent=2)
    
    def generate_summary(self) -> Dict:
        """
        Generate a summary of the session (auto-summarization).
        
        In a full version, this would use AI to generate natural language summaries.
        """
        summary = {
            "session_id": self.session_id,
            "agent_name": self.agent_name,
            "duration_seconds": self._calculate_duration(),
            "total_actions": len(self.session_data["actions"]),
            "total_checkpoints": len(self.session_data["checkpoints"]),
            "action_breakdown": self._get_action_breakdown(),
            "files_modified": self._get_all_modified_files(),
            "key_decisions": self._extract_key_decisions()
        }
        
        return summary
    
    def _calculate_duration(self) -> float:
        """Calculate session duration in seconds"""
        if not self.session_data["actions"]:
            return 0
        
        start = datetime.fromisoformat(self.session_data["start_time"])
        last_action = datetime.fromisoformat(self.session_data["actions"][-1]["timestamp"])
        return (last_action - start).total_seconds()
    
    def _get_action_breakdown(self) -> Dict[str, int]:
        """Get breakdown of action types"""
        breakdown = {}
        for action in self.session_data["actions"]:
            action_type = action["action_type"]
            breakdown[action_type] = breakdown.get(action_type, 0) + 1
        return breakdown
    
    def _get_all_modified_files(self) -> List[str]:
        """Get all files modified in this session"""
        files = set()
        for checkpoint in self.session_data["checkpoints"]:
            files.update(checkpoint.get("files_modified", []))
        return sorted(list(files))
    
    def _extract_key_decisions(self) -> List[str]:
        """Extract key decisions from checkpoints"""
        decisions = []
        for checkpoint in self.session_data["checkpoints"]:
            for decision in checkpoint.get("decisions", []):
                if isinstance(decision, dict):
                    decisions.append(decision.get("description", str(decision)))
                else:
                    decisions.append(str(decision))
        return decisions
    
    def end_session(self):
        """End the session and save final state"""
        self.session_data["end_time"] = datetime.utcnow().isoformat()
        self._save_session()
        
        summary = self.generate_summary()
        summary_file = self.storage_path / f"{self.session_id}-summary.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n📊 Session ended: {self.session_id}")
        print(f"⏱️  Duration: {summary['duration_seconds']:.1f} seconds")
        print(f"📝 Total actions: {summary['total_actions']}")
        print(f"✅ Checkpoints: {summary['total_checkpoints']}")
        print(f"📁 Files modified: {len(summary['files_modified'])}")
        print(f"💡 Key decisions: {len(summary['key_decisions'])}")
        print(f"\n💾 Session data saved to: {self.storage_path}")
        
        return summary


# Demo: Using the Transparency Layer
def demo_transparency_layer():
    """Demonstrate how to use the Transparency Layer with an AI agent"""
    
    print("=" * 80)
    print("🚀 OpenClaw Transparency Layer MVP Demo")
    print("=" * 80)
    print()
    
    # Initialize transparency layer for an agent
    transparency = TransparencyLayer(
        agent_name="CodeGeneratorAgent",
        storage_path="./demo-sessions"
    )
    
    print("\n--- Simulating AI Agent Workflow ---\n")
    
    # Action 1: Agent receives a prompt
    print("Step 1: Agent receives user prompt")
    transparency.track_action(
        action_type="prompt",
        input_data="Create a REST API endpoint for user authentication",
        output_data="I'll create a FastAPI endpoint with JWT authentication",
        metadata={
            "user": "brad",
            "context": "Building authentication system"
        }
    )
    time.sleep(1)
    
    # Action 2: Agent makes a tool call
    print("\nStep 2: Agent reads existing code")
    transparency.track_action(
        action_type="tool_call",
        input_data={
            "tool": "read_file",
            "file": "auth.py"
        },
        output_data={
            "status": "success",
            "content": "Existing authentication logic found"
        },
        metadata={
            "reason": "Need to understand existing implementation"
        }
    )
    time.sleep(1)
    
    # Action 3: Agent makes a decision
    print("\nStep 3: Agent decides on approach")
    transparency.track_action(
        action_type="decision",
        input_data="Choose authentication method",
        output_data="Use JWT with refresh tokens",
        metadata={
            "alternatives": ["Session-based", "OAuth", "JWT"],
            "reasoning": "JWT is stateless and scalable"
        }
    )
    time.sleep(1)
    
    # Create first checkpoint
    print("\nStep 4: Create checkpoint after planning")
    transparency.create_checkpoint(
        description="Completed planning phase for authentication endpoint",
        files_modified=["auth.py"],
        decisions=[
            {
                "description": "Use JWT authentication",
                "rationale": "Stateless and scalable"
            },
            {
                "description": "Implement refresh token rotation",
                "rationale": "Security best practice"
            }
        ]
    )
    time.sleep(1)
    
    # Action 4: Agent writes code
    print("\nStep 5: Agent writes authentication code")
    transparency.track_action(
        action_type="code_generation",
        input_data="Implement JWT authentication endpoint",
        output_data={
            "file": "auth.py",
            "lines_added": 45,
            "lines_removed": 3
        },
        metadata={
            "approach": "Incremental enhancement of existing code"
        }
    )
    time.sleep(1)
    
    # Action 5: Agent runs tests
    print("\nStep 6: Agent tests the implementation")
    transparency.track_action(
        action_type="tool_call",
        input_data={
            "tool": "run_tests",
            "test_file": "test_auth.py"
        },
        output_data={
            "status": "passed",
            "tests_run": 5,
            "tests_passed": 5
        },
        metadata={
            "test_framework": "pytest"
        }
    )
    time.sleep(1)
    
    # Create final checkpoint
    print("\nStep 7: Create checkpoint after implementation")
    transparency.create_checkpoint(
        description="Completed JWT authentication endpoint implementation",
        files_modified=["auth.py", "test_auth.py"],
        decisions=[
            {
                "description": "Add rate limiting",
                "rationale": "Prevent brute force attacks"
            }
        ]
    )
    
    # End session and generate summary
    print("\n--- Ending Session ---\n")
    summary = transparency.end_session()
    
    # Display summary
    print("\n📊 Session Summary:")
    print(json.dumps(summary, indent=2))
    
    print("\n✅ Demo completed successfully!")
    print(f"📁 Check the ./demo-sessions/ directory for session data")


if __name__ == "__main__":
    demo_transparency_layer()
