# Terraform Development Workflow

## Purpose and Usage

This workflow guide provides a structured approach for developing valid, secure Terraform configurations for AWS infrastructure. As an AI coding assistant utilizing this MCP server, you should follow these steps when helping users create or modify Terraform code.

## How to Use This Guide
You have access to specialized tools and resources through this MCP server that significantly enhance your ability to assist with Terraform development. When working with users on Terraform code:

1. Reference this workflow consistently throughout your interactions
2. Leverage this MCP server's capabilities rather than relying solely on your general knowledge
3. Explain the workflow steps to users as you assist them
4. Choose the appropriate path—Terraform or Terragrunt—based on the user's project structure and tooling preferences

## Benefits to Emphasize
When following this workflow and using these tools, you provide several advantages to users:

- Early detection of configuration errors
- Identification of security vulnerabilities before deployment
- Adherence to AWS best practices
- Validation that code will work correctly when deployed
- Support for layered, DRY configurations through Terragrunt when modularization and environment inheritance are needed

By following this workflow guide and leveraging the provided tools and resources, you'll deliver consistent, high-quality assistance for Terraform development on AWS, helping users create infrastructure code that is syntactically valid, secure, and ready for review before deployment.

## DEVELOPMENT WORKFLOW

``` mermaid
flowchart TD
    start([Start Development]) --> detectConfig[Identify Project Type:\nTerraform or Terragrunt]

    detectConfig --> edit[Edit Code]

    %% Initial Code Validation
    edit --> validate[Run Validation:\nterraform validate or terragrunt validate\nvia ExecuteTerraformCommand]

    %% Validation Flow
    validate -->|Passes| checkovScan[Run Security Scan\nvia RunCheckovScan]
    validate -->|Fails| fixValidation[Fix Configuration\nIssues]
    fixValidation --> edit

    %% Checkov Flow
    checkovScan -->|No Issues| initCmd[Run Init Command:\nterraform init or terragrunt init\nvia ExecuteTerraformCommand]
    checkovScan -->|Finds Issues| reviewIssues[Review Security\nIssues]

    reviewIssues --> manualFix[Fix Security Issues]
    manualFix --> edit

    %% Init & Plan (No Apply)
    initCmd -->|Success| planCmd[Run Plan Command:\nterraform plan or terragrunt plan\nvia ExecuteTerraformCommand]
    initCmd -->|Fails| fixInit[Fix Provider/Module\nIssues]
    fixInit --> edit

    %% Final Review & Handoff to Developer
    planCmd -->|Plan Generated| reviewPlan[Review Planned Changes]
    planCmd -->|Issues Detected| edit

    reviewPlan --> codeReady[Valid, Secure Code Ready\nfor Developer Review]

    %% Iteration for Improvements
    codeReady --> newChanges{Need Code\nImprovements?}
    newChanges -->|Yes| edit
    newChanges -->|No| handoff([Hand Off to Developer\nfor Deployment Decision])

    %% Styling
    classDef success fill:#bef5cb,stroke:#28a745
    classDef warning fill:#fff5b1,stroke:#dbab09
    classDef error fill:#ffdce0,stroke:#cb2431
    classDef process fill:#f1f8ff,stroke:#0366d6
    classDef decision fill:#d1bcf9,stroke:#8a63d2
    classDef mcptool fill:#d0f0fd,stroke:#0969da,font-style:italic
    classDef handoff fill:#ffdfb6,stroke:#f9a03f

    class codeReady success
    class reviewIssues,reviewPlan warning
    class fixValidation,fixInit,manualFix error
    class edit process
    class detectConfig,newChanges decision
    class validate,checkovScan,initCmd,planCmd mcptool
    class handoff handoff
```

