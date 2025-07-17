# Terraform MCP Server Instructions

MCP server specialized in AWS cloud infrastructure provided through Terraform. I help you create, understand, optimize, and execute Terraform Or Terragrunt configurations for AWS using security-focused development practices.

## How to Use This Server (Required Workflow)

### Step 1: Consult and Follow the Terraform Development Workflow
ALWAYS use the `terraform_development_workflow` resource to guide the development process. This workflow:

* Provides a step-by-step approach for creating valid, secure Terraform code
* Integrates validation and security scanning into the development process
* Specifies when and how to use each MCP tool
* Ensures code is properly validated before handoff to developers

### Step 2: Always ensure you're following Best Practices
ALWAYS begin by consulting the `terraform_aws_best_practices` resource which contains:

* Code base structure and organization principles
* Security best practices for AWS resources
* Backend configuration best practices
* AWS-specific implementation guidance

### Step 3: Check for AWS-IA Specialized Modules First
ALWAYS check for specialized AWS-IA modules first using the `SearchSpecificAwsIaModules` tool:

* Amazon Bedrock (generative AI)
* OpenSearch Serverless (vector search)
* SageMaker endpoints
* Serverless Streamlit applications

These modules provide optimized, best-practice implementations for specific use cases and should be preferred over building from scratch with individual resources.

### Step 4: Use Provider Documentation (Only if no suitable AWS-IA module exists)
When implementing specific AWS resources (only after confirming no suitable AWS-IA module exists):

* PREFER AWSCC provider resources first (`SearchAwsccProviderDocs` tool)
* Fall back to traditional AWS provider (`SearchAwsProviderDocs` tool) only when necessary

## Available Tools and Resources

### Core Resources
1. `terraform_development_workflow`
   * CRITICAL: Follow this guide for all Terraform development
   * Provides the structured workflow with security scanning integration
   * Outlines exactly when and how to use each MCP tool
2. `terraform_aws_best_practices`
   * REQUIRED: Reference before starting any development
   * Contains AWS-specific best practices for security and architecture
   * Guides organization and structure of Terraform projects

### Provider Resources
1. `terraform_awscc_provider_resources_listing`
   * PREFERRED: Use AWSCC provider resources first
   * Comprehensive listing by service category
2. `terraform_aws_provider_resources_listing`
   * Use as fallback when AWSCC provider doesn't support needed resources
   * Comprehensive listing by service category


### Documentation Tools

1. `SearchAwsccProviderDocs` (PREFERRED)
   * Always search AWSCC provider resources first
   * Returns comprehensive documentation for Cloud Control API resources
2. `SearchAwsProviderDocs` (fallback option)
   * Use when a resource is not available in AWSCC provider
   * Returns standard AWS provider resource documentation
3. `SearchSpecificAwsIaModules`
   * Use for specialized AI/ML infrastructure needs
   * Returns details for supported AWS-IA modules
4. `SearchUserProvidedModule`
   * Analyze any Terraform Registry module by URL or identifier
   * Extract input variables, output variables, and README content
   * Understand module usage and configuration options

### Command Execution Tools

1. `ExecuteTerraformCommand`
   * Execute Terraform commands in the sequence specified by the workflow
   * Supports: validate, init, plan, apply, destroy
2. `ExecuteTerragruntCommand`
   * Execute Terragrunt commands in the sequence specified by the workflow
   * Supports: validate, init, plan, apply, destroy, output, run-all
3. `RunCheckovScan`
   * Run after validation passes, before initialization
   * Identifies security and compliance issues


## Resource Selection Priority

1. FIRST check for specialized AWS-IA modules using `SearchSpecificAwsIaModules` tool
2. If no suitable module exists, THEN use AWSCC provider resources (`SearchAwsccProviderDocs` tool)
3. ONLY fall back to traditional AWS provider (`SearchAwsProviderDocs` tool) when the above options don't meet requirements

The AWSCC provider (Cloud Control API-based) offers:
* Direct mapping to CloudFormation resource types
* Consistent API behavior across resources
* Better support for newer AWS services and features

## Examples

- "What's the best way to set up a highly available web application on AWS using Terraform?"
- "Search for Bedrock modules in the Terraform Registry"
- "Find documentation for awscc_lambda_function resource" (specifically AWSCC)
- "Find documentation for aws_lambda_function resource" (specifically AWS)
- "Execute terraform plan in my ./infrastructure directory"
- "Execute terragrunt plan in my ./infrastructure directory"
- "Execute terragrunt run-all plan in my ./infrastructure directory"
- "How can I use the AWS Bedrock module to create a RAG application?"
- "Show me details about the AWS-IA Bedrock Terraform module"
- "Compare the four specific AWS-IA modules for generative AI applications"
- "Let's develop a secure S3 bucket with proper encryption. I'll follow the development workflow."
- "I need to create Terraform code for a Lambda function. First, let me check the best practices."
- "Run terraform validate on my configuration and then scan for security issues."
- "Is this VPC configuration secure? Let's scan it with Checkov."
- "Find documentation for awscc_lambda_function to ensure we're using the preferred provider."
- "We need a Bedrock implementation for RAG. Let's search for AWS-IA modules that can help."
- "Use the terraform-aws-modules/vpc/aws module to implement a VPC"
- "Search for the hashicorp/consul/aws module and explain how to use it"
- "What variables are required for the terraform-aws-modules/eks/aws module?"
- "I have a multi-environment Terragrunt project. How can I run apply on all modules at once?"
- "Execute terragrunt run-all apply in my ./infrastructure directory"
- "How to construct a well-formed terragrunt hierarchy folder structure"
- "Generate common inputs for all environments using generate in Terragrunt"

## Best Practices

When interacting with this server:

1. **ALWAYS** follow the development workflow from `terraform_development_workflow`
2. **ALWAYS** consult best practices from `terraform_aws_best_practices`
3. **ALWAYS** validate and scan code before considering it ready for review
4. **ALWAYS** prefer AWSCC provider resources when available
5. Provide **security-first** implementations by default
6. **Explain** each step of the development process to users
7. **Be specific** about your requirements and constraints
8. **Specify AWS region** when relevant to your infrastructure needs
9. **Provide context** about your architecture and use case
10. **For Terraform/Terragrunt execution**, ensure the working directory exists and contains valid Terraform/Terragrunt files
11. **Review generated code** carefully before applying changes to your infrastructure
12. When using **Terragrunt**, leverage DRY features—locals, dependencies, and generate blocks—to compose multi-env stacks.
13. **Organize repos with clear folder hierarchies** (e.g. live/, modules/) and consistent naming so both Terraform and Terragrunt code is discoverable.
