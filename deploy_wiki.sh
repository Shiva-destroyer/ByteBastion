#!/bin/bash
#
# ByteBastion Wiki Deployment Script
# Deploys wiki documentation to GitHub Wiki repository
#
# Developer: Sai Srujan Murthy
# Contact: saisrujanmurthy@gmail.com
#

set -e  # Exit immediately on error

# Terminal colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
WIKI_REPO="https://github.com/Shiva-destroyer/ByteBastion.wiki.git"
WIKI_TEMP_DIR="temp_wiki"
WIKI_DOCS_DIR="wiki_docs"

# Script banner
echo -e "${CYAN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║         ByteBastion Wiki Deployment Script               ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if wiki_docs directory exists
if [ ! -d "$WIKI_DOCS_DIR" ]; then
    echo -e "${RED}✗ Error: $WIKI_DOCS_DIR directory not found${NC}"
    echo "  Please run this script from the ByteBastion root directory."
    exit 1
fi

# Check if markdown files exist
MD_COUNT=$(find "$WIKI_DOCS_DIR" -maxdepth 1 -name "*.md" 2>/dev/null | wc -l)
if [ "$MD_COUNT" -eq 0 ]; then
    echo -e "${RED}✗ Error: No markdown files found in $WIKI_DOCS_DIR${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Found $MD_COUNT markdown files in $WIKI_DOCS_DIR${NC}"
echo ""

# Check prerequisites
echo -e "${YELLOW}📋 Checking prerequisites...${NC}"

if ! command -v git &> /dev/null; then
    echo -e "${RED}✗ Git is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Git is available${NC}"

# Clean up existing temp directory
if [ -d "$WIKI_TEMP_DIR" ]; then
    echo -e "${YELLOW}⚠  Removing existing temporary directory...${NC}"
    rm -rf "$WIKI_TEMP_DIR"
fi

# Clone the wiki repository
echo ""
echo -e "${BLUE}📥 Cloning wiki repository...${NC}"
echo -e "${CYAN}   Repository: $WIKI_REPO${NC}"
echo ""

if ! git clone "$WIKI_REPO" "$WIKI_TEMP_DIR" 2>&1; then
    echo ""
    echo -e "${RED}✗ Failed to clone wiki repository${NC}"
    echo ""
    echo -e "${YELLOW}This could mean:${NC}"
    echo "  1. The wiki doesn't exist yet (create it on GitHub first)"
    echo "  2. You don't have permission to access the repository"
    echo "  3. Network connectivity issues"
    echo ""
    echo -e "${CYAN}To create the wiki:${NC}"
    echo "  1. Go to https://github.com/Shiva-destroyer/ByteBastion"
    echo "  2. Click on 'Wiki' tab"
    echo "  3. Click 'Create the first page'"
    echo "  4. Add any content and save"
    echo "  5. Re-run this script"
    echo ""
    exit 1
fi

echo -e "${GREEN}✓ Wiki repository cloned successfully${NC}"

# Copy markdown files
echo ""
echo -e "${BLUE}📄 Copying wiki documentation files...${NC}"

COPIED_COUNT=0
for file in "$WIKI_DOCS_DIR"/*.md; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        cp "$file" "$WIKI_TEMP_DIR/"
        echo -e "  ${GREEN}✓${NC} Copied: $filename"
        ((COPIED_COUNT++))
    fi
done

echo -e "${GREEN}✓ Copied $COPIED_COUNT markdown files${NC}"

# Navigate to wiki directory
cd "$WIKI_TEMP_DIR"

# Configure git user
echo ""
echo -e "${BLUE}⚙️  Configuring git...${NC}"
git config user.name "Sai Srujan Murthy" 2>/dev/null || true
git config user.email "saisrujanmurthy@gmail.com" 2>/dev/null || true
echo -e "${GREEN}✓ Git configured${NC}"

# Add all files
echo ""
echo -e "${BLUE}📦 Staging files...${NC}"
git add *.md
echo -e "${GREEN}✓ Files staged for commit${NC}"

# Check if there are changes to commit
if git diff --cached --quiet; then
    echo ""
    echo -e "${YELLOW}ℹ  No changes detected - wiki is already up to date${NC}"
    cd ..
    rm -rf "$WIKI_TEMP_DIR"
    echo -e "${GREEN}✓ Deployment complete (no changes needed)${NC}"
    echo ""
    exit 0
fi

# Show files to be committed
echo ""
echo -e "${CYAN}Files to be committed:${NC}"
git diff --cached --name-only | while read filename; do
    echo -e "  • $filename"
done

# Commit changes
echo ""
echo -e "${BLUE}💾 Committing changes...${NC}"

COMMIT_MSG="Update ByteBastion Wiki Documentation

- Updated/added comprehensive technical documentation
- Includes deep-dive explanations and usage guides
- Professional security documentation with examples

Developer: Sai Srujan Murthy
Contact: saisrujanmurthy@gmail.com
Date: $(date '+%Y-%m-%d %H:%M:%S')"

git commit -m "$COMMIT_MSG"
echo -e "${GREEN}✓ Changes committed successfully${NC}"

# Push to remote
echo ""
echo -e "${BLUE}🚀 Pushing to GitHub Wiki...${NC}"
echo -e "${YELLOW}   (You may be prompted for GitHub credentials)${NC}"
echo ""

if git push origin master; then
    echo ""
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║               ✓ DEPLOYMENT SUCCESSFUL                     ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${CYAN}📖 View your wiki at:${NC}"
    echo -e "${BLUE}   https://github.com/Shiva-destroyer/ByteBastion/wiki${NC}"
    echo ""
    echo -e "${CYAN}📊 Deployment Summary:${NC}"
    echo -e "   • Files deployed: $COPIED_COUNT"
    echo -e "   • Commit: $(git rev-parse --short HEAD)"
    echo -e "   • Branch: master"
    echo ""
else
    echo ""
    echo -e "${RED}✗ Failed to push to GitHub${NC}"
    echo ""
    echo -e "${YELLOW}This could mean:${NC}"
    echo "  1. Authentication failed (check your GitHub credentials)"
    echo "  2. You don't have write access to the repository"
    echo "  3. Network connectivity issues"
    echo ""
    echo -e "${CYAN}The changes are committed locally in: $WIKI_TEMP_DIR${NC}"
    echo "You can manually push from there after resolving authentication."
    echo ""
    cd ..
    exit 1
fi

# Clean up
cd ..
echo -e "${BLUE}🧹 Cleaning up temporary files...${NC}"
rm -rf "$WIKI_TEMP_DIR"
echo -e "${GREEN}✓ Cleanup complete${NC}"
echo ""

# Final message
echo -e "${CYAN}╭───────────────────────────────────────────────────────────╮${NC}"
echo -e "${CYAN}│                   Deployment Complete                     │${NC}"
echo -e "${CYAN}╰───────────────────────────────────────────────────────────╯${NC}"
echo ""
echo -e "${YELLOW}📬 Developer: Sai Srujan Murthy${NC}"
echo -e "${YELLOW}📧 Contact: saisrujanmurthy@gmail.com${NC}"
echo ""
echo -e "${GREEN}✨ Your ByteBastion wiki is now live!${NC}"
echo ""