1. Edit Terraform or Terragrunt Code
    - Write or modify Terraform or Terragrunt configuration files for AWS resources
    - When writing code, follow this priority order:
        * FIRST check for specialized AWS-IA modules (`SearchSpecificAwsIaModules` tool)
        * If no suitable module exists, THEN use AWSCC provider resources (`SearchAwsccProviderDocs` tool)
        * ONLY fall back to traditional AWS provider (`SearchAwsProviderDocs` tool) when the above options don't meet requirements
    - When using Terragrunt:
        * Ensure that the terraform block references the correct module or configuration directory
        * Use Terragrunt features such as locals, dependencies, generate, and inputs to manage DRY configuration
    - When a user provides a specific Terraform Registry module to use:
        * Use the `SearchUserProvidedModule` tool to analyze the module
        * Extract input variables, output variables, and README content
        * Understand module usage and configuration options
        * Provide guidance on how to use the module correctly
    - MCP Resources and tools to consult:
        - Resources
            - *terraform_development_workflow* to consult this guide and to use it to ensure you're following the development workflow correctly
            - *terraform_aws_best_practices* for AWS best practices about security, code base structure and organization, AWS Provider version management, and usage of community modules
            - *terragrunt_aws_best_practices* for AWS best practices about security, code base structure and organization, AWS Provider version management, and usage of community modules
            - *terraform_awscc_provider_resources_listing* for available AWS Cloud Control API resources
            - *terraform_aws_provider_resources_listing* for available AWS resources
        - Tools
            - *SearchSpecificAwsIaModules* tool to check for specialized AWS-IA modules first (Bedrock, OpenSearch Serverless, SageMaker, Streamlit)
            - *SearchUserProvidedModule* tool to analyze any Terraform Registry module provided by the user
            - *SearchAwsccProviderDocs* tool to look up specific Cloud Control API resources
            - *SearchAwsProviderDocs* tool to look up specific resource documentation
2. Validate Code
    - Tools:
      - *ExecuteTerraformCommand* with command="validate"
      - *ExecuteTerragruntCommand* with command="validate"
    - Purpose:
      - Checks syntax and configuration validity without accessing AWS
      - Identifies syntax errors, invalid resource configurations, and reference issues
    - Examples:
      - ExecuteTerraformCommand(TerraformExecutionRequest(command="validate", working_directory="./my_project"))
      - ExecuteTerragruntCommand(TerragruntExecutionRequest(command="validate", working_directory="./my_project"))
3. Run Security Scan
    - Tool: *RunCheckovScan*
        - Scans code for security misconfigurations, compliance issues, and AWS best practice violations
        - Example: RunCheckovScan(CheckovScanRequest(working_directory="./my_project", framework="terraform"))
4. Fix Security Issues
    - For fixes:
        - Edit the code to address security issues identified by the scan
        - Consult *terraform_aws_best_practices* resource for guidance
5. Initialize Working Directory
    - Tools:
      - Terraform: *ExecuteTerraformCommand* with command="init"
      - Terragrunt: *ExecuteTerragruntCommand* with command="init"
    - Purpose:
        - Downloads provider plugins and sets up modules
    - Example:
      - ExecuteTerraformCommand(TerraformExecutionRequest(command="init", working_directory="./my_project"))
      - ExecuteTerragruntCommand(TerragruntExecutionRequest(command="init", working_directory="./my_project"))
6. Plan Changes
    - Tools:
      - *ExecuteTerraformCommand* with command="plan"
      - *ExecuteTerragruntCommand* with command="plan"
    - Purpose:
        - Creates an execution plan showing what changes would be made (without applying)
        - Verifies that the configuration is deployable
    - Examples:
      - ExecuteTerraformCommand(TerraformExecutionRequest(command="plan", working_directory="./my_project", output_file="tfplan"))
      - ExecuteTerragruntCommand(TerragruntExecutionRequest(command="plan", working_directory="./my_project", output_file="tfplan"))
7. Review Plan & Code Ready
    - Review the plan output to ensure it reflects intended changes
    - Confirm all validation and security checks have passed
    - Code is now ready for handoff to the developer for deployment decisions


## Core Commands

### Terraform Commands

#### terraform init

* Purpose: Initializes a Terraform working directory, downloading provider plugins and setting up modules.
* When to use: Before running any other commands on a new configuration or after adding new modules/providers.

Options:
- `-backend-config=PATH` - Configuration for backend
- `-reconfigure` - Reconfigure backend

#### terraform validate

* Purpose: Checks whether a configuration is syntactically valid and internally consistent.
* When to use: After making changes to configuration files but before planning or applying.

```python
ExecuteTerraformCommand(TerraformExecutionRequest(
    command="validate",
    working_directory="./project_dir"
))
```

#### terraform plan

* Purpose: Creates an execution plan showing what actions Terraform would take to apply the current configuration.
* When to use: After validation passes to preview changes before applying them.

Options:
- `-var 'name=value'` - Set variable
- `-var-file=filename` - Set variables from file

#### terraform apply

* Purpose: Applies changes required to reach the desired state of the configuration.
* When to use: After plan confirms the intended changes, and developer decides to proceed.

>Note: This is typically executed by the developer after reviewing code generated by the assistant.

Options:
- `-auto-approve` - Skip interactive approval
- `-var 'name=value'` - Set variable
- Use `-out` to save plans and apply those exact plans.

#### terraform destroy

* Purpose: Destroys all resources managed by the current configuration.
* When to use: When resources are no longer needed, typically executed by the developer.

