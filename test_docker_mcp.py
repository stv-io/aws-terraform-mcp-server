#!/usr/bin/env python3
"""
Test script to verify the Dockerized Terraform MCP server is working.
This script will test the MCP server running in Docker.
"""

import json
import subprocess
import sys
import time
from typing import Dict, Any

def test_docker_mcp_server():
    """Test the Dockerized Terraform MCP server."""
    print("🐳 Starting Dockerized Terraform MCP Server test...")
    
    # Start the MCP server in Docker
    cmd = [
        "docker", "run", "--rm", "--interactive",
        "--env", "FASTMCP_LOG_LEVEL=ERROR",
        "awslabs/terraform-mcp-server:latest"
    ]
    
    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    try:
        # Test 1: Initialize the MCP connection
        print("📡 Testing MCP initialization...")
        init_message = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "roots": {
                        "listChanged": True
                    },
                    "sampling": {}
                },
                "clientInfo": {
                    "name": "docker-test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        # Send initialization message
        process.stdin.write(json.dumps(init_message) + '\n')
        process.stdin.flush()
        
        # Read response
        response_line = process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            print(f"✅ Initialize response: {response}")
            
            # Send initialized notification
            initialized_notification = {
                "jsonrpc": "2.0",
                "method": "notifications/initialized"
            }
            process.stdin.write(json.dumps(initialized_notification) + '\n')
            process.stdin.flush()
            
            # Test 2: List available tools
            print("\n🔧 Testing tools listing...")
            tools_message = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list"
            }
            
            process.stdin.write(json.dumps(tools_message) + '\n')
            process.stdin.flush()
            
            tools_response = process.stdout.readline()
            if tools_response:
                tools_data = json.loads(tools_response.strip())
                print(f"✅ Tools available: {len(tools_data.get('result', {}).get('tools', []))} tools")
                
                # Print tool names
                for tool in tools_data.get('result', {}).get('tools', []):
                    print(f"   - {tool.get('name', 'Unknown')}: {tool.get('description', 'No description')}")
            
            # Test 3: List available resources
            print("\n📚 Testing resources listing...")
            resources_message = {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "resources/list"
            }
            
            process.stdin.write(json.dumps(resources_message) + '\n')
            process.stdin.flush()
            
            resources_response = process.stdout.readline()
            if resources_response:
                resources_data = json.loads(resources_response.strip())
                print(f"✅ Resources available: {len(resources_data.get('result', {}).get('resources', []))} resources")
                
                # Print resource names
                for resource in resources_data.get('result', {}).get('resources', []):
                    print(f"   - {resource.get('name', 'Unknown')}: {resource.get('description', 'No description')}")
        
        print("\n🎉 Dockerized MCP Server test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        # Print stderr for debugging
        stderr_output = process.stderr.read()
        if stderr_output:
            print(f"Server stderr: {stderr_output}")
    
    finally:
        # Clean up
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()

if __name__ == "__main__":
    test_docker_mcp_server()
