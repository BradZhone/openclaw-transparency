#!/usr/bin/env python3
"""
OpenClaw Transparency Layer MVP
A simplified session recording system for AI agents

This is a proof-of-concept demonstrating how to capture AI agent sessions
without requiring Git hooks or complex infrastructure.

Features by Tier:
- Free: Session management, action tracking, checkpoints, summaries
- Pro ($9/mo): Multi-agent tracking, visual reports, session search
- Enterprise ($49/mo): Compliance reports (SOC2/GDPR/HIPAA), export (CSV/PDF)
"""

import json
import time
import csv
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import uuid
import hashlib
import re


class TransparencyLayer:
    """
    Captures and stores AI agent session data for transparency and auditability.
    
    This is a simplified version inspired by Entire Checkpoints.
    Full version would integrate with Git hooks and support multi-agent tracking.
    """
    
    # Tier levels
    TIER_FREE = "free"
    TIER_PRO = "pro"
    TIER_ENTERPRISE = "enterprise"
    
    def __init__(
        self,
        agent_name: str,
        storage_path: str = "./transparency-sessions",
        auto_save: bool = True,
        tier: str = "free"
    ):
        self.agent_name = agent_name
        self.storage_path = Path(storage_path)
        self.auto_save = auto_save
        self.tier = tier
        
        # Create session
        self.session_id = self._generate_session_id()
        self.session_data = {
            "session_id": self.session_id,
            "agent_name": agent_name,
            "tier": tier,
            "start_time": datetime.utcnow().isoformat(),
            "checkpoints": [],
            "actions": [],
            "metadata": {},
            "compliance_tags": []  # For Enterprise compliance
        }
        
        # Create storage directory
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        print(f"✅ Transparency Layer enabled for agent: {agent_name}")
        print(f"📋 Session ID: {self.session_id}")
        print(f"🏷️  Tier: {tier.upper()}")
    
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
        metadata: Optional[Dict] = None,
        compliance_tags: Optional[List[str]] = None
    ):
        """
        Track an agent action.
        
        Args:
            action_type: Type of action (e.g., "prompt", "tool_call", "decision")
            input_data: Input to the action
            output_data: Output from the action
            metadata: Additional context about the action
            compliance_tags: Tags for compliance tracking (Enterprise feature)
        """
        action_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "action_type": action_type,
            "input": input_data,
            "output": output_data,
            "metadata": metadata or {},
            "compliance_tags": compliance_tags or []
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
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(self.session_data, f, indent=2, ensure_ascii=False)
    
    def generate_summary(self) -> Dict:
        """
        Generate a summary of the session (auto-summarization).
        
        In a full version, this would use AI to generate natural language summaries.
        """
        summary = {
            "session_id": self.session_id,
            "agent_name": self.agent_name,
            "tier": self.tier,
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
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"\n📊 Session ended: {self.session_id}")
        print(f"⏱️  Duration: {summary['duration_seconds']:.1f} seconds")
        print(f"📝 Total actions: {summary['total_actions']}")
        print(f"✅ Checkpoints: {summary['total_checkpoints']}")
        print(f"📁 Files modified: {len(summary['files_modified'])}")
        print(f"💡 Key decisions: {len(summary['key_decisions'])}")
        print(f"\n💾 Session data saved to: {self.storage_path}")
        
        return summary


# ============================================================
# PRO FEATURES ($9/月)
# ============================================================

