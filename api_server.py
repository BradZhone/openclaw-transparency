#!/usr/bin/env python3
"""
OpenClaw Transparency Layer - Web API Server
FastAPI-based REST API for transparency tracking
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import json
import uuid
from datetime import datetime
import os

# Import transparency layer
from openclaw_transparency_mvp import TransparencyLayer, MultiAgentTracker

app = FastAPI(
    title="OpenClaw Transparency API",
    description="AI Agent Transparency & Audit API",
    version="1.0.0"
)

# CORS for web access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session storage (for demo)
sessions: Dict[str, TransparencyLayer] = {}

# Request models
class CreateSessionRequest(BaseModel):
    agent_name: str
    tier: str = "free"  # free, pro, enterprise

class TrackActionRequest(BaseModel):
    session_id: str
    action_type: str
    target: str
    result: str
    metadata: Optional[Dict[str, Any]] = None

class CheckpointRequest(BaseModel):
    session_id: str
    description: str
    files_modified: List[str] = []
    decisions: List[str] = []

# Response models
class SessionResponse(BaseModel):
    session_id: str
    agent_name: str
    tier: str
    created_at: str
    status: str

class SummaryResponse(BaseModel):
    session_id: str
    summary: Dict[str, Any]
    actions_count: int
    checkpoints_count: int

# API Endpoints

@app.get("/")
async def root():
    """API root - show available endpoints"""
    return {
        "name": "OpenClaw Transparency API",
        "version": "1.0.0",
        "endpoints": {
            "POST /sessions": "Create new tracking session",
            "POST /track": "Track an action",
            "POST /checkpoint": "Create a checkpoint",
            "GET /summary/{session_id}": "Get session summary",
            "GET /tiers": "View pricing tiers",
        },
        "github": "https://github.com/BradZhone/openclaw-transparency",
        "pricing": {
            "free": "$0/month - Basic tracking",
            "pro": "$9/month - Multi-agent + visualization",
            "enterprise": "$49/month - Compliance reports + support"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "OpenClaw Transparency API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/tiers")
async def get_tiers():
    """Show pricing tiers"""
    return {
        "free": {
            "price": "$0/month",
            "features": [
                "Basic transparency tracking",
                "Checkpoints",
                "Session summaries",
                "JSON storage",
                "Community support"
            ]
        },
        "pro": {
            "price": "$9/month",
            "features": [
                "Everything in Free, plus:",
                "Multi-agent tracking",
                "Visual reports (ASCII + HTML)",
                "Session search",
                "Priority support"
            ],
            "buy_url": "https://gum.co/openclaw-transparency-pro"
        },
        "enterprise": {
            "price": "$49/month",
            "features": [
                "Everything in Pro, plus:",
                "Compliance reports (SOC2, GDPR, HIPAA)",
                "Export (CSV, PDF)",
                "Session merge/compare",
                "Dedicated support",
                "SLA guarantee"
            ],
            "buy_url": "https://gum.co/openclaw-transparency-enterprise"
        }
    }

@app.post("/sessions", response_model=SessionResponse)
async def create_session(request: CreateSessionRequest):
    """Create a new tracking session"""
    # Create transparency layer (it generates its own session_id)
    tracker = TransparencyLayer(
        agent_name=request.agent_name,
        tier=request.tier
    )

    session_id = tracker.session_id
    sessions[session_id] = tracker

    return SessionResponse(
        session_id=session_id,
        agent_name=request.agent_name,
        tier=request.tier,
        created_at=datetime.utcnow().isoformat(),
        status="active"
    )

@app.post("/track")
async def track_action(request: TrackActionRequest):
    """Track an AI agent action"""
    if request.session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    tracker = sessions[request.session_id]
    tracker.track_action(
        action_type=request.action_type,
        target=request.target,
        result=request.result,
        metadata=request.metadata
    )
    
    return {"status": "tracked", "session_id": request.session_id}

@app.post("/checkpoint")
async def create_checkpoint(request: CheckpointRequest):
    """Create a checkpoint in the session"""
    if request.session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    tracker = sessions[request.session_id]
    checkpoint_id = tracker.create_checkpoint(
        description=request.description,
        files_modified=request.files_modified,
        decisions=request.decisions
    )
    
    return {
        "status": "checkpoint_created",
        "checkpoint_id": checkpoint_id,
        "session_id": request.session_id
    }

@app.get("/summary/{session_id}", response_model=SummaryResponse)
async def get_summary(session_id: str):
    """Get session summary"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    tracker = sessions[session_id]
    summary = tracker.end_session()
    
    return SummaryResponse(
        session_id=session_id,
        summary=summary,
        actions_count=len(summary.get("actions", [])),
        checkpoints_count=len(summary.get("checkpoints", []))
    )

@app.get("/demo")
async def run_demo():
    """Run a demo session to show capabilities"""
    # Create demo session
    session_id = str(uuid.uuid4())
    tracker = TransparencyLayer(
        agent_name="DemoBot",
        session_id=session_id,
        tier="free"
    )
    
    # Track some actions
    tracker.track_action("file_read", "config.py", "Configuration loaded")
    tracker.track_action("api_call", "https://api.example.com/data", "Data fetched")
    tracker.track_action("decision", "Use model GPT-4", "Selected best model")
    
    # Create checkpoint
    tracker.create_checkpoint(
        "Initialization complete",
        ["config.py"],
        ["Selected GPT-4 model"]
    )
    
    # Get summary
    summary = tracker.end_session()
    
    return {
        "demo": "success",
        "session_id": session_id,
        "summary": summary,
        "message": "This is a demo session. Create your own session with POST /sessions"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
