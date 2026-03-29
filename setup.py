"""
Quick start script to setup and run the GitHub Connector
"""
import os
import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.8 or higher"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✓ Python {version.major}.{version.minor}.{version.micro} detected")
    return True


def check_env_file():
    """Check if .env file exists"""
    if not Path(".env").exists():
        print("⚠️ .env file not found!")
        if Path(".env.example").exists():
            print("Creating .env from .env.example...")
            with open(".env.example", "r") as f:
                example = f.read()
            with open(".env", "w") as f:
                f.write(example)
            print("✓ .env file created")
            print("⚠️ Please edit .env and add your GitHub Personal Access Token")
            return False
    else:
        print("✓ .env file exists")
        with open(".env", "r") as f:
            content = f.read()
            if "your_personal_access_token_here" in content:
                print("⚠️ GitHub token not set in .env file!")
                return False
        return True


def install_dependencies():
    """Install required packages"""
    print("\nInstalling dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"])
        print("✓ Dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False


def run_server():
    """Run the FastAPI server"""
    print("\n" + "="*60)
    print("Starting GitHub Connector API...")
    print("="*60)
    print("\n📚 API Documentation:")
    print("   - Swagger UI: http://localhost:8000/docs")
    print("   - ReDoc: http://localhost:8000/redoc")
    print("\n💡 Quick test:")
    print("   curl http://localhost:8000/health")
    print("\n❌ Press Ctrl+C to stop the server\n")
    
    try:
        import uvicorn
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\nServer stopped")
        sys.exit(0)


def main():
    """Main setup and run function"""
    print("GitHub Connector API - Quick Start")
    print("="*60 + "\n")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check environment setup
    env_ready = check_env_file()
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Check if GitHub token is set
    if not env_ready:
        print("\n⚠️ Please configure your GitHub token in .env file first")
        print("   Instructions: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token")
        sys.exit(1)
    
    # Run the server
    run_server()


if __name__ == "__main__":
    main()
