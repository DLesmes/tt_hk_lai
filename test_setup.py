#!/usr/bin/env python3
"""
Test script to verify the ETA Agent System foundation setup
"""

import os
import sys
import subprocess
from pathlib import Path

def check_file_exists(file_path: str, description: str) -> bool:
    """Check if a file exists"""
    exists = Path(file_path).exists()
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {file_path}")
    return exists

def check_directory_exists(dir_path: str, description: str) -> bool:
    """Check if a directory exists"""
    exists = Path(dir_path).exists()
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {dir_path}")
    return exists

def main():
    """Main test function"""
    print("🚚 ETA Agent System - Foundation Setup Test")
    print("=" * 50)
    
    # Check project structure
    print("\n📁 Project Structure:")
    structure_ok = True
    
    # Root files
    structure_ok &= check_file_exists("docker-compose.yml", "Docker Compose")
    structure_ok &= check_file_exists("env.example", "Environment Template")
    structure_ok &= check_file_exists("README.md", "README")
    
    # Backend structure
    structure_ok &= check_directory_exists("backend", "Backend Directory")
    structure_ok &= check_file_exists("backend/requirements.txt", "Backend Requirements")
    structure_ok &= check_file_exists("backend/pyproject.toml", "Backend PyProject")
    structure_ok &= check_file_exists("backend/Dockerfile", "Backend Dockerfile")
    structure_ok &= check_directory_exists("backend/app", "Backend App Directory")
    structure_ok &= check_file_exists("backend/app/settings.py", "Backend Settings")
    structure_ok &= check_file_exists("backend/app/main.py", "Backend Main App")
    structure_ok &= check_directory_exists("backend/app/models", "Backend Models")
    structure_ok &= check_directory_exists("backend/app/clients", "Backend Clients")
    structure_ok &= check_directory_exists("backend/app/services", "Backend Services")
    structure_ok &= check_directory_exists("backend/app/api", "Backend API")
    structure_ok &= check_directory_exists("backend/data", "Backend Data Directory")
    structure_ok &= check_directory_exists("backend/alembic", "Backend Alembic")
    
    # Frontend structure
    structure_ok &= check_directory_exists("frontend", "Frontend Directory")
    structure_ok &= check_file_exists("frontend/requirements.txt", "Frontend Requirements")
    structure_ok &= check_file_exists("frontend/Dockerfile", "Frontend Dockerfile")
    structure_ok &= check_file_exists("frontend/app.py", "Frontend Main App")
    structure_ok &= check_directory_exists("frontend/utils", "Frontend Utils")
    
    # Check Python syntax
    print("\n🐍 Python Syntax Check:")
    syntax_ok = True
    
    python_files = [
        "backend/app/settings.py",
        "backend/app/main.py",
        "backend/app/models/database.py",
        "backend/app/models/conversation.py",
        "backend/app/models/user.py",
        "frontend/app.py",
        "frontend/utils/api_client.py"
    ]
    
    for file_path in python_files:
        if Path(file_path).exists():
            try:
                result = subprocess.run([sys.executable, "-m", "py_compile", file_path], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✅ {file_path}")
                else:
                    print(f"❌ {file_path}: {result.stderr}")
                    syntax_ok = False
            except Exception as e:
                print(f"❌ {file_path}: {e}")
                syntax_ok = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    
    if structure_ok and syntax_ok:
        print("🎉 All tests passed! Foundation setup is complete.")
        print("\n🚀 Next steps:")
        print("1. Copy env.example to .env and configure your API keys")
        print("2. Run: docker-compose up --build")
        print("3. Access frontend at: http://localhost:8501")
        print("4. Access backend at: http://localhost:8000")
        return True
    else:
        print("❌ Some tests failed. Please check the issues above.")
        if not structure_ok:
            print("   - Missing files or directories")
        if not syntax_ok:
            print("   - Python syntax errors")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 