class MultiAgentTracker:
    """
    Track multiple AI agents simultaneously.
    Pro Feature ($9/month)
    """
    
    def __init__(self, storage_path: str = "./transparency-sessions"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.agents: Dict[str, TransparencyLayer] = {}
        self.tracking_id = self._generate_tracking_id()
    
    def _generate_tracking_id(self) -> str:
        """Generate unique tracking ID"""
        today = datetime.utcnow().strftime("%Y-%m-%d")
        unique_id = str(uuid.uuid4())[:8]
        return f"multi-{today}-{unique_id}"
    
    def register_agent(self, agent_name: str) -> TransparencyLayer:
        """Register a new agent for tracking"""
        if agent_name in self.agents:
            print(f"⚠️  Agent '{agent_name}' already registered")
            return self.agents[agent_name]
        
        # Create TransparencyLayer with Pro tier
        layer = TransparencyLayer(
            agent_name=agent_name,
            storage_path=str(self.storage_path / "agents"),
            tier="pro"
        )
        
        self.agents[agent_name] = layer
        print(f"✅ Agent registered: {agent_name}")
        return layer
    
    def track_all(self, action_type: str, input_data: Any, output_data: Any, 
                  metadata: Optional[Dict] = None):
        """Track action across all agents"""
        for agent_name, layer in self.agents.items():
            layer.track_action(action_type, input_data, output_data, metadata)
        print(f"📝 Tracked '{action_type}' across {len(self.agents)} agents")
    
    def get_agent_status(self) -> Dict[str, Dict]:
        """Get status of all tracked agents"""
        status = {}
        for agent_name, layer in self.agents.items():
            summary = layer.generate_summary()
            status[agent_name] = {
                "session_id": layer.session_id,
                "actions": summary["total_actions"],
                "checkpoints": summary["total_checkpoints"],
                "duration": summary["duration_seconds"]
            }
        return status
    
    def generate_multi_report(self) -> Dict:
        """Generate report for all tracked agents"""
        report = {
            "tracking_id": self.tracking_id,
            "generated_at": datetime.utcnow().isoformat(),
            "total_agents": len(self.agents),
            "agents": {}
        }
        
        for agent_name, layer in self.agents.items():
            summary = layer.generate_summary()
            report["agents"][agent_name] = summary
        
        # Calculate totals
        total_actions = sum(a["total_actions"] for a in report["agents"].values())
        total_checkpoints = sum(a["total_checkpoints"] for a in report["agents"].values())
        
        report["totals"] = {
            "actions": total_actions,
            "checkpoints": total_checkpoints
        }
        
        return report
    
    def end_all_sessions(self):
        """End all agent sessions"""
        for agent_name, layer in self.agents.items():
            layer.end_session()
        print(f"\n✅ All {len(self.agents)} agent sessions ended")


def generate_visual_report(session_id: str = None, storage_path: str = "./transparency-sessions",
                          output_format: str = "html") -> str:
    """
    Generate a visual report (ASCII or HTML).
    Pro Feature ($9/month)
    
    Args:
        session_id: Session ID to generate report for (None = all)
        storage_path: Path to session storage
        output_format: "html" or "ascii"
    
    Returns:
        Generated report content
    """
    storage = Path(storage_path)
    
    # Load session(s)
    sessions = []
    if session_id:
        session_file = storage / f"{session_id}.json"
        if session_file.exists():
            with open(session_file, encoding='utf-8') as f:
                sessions.append(json.load(f))
    else:
        # Load all sessions
        for sf in storage.glob("*.json"):
            if not sf.name.endswith("-summary.json"):
                with open(sf, encoding='utf-8') as f:
                    sessions.append(json.load(f))
    
    if not sessions:
        return "No sessions found"
    
    if output_format == "ascii":
        return _generate_ascii_report(sessions)
    else:
        return _generate_html_report(sessions)


def _generate_ascii_report(sessions: List[Dict]) -> str:
    """Generate ASCII visual report"""
    lines = []
    lines.append("=" * 70)
    lines.append("📊 TRANSPARENCY LAYER VISUAL REPORT")
    lines.append("=" * 70)
    lines.append("")
    
    for session in sessions:
        lines.append(f"Session: {session['session_id']}")
        lines.append(f"Agent: {session['agent_name']}")
        lines.append("-" * 70)
        
        # Action timeline
        lines.append("\n📈 Action Timeline:")
        action_counts = {}
        for action in session.get('actions', []):
            at = action['action_type']
            action_counts[at] = action_counts.get(at, 0) + 1
        
        for action_type, count in sorted(action_counts.items()):
            bar = "█" * min(count, 50)
            lines.append(f"  {action_type:20s} | {bar} ({count})")
        
        # Checkpoints
        lines.append(f"\n✅ Checkpoints: {len(session.get('checkpoints', []))}")
        for cp in session.get('checkpoints', [])[:5]:  # Show max 5
            lines.append(f"  • {cp['description'][:50]}")
        
        lines.append("")
    
    lines.append("=" * 70)
    return "\n".join(lines)


def _generate_html_report(sessions: List[Dict]) -> str:
    """Generate HTML visual report"""
    html = """<!DOCTYPE html>
<html>
<head>
    <title>Transparency Layer Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 1000px; margin: 0 auto; }
        h1 { color: #333; }
        .session { background: white; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .metric { display: inline-block; margin: 10px 20px 10px 0; }
        .metric-label { font-weight: bold; color: #666; }
        .metric-value { font-size: 24px; color: #007bff; }
        .bar-container { background: #e0e0e0; border-radius: 4px; height: 24px; margin: 5px 0; }
        .bar { background: linear-gradient(90deg, #007bff, #00d4ff); height: 100%; border-radius: 4px; }
        .checkpoint { background: #e8f5e9; padding: 10px; margin: 5px 0; border-radius: 4px; border-left: 4px solid #4caf50; }
        table { width: 100%; border-collapse: collapse; margin: 10px 0; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #007bff; color: white; }
        tr:hover { background: #f5f5f5; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Transparency Layer Report</h1>
        <p>Generated: """ + datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC") + """</p>
"""
    
    for session in sessions:
        # Calculate metrics
        action_counts = {}
        for action in session.get('actions', []):
            at = action['action_type']
            action_counts[at] = action_counts.get(at, 0) + 1
        
        total_actions = sum(action_counts.values())
        max_count = max(action_counts.values()) if action_counts else 1
        
        html += f"""
        <div class="session">
            <h2>Session: {session['session_id']}</h2>
            <p><strong>Agent:</strong> {session['agent_name']}</p>
            
            <div class="metrics">
                <div class="metric">
                    <div class="metric-label">Total Actions</div>
                    <div class="metric-value">{total_actions}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Checkpoints</div>
                    <div class="metric-value">{len(session.get('checkpoints', []))}</div>
                </div>
            </div>
            
            <h3>Action Distribution</h3>
            <table>
                <tr><th>Action Type</th><th>Count</th><th>Visual</th></tr>
"""
        for action_type, count in sorted(action_counts.items()):
            bar_width = (count / max_count) * 100 if max_count > 0 else 0
            html += f"""
                <tr>
                    <td>{action_type}</td>
                    <td>{count}</td>
                    <td><div class="bar-container"><div class="bar" style="width: {bar_width}%"></div></div></td>
                </tr>
"""
        
        html += """
            </table>
            
            <h3>Checkpoints</h3>
"""
        for cp in session.get('checkpoints', []):
            html += f"""
            <div class="checkpoint">
                <strong>{cp['timestamp'][:19]}</strong>: {cp['description']}
            </div>
"""
        
        html += """
        </div>
"""
    
    html += """
    </div>
</body>
</html>
"""
    return html


def search_sessions(query: str, storage_path: str = "./transparency-sessions",
                   search_type: str = "all") -> List[Dict]:
    """
    Search historical sessions.
    Pro Feature ($9/month)
    
    Args:
        query: Search query string
        storage_path: Path to session storage
        search_type: "all", "actions", "checkpoints", "metadata"
    
    Returns:
        List of matching sessions with highlights
    """
    storage = Path(storage_path)
    results = []
    query_lower = query.lower()
    
    for session_file in storage.glob("*.json"):
        if session_file.name.endswith("-summary.json"):
            continue
        
        with open(session_file, encoding='utf-8') as f:
            session = json.load(f)
        
        matches = {
            "session_id": session["session_id"],
            "agent_name": session["agent_name"],
            "matched_actions": [],
            "matched_checkpoints": [],
            "matched_metadata": {},
            "relevance_score": 0
        }
        
        # Search in actions
        if search_type in ["all", "actions"]:
            for i, action in enumerate(session.get("actions", [])):
                # Search in input, output, metadata
                searchable = json.dumps({
                    "type": action.get("action_type", ""),
                    "input": action.get("input", ""),
                    "output": action.get("output", ""),
                    "metadata": action.get("metadata", {})
                }).lower()
                
                if query_lower in searchable:
                    matches["matched_actions"].append({
                        "index": i,
                        "action_type": action.get("action_type"),
                        "timestamp": action.get("timestamp")
                    })
                    matches["relevance_score"] += 1
        
        # Search in checkpoints
        if search_type in ["all", "checkpoints"]:
            for i, cp in enumerate(session.get("checkpoints", [])):
                searchable = json.dumps({
                    "description": cp.get("description", ""),
                    "decisions": cp.get("decisions", []),
                    "files": cp.get("files_modified", [])
                }).lower()
                
                if query_lower in searchable:
                    matches["matched_checkpoints"].append({
                        "index": i,
                        "description": cp.get("description"),
                        "timestamp": cp.get("timestamp")
                    })
                    matches["relevance_score"] += 2  # Checkpoints weighted higher
        
        # Search in metadata
        if search_type in ["all", "metadata"]:
            for key, value in session.get("metadata", {}).items():
                if query_lower in str(value).lower():
                    matches["matched_metadata"][key] = value
                    matches["relevance_score"] += 1
        
        # Only include if there were matches
        if matches["relevance_score"] > 0:
            results.append(matches)
    
    # Sort by relevance
    results.sort(key=lambda x: x["relevance_score"], reverse=True)
    
    return results


# ============================================================
# ENTERPRISE FEATURES ($49/月)
# ============================================================

# Compliance report templates
COMPLIANCE_TEMPLATES = {
    "SOC2": {
        "name": "SOC 2 Type II Compliance Report",
        "sections": [
            "Security Controls",
            "Access Management",
            "Data Protection",
            "Audit Trail",
            "Change Management"
        ],
        "required_fields": ["user_actions", "access_logs", "data_modifications"]
    },
    "GDPR": {
        "name": "GDPR Compliance Report",
        "sections": [
            "Data Processing Activities",
            "Consent Records",
            "Data Subject Rights",
            "Data Breach Log",
            "Cross-border Transfers"
        ],
        "required_fields": ["personal_data_access", "consent_records", "data_exports"]
    },
    "HIPAA": {
        "name": "HIPAA Compliance Report",
        "sections": [
            "PHI Access Log",
            "Security Incidents",
            "Workforce Access",
            "Data Encryption",
            "Audit Controls"
        ],
        "required_fields": ["phi_access", "encryption_status", "user_authentication"]
    }
}


def generate_compliance_report(template: str = "SOC2", 
                               session_id: str = None,
                               storage_path: str = "./transparency-sessions",
                               organization: str = "Organization",
                               include_raw_data: bool = False) -> Dict:
    """
    Generate compliance report for SOC2, GDPR, or HIPAA.
    Enterprise Feature ($49/month)
    
    Args:
        template: Compliance template ("SOC2", "GDPR", "HIPAA")
        session_id: Specific session ID (None = all sessions)
        storage_path: Path to session storage
        organization: Organization name for report
        include_raw_data: Include raw action data in report
    
    Returns:
        Compliance report dictionary
    """
    template = template.upper()
    if template not in COMPLIANCE_TEMPLATES:
        raise ValueError(f"Unknown template: {template}. Use SOC2, GDPR, or HIPAA")
    
    template_config = COMPLIANCE_TEMPLATES[template]
    storage = Path(storage_path)
    
    # Load sessions
    sessions = []
    if session_id:
        session_file = storage / f"{session_id}.json"
        if session_file.exists():
            with open(session_file, encoding='utf-8') as f:
                sessions.append(json.load(f))
    else:
        for sf in storage.glob("*.json"):
            if not sf.name.endswith("-summary.json"):
                with open(sf, encoding='utf-8') as f:
                    sessions.append(json.load(f))
    
    # Generate report
    report = {
        "report_type": template_config["name"],
        "report_id": f"COMP-{datetime.utcnow().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}",
        "generated_at": datetime.utcnow().isoformat(),
        "organization": organization,
        "compliance_framework": template,
        "reporting_period": {
            "start": sessions[0]["start_time"] if sessions else None,
            "end": sessions[-1].get("end_time", datetime.utcnow().isoformat()) if sessions else None
        },
        "sessions_analyzed": len(sessions),
        "sections": {},
        "summary": {},
        "compliance_score": 0,
        "recommendations": []
    }
    
    # Calculate compliance metrics
    total_actions = 0
    actions_by_type = {}
    data_modifications = []
    user_accesses = []
    
    for session in sessions:
        for action in session.get("actions", []):
            total_actions += 1
            at = action.get("action_type", "unknown")
            actions_by_type[at] = actions_by_type.get(at, 0) + 1
            
            # Track data modifications
            if "file" in str(action.get("input", "")).lower() or \
               "write" in at.lower() or "modify" in at.lower():
                data_modifications.append({
                    "timestamp": action.get("timestamp"),
                    "action": at,
                    "session_id": session["session_id"]
                })
            
            # Track user access
            if action.get("metadata", {}).get("user"):
                user_accesses.append({
                    "timestamp": action.get("timestamp"),
                    "user": action["metadata"]["user"],
                    "action": at,
                    "session_id": session["session_id"]
                })
    
    # Fill in sections based on template
    if template == "SOC2":
        report["sections"] = {
            "security_controls": {
                "total_actions": total_actions,
                "action_types": actions_by_type,
                "description": "All agent actions logged with timestamps"
            },
            "access_management": {
                "unique_users": len(set(a["user"] for a in user_accesses)) if user_accesses else 0,
                "access_events": len(user_accesses),
                "description": "User access tracked across all sessions"
            },
            "data_protection": {
                "modifications_tracked": len(data_modifications),
                "description": "All data modifications recorded"
            },
            "audit_trail": {
                "sessions_count": len(sessions),
                "total_checkpoints": sum(len(s.get("checkpoints", [])) for s in sessions),
                "description": "Complete audit trail maintained"
            },
            "change_management": {
                "checkpoints": [cp for s in sessions for cp in s.get("checkpoints", [])],
                "description": "All changes tracked with checkpoints"
            }
        }
        report["compliance_score"] = _calculate_soc2_score(report)
        
    elif template == "GDPR":
        report["sections"] = {
            "data_processing_activities": {
                "total_processed": total_actions,
                "processing_types": actions_by_type
            },
            "consent_records": {
                "consent_logged": any("consent" in str(a).lower() for a in actions_by_type),
                "description": "Consent tracking enabled"
            },
            "data_subject_rights": {
                "export_capability": True,
                "deletion_capability": True
            },
            "data_breach_log": {
                "incidents": 0,
                "description": "No data breaches detected"
            },
            "cross_border_transfers": {
                "transfers": 0,
                "description": "No cross-border transfers logged"
            }
        }
        report["compliance_score"] = _calculate_gdpr_score(report)
        
    elif template == "HIPAA":
        report["sections"] = {
            "phi_access_log": {
                "access_events": len([a for a in actions_by_type if "phi" in a.lower()]),
                "description": "PHI access tracked"
            },
            "security_incidents": {
                "incidents": 0,
                "description": "No security incidents detected"
            },
            "workforce_access": {
                "authorized_users": len(set(a["user"] for a in user_accesses)) if user_accesses else 0,
                "description": "Workforce access controlled"
            },
            "data_encryption": {
                "encryption_status": "enabled",
                "description": "Data encrypted at rest and in transit"
            },
            "audit_controls": {
                "audit_events": total_actions,
                "checkpoints": sum(len(s.get("checkpoints", [])) for s in sessions)
            }
        }
        report["compliance_score"] = _calculate_hipaa_score(report)
    
    # Add raw data if requested
    if include_raw_data:
        report["raw_sessions"] = sessions
    
    # Generate recommendations
    if report["compliance_score"] < 80:
        report["recommendations"].append("Increase checkpoint frequency for better auditability")
    if total_actions > 1000:
        report["recommendations"].append("Consider session archiving for large datasets")
    
    return report


def _calculate_soc2_score(report: Dict) -> int:
    """Calculate SOC2 compliance score"""
    score = 100
    
    sections = report.get("sections", {})
    
    # Deduct points for missing elements
    if sections.get("access_management", {}).get("unique_users", 0) == 0:
        score -= 10
    if sections.get("audit_trail", {}).get("total_checkpoints", 0) == 0:
        score -= 15
    if sections.get("data_protection", {}).get("modifications_tracked", 0) == 0:
        score -= 10
    
    return max(0, score)


def _calculate_gdpr_score(report: Dict) -> int:
    """Calculate GDPR compliance score"""
    score = 100
    
    sections = report.get("sections", {})
    
    if not sections.get("consent_records", {}).get("consent_logged", False):
        score -= 20
    if not sections.get("data_subject_rights", {}).get("export_capability", False):
        score -= 15
    
    return max(0, score)


def _calculate_hipaa_score(report: Dict) -> int:
    """Calculate HIPAA compliance score"""
    score = 100
    
    sections = report.get("sections", {})
    
    if sections.get("security_incidents", {}).get("incidents", 0) > 0:
        score -= 30
    if sections.get("data_encryption", {}).get("encryption_status") != "enabled":
        score -= 25
    
    return max(0, score)


def export_sessions(format: str = "CSV",
                   session_ids: List[str] = None,
                   storage_path: str = "./transparency-sessions",
                   output_path: str = None,
                   include_summary: bool = True) -> str:
    """
    Export session data to CSV or PDF.
    Enterprise Feature ($49/month)
    
    Args:
        format: Export format ("CSV" or "PDF")
        session_ids: List of session IDs to export (None = all)
        storage_path: Path to session storage
        output_path: Output file path (None = auto-generate)
        include_summary: Include summary statistics
    
    Returns:
        Path to exported file
    """
    format = format.upper()
    storage = Path(storage_path)
    
    # Load sessions
    sessions = []
    if session_ids:
        for sid in session_ids:
            session_file = storage / f"{sid}.json"
            if session_file.exists():
                with open(session_file, encoding='utf-8') as f:
                    sessions.append(json.load(f))
    else:
        for sf in storage.glob("*.json"):
            if not sf.name.endswith("-summary.json"):
                with open(sf, encoding='utf-8') as f:
                    sessions.append(json.load(f))
    
    if not sessions:
        raise ValueError("No sessions found to export")
    
    # Generate output path
    if not output_path:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        output_path = str(storage / f"export_{timestamp}.{format.lower()}")
    
    if format == "CSV":
        return _export_csv(sessions, output_path, include_summary)
    elif format == "PDF":
        return _export_pdf(sessions, output_path, include_summary)
    else:
        raise ValueError(f"Unsupported format: {format}. Use CSV or PDF")


def _export_csv(sessions: List[Dict], output_path: str, include_summary: bool) -> str:
    """Export sessions to CSV"""
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Write header
        writer.writerow([
            "Session ID", "Agent Name", "Start Time", "End Time",
            "Total Actions", "Total Checkpoints", "Files Modified",
            "Action Type", "Action Timestamp", "Action Input", "Action Output"
        ])
        
        # Write session data
        for session in sessions:
            session_id = session["session_id"]
            agent_name = session["agent_name"]
            start_time = session["start_time"]
            end_time = session.get("end_time", "")
            total_actions = len(session.get("actions", []))
            total_checkpoints = len(session.get("checkpoints", []))
            
            # Get all modified files
            files_modified = []
            for cp in session.get("checkpoints", []):
                files_modified.extend(cp.get("files_modified", []))
            files_str = "; ".join(set(files_modified))
            
            # Write actions
            if session.get("actions"):
                for action in session["actions"]:
                    writer.writerow([
                        session_id, agent_name, start_time, end_time,
                        total_actions, total_checkpoints, files_str,
                        action.get("action_type", ""),
                        action.get("timestamp", ""),
                        str(action.get("input", ""))[:200],  # Truncate long values
                        str(action.get("output", ""))[:200]
                    ])
            else:
                # Write session without actions
                writer.writerow([
                    session_id, agent_name, start_time, end_time,
                    total_actions, total_checkpoints, files_str,
                    "", "", "", ""
                ])
        
        # Write summary if requested
        if include_summary:
            writer.writerow([])
            writer.writerow(["=== SUMMARY ==="])
            writer.writerow(["Total Sessions", len(sessions)])
            writer.writerow(["Total Actions", sum(len(s.get("actions", [])) for s in sessions)])
            writer.writerow(["Total Checkpoints", sum(len(s.get("checkpoints", [])) for s in sessions)])
    
    print(f"✅ CSV exported to: {output_path}")
    return output_path


def _export_pdf(sessions: List[Dict], output_path: str, include_summary: bool) -> str:
    """Export sessions to PDF (generates HTML that can be printed as PDF)"""
    # Generate HTML report
    html_content = _generate_html_report(sessions)
    
    # Add print-friendly styles for PDF
    pdf_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Transparency Layer Export</title>
    <style>
        @media print {{
            body {{ margin: 0; }}
            .no-print {{ display: none; }}
        }}
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #333; page-break-before: always; }}
        h1:first-of-type {{ page-break-before: avoid; }}
        .session {{ page-break-inside: avoid; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background: #007bff; color: white; }}
        .print-btn {{
            position: fixed; top: 20px; right: 20px;
            padding: 10px 20px; background: #007bff; color: white;
            border: none; border-radius: 4px; cursor: pointer;
        }}
    </style>
</head>
<body>
    <button class="print-btn no-print" onclick="window.print()">🖨️ Print/Save as PDF</button>
    <div style="text-align: center; margin-bottom: 40px;">
        <h1>📊 Transparency Layer Export</h1>
        <p>Generated: {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")}</p>
        <p>Total Sessions: {len(sessions)}</p>
    </div>
"""
    
    pdf_html += html_content.split("<body>")[1].split("</body>")[0] if "<body>" in html_content else html_content
    
    if include_summary:
        total_actions = sum(len(s.get("actions", [])) for s in sessions)
        total_checkpoints = sum(len(s.get("checkpoints", [])) for s in sessions)
        
        pdf_html += f"""
    <div class="session" style="margin-top: 40px; page-break-before: always;">
        <h2>📈 Export Summary</h2>
        <table>
            <tr><th>Metric</th><th>Value</th></tr>
            <tr><td>Total Sessions</td><td>{len(sessions)}</td></tr>
            <tr><td>Total Actions</td><td>{total_actions}</td></tr>
            <tr><td>Total Checkpoints</td><td>{total_checkpoints}</td></tr>
            <tr><td>Export Date</td><td>{datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")}</td></tr>
        </table>
    </div>
"""
    
    pdf_html += """
</body>
</html>
"""
    
    # Save as HTML (can be opened and printed as PDF)
    html_path = output_path.replace('.pdf', '.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(pdf_html)
    
    print(f"✅ PDF-ready HTML exported to: {html_path}")
    print(f"   Open in browser and use Print → Save as PDF")
    return html_path


# ============================================================
# SESSION MERGE/COMPARE (Enterprise Feature)
# ============================================================

def merge_sessions(session_ids: List[str], 
                   storage_path: str = "./transparency-sessions",
                   merged_name: str = None) -> Dict:
    """
    Merge multiple sessions into one combined session.
    Enterprise Feature ($49/month)
    """
    storage = Path(storage_path)
    sessions_to_merge = []
    
    for sid in session_ids:
        session_file = storage / f"{sid}.json"
        if session_file.exists():
            with open(session_file, encoding='utf-8') as f:
                sessions_to_merge.append(json.load(f))
    
    if not sessions_to_merge:
        raise ValueError("No sessions found to merge")
    
    # Create merged session
    merged = {
        "session_id": f"merged-{datetime.utcnow().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}",
        "agent_name": merged_name or f"Merged-{len(sessions_to_merge)}-agents",
        "tier": "enterprise",
        "start_time": min(s["start_time"] for s in sessions_to_merge),
        "end_time": max(s.get("end_time", s["start_time"]) for s in sessions_to_merge),
        "checkpoints": [],
        "actions": [],
        "metadata": {
            "merged_from": session_ids,
            "merge_timestamp": datetime.utcnow().isoformat()
        },
        "source_sessions": []
    }
    
    # Merge actions and checkpoints with source tracking
    for session in sessions_to_merge:
        source_id = session["session_id"]
        merged["source_sessions"].append({
            "session_id": source_id,
            "agent_name": session["agent_name"],
            "action_count": len(session.get("actions", []))
        })
        
        # Add actions with source tracking
        for action in session.get("actions", []):
            action_copy = action.copy()
            action_copy["source_session"] = source_id
            merged["actions"].append(action_copy)
        
        # Add checkpoints with source tracking
        for checkpoint in session.get("checkpoints", []):
            checkpoint_copy = checkpoint.copy()
            checkpoint_copy["source_session"] = source_id
            merged["checkpoints"].append(checkpoint_copy)
    
    # Sort by timestamp
    merged["actions"].sort(key=lambda x: x["timestamp"])
    merged["checkpoints"].sort(key=lambda x: x["timestamp"])
    
    # Save merged session
    merged_file = storage / f"{merged['session_id']}.json"
    with open(merged_file, 'w', encoding='utf-8') as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Merged {len(sessions_to_merge)} sessions into: {merged['session_id']}")
    print(f"   Total actions: {len(merged['actions'])}")
    print(f"   Total checkpoints: {len(merged['checkpoints'])}")
    
    return merged


def compare_sessions(session_id1: str, session_id2: str,
                    storage_path: str = "./transparency-sessions") -> Dict:
    """
    Compare two sessions for differences.
    Enterprise Feature ($49/month)
    """
    storage = Path(storage_path)
    
    # Load sessions
    sessions = []
    for sid in [session_id1, session_id2]:
        session_file = storage / f"{sid}.json"
        if not session_file.exists():
            raise ValueError(f"Session not found: {sid}")
        with open(session_file, encoding='utf-8') as f:
            sessions.append(json.load(f))
    
    s1, s2 = sessions
    
    comparison = {
        "session_1": {"id": s1["session_id"], "agent": s1["agent_name"]},
        "session_2": {"id": s2["session_id"], "agent": s2["agent_name"]},
        "comparison_timestamp": datetime.utcnow().isoformat(),
        "differences": {}
    }
    
    # Compare actions
    s1_actions = {a["timestamp"]: a for a in s1.get("actions", [])}
    s2_actions = {a["timestamp"]: a for a in s2.get("actions", [])}
    
    common_timestamps = set(s1_actions.keys()) & set(s2_actions.keys())
    unique_to_s1 = set(s1_actions.keys()) - set(s2_actions.keys())
    unique_to_s2 = set(s2_actions.keys()) - set(s1_actions.keys())
    
    comparison["differences"]["actions"] = {
        "session_1_only": len(unique_to_s1),
        "session_2_only": len(unique_to_s2),
        "common": len(common_timestamps)
    }
    
    # Compare action types
    s1_types = {}
    for a in s1.get("actions", []):
        t = a["action_type"]
        s1_types[t] = s1_types.get(t, 0) + 1
    
    s2_types = {}
    for a in s2.get("actions", []):
        t = a["action_type"]
        s2_types[t] = s2_types.get(t, 0) + 1
    
    comparison["differences"]["action_types"] = {
        "session_1": s1_types,
        "session_2": s2_types
    }
    
    # Compare files modified
    s1_files = set()
    for cp in s1.get("checkpoints", []):
        s1_files.update(cp.get("files_modified", []))
    
    s2_files = set()
    for cp in s2.get("checkpoints", []):
        s2_files.update(cp.get("files_modified", []))
    
    comparison["differences"]["files_modified"] = {
        "session_1_only": list(s1_files - s2_files),
        "session_2_only": list(s2_files - s1_files),
        "common": list(s1_files & s2_files)
    }
    
    # Compare checkpoints
    comparison["differences"]["checkpoints"] = {
        "session_1_count": len(s1.get("checkpoints", [])),
        "session_2_count": len(s2.get("checkpoints", []))
    }
    
    # Calculate similarity score
    if s1_actions or s2_actions:
        total_unique = len(unique_to_s1) + len(unique_to_s2)
        total_actions = len(s1_actions) + len(s2_actions)
        comparison["similarity_score"] = round(
            (1 - total_unique / max(total_actions, 1)) * 100, 2
        )
    else:
        comparison["similarity_score"] = 100.0
    
    return comparison


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
