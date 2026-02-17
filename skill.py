#!/usr/bin/env python3
"""
OpenClaw Transparency Skill
Integrates Transparency Layer into OpenClaw as a skill
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import Dict, Any, Optional
from openclaw import Skill, Context, Message
from openclaw_transparency_mvp import TransparencyLayer


class TransparencySkill(Skill):
    """
    OpenClaw Skill for AI Agent Transparency
    
    Features:
    - Automatic action tracking
    - Checkpoint creation
    - Session summaries
    - Audit reports
    """
    
    name = 'transparency'
    description = 'AI Agent 透明度记录和审计'
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        
        # Initialize transparency layer
        self.transparency = TransparencyLayer(
            agent_name="OpenClaw-Agent",
            storage_path="./openclaw-sessions",
            auto_save=True
        )
        
        print("✅ Transparency Skill enabled")
    
    async def execute(self, context: Context, message: Message) -> str:
        """
        Execute transparency tracking
        
        Commands:
        - /transparency status - Show current session status
        - /transparency checkpoint - Create a checkpoint
        - /transparency summary - Generate session summary
        - /transparency report - Generate audit report
        """
        
        # Extract command
        command = message.content.lower().strip()
        
        # Track this action
        self.transparency.track_action(
            action_type="transparency_command",
            input_data=command,
            output_data="Processing...",
            metadata={"user": message.author if hasattr(message, 'author') else "unknown"}
        )
        
        # Handle commands
        if "status" in command:
            return self._get_status()
        elif "checkpoint" in command:
            return await self._create_checkpoint(message)
        elif "summary" in command:
            return self._get_summary()
        elif "report" in command:
            return self._get_report()
        else:
            return self._help()
    
    def _get_status(self) -> str:
        """Get current session status"""
        session = self.transparency.session_data
        
        status = f"""📊 **Transparency Status**

📋 **Session ID:** {session['session_id']}
🤖 **Agent:** {session['agent_name']}
⏱️  **Started:** {session['start_time']}
📝 **Actions:** {len(session['actions'])}
✅ **Checkpoints:** {len(session['checkpoints'])}
"""
        return status
    
    async def _create_checkpoint(self, message: Message) -> str:
        """Create a checkpoint"""
        
        # Extract description from message
        parts = message.content.split("checkpoint", 1)
        description = parts[1].strip() if len(parts) > 1 else "Manual checkpoint"
        
        # Create checkpoint
        checkpoint = self.transparency.create_checkpoint(
            description=description,
            files_modified=[],  # Would be populated by file operations
            decisions=[]
        )
        
        return f"""✅ **Checkpoint Created**

📋 **ID:** {checkpoint['checkpoint_id']}
📝 **Description:** {description}
⏰ **Time:** {checkpoint['timestamp']}
"""
    
    def _get_summary(self) -> str:
        """Generate session summary"""
        summary = self.transparency.generate_summary()
        
        return f"""📊 **Session Summary**

📋 **Session ID:** {summary['session_id']}
⏱️  **Duration:** {summary['duration']}
📝 **Total Actions:** {summary['total_actions']}
✅ **Checkpoints:** {summary['checkpoints']}
📁 **Files Modified:** {summary['files_modified']}
💡 **Key Decisions:** {summary['key_decisions']}
"""
    
    def _get_report(self) -> str:
        """Generate audit report"""
        report = self.transparency.export_session()
        
        return f"""📋 **Audit Report**

{report}

✅ Report generated successfully
"""
    
    def _help(self) -> str:
        """Show help"""
        return """🤖 **Transparency Skill Help**

**Commands:**
- `/transparency status` - Show current session status
- `/transparency checkpoint [description]` - Create a checkpoint
- `/transparency summary` - Generate session summary
- `/transparency report` - Generate audit report

**What it does:**
- Automatically tracks all AI agent actions
- Creates checkpoints for important decisions
- Generates transparency reports
- Enables audit and compliance

**Example:**
```
User: /transparency checkpoint Fixed critical bug
AI: ✅ Checkpoint Created
```
"""
    
    def track_action(
        self,
        action_type: str,
        input_data: Any,
        output_data: Any,
        metadata: Optional[Dict] = None
    ):
        """
        Public method for other skills to track actions
        """
        return self.transparency.track_action(
            action_type=action_type,
            input_data=input_data,
            output_data=output_data,
            metadata=metadata
        )


# Export
__all__ = ['TransparencySkill']


if __name__ == "__main__":
    # Test the skill
    print("🧪 Testing Transparency Skill...")
    
    skill = TransparencySkill()
    
    # Simulate tracking
    skill.track_action(
        action_type="test",
        input_data="test input",
        output_data="test output"
    )
    
    # Create checkpoint
    skill.transparency.create_checkpoint("Test checkpoint")
    
    # Generate summary
    print(skill._get_summary())
    
    print("✅ Test complete!")
