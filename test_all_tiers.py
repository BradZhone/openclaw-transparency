#!/usr/bin/env python3
"""
Complete Test Suite for Transparency Layer - All Tiers
Tests Free, Pro, and Enterprise features

Tier Coverage:
- Free (5 tests): Basic functionality
- Pro (4 tests): Multi-agent, visual reports, search
- Enterprise (4 tests): Compliance reports, export, merge/compare
"""

import sys
import json
import time
import traceback
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from openclaw_transparency_mvp import (
    TransparencyLayer,
    MultiAgentTracker,
    generate_visual_report,
    search_sessions,
    generate_compliance_report,
    export_sessions,
    merge_sessions,
    compare_sessions
)


class TestRunner:
    """Test runner with detailed reporting"""
    
    def __init__(self):
        self.results = {
            "passed": [],
            "failed": [],
            "errors": []
        }
        self.start_time = datetime.utcnow()
        self.test_env = {
            "python_version": sys.version,
            "platform": sys.platform,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.tier_results = {
            "free": {"passed": 0, "failed": 0},
            "pro": {"passed": 0, "failed": 0},
            "enterprise": {"passed": 0, "failed": 0}
        }
    
    def test(self, name, func, tier="free"):
        """Run a test and record results"""
        print(f"\n🧪 [{tier.upper()}] Testing: {name}")
        try:
            start = time.time()
            func()
            duration = time.time() - start
            self.results["passed"].append({
                "name": name,
                "tier": tier,
                "duration": duration
            })
            self.tier_results[tier]["passed"] += 1
            print(f"   ✅ PASSED ({duration:.3f}s)")
            return True
        except AssertionError as e:
            print(f"   ❌ FAILED: {str(e)}")
            self.results["failed"].append({
                "name": name,
                "tier": tier,
                "error": str(e),
                "traceback": traceback.format_exc()
            })
            self.tier_results[tier]["failed"] += 1
            return False
        except Exception as e:
            print(f"   ⚠️  ERROR: {str(e)}")
            self.results["errors"].append({
                "name": name,
                "tier": tier,
                "error": str(e),
                "traceback": traceback.format_exc()
            })
            self.tier_results[tier]["failed"] += 1
            return False
    
    def report(self):
        """Generate test report"""
        total_time = (datetime.utcnow() - self.start_time).total_seconds()
        
        report = {
            "test_environment": self.test_env,
            "summary": {
                "total": len(self.results["passed"]) + len(self.results["failed"]) + len(self.results["errors"]),
                "passed": len(self.results["passed"]),
                "failed": len(self.results["failed"]),
                "errors": len(self.results["errors"]),
                "duration_seconds": total_time
            },
            "tier_summary": self.tier_results,
            "results": self.results,
            "status": "PASS" if len(self.results["failed"]) == 0 and len(self.results["errors"]) == 0 else "FAIL"
        }
        
        return report


def run_all_tests():
    """Run all tier tests"""
    runner = TestRunner()
    
    # Create temporary directory for tests
    test_dir = tempfile.mkdtemp(prefix="transparency_test_")
    print(f"📁 Test directory: {test_dir}")
    
    try:
        # ========================================
        # FREE TIER TESTS (5 tests)
        # ========================================
        print("\n" + "="*80)
        print("🆓 FREE TIER TESTS")
        print("="*80)
        
        def test_free_init():
            """Test TransparencyLayer initialization"""
            t = TransparencyLayer("TestAgent", storage_path=test_dir, tier="free")
            assert t.agent_name == "TestAgent"
            assert t.session_id is not None
            assert t.tier == "free"
            assert "session_id" in t.session_data
            print(f"      Session ID: {t.session_id}")
        
        runner.test("Initialize TransparencyLayer", test_free_init, tier="free")
        
        def test_free_track_action():
            """Test action tracking"""
            t = TransparencyLayer("TestAgent", storage_path=test_dir, tier="free")
            action = t.track_action(
                action_type="test_action",
                input_data="test input",
                output_data="test output",
                metadata={"key": "value"}
            )
            assert action is not None
            assert action["action_type"] == "test_action"
            assert len(t.session_data["actions"]) == 1
        runner.test("track_action()", test_free_track_action, tier="free")
        
        def test_free_checkpoint():
            """Test checkpoint creation"""
            t = TransparencyLayer("TestAgent", storage_path=test_dir, tier="free")
            t.track_action("test", "in", "out")
            checkpoint = t.create_checkpoint(
                description="Test checkpoint",
                files_modified=["file1.py"],
                decisions=[{"decision": "test"}]
            )
            assert checkpoint is not None
            assert checkpoint["description"] == "Test checkpoint"
            assert len(t.session_data["checkpoints"]) == 1
        runner.test("create_checkpoint()", test_free_checkpoint, tier="free")
        
        def test_free_summary():
            """Test summary generation"""
            t = TransparencyLayer("TestAgent", storage_path=test_dir, tier="free")
            t.track_action("action1", "in1", "out1")
            t.track_action("action2", "in2", "out2")
            t.create_checkpoint("Test", ["file.py"], [])
            summary = t.generate_summary()
            assert summary["total_actions"] == 2
            assert summary["total_checkpoints"] == 1
        runner.test("generate_summary()", test_free_summary, tier="free")
        
        def test_free_end_session():
            """Test session ending"""
            t = TransparencyLayer("TestAgent", storage_path=test_dir, tier="free")
            t.track_action("test", "in", "out")
            summary = t.end_session()
            assert "end_time" in t.session_data
            assert summary["total_actions"] == 1
        runner.test("end_session()", test_free_end_session, tier="free")
        
        # ========================================
        # PRO TIER TESTS (4 tests)
        # ========================================
        print("\n" + "="*80)
        print("⭐ PRO TIER TESTS ($9/month)")
        print("="*80)
        
        def test_pro_multi_agent():
            """Test multi-agent tracking"""
            tracker = MultiAgentTracker(storage_path=test_dir)
            
            # Register multiple agents
            agent1 = tracker.register_agent("CodeAgent")
            agent2 = tracker.register_agent("TestAgent")
            agent3 = tracker.register_agent("DeployAgent")
            
            assert len(tracker.agents) == 3
            assert "CodeAgent" in tracker.agents
            assert "TestAgent" in tracker.agents
            
            # Track action across all
            tracker.track_all("system_event", "startup", "ok")
            
            status = tracker.get_agent_status()
            assert len(status) == 3
            assert status["CodeAgent"]["actions"] == 1
            
            tracker.end_all_sessions()
            print(f"      Tracked {len(tracker.agents)} agents successfully")
        
        runner.test("MultiAgentTracker", test_pro_multi_agent, tier="pro")
        
        def test_pro_visual_report_ascii():
            """Test ASCII visual report generation"""
            # Create a test session
            t = TransparencyLayer("ReportAgent", storage_path=test_dir, tier="pro")
            for i in range(10):
                t.track_action(f"action_type_{i % 3}", f"input_{i}", f"output_{i}")
            t.create_checkpoint("Test checkpoint", ["file.py"], [])
            t.end_session()
            
            # Generate ASCII report
            report = generate_visual_report(
                session_id=t.session_id,
                storage_path=test_dir,
                output_format="ascii"
            )
            
            assert "TRANSPARENCY LAYER VISUAL REPORT" in report
            assert t.session_id in report
            assert "action_type_" in report
            print(f"      ASCII report length: {len(report)} chars")
        
        runner.test("Visual Report (ASCII)", test_pro_visual_report_ascii, tier="pro")
        
        def test_pro_visual_report_html():
            """Test HTML visual report generation"""
            # Create a test session
            t = TransparencyLayer("HTMLAgent", storage_path=test_dir, tier="pro")
            t.track_action("web_action", "input", "output")
            t.end_session()
            
            # Generate HTML report
            report = generate_visual_report(
                session_id=t.session_id,
                storage_path=test_dir,
                output_format="html"
            )
            
            assert "<!DOCTYPE html>" in report
            assert "<title>Transparency Layer Report</title>" in report
            assert t.session_id in report
            print(f"      HTML report length: {len(report)} chars")
        
        runner.test("Visual Report (HTML)", test_pro_visual_report_html, tier="pro")
        
        def test_pro_search():
            """Test session search functionality"""
            # Create test sessions with searchable content
            t1 = TransparencyLayer("SearchAgent1", storage_path=test_dir, tier="pro")
            t1.track_action("file_operation", "reading config.json", "done")
            t1.track_action("database", "query users table", "results")
            t1.end_session()
            
            t2 = TransparencyLayer("SearchAgent2", storage_path=test_dir, tier="pro")
            t2.track_action("api_call", "GET /users", "response")
            t2.track_action("file_operation", "writing log.txt", "done")
            t2.end_session()
            
            # Search for "users"
            results = search_sessions("users", storage_path=test_dir)
            assert len(results) >= 2  # Should find in both sessions
            
            # Search for "config"
            results_config = search_sessions("config", storage_path=test_dir)
            assert len(results_config) >= 1
            
            print(f"      Found {len(results)} results for 'users'")
            print(f"      Found {len(results_config)} results for 'config'")
        
        runner.test("Session Search", test_pro_search, tier="pro")
        
        # ========================================
        # ENTERPRISE TIER TESTS (4 tests)
        # ========================================
        print("\n" + "="*80)
        print("🏢 ENTERPRISE TIER TESTS ($49/month)")
        print("="*80)
        
        def test_enterprise_soc2_report():
            """Test SOC2 compliance report generation"""
            # Create enterprise session
            t = TransparencyLayer("EnterpriseAgent", storage_path=test_dir, tier="enterprise")
            t.track_action("access", "user_login", "success", metadata={"user": "admin"})
            t.track_action("data_modify", "update_record", "done")
            t.create_checkpoint("Security checkpoint", ["secure.py"], [])
            t.end_session()
            
            # Generate SOC2 report
            report = generate_compliance_report(
                template="SOC2",
                session_id=t.session_id,
                storage_path=test_dir,
                organization="Test Corp"
            )
            
            assert report["compliance_framework"] == "SOC2"
            assert "security_controls" in report["sections"]
            assert "audit_trail" in report["sections"]
            assert report["compliance_score"] >= 0
            assert report["organization"] == "Test Corp"
            print(f"      SOC2 compliance score: {report['compliance_score']}")
        
        runner.test("SOC2 Compliance Report", test_enterprise_soc2_report, tier="enterprise")
        
        def test_enterprise_gdpr_report():
            """Test GDPR compliance report generation"""
            t = TransparencyLayer("GDPRAgent", storage_path=test_dir, tier="enterprise")
            t.track_action("data_access", "read personal data", "done", 
                          compliance_tags=["personal_data"])
            t.track_action("consent", "user consent recorded", "yes")
            t.end_session()
            
            report = generate_compliance_report(
                template="GDPR",
                session_id=t.session_id,
                storage_path=test_dir
            )
            
            assert report["compliance_framework"] == "GDPR"
            assert "data_processing_activities" in report["sections"]
            assert "consent_records" in report["sections"]
            print(f"      GDPR compliance score: {report['compliance_score']}")
        
        runner.test("GDPR Compliance Report", test_enterprise_gdpr_report, tier="enterprise")
        
        def test_enterprise_hipaa_report():
            """Test HIPAA compliance report generation"""
            t = TransparencyLayer("HIPAAAgent", storage_path=test_dir, tier="enterprise")
            t.track_action("phi_access", "view medical record", "done",
                          compliance_tags=["phi"])
            t.end_session()
            
            report = generate_compliance_report(
                template="HIPAA",
                session_id=t.session_id,
                storage_path=test_dir
            )
            
            assert report["compliance_framework"] == "HIPAA"
            assert "phi_access_log" in report["sections"]
            assert "data_encryption" in report["sections"]
            print(f"      HIPAA compliance score: {report['compliance_score']}")
        
        runner.test("HIPAA Compliance Report", test_enterprise_hipaa_report, tier="enterprise")
        
        def test_enterprise_export_csv():
            """Test CSV export functionality"""
            # Create sessions for export
            t1 = TransparencyLayer("ExportAgent1", storage_path=test_dir, tier="enterprise")
            t1.track_action("action1", "in1", "out1")
            t1.track_action("action2", "in2", "out2")
            t1.create_checkpoint("Checkpoint 1", ["file1.py"], [])
            t1.end_session()
            
            t2 = TransparencyLayer("ExportAgent2", storage_path=test_dir, tier="enterprise")
            t2.track_action("action3", "in3", "out3")
            t2.end_session()
            
            # Export to CSV
            csv_path = export_sessions(
                format="CSV",
                session_ids=[t1.session_id, t2.session_id],
                storage_path=test_dir,
                output_path=str(Path(test_dir) / "export_test.csv")
            )
            
            assert Path(csv_path).exists()
            
            # Verify CSV content
            with open(csv_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            assert "Session ID" in content
            assert t1.session_id in content
            assert t2.session_id in content
            assert "SUMMARY" in content
            print(f"      CSV exported to: {csv_path}")
        
        runner.test("Export to CSV", test_enterprise_export_csv, tier="enterprise")
        
        def test_enterprise_export_pdf():
            """Test PDF (HTML) export functionality"""
            t = TransparencyLayer("PDFAgent", storage_path=test_dir, tier="enterprise")
            t.track_action("export_action", "data", "result")
            t.end_session()
            
            # Export to PDF (HTML)
            html_path = export_sessions(
                format="PDF",
                session_ids=[t.session_id],
                storage_path=test_dir
            )
            
            assert Path(html_path).exists()
            
            with open(html_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            assert "Transparency Layer Export" in content
            assert t.session_id in content
            print(f"      PDF-ready HTML exported to: {html_path}")
        
        runner.test("Export to PDF", test_enterprise_export_pdf, tier="enterprise")
        
        def test_enterprise_merge_sessions():
            """Test session merging"""
            # Create sessions to merge
            t1 = TransparencyLayer("MergeAgent1", storage_path=test_dir, tier="enterprise")
            t1.track_action("action1", "in1", "out1")
            t1.end_session()
            
            t2 = TransparencyLayer("MergeAgent2", storage_path=test_dir, tier="enterprise")
            t2.track_action("action2", "in2", "out2")
            t2.track_action("action3", "in3", "out3")
            t2.end_session()
            
            # Merge sessions
            merged = merge_sessions(
                session_ids=[t1.session_id, t2.session_id],
                storage_path=test_dir,
                merged_name="MergedSession"
            )
            
            assert "merged-" in merged["session_id"]
            assert len(merged["actions"]) == 3  # 1 + 2
            assert len(merged["source_sessions"]) == 2
            assert merged["agent_name"] == "MergedSession"
            print(f"      Merged session ID: {merged['session_id']}")
            print(f"      Total actions: {len(merged['actions'])}")
        
        runner.test("Session Merge", test_enterprise_merge_sessions, tier="enterprise")
        
        def test_enterprise_compare_sessions():
            """Test session comparison"""
            # Create sessions to compare
            t1 = TransparencyLayer("CompareAgent1", storage_path=test_dir, tier="enterprise")
            t1.track_action("unique_to_1", "in1", "out1")
            t1.track_action("common_action", "in", "out")
            t1.create_checkpoint("CP1", ["file1.py"], [])
            t1.end_session()
            
            t2 = TransparencyLayer("CompareAgent2", storage_path=test_dir, tier="enterprise")
            t2.track_action("unique_to_2", "in2", "out2")
            t2.track_action("common_action", "in", "out")
            t2.create_checkpoint("CP2", ["file2.py"], [])
            t2.end_session()
            
            # Compare sessions
            comparison = compare_sessions(
                session_id1=t1.session_id,
                session_id2=t2.session_id,
                storage_path=test_dir
            )
            
            assert "differences" in comparison
            assert "similarity_score" in comparison
            assert comparison["differences"]["checkpoints"]["session_1_count"] == 1
            assert comparison["differences"]["checkpoints"]["session_2_count"] == 1
            print(f"      Similarity score: {comparison['similarity_score']}%")
            print(f"      Session 1 only actions: {comparison['differences']['actions']['session_1_only']}")
            print(f"      Session 2 only actions: {comparison['differences']['actions']['session_2_only']}")
        
        runner.test("Session Compare", test_enterprise_compare_sessions, tier="enterprise")
        
        # ========================================
        # CROSS-TIER COMPATIBILITY TESTS
        # ========================================
        print("\n" + "="*80)
        print("🔗 CROSS-TIER COMPATIBILITY TESTS")
        print("="*80)
        
        def test_cross_tier_compatibility():
            """Test that different tiers can work together"""
            # Free tier session
            free = TransparencyLayer("FreeAgent", storage_path=test_dir, tier="free")
            free.track_action("free_action", "in", "out")
            free.end_session()
            
            # Enterprise tier can read Free session
            report = generate_compliance_report(
                template="SOC2",
                session_id=free.session_id,
                storage_path=test_dir
            )
            assert report["sessions_analyzed"] == 1
            
            # Pro search can find Free session
            results = search_sessions("free_action", storage_path=test_dir)
            assert len(results) >= 1
            
            print("      ✅ All tiers compatible")
        
        runner.test("Cross-Tier Compatibility", test_cross_tier_compatibility, tier="free")
        
    finally:
        # Cleanup test directory
        try:
            shutil.rmtree(test_dir)
            print(f"\n🧹 Cleaned up test directory: {test_dir}")
        except:
            pass
    
    # Generate report
    print("\n" + "="*80)
    print("📊 FINAL TEST REPORT")
    print("="*80)
    
    report = runner.report()
    
    print(f"\n📈 Summary:")
    print(f"   ✅ Passed: {report['summary']['passed']}")
    print(f"   ❌ Failed: {report['summary']['failed']}")
    print(f"   ⚠️  Errors: {report['summary']['errors']}")
    print(f"   ⏱️  Duration: {report['summary']['duration_seconds']:.2f}s")
    
    print(f"\n📊 By Tier:")
    for tier, stats in report['tier_summary'].items():
        total = stats['passed'] + stats['failed']
        status = "✅" if stats['failed'] == 0 else "❌"
        print(f"   {status} {tier.upper():12s}: {stats['passed']}/{total} passed")
    
    print(f"\n🎯 Overall Status: {report['status']}")
    
    # Save report
    report_file = Path(__file__).parent / "test_results.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\n📁 Report saved to: {report_file}")
    
    return report


if __name__ == "__main__":
    report = run_all_tests()
    sys.exit(0 if report['status'] == 'PASS' else 1)
