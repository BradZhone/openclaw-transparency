#!/usr/bin/env python3
"""
HTML Report Generator for Multi-Agent Transparency Layer
Generates beautiful, interactive HTML reports with visualizations
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any
import base64


class HTMLReportGenerator:
    """Generate interactive HTML reports for multi-agent sessions"""
    
    def __init__(self):
        self.template_dir = Path(__file__).parent / "templates"
        self.static_dir = Path(__file__).parent / "static"
    
    def generate_report(
        self,
        summary: Dict,
        interactions: List[Dict],
        agents: Dict,
        conflicts: List[Dict],
        coordinations: List[Dict],
        output_path: str = None
    ) -> str:
        """
        Generate a complete HTML report
        
        Args:
            summary: Session summary
            interactions: List of agent interactions
            agents: Agent information
            conflicts: Detected conflicts
            coordinations: Coordination events
            output_path: Where to save the report
        
        Returns:
            HTML content as string
        """
        # Generate Mermaid diagrams
        interaction_graph = self._generate_interaction_graph(interactions, agents)
        timeline_chart = self._generate_timeline_chart(interactions)
        
        # Generate statistics cards
        stats_html = self._generate_stats_cards(summary)
        
        # Generate agent cards
        agents_html = self._generate_agent_cards(agents)
        
        # Generate interaction list
        interactions_html = self._generate_interaction_list(interactions)
        
        # Generate conflicts section
        conflicts_html = self._generate_conflicts_section(conflicts)
        
        # Generate coordinations section
        coordinations_html = self._generate_coordinations_section(coordinations)
        
        # Build complete HTML
        html = self._build_html(
            title=f"Multi-Agent Transparency Report - {summary['session_id']}",
            stats=stats_html,
            agents=agents_html,
            interaction_graph=interaction_graph,
            timeline=timeline_chart,
            interactions=interactions_html,
            conflicts=conflicts_html,
            coordinations=coordinations_html,
            summary=summary
        )
        
        # Save if path provided
        if output_path:
            Path(output_path).write_text(html)
            print(f"✅ HTML report saved to: {output_path}")
        
        return html
    
    def _generate_interaction_graph(self, interactions: List[Dict], agents: Dict) -> str:
        """Generate Mermaid flowchart for agent interactions"""
        if not interactions:
            return "<p>No interactions to display</p>"
        
        # Build Mermaid graph
        lines = ["```mermaid", "graph TD"]
        
        # Add agent nodes
        for agent_name, agent_info in agents.items():
            node_type = agent_info.get('agent_type', 'unknown')
            emoji = self._get_agent_emoji(node_type)
            lines.append(f"    {agent_name}[{emoji} {agent_name}]")
        
        # Add interaction edges
        for interaction in interactions[:20]:  # Limit to 20 most recent
            from_agent = interaction['from_agent']
            to_agent = interaction['to_agent']
            interaction_type = interaction['interaction_type']
            
            # Use different arrow styles for different interaction types
            arrow = self._get_arrow_style(interaction_type)
            label = interaction_type.replace('_', ' ').title()
            
            lines.append(f"    {from_agent} {arrow}|{label}| {to_agent}")
        
        lines.append("```")
        
        return "\n".join(lines)
    
    def _generate_timeline_chart(self, interactions: List[Dict]) -> str:
        """Generate a timeline visualization"""
        if not interactions:
            return "<p>No timeline data</p>"
        
        # Simple text-based timeline
        lines = ["<div class='timeline'>"]
        
        for interaction in interactions[:15]:
            timestamp = interaction['timestamp']
            from_agent = interaction['from_agent']
            to_agent = interaction['to_agent']
            interaction_type = interaction['interaction_type']
            
            lines.append(f"""
                <div class='timeline-item'>
                    <div class='timeline-marker'></div>
                    <div class='timeline-content'>
                        <div class='timeline-time'>{timestamp}</div>
                        <div class='timeline-title'>
                            {from_agent} → {to_agent}
                        </div>
                        <div class='timeline-subtitle'>{interaction_type}</div>
                    </div>
                </div>
            """)
        
        lines.append("</div>")
        
        return "\n".join(lines)
    
    def _generate_stats_cards(self, summary: Dict) -> str:
        """Generate statistics cards"""
        stats = summary.get('statistics', {})
        
        return f"""
        <div class='stats-grid'>
            <div class='stat-card'>
                <div class='stat-icon'>🤖</div>
                <div class='stat-value'>{stats.get('total_agents', 0)}</div>
                <div class='stat-label'>Total Agents</div>
            </div>
            <div class='stat-card'>
                <div class='stat-icon'>🤝</div>
                <div class='stat-value'>{stats.get('total_interactions', 0)}</div>
                <div class='stat-label'>Interactions</div>
            </div>
            <div class='stat-card'>
                <div class='stat-icon'>🎯</div>
                <div class='stat-value'>{stats.get('total_coordinations', 0)}</div>
                <div class='stat-label'>Coordinations</div>
            </div>
            <div class='stat-card'>
                <div class='stat-icon'>⚠️</div>
                <div class='stat-value'>{stats.get('detected_conflicts', 0)}</div>
                <div class='stat-label'>Conflicts</div>
            </div>
        </div>
        """
    
    def _generate_agent_cards(self, agents: Dict) -> str:
        """Generate agent information cards"""
        if not agents:
            return "<p>No agents registered</p>"
        
        lines = ["<div class='agents-grid'>"]
        
        for agent_name, agent_info in agents.items():
            agent_type = agent_info.get('agent_type', 'unknown')
            emoji = self._get_agent_emoji(agent_type)
            capabilities = agent_info.get('capabilities', [])
            actions = agent_info.get('actions_count', 0)
            interactions_count = agent_info.get('interactions_count', 0)
            
            capabilities_html = ", ".join(capabilities) if capabilities else "None"
            
            lines.append(f"""
                <div class='agent-card'>
                    <div class='agent-header'>
                        <span class='agent-emoji'>{emoji}</span>
                        <h3 class='agent-name'>{agent_name}</h3>
                    </div>
                    <div class='agent-type'>{agent_type}</div>
                    <div class='agent-stats'>
                        <span>📝 {actions} actions</span>
                        <span>🤝 {interactions_count} interactions</span>
                    </div>
                    <div class='agent-capabilities'>
                        <strong>Capabilities:</strong><br>
                        {capabilities_html}
                    </div>
                </div>
            """)
        
        lines.append("</div>")
        
        return "\n".join(lines)
    
    def _generate_interaction_list(self, interactions: List[Dict]) -> str:
        """Generate list of interactions"""
        if not interactions:
            return "<p>No interactions recorded</p>"
        
        lines = ["<div class='interactions-list'>"]
        
        for interaction in interactions[:30]:  # Show last 30
            from_agent = interaction['from_agent']
            to_agent = interaction['to_agent']
            interaction_type = interaction['interaction_type']
            timestamp = interaction['timestamp']
            content = interaction.get('content', 'No content')
            
            # Truncate long content
            if len(str(content)) > 100:
                content = str(content)[:100] + "..."
            
            emoji = self._get_interaction_emoji(interaction_type)
            
            lines.append(f"""
                <div class='interaction-item'>
                    <div class='interaction-header'>
                        <span class='interaction-emoji'>{emoji}</span>
                        <span class='interaction-type'>{interaction_type}</span>
                        <span class='interaction-time'>{timestamp}</span>
                    </div>
                    <div class='interaction-flow'>
                        <strong>{from_agent}</strong> → <strong>{to_agent}</strong>
                    </div>
                    <div class='interaction-content'>
                        {content}
                    </div>
                </div>
            """)
        
        lines.append("</div>")
        
        return "\n".join(lines)
    
    def _generate_conflicts_section(self, conflicts: List[Dict]) -> str:
        """Generate conflicts section"""
        if not conflicts:
            return """
            <div class='section'>
                <h2>⚠️ Conflicts</h2>
                <div class='alert alert-success'>
                    ✅ No conflicts detected during this session
                </div>
            </div>
            """
        
        lines = ["<div class='section'>", "<h2>⚠️ Conflicts</h2>"]
        
        for conflict in conflicts:
            conflict_type = conflict.get('conflict_type', 'Unknown')
            description = conflict.get('description', 'No description')
            agents = conflict.get('agents_involved', [])
            
            lines.append(f"""
                <div class='alert alert-warning'>
                    <strong>{conflict_type}:</strong> {description}<br>
                    <strong>Agents:</strong> {', '.join(agents)}
                </div>
            """)
        
        lines.append("</div>")
        
        return "\n".join(lines)
    
    def _generate_coordinations_section(self, coordinations: List[Dict]) -> str:
        """Generate coordinations section"""
        if not coordinations:
            return ""
        
        lines = ["<div class='section'>", "<h2>🎯 Coordination Events</h2>"]
        
        for coord in coordinations:
            coordinator = coord.get('coordinating_agent', 'Unknown')
            coordinated = coord.get('coordinated_agents', [])
            coord_type = coord.get('coordination_type', 'Unknown')
            description = coord.get('description', 'No description')
            
            lines.append(f"""
                <div class='coordination-item'>
                    <div class='coordination-header'>
                        <strong>{coordinator}</strong> coordinates {len(coordinated)} agents
                    </div>
                    <div class='coordination-type'>{coord_type}</div>
                    <div class='coordination-desc'>{description}</div>
                    <div class='coordination-agents'>
                        Agents: {', '.join(coordinated)}
                    </div>
                </div>
            """)
        
        lines.append("</div>")
        
        return "\n".join(lines)
    
    def _build_html(
        self,
        title: str,
        stats: str,
        agents: str,
        interaction_graph: str,
        timeline: str,
        interactions: str,
        conflicts: str,
        coordinations: str,
        summary: Dict
    ) -> str:
        """Build complete HTML document"""
        
        # Get current timestamp
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        {self._get_css()}
    </style>
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{ startOnLoad: true }});
    </script>
</head>
<body>
    <div class='container'>
        <header class='header'>
            <h1>🧠 Multi-Agent Transparency Report</h1>
            <div class='session-info'>
                <div><strong>Session ID:</strong> {summary['session_id']}</div>
                <div><strong>Project:</strong> {summary.get('project_name', 'Unknown')}</div>
                <div><strong>Generated:</strong> {now}</div>
            </div>
        </header>

        {stats}

        <div class='section'>
            <h2>🤖 Agents</h2>
            {agents}
        </div>

        <div class='section'>
            <h2>📊 Interaction Graph</h2>
            <div class='graph-container'>
                {interaction_graph}
            </div>
        </div>

        <div class='section'>
            <h2>⏱️ Timeline</h2>
            {timeline}
        </div>

        <div class='section'>
            <h2>🤝 Interactions</h2>
            {interactions}
        </div>

        {conflicts}
        
        {coordinations}

        <footer class='footer'>
            <p>
                Generated by <strong>OpenClaw Transparency Layer v0.2.0</strong><br>
                <a href='https://github.com/BradZhone/openclaw-transparency'>GitHub Repository</a>
            </p>
        </footer>
    </div>
</body>
</html>"""
        
        return html
    
    def _get_css(self) -> str:
        """Get CSS styles"""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            line-height: 1.6;
            padding: 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5em;
            margin-bottom: 20px;
        }

        .session-info {
            display: flex;
            justify-content: center;
            gap: 40px;
            font-size: 0.9em;
            opacity: 0.9;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 40px;
            background: #f8f9fa;
        }

        .stat-card {
            background: white;
            padding: 30px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            transition: transform 0.2s;
        }

        .stat-card:hover {
            transform: translateY(-5px);
        }

        .stat-icon {
            font-size: 3em;
            margin-bottom: 10px;
        }

        .stat-value {
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
        }

        .stat-label {
            font-size: 0.9em;
            color: #666;
            margin-top: 5px;
        }

        .section {
            padding: 40px;
            border-bottom: 1px solid #eee;
        }

        .section h2 {
            font-size: 1.8em;
            margin-bottom: 20px;
            color: #667eea;
        }

        .agents-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
        }

        .agent-card {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 25px;
            border-radius: 12px;
            border-left: 4px solid #667eea;
        }

        .agent-header {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 15px;
        }

        .agent-emoji {
            font-size: 2em;
        }

        .agent-name {
            font-size: 1.3em;
            margin: 0;
        }

        .agent-type {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            margin-bottom: 10px;
        }

        .agent-stats {
            display: flex;
            gap: 20px;
            margin: 10px 0;
            font-size: 0.9em;
            color: #666;
        }

        .agent-capabilities {
            margin-top: 15px;
            font-size: 0.85em;
            color: #666;
        }

        .graph-container {
            background: #f8f9fa;
            padding: 30px;
            border-radius: 12px;
            overflow-x: auto;
        }

        .timeline {
            position: relative;
            padding-left: 40px;
        }

        .timeline-item {
            position: relative;
            padding: 20px 0;
        }

        .timeline-marker {
            position: absolute;
            left: -30px;
            top: 25px;
            width: 12px;
            height: 12px;
            background: #667eea;
            border-radius: 50%;
        }

        .timeline-content {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
        }

        .timeline-time {
            font-size: 0.8em;
            color: #999;
            margin-bottom: 5px;
        }

        .timeline-title {
            font-weight: bold;
            font-size: 1.1em;
        }

        .timeline-subtitle {
            font-size: 0.9em;
            color: #666;
            margin-top: 5px;
        }

        .interactions-list {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        .interaction-item {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }

        .interaction-header {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 10px;
        }

        .interaction-emoji {
            font-size: 1.5em;
        }

        .interaction-type {
            font-weight: bold;
            color: #667eea;
        }

        .interaction-time {
            margin-left: auto;
            font-size: 0.8em;
            color: #999;
        }

        .interaction-flow {
            font-size: 1.1em;
            margin-bottom: 10px;
        }

        .interaction-content {
            font-size: 0.9em;
            color: #666;
            background: white;
            padding: 10px;
            border-radius: 4px;
        }

        .alert {
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
        }

        .alert-success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }

        .alert-warning {
            background: #fff3cd;
            color: #856404;
            border: 1px solid #ffeeba;
        }

        .coordination-item {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 15px;
            border-left: 4px solid #28a745;
        }

        .coordination-header {
            font-size: 1.1em;
            font-weight: bold;
            margin-bottom: 5px;
        }

        .coordination-type {
            display: inline-block;
            background: #28a745;
            color: white;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.8em;
            margin: 5px 0;
        }

        .coordination-desc {
            color: #666;
            margin: 10px 0;
        }

        .coordination-agents {
            font-size: 0.9em;
            color: #666;
        }

        .footer {
            padding: 30px;
            text-align: center;
            background: #f8f9fa;
            color: #666;
            font-size: 0.9em;
        }

        .footer a {
            color: #667eea;
            text-decoration: none;
        }

        .footer a:hover {
            text-decoration: underline;
        }
        """
    
    def _get_agent_emoji(self, agent_type: str) -> str:
        """Get emoji for agent type"""
        emojis = {
            'designer': '🎨',
            'developer': '💻',
            'tester': '🧪',
            'manager': '👔',
            'analyst': '📊',
            'reviewer': '👀',
            'unknown': '🤖'
        }
        return emojis.get(agent_type.lower(), '🤖')
    
    def _get_arrow_style(self, interaction_type: str) -> str:
        """Get Mermaid arrow style for interaction type"""
        arrows = {
            'delegation': '==>',
            'request': '-->',
            'response': '-.->',
            'collaboration': '---',
            'handoff': '==>'
        }
        return arrows.get(interaction_type, '-->')
    
    def _get_interaction_emoji(self, interaction_type: str) -> str:
        """Get emoji for interaction type"""
        emojis = {
            'delegation': '📤',
            'request': '❓',
            'response': '✅',
            'collaboration': '🤝',
            'handoff': '🔄'
        }
        return emojis.get(interaction_type, '💬')


# Convenience function
def generate_html_report(
    summary: Dict,
    interactions: List[Dict],
    agents: Dict,
    conflicts: List[Dict],
    coordinations: List[Dict],
    output_path: str = None
) -> str:
    """Generate HTML report (convenience function)"""
    generator = HTMLReportGenerator()
    return generator.generate_report(
        summary=summary,
        interactions=interactions,
        agents=agents,
        conflicts=conflicts,
        coordinations=coordinations,
        output_path=output_path
    )
