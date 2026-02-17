#!/usr/bin/env python3
"""
Standalone Demo - OpenClaw Transparency Skill
演示版本，不依赖 OpenClaw 框架
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from openclaw_transparency_mvp import TransparencyLayer


def main():
    print("🧪 OpenClaw Transparency Layer - Standalone Demo\n")
    print("=" * 60)
    
    # 1. Initialize transparency layer
    print("\n1️⃣  Initializing Transparency Layer...")
    transparency = TransparencyLayer(
        agent_name="Demo-Agent",
        storage_path="./demo-sessions",
        auto_save=True
    )
    print()
    
    # 2. Track some actions
    print("2️⃣  Tracking AI agent actions...")
    print("-" * 60)
    
    transparency.track_action(
        action_type="prompt",
        input_data="帮我分析这个文件",
        output_data="文件分析完成",
        metadata={"file": "data.csv", "lines": 1000}
    )
    
    transparency.track_action(
        action_type="tool_call",
        input_data="read_file",
        output_data="文件内容读取成功",
        metadata={"tool": "file_reader"}
    )
    
    transparency.track_action(
        action_type="decision",
        input_data="是否删除敏感信息？",
        output_data="是，根据安全策略",
        metadata={"policy": "data-security-v1"}
    )
    
    print("\n✅ 3 actions tracked\n")
    
    # 3. Create a checkpoint
    print("3️⃣  Creating checkpoint...")
    print("-" * 60)
    
    checkpoint = transparency.create_checkpoint(
        description="完成数据分析",
        files_modified=["data.csv", "report.txt"],
        decisions=[{"type": "security", "action": "deleted_sensitive_data"}]
    )
    
    print(f"✅ Checkpoint created: {checkpoint['checkpoint_id']}\n")
    
    # 4. More actions
    print("4️⃣  More actions after checkpoint...")
    print("-" * 60)
    
    transparency.track_action(
        action_type="file_write",
        input_data="保存分析报告",
        output_data="报告已保存",
        metadata={"file": "report.txt"}
    )
    
    transparency.track_action(
        action_type="notification",
        input_data="通知用户任务完成",
        output_data="通知已发送",
        metadata={"channel": "telegram"}
    )
    
    print("\n✅ 2 more actions tracked\n")
    
    # 5. Generate summary
    print("5️⃣  Session Summary")
    print("=" * 60)
    
    summary = transparency.generate_summary()
    
    print(f"\n📋 Session ID: {summary['session_id']}")
    print(f"🤖 Agent: {summary['agent_name']}")
    print(f"⏱️  Duration: {summary['duration_seconds']:.1f} seconds")
    print(f"📝 Total Actions: {summary['total_actions']}")
    print(f"✅ Checkpoints: {summary['total_checkpoints']}")
    print(f"📁 Files Modified: {len(summary['files_modified'])}")
    print(f"💡 Key Decisions: {len(summary['key_decisions'])}")
    
    # 6. End session
    print("\n6️⃣  Ending session...")
    print("=" * 60)
    
    transparency.end_session()
    
    # 7. Show file locations
    print("\n7️⃣  Session Files")
    print("=" * 60)
    
    import os
    session_files = list(Path("./demo-sessions").glob("*.json"))
    print(f"\n📁 Session data saved to:")
    for file in session_files:
        size = os.path.getsize(file)
        print(f"   - {file.name} ({size} bytes)")
    
    print("\n" + "=" * 60)
    print("✅ Demo complete!")
    print("=" * 60)
    
    print("\n💡 Next Steps:")
    print("   1. View session files in ./demo-sessions/")
    print("   2. Integrate into OpenClaw as a skill")
    print("   3. Add to your AI agent workflow")
    print()


if __name__ == "__main__":
    main()
