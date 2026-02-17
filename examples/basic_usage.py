#!/usr/bin/env python3
"""
Basic Usage Example - OpenClaw Transparency Skill
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from skill import TransparencySkill


def main():
    print("🧪 OpenClaw Transparency Skill - Basic Usage\n")
    
    # 1. Initialize transparency skill
    print("1️⃣  Initializing Transparency Skill...")
    transparency = TransparencySkill()
    print()
    
    # 2. Track some actions
    print("2️⃣  Tracking AI agent actions...")
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
    print("✅ 3 actions tracked\n")
    
    # 3. Create a checkpoint
    print("3️⃣  Creating checkpoint...")
    transparency.transparency.create_checkpoint(
        description="完成数据分析",
        files_modified=["data.csv", "report.txt"],
        decisions=[{"type": "security", "action": "deleted_sensitive_data"}]
    )
    print()
    
    # 4. Get status
    print("4️⃣  Checking status...")
    status = transparency._get_status()
    print(status)
    
    # 5. Generate summary
    print("5️⃣  Generating summary...")
    summary = transparency._get_summary()
    print(summary)
    
    # 6. Export report
    print("6️⃣  Exporting audit report...")
    report = transparency._get_report()
    print(report[:500] + "...")  # Print first 500 chars
    
    print("\n✅ Demo complete!")
    print(f"📁 Session data saved to: ./openclaw-sessions/")


if __name__ == "__main__":
    main()
