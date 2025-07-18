# Contributing to AWS Terraform MCP Server

## Conventional Commits

This project uses [Conventional Commits](https://www.conventionalcommits.org/) for automated semantic versioning. Please follow this format for your commit messages:

### Commit Message Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types

- **feat**: A new feature (triggers minor version bump)
- **fix**: A bug fix (triggers patch version bump)
- **docs**: Documentation only changes
- **style**: Changes that do not affect the meaning of the code
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **perf**: A code change that improves performance
- **test**: Adding missing tests or correcting existing tests
- **chore**: Changes to the build process or auxiliary tools

### Breaking Changes

To trigger a major version bump, use one of these approaches:

1. Add `!` after the type: `feat!: remove deprecated API`
2. Add `BREAKING CHANGE:` in the footer:
   ```
   feat: add new authentication method
   
   BREAKING CHANGE: The old authentication method is no longer supported
   ```

### Examples

```bash
# Patch version bump (1.0.0 -> 1.0.1)
git commit -m "fix: resolve Docker healthcheck timeout issue"

# Minor version bump (1.0.0 -> 1.1.0)
git commit -m "feat: add support for Terragrunt run-all commands"

# Major version bump (1.0.0 -> 2.0.0)
git commit -m "feat!: change MCP protocol version to 2024-11-05"

# No version bump
git commit -m "docs: update README with new examples"
git commit -m "chore: update dependencies"
```

## Automated Versioning

### How It Works

1. **Pull Requests**: Build and test Docker images, but don't publish versions
2. **Main Branch**: Build, test, and push `:latest` tag
3. **Release Workflow**: Analyzes commits since last tag and creates semantic version

### Version Bumping Rules

- **Major** (X.0.0): Breaking changes (`feat!:`, `fix!:`, or `BREAKING CHANGE:`)
- **Minor** (x.Y.0): New features (`feat:`)
- **Patch** (x.y.Z): Bug fixes (`fix:`) or any other changes

### Manual Releases

You can trigger a manual release with a specific version:

1. Go to Actions → Release and Tag
2. Click "Run workflow"
3. Enter the desired version (e.g., `v1.2.3`)

## Docker Image Tags

After each release, the following Docker image tags are available:

- `ghcr.io/stv-io/aws-terraform-mcp-server:latest` - Always points to the latest release
- `ghcr.io/stv-io/aws-terraform-mcp-server:v1.2.3` - Specific version
- `ghcr.io/stv-io/aws-terraform-mcp-server:v1.2` - Latest patch of minor version
- `ghcr.io/stv-io/aws-terraform-mcp-server:v1` - Latest minor of major version

## Development Workflow

1. Create a feature branch from `main`
2. Make your changes with conventional commit messages
3. Create a pull request
4. After review and merge, the release workflow will automatically:
   - Analyze your commits
   - Determine the appropriate version bump
   - Create a new release with proper semantic version
   - Tag and push Docker images

## Testing

Before submitting a PR, please run the tests:

```bash
# Test locally built Docker image
python3 test_docker_mcp.py

# Test server directly
python3 test_mcp_server.py

# Run unit tests
python3 -m pytest tests/ -v
```
