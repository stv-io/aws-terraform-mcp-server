#!/usr/bin/env python3
"""
Simple test script to verify the Terraform MCP server is working.
This script will test the MCP server by sending basic protocol messages.
"""

import json
import subprocess
import sys
import time
from typing import Dict, Any

def send_mcp_message(process: subprocess.Popen, message: Dict[str, Any]) -> Dict[str, Any]:
    """Send a message to the MCP server and get the response."""
    # Send the message
    message_str = json.dumps(message) + '\n'
    process.stdin.write(message_str.encode())
    process.stdin.flush()
    
    # Read the response
    response_line = process.stdout.readline()
    if response_line:
        return json.loads(response_line.decode().strip())
    return {}

def test_mcp_server():
    """Test the Terraform MCP server."""
    print("🚀 Starting Terraform MCP Server test...")
    
    # Start the MCP server
    cmd = ["uv", "run", "awslabs.terraform-mcp-server"]
    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd="/Users/steve/labs/aws-terraform-mcp-server/mcp/src/terraform-mcp-server"
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
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        response = send_mcp_message(process, init_message)
        print(f"✅ Initialize response: {response}")
        
        # Test 2: List available tools
        print("\n🔧 Testing tools listing...")
        tools_message = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        
        response = send_mcp_message(process, tools_message)
        print(f"✅ Tools list response: {response}")
        
        # Test 3: List available resources
        print("\n📚 Testing resources listing...")
        resources_message = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "resources/list",
            "params": {}
        }
        
        response = send_mcp_message(process, resources_message)
        print(f"✅ Resources list response: {response}")
        
        print("\n🎉 MCP Server test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        # Print stderr for debugging
        stderr_output = process.stderr.read().decode()
        if stderr_output:
            print(f"Server stderr: {stderr_output}")
    
    finally:
        # Clean up
        process.terminate()
        process.wait()

if __name__ == "__main__":
    test_mcp_server()