>Note: This is typically executed by the developer once it has been decided the application should be destroyed.

Options:
- `-auto-approve` - Skip interactive approval

### Terragrunt Commands

#### terragrunt init

* Purpose: Initializes a Terragrunt working directory by preparing the underlying Terraform modules and provider plugins.
* When to use: Before running any other commands in a new or updated Terragrunt configuration directory.

Options:
- `--terragrunt-config=PATH` - Path to the Terragrunt configuration file (default: terragrunt.hcl)

```python
ExecuteTerragruntCommand(TerragruntExecutionRequest(
    command="init",
    working_directory="./project_dir"
))
```

#### terragrunt validate

* Purpose: Validates the underlying Terraform configuration referenced by the Terragrunt wrapper.
* When to use: After editing Terragrunt or Terraform configuration files, to check for syntax and reference issues.

```python
ExecuteTerragruntCommand(TerragruntExecutionRequest(
    command="validate",
    working_directory="./project_dir"
))
```
Options:
- `--terragrunt-config=PATH` - Path to the Terragrunt configuration file (default: `terragrunt.hcl`)

#### terragrunt plan

* Purpose: Creates an execution plan for infrastructure changes using the Terragrunt wrapper.
* When to use: After validation passes, to preview changes before applying them.

Options:
- `-var 'name=value'` - Set variable (passed to Terraform)
- `-var-file=filename` - Load variables from file (passed to Terraform)
- `--terragrunt-config=PATH` - Path to the Terragrunt configuration file (default: `terragrunt.hcl`)

```python
ExecuteTerragruntCommand(TerragruntExecutionRequest(
    command="plan",
    working_directory="./project_dir",
))
```

#### terragrunt apply

* Purpose: Applies the planned changes using the Terragrunt wrapper.
* When to use: After plan output is approved and developer chooses to proceed.

>Note: This is typically executed by the developer after reviewing code and plan output.

Options:
- `-auto-approve` - Skip interactive approval
- `--non-interactive` - Disables all interactive approval prompts (Terragrunt as well of Terraform)
- `-var 'name=value'` - Set variable
- `--terragrunt-config=PATH` - Use a specific Terragrunt configuration file

```python
ExecuteTerragruntCommand(TerragruntExecutionRequest(
    command="apply",
    working_directory="./project_dir"
))
```

#### terragrunt destroy

* Purpose: Destroys all infrastructure managed through the Terragrunt configuration.
* When to use: When the infrastructure is no longer needed.

>Note: This is typically executed by the developer once the application or environment is being decommissioned.

Options:
- `-auto-approve` - Skip interactive approval
- `--non-interactive` - Disables all interactive approval prompts (Terragrunt as well of Terraform)
- `--terragrunt-config=PATH` - Use a specific Terragrunt configuration file

```python
ExecuteTerragruntCommand(TerragruntExecutionRequest(
    command="destroy",
    working_directory="./project_dir"
))
```

#### terragrunt run-all apply

* Purpose: Recursively runs the `apply` command across all child Terragrunt modules in a directory tree.
* When to use: To apply changes across an entire environment or stack, typically in a root coordination folder.

Options:
- `--non-interactive` - Disables all interactive approval prompts (Terragrunt as well of Terraform)
- `--queue-exclude-dir` - Exclude glob path that should be excluded when issuing run-all commands. If a relative path is specified, it should be relative from working-dir.
- `--queue-include-dir` - Include glob path that should be included when issuing run-all commands. If a relative path is specified, it should be relative from working-dir.

```python
ExecuteTerragruntCommand(TerragruntExecutionRequest(
    command="run-all apply",
    working_directory="./live/production"
))
```

### Checkov Commands

These security scanning commands are available through dedicated tools:

#### Checkov Scan

* Purpose: Scans Terraform code for security issues, misconfigurations, and compliance violations.
* Tool: RunCheckovScan
* When to use: After code passes terraform validate but before initializing and planning.

## Key Principles
- **Module-First Approach**: Always check for specialized AWS-IA modules before building with individual resources
- **Provider Selection**: When using individual resources, prefer the AWSCC provider (Cloud Control API-based) before falling back to the traditional AWS provider
- **Security First**: Always implement security best practices by default
- **Cost Optimization**: Design resources to minimize costs while meeting requirements
- **Operational Excellence**: Implement proper monitoring, logging, and observability
- **Serverless-First**: Prefer serverless services when possible
- **Infrastructure as Code**: Define all infrastructure declaratively using Terraform (or Terragrunt where applicable)
- **Regional Awareness**: Consider regional availability and constraints for services
