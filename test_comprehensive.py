#!/usr/bin/env python3
"""
Comprehensive Test Suite for Transparency Layer
Tests all functionality including edge cases and error handling
"""

import sys
import json
import time
import traceback
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from openclaw_transparency_mvp import TransparencyLayer


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
    
    def test(self, name, func):
        """Run a test and record results"""
        print(f"\n🧪 Testing: {name}")
        try:
            start = time.time()
            func()
            duration = time.time() - start
            self.results["passed"].append({
                "name": name,
                "duration": duration
            })
            print(f"   ✅ PASSED ({duration:.3f}s)")
            return True
        except AssertionError as e:
            print(f"   ❌ FAILED: {str(e)}")
            self.results["failed"].append({
                "name": name,
                "error": str(e),
                "traceback": traceback.format_exc()
            })
            return False
        except Exception as e:
            print(f"   ⚠️  ERROR: {str(e)}")
            self.results["errors"].append({
                "name": name,
                "error": str(e),
                "traceback": traceback.format_exc()
            })
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
            "results": self.results,
            "status": "PASS" if len(self.results["failed"]) == 0 and len(self.results["errors"]) == 0 else "FAIL"
        }
        
        return report


def run_tests():
    """Run all transparency layer tests"""
    runner = TestRunner()
    
    # ========================================
    # 1. BASIC FUNCTIONALITY TESTS
    # ========================================
    print("\n" + "="*80)
    print("1️⃣  BASIC FUNCTIONALITY TESTS")
    print("="*80)
    
    def test_init():
        """Test TransparencyLayer initialization"""
        t = TransparencyLayer("TestAgent", storage_path="./test-sessions")
        assert t.agent_name == "TestAgent"
        assert t.session_id is not None
        assert t.session_data is not None
        assert "session_id" in t.session_data
        assert "agent_name" in t.session_data
        assert "start_time" in t.session_data
        print(f"      Session ID: {t.session_id}")
    
    runner.test("Initialize TransparencyLayer", test_init)
    
    def test_track_action():
        """Test action tracking"""
        t = TransparencyLayer("TestAgent", storage_path="./test-sessions")
        action = t.track_action(
            action_type="test_action",
            input_data="test input",
            output_data="test output",
            metadata={"key": "value"}
        )
        assert action is not None
        assert action["action_type"] == "test_action"
        assert action["input"] == "test input"
        assert action["output"] == "test output"
        assert action["metadata"]["key"] == "value"
        assert len(t.session_data["actions"]) == 1
    
    runner.test("track_action()", test_track_action)
    
    def test_create_checkpoint():
        """Test checkpoint creation"""
        t = TransparencyLayer("TestAgent", storage_path="./test-sessions")
        t.track_action("test", "in", "out")
        checkpoint = t.create_checkpoint(
            description="Test checkpoint",
            files_modified=["file1.py", "file2.py"],
            decisions=[{"decision": "test decision"}]
        )
        assert checkpoint is not None
        assert checkpoint["description"] == "Test checkpoint"
        assert len(checkpoint["files_modified"]) == 2
        assert len(t.session_data["checkpoints"]) == 1
    
    runner.test("create_checkpoint()", test_create_checkpoint)
    
    def test_generate_summary():
        """Test summary generation"""
        t = TransparencyLayer("TestAgent", storage_path="./test-sessions")
        t.track_action("action1", "in1", "out1")
        t.track_action("action2", "in2", "out2")
        t.create_checkpoint("Test", ["file.py"], [])
        summary = t.generate_summary()
        assert summary["session_id"] == t.session_id
        assert summary["total_actions"] == 2
        assert summary["total_checkpoints"] == 1
        assert "action_breakdown" in summary
    
    runner.test("generate_summary()", test_generate_summary)
    
    def test_end_session():
        """Test session ending"""
        t = TransparencyLayer("TestAgent", storage_path="./test-sessions")
        t.track_action("test", "in", "out")
        summary = t.end_session()
        assert "end_time" in t.session_data
        assert summary["total_actions"] == 1
    
    runner.test("end_session()", test_end_session)
    
    # ========================================
    # 2. DATA PERSISTENCE TESTS
    # ========================================
    print("\n" + "="*80)
    print("2️⃣  DATA PERSISTENCE TESTS")
    print("="*80)
    
    def test_json_save():
        """Test JSON file saving"""
        t = TransparencyLayer("TestAgent", storage_path="./test-sessions")
        t.track_action("test", "input", "output")
        t.create_checkpoint("Test checkpoint", [], [])
        
        # Check file exists
        session_file = Path(f"./test-sessions/{t.session_id}.json")
        assert session_file.exists(), f"Session file not found: {session_file}"
        
        # Verify content
        with open(session_file) as f:
            data = json.load(f)
        
        assert data["session_id"] == t.session_id
        assert len(data["actions"]) == 1
        assert len(data["checkpoints"]) == 1
        print(f"      Session file: {session_file}")
    
    runner.test("JSON file saving", test_json_save)
    
    def test_data_integrity():
        """Test data integrity"""
        t = TransparencyLayer("TestAgent", storage_path="./test-sessions")
        
        # Add various data
        t.track_action("type1", {"key": "value"}, {"result": "ok"})
        t.track_action("type2", [1, 2, 3], {"count": 3})
        t.create_checkpoint("Checkpoint 1", ["file1.py"], [{"decision": "d1"}])
        t.track_action("type3", "string", None)
        
        # Save and reload
        session_file = Path(f"./test-sessions/{t.session_id}.json")
        with open(session_file) as f:
            data = json.load(f)
        
        # Verify all data preserved
        assert len(data["actions"]) == 3
        assert data["actions"][0]["input"]["key"] == "value"
        assert data["actions"][1]["input"] == [1, 2, 3]
        assert data["actions"][2]["output"] is None
        assert data["checkpoints"][0]["files_modified"] == ["file1.py"]
        print("      All data integrity checks passed")
    
    runner.test("Data integrity", test_data_integrity)
    
    # ========================================
    # 3. ERROR HANDLING TESTS
    # ========================================
    print("\n" + "="*80)
    print("3️⃣  ERROR HANDLING TESTS")
    print("="*80)
    
    def test_empty_input():
        """Test handling empty input"""
        t = TransparencyLayer("TestAgent", storage_path="./test-sessions")
        # Should not crash with empty data
        action = t.track_action("", "", "")
        assert action["action_type"] == ""
        assert action["input"] == ""
        assert action["output"] == ""
        print("      Empty input handled gracefully")
    
    runner.test("Empty input handling", test_empty_input)
    
    def test_none_values():
        """Test handling None values"""
        t = TransparencyLayer("TestAgent", storage_path="./test-sessions")
        action = t.track_action("test", None, None, None)
        assert action["input"] is None
        assert action["output"] is None
        assert action["metadata"] == {}
        print("      None values handled correctly")
    
    runner.test("None values handling", test_none_values)
    
    def test_invalid_metadata():
        """Test handling invalid metadata types"""
        t = TransparencyLayer("TestAgent", storage_path="./test-sessions")
        # Metadata should default to {} if None
        action = t.track_action("test", "in", "out", None)
        assert action["metadata"] == {}
        print("      Invalid metadata handled")
    
    runner.test("Invalid metadata handling", test_invalid_metadata)
    
    def test_unicode_handling():
        """Test Unicode character handling"""
        t = TransparencyLayer("TestAgent", storage_path="./test-sessions")
        unicode_str = "测试 🔥 日本語 العربية"
        action = t.track_action("test", unicode_str, unicode_str, {"unicode": unicode_str})
        assert action["input"] == unicode_str
        t.end_session()
        
        # Verify saved correctly
        session_file = Path(f"./test-sessions/{t.session_id}.json")
        with open(session_file, encoding='utf-8') as f:
            data = json.load(f)
        assert data["actions"][0]["input"] == unicode_str
        print(f"      Unicode preserved: {unicode_str}")
    
    runner.test("Unicode handling", test_unicode_handling)
    
    # ========================================
    # 4. BOUNDARY CASE TESTS
    # ========================================
    print("\n" + "="*80)
    print("4️⃣  BOUNDARY CASE TESTS")
    print("="*80)
    
    def test_large_volume():
        """Test handling 100+ actions"""
        t = TransparencyLayer("VolumeTest", storage_path="./test-sessions")
        
        start = time.time()
        for i in range(150):
            t.track_action(f"action_{i % 5}", f"input_{i}", f"output_{i}")
        
        duration = time.time() - start
        
        assert len(t.session_data["actions"]) == 150
        print(f"      150 actions tracked in {duration:.2f}s")
        assert duration < 5.0, "Should handle 150 actions in under 5 seconds"
    
    runner.test("Large volume (150 actions)", test_large_volume)
    
    def test_long_session():
        """Test long-running session"""
        t = TransparencyLayer("LongSession", storage_path="./test-sessions")
        
        start = time.time()
        # Simulate a long session
        for i in range(50):
            t.track_action("action", f"step_{i}", f"result_{i}")
            if i % 10 == 9:
                t.create_checkpoint(f"Milestone {i//10 + 1}", [], [])
        
        summary = t.end_session()
        duration = time.time() - start
        
        assert summary["total_actions"] == 50
        assert summary["total_checkpoints"] == 5
        print(f"      50 actions + 5 checkpoints in {duration:.2f}s")
    
    runner.test("Long session simulation", test_long_session)
    
    def test_special_characters():
        """Test special character handling"""
        t = TransparencyLayer("SpecialChars", storage_path="./test-sessions")
        
        special_strings = [
            "Newline\nand\ttabs",
            "Quotes \"single\" and 'double'",
            "Backslash\\path",
            "HTML <script>alert('xss')</script>",
            "JSON {\"key\": \"value\"}",
            "Path ../../../etc/passwd",
            "SQL'; DROP TABLE users;--"
        ]
        
        for i, s in enumerate(special_strings):
            action = t.track_action(f"test_{i}", s, s)
            assert action["input"] == s
        
        # Verify saved and reloaded correctly
        session_file = Path(f"./test-sessions/{t.session_id}.json")
        with open(session_file, encoding='utf-8') as f:
            data = json.load(f)
        
        for i, s in enumerate(special_strings):
            assert data["actions"][i]["input"] == s
        
        print(f"      {len(special_strings)} special character cases handled")
    
    runner.test("Special characters handling", test_special_characters)
    
    def test_large_data():
        """Test handling large data payloads"""
        t = TransparencyLayer("LargeData", storage_path="./test-sessions")
        
        # Create a large string (100KB)
        large_string = "x" * 100000
        action = t.track_action("large", large_string, {"data": large_string[:1000]})
        
        assert action["input"] == large_string
        assert len(action["input"]) == 100000
        print(f"      100KB data payload handled")
    
    runner.test("Large data payload", test_large_data)
    
    def test_nested_structures():
        """Test nested data structures"""
        t = TransparencyLayer("NestedTest", storage_path="./test-sessions")
        
        nested_data = {
            "level1": {
                "level2": {
                    "level3": {
                        "items": [1, 2, 3],
                        "nested_list": [{"a": 1}, {"b": 2}]
                    }
                }
            }
        }
        
        action = t.track_action("nested", nested_data, nested_data)
        assert action["input"]["level1"]["level2"]["level3"]["items"] == [1, 2, 3]
        print("      Deeply nested structures handled")
    
    runner.test("Nested data structures", test_nested_structures)
    
    # ========================================
    # 5. PERFORMANCE TESTS
    # ========================================
    print("\n" + "="*80)
    print("5️⃣  PERFORMANCE TESTS")
    print("="*80)
    
    def test_action_performance():
        """Test action tracking performance"""
        t = TransparencyLayer("PerfTest", storage_path="./test-sessions")
        
        # Track 100 actions and measure time
        times = []
        for i in range(100):
            start = time.time()
            t.track_action(f"perf_{i}", f"in_{i}", f"out_{i}")
            times.append(time.time() - start)
        
        avg_time = sum(times) / len(times)
        max_time = max(times)
        
        print(f"      Avg: {avg_time*1000:.2f}ms, Max: {max_time*1000:.2f}ms")
        assert avg_time < 0.1, "Average action time should be under 100ms"
    
    runner.test("Action performance (100 ops)", test_action_performance)
    
    def test_file_io_performance():
        """Test file I/O performance"""
        t = TransparencyLayer("IOTest", storage_path="./test-sessions")
        
        # Add data
        for i in range(50):
            t.track_action(f"test_{i}", f"input_{i}", f"output_{i}")
        
        # Measure save time
        start = time.time()
        t._save_session()
        save_time = time.time() - start
        
        # Measure load time
        session_file = Path(f"./test-sessions/{t.session_id}.json")
        start = time.time()
        with open(session_file) as f:
            json.load(f)
        load_time = time.time() - start
        
        print(f"      Save: {save_time*1000:.2f}ms, Load: {load_time*1000:.2f}ms")
        assert save_time < 1.0, "Save should complete in under 1 second"
        assert load_time < 0.5, "Load should complete in under 0.5 seconds"
    
    runner.test("File I/O performance", test_file_io_performance)
    
    # Generate report
    print("\n" + "="*80)
    print("📊 TEST REPORT")
    print("="*80)
    
    report = runner.report()
    
    print(f"\n✅ Passed: {report['summary']['passed']}")
    print(f"❌ Failed: {report['summary']['failed']}")
    print(f"⚠️  Errors: {report['summary']['errors']}")
    print(f"⏱️  Total Duration: {report['summary']['duration_seconds']:.2f}s")
    print(f"\n🎯 Overall Status: {report['status']}")
    
    # Save report
    report_file = Path("./test-sessions/test_report.json")
    report_file.parent.mkdir(parents=True, exist_ok=True)
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\n📁 Report saved to: {report_file}")
    
    return report


if __name__ == "__main__":
    report = run_tests()
    sys.exit(0 if report['status'] == 'PASS' else 1)
