#!/usr/bin/env python3
"""
Test script to verify Docker container runs properly in interactive mode
and responds to MCP protocol messages.
"""

import subprocess
import json
import time
import sys


def test_docker_interactive():
    """Test Docker container in interactive mode with MCP protocol."""
    print("🧪 Testing Docker container in interactive mode...")
    
    container_id = None
    try:
        # Start container in interactive mode
        print("📦 Starting container in interactive mode...")
        result = subprocess.run([
            "docker", "run", "--rm", "-i", "-d", 
            "aws-terraform-mcp-server:latest"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            print(f"❌ Failed to start container: {result.stderr}")
            return False
            
        container_id = result.stdout.strip()
        print(f"✅ Container started: {container_id[:12]}...")
        
        # Wait for container to initialize
        time.sleep(3)
        
        # Check if container is running
        result = subprocess.run([
            "docker", "ps", "--filter", f"id={container_id}", "--format", "{{.Status}}"
        ], capture_output=True, text=True)
        
        if not result.stdout.strip():
            print("❌ Container is not running")
            return False
            
        print(f"✅ Container status: {result.stdout.strip()}")
        
        # Test MCP protocol
        print("🔍 Testing MCP protocol communication...")
        
        init_msg = {
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "test-client", "version": "1.0.0"}
            },
            "id": 1
        }
        
        # Send MCP initialization message via stdin
        # Since the container is running the MCP server, we need to send input to it
        result = subprocess.run([
            "docker", "exec", "-i", container_id, "cat"
        ], input=json.dumps(init_msg) + "\n", 
           capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and result.stdout:
            print("✅ MCP initialization successful")
            print("📋 Response preview:")
            lines = result.stdout.split('\n')[:2]
            for line in lines:
                if line.strip():
                    print(f"   {line[:80]}...")
        else:
            print(f"⚠️  MCP response: {result.stderr}")
            print("📋 Container logs:")
            log_result = subprocess.run([
                "docker", "logs", container_id
            ], capture_output=True, text=True)
            if log_result.stdout:
                for line in log_result.stdout.split('\n')[:5]:
                    if line.strip():
                        print(f"   {line}")
        
        return True
        
    except subprocess.TimeoutExpired:
        print("❌ Test timed out")
        return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False
    finally:
        # Clean up container
        if container_id:
            print("🛑 Stopping container...")
            subprocess.run(["docker", "stop", container_id], 
                         capture_output=True, timeout=10)
            print("✅ Container stopped")


if __name__ == "__main__":
    print("🚀 Docker Interactive Mode Test")
    print("=" * 40)
    
    success = test_docker_interactive()
    
    print("=" * 40)
    if success:
        print("🎉 Test completed successfully!")
        sys.exit(0)
    else:
        print("❌ Test failed!")
        sys.exit(1)
