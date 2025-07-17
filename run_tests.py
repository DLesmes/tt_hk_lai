#!/usr/bin/env python3
"""
Comprehensive test runner for the ETA Agent System
"""
import subprocess
import sys
import os
import time
import json
from datetime import datetime
from typing import Dict, List, Any

class TestRunner:
    """Test runner for the ETA Agent System"""
    
    def __init__(self):
        self.test_results = {}
        self.start_time = None
        self.end_time = None
    
    def run_backend_tests(self) -> Dict[str, Any]:
        """Run backend integration tests"""
        print("🧪 Running Backend Tests...")
        print("=" * 50)
        
        try:
            result = subprocess.run([
                sys.executable, "-m", "pytest", 
                "tests/test_backend.py", 
                "-v", 
                "--tb=short",
                "--json-report",
                "--json-report-file=test_results_backend.json"
            ], capture_output=True, text=True, timeout=300)
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "stdout": "",
                "stderr": "Tests timed out after 5 minutes",
                "returncode": 1
            }
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "returncode": 1
            }
    
    def run_frontend_tests(self) -> Dict[str, Any]:
        """Run frontend integration tests"""
        print("🎨 Running Frontend Tests...")
        print("=" * 50)
        
        try:
            result = subprocess.run([
                sys.executable, "-m", "pytest", 
                "tests/test_frontend.py", 
                "-v", 
                "--tb=short",
                "--json-report",
                "--json-report-file=test_results_frontend.json"
            ], capture_output=True, text=True, timeout=300)
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "stdout": "",
                "stderr": "Tests timed out after 5 minutes",
                "returncode": 1
            }
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "returncode": 1
            }
    
    def run_system_tests(self) -> Dict[str, Any]:
        """Run system-wide integration tests"""
        print("🔗 Running System Integration Tests...")
        print("=" * 50)
        
        try:
            result = subprocess.run([
                sys.executable, "test_frontend.py"
            ], capture_output=True, text=True, timeout=120)
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "stdout": "",
                "stderr": "System tests timed out after 2 minutes",
                "returncode": 1
            }
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "returncode": 1
            }
    
    def check_system_health(self) -> Dict[str, Any]:
        """Check overall system health"""
        print("🏥 Checking System Health...")
        print("=" * 50)
        
        import requests
        
        health_checks = {
            "backend": False,
            "frontend": False,
            "chat_endpoint": False,
            "external_apis": False
        }
        
        # Check backend health
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            health_checks["backend"] = response.status_code == 200
            print(f"✅ Backend: {'Healthy' if health_checks['backend'] else 'Unhealthy'}")
        except:
            print("❌ Backend: Not accessible")
        
        # Check frontend health
        try:
            response = requests.get("http://localhost:8501", timeout=10)
            health_checks["frontend"] = response.status_code == 200
            print(f"✅ Frontend: {'Accessible' if health_checks['frontend'] else 'Not accessible'}")
        except:
            print("❌ Frontend: Not accessible")
        
        # Check chat endpoint
        if health_checks["backend"]:
            try:
                payload = {"message": "Health check", "agent_type": "user"}
                response = requests.post("http://localhost:8000/chat", json=payload, timeout=30)
                health_checks["chat_endpoint"] = response.status_code == 200
                print(f"✅ Chat Endpoint: {'Working' if health_checks['chat_endpoint'] else 'Not working'}")
            except:
                print("❌ Chat Endpoint: Not working")
        
        # Check external APIs
        if health_checks["backend"]:
            try:
                weather_response = requests.get("http://localhost:8000/weather/test", timeout=10)
                traffic_response = requests.get("http://localhost:8000/traffic/test", timeout=10)
                health_checks["external_apis"] = (
                    weather_response.status_code == 200 and 
                    traffic_response.status_code == 200
                )
                print(f"✅ External APIs: {'Working' if health_checks['external_apis'] else 'Not working'}")
            except:
                print("❌ External APIs: Not working")
        
        return health_checks
    
    def generate_test_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "test_duration": self.end_time - self.start_time if self.start_time and self.end_time else 0,
            "system_health": self.test_results.get("health", {}),
            "backend_tests": self.test_results.get("backend", {}),
            "frontend_tests": self.test_results.get("frontend", {}),
            "system_tests": self.test_results.get("system", {}),
            "overall_status": "PASS" if self._all_tests_passed() else "FAIL"
        }
        
        # Save report to file
        with open("test_report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        return report
    
    def _all_tests_passed(self) -> bool:
        """Check if all tests passed"""
        backend_success = self.test_results.get("backend", {}).get("success", False)
        frontend_success = self.test_results.get("frontend", {}).get("success", False)
        system_success = self.test_results.get("system", {}).get("success", False)
        
        return backend_success and frontend_success and system_success
    
    def print_summary(self, report: Dict[str, Any]):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        print(f"⏱️  Test Duration: {report['test_duration']:.2f} seconds")
        print(f"🎯 Overall Status: {report['overall_status']}")
        
        print("\n🏥 System Health:")
        health = report.get("system_health", {})
        for component, status in health.items():
            status_icon = "✅" if status else "❌"
            print(f"   {status_icon} {component.title()}: {'Healthy' if status else 'Unhealthy'}")
        
        print("\n🧪 Test Results:")
        backend_result = report.get("backend_tests", {})
        frontend_result = report.get("frontend_tests", {})
        system_result = report.get("system_tests", {})
        
        print(f"   {'✅' if backend_result.get('success') else '❌'} Backend Tests: {'PASS' if backend_result.get('success') else 'FAIL'}")
        print(f"   {'✅' if frontend_result.get('success') else '❌'} Frontend Tests: {'PASS' if frontend_result.get('success') else 'FAIL'}")
        print(f"   {'✅' if system_result.get('success') else '❌'} System Tests: {'PASS' if system_result.get('success') else 'FAIL'}")
        
        print(f"\n📄 Detailed report saved to: test_report.json")
    
    def run_all_tests(self):
        """Run all tests and generate report"""
        print("🚚 ETA Agent System - Comprehensive Test Suite")
        print("=" * 60)
        
        self.start_time = time.time()
        
        # Check system health
        self.test_results["health"] = self.check_system_health()
        
        # Run backend tests
        self.test_results["backend"] = self.run_backend_tests()
        
        # Run frontend tests
        self.test_results["frontend"] = self.run_frontend_tests()
        
        # Run system tests
        self.test_results["system"] = self.run_system_tests()
        
        self.end_time = time.time()
        
        # Generate and print report
        report = self.generate_test_report()
        self.print_summary(report)
        
        return report

def main():
    """Main test runner"""
    runner = TestRunner()
    report = runner.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if report["overall_status"] == "PASS" else 1)

if __name__ == "__main__":
    main() 