# AWS Terraform MCP Server

[![Docker Image](https://img.shields.io/badge/Docker-ghcr.io/stv--io/aws--terraform--mcp--server-blue?logo=docker)](https://github.com/stv-io/aws-terraform-mcp-server/pkgs/container/aws-terraform-mcp-server)
[![GitHub](https://img.shields.io/badge/GitHub-stv--io/aws--terraform--mcp--server-black?logo=github)](https://github.com/stv-io/aws-terraform-mcp-server)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Docker containerized version of the [AWS Labs Terraform MCP Server](https://github.com/awslabs/mcp/tree/main/src/terraform-mcp-server) - a Model Context Protocol (MCP) server for Terraform on AWS best practices, infrastructure as code patterns, and security compliance with Checkov.

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# Pull and run the latest image
docker run --rm --interactive ghcr.io/stv-io/aws-terraform-mcp-server:latest
```

### Using with MCP Clients

#### Windsurf IDE
Add to your Windsurf MCP settings:
```json
{
  "name": "AWS Terraform MCP Server",
  "command": "docker",
  "args": [
    "run", "--rm", "--interactive",
    "--env", "FASTMCP_LOG_LEVEL=ERROR",
    "ghcr.io/stv-io/aws-terraform-mcp-server:latest"
  ],
  "env": {},
  "disabled": false,
  "autoApprove": []
}
```

#### Cursor IDE
Add to your Cursor MCP configuration:
```json
{
  "mcpServers": {
    "aws-terraform-mcp-server": {
      "command": "docker",
      "args": [
        "run", "--rm", "--interactive",
        "--env", "FASTMCP_LOG_LEVEL=ERROR",
        "ghcr.io/stv-io/aws-terraform-mcp-server:latest"
      ],
      "env": {},
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

## 🛠️ Features

### Tools Available
- **ExecuteTerraformCommand** - Run Terraform commands (init, plan, validate, apply, destroy)
- **ExecuteTerragruntCommand** - Run Terragrunt workflows with advanced features
- **SearchAwsProviderDocs** - Search AWS provider documentation
- **SearchAwsccProviderDocs** - Search AWSCC provider documentation
- **SearchSpecificAwsIaModules** - Access AWS-IA GenAI modules (Bedrock, OpenSearch, SageMaker, Streamlit)
- **RunCheckovScan** - Security and compliance scanning with Checkov
- **SearchUserProvidedModule** - Analyze Terraform Registry modules

### Resources Available
- **terraform_development_workflow** - Security-focused development process guide
- **terraform_aws_provider_resources_listing** - Comprehensive AWS provider resources catalog
- **terraform_awscc_provider_resources_listing** - AWSCC provider resources catalog
- **terraform_aws_best_practices** - AWS Terraform best practices guidance

## 🔧 Development

### Building Locally

```bash
# Clone the repository
git clone https://github.com/stv-io/aws-terraform-mcp-server.git
cd aws-terraform-mcp-server

# Build the Docker image
docker build -t aws-terraform-mcp-server .

# Run locally
docker run --rm --interactive aws-terraform-mcp-server
```

### Testing

```bash
# Run the test script
python3 test_docker_mcp.py
```

### Using UV (Alternative)

```bash
# Install dependencies
uv sync

# Run the server
uv run awslabs.terraform-mcp-server
```

## 📋 Prerequisites

For local development:
1. [uv](https://docs.astral.sh/uv/getting-started/installation/) - Python package manager
2. Python 3.10+
3. Terraform CLI (for workflow execution)
4. Checkov (for security scanning)

For Docker usage:
1. Docker or compatible container runtime

## 🔒 Security Considerations

- **Follow structured development workflow** with integrated validation and security scanning
- **Review all Checkov warnings** and fix security issues when possible
- **Use AWSCC provider** for consistent API behavior and better security defaults
- **Conduct independent assessment** before applying changes to production environments

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Original implementation by [AWS Labs](https://github.com/awslabs/mcp)
- Built on the [Model Context Protocol](https://modelcontextprotocol.io/)
- Uses [FastMCP](https://github.com/jlowin/fastmcp) framework

## 📞 Support

For issues and questions:
- [GitHub Issues](https://github.com/stv-io/aws-terraform-mcp-server/issues)
- [Original AWS Labs Repository](https://github.com/awslabs/mcp)

---

**Note**: This is a containerized distribution of the AWS Labs Terraform MCP Server. All credit for the core functionality goes to the AWS Labs team.
