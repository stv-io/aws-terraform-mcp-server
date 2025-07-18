#!/bin/bash
set -e

# Semantic versioning script for AWS Terraform MCP Server
# This script determines the next version based on conventional commits

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Get the latest tag
get_latest_tag() {
    git tag -l --sort=-version:refname | grep -E '^v[0-9]+\.[0-9]+\.[0-9]+$' | head -n1 || echo "v0.0.0"
}

# Parse version components
parse_version() {
    local version=$1
    # Remove 'v' prefix if present
    version=${version#v}
    
    IFS='.' read -r major minor patch <<< "$version"
    echo "$major $minor $patch"
}

# Increment version based on type
increment_version() {
    local current_version=$1
    local increment_type=$2
    
    read -r major minor patch <<< "$(parse_version "$current_version")"
    
    case $increment_type in
        "major")
            major=$((major + 1))
            minor=0
            patch=0
            ;;
        "minor")
            minor=$((minor + 1))
            patch=0
            ;;
        "patch")
            patch=$((patch + 1))
            ;;
        *)
            print_error "Invalid increment type: $increment_type"
            exit 1
            ;;
    esac
    
    echo "v$major.$minor.$patch"
}

# Analyze commits since last tag to determine version bump
analyze_commits() {
    local latest_tag=$1
    local has_breaking=false
    local has_feat=false
    local has_fix=false
    
    print_info "Analyzing commits since $latest_tag..."
    
    # Get commits since last tag
    if [ "$latest_tag" = "v0.0.0" ]; then
        # If no tags exist, analyze all commits
        commits=$(git log --pretty=format:"%s" --no-merges)
    else
        commits=$(git log "$latest_tag"..HEAD --pretty=format:"%s" --no-merges)
    fi
    
    if [ -z "$commits" ]; then
        print_warning "No new commits found since $latest_tag"
        echo "none"
        return
    fi
    
    # Analyze commit messages
    while IFS= read -r commit; do
        print_info "  📝 $commit"
        
        # Check for breaking changes
        if echo "$commit" | grep -qE "(BREAKING CHANGE|!:)" || echo "$commit" | grep -qE "^[a-z]+(\(.+\))?!:"; then
            has_breaking=true
            print_warning "    🚨 Breaking change detected"
        fi
        
        # Check for features
        if echo "$commit" | grep -qE "^feat(\(.+\))?:"; then
            has_feat=true
            print_info "    ✨ Feature detected"
        fi
        
        # Check for fixes
        if echo "$commit" | grep -qE "^fix(\(.+\))?:"; then
            has_fix=true
            print_info "    🐛 Fix detected"
        fi
    done <<< "$commits"
    
    # Determine version bump
    if [ "$has_breaking" = true ]; then
        echo "major"
    elif [ "$has_feat" = true ]; then
        echo "minor"
    elif [ "$has_fix" = true ]; then
        echo "patch"
    else
        echo "patch"  # Default to patch for any other changes
    fi
}

# Main function
main() {
    print_info "🏷️  AWS Terraform MCP Server - Semantic Versioning"
    print_info "=================================================="
    
    # Get current latest tag
    latest_tag=$(get_latest_tag)
    print_info "Current latest tag: $latest_tag"
    
    # Analyze commits to determine version bump
    bump_type=$(analyze_commits "$latest_tag")
    
    if [ "$bump_type" = "none" ]; then
        print_warning "No version bump needed"
        echo "$latest_tag"
        exit 0
    fi
    
    # Calculate new version
    new_version=$(increment_version "$latest_tag" "$bump_type")
    
    print_success "Version bump type: $bump_type"
    print_success "New version: $new_version"
    
    # Output for GitHub Actions
    if [ "${GITHUB_ACTIONS:-false}" = "true" ]; then
        echo "current_version=$latest_tag" >> "$GITHUB_OUTPUT"
        echo "new_version=$new_version" >> "$GITHUB_OUTPUT"
        echo "bump_type=$bump_type" >> "$GITHUB_OUTPUT"
        echo "should_release=true" >> "$GITHUB_OUTPUT"
    fi
    
    echo "$new_version"
}

# Run main function
main "$@"
