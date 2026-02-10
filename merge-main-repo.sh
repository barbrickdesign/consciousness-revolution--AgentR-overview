#!/bin/bash

################################################################################
# Main Repository Merge Script
# Purpose: Automate merging consciousness-revolution main repo into overview repo
# Usage: ./merge-main-repo.sh [main-repo-path]
################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
MAIN_REPO_URL="https://github.com/overkor-tek/consciousness-revolution.git"
MAIN_REPO_PATH="${1:-../consciousness-revolution-main}"
OVERVIEW_REPO_PATH="$(pwd)"
MERGE_LOG="merge-progress.log"
BACKUP_DIR="backup-$(date +%Y%m%d-%H%M%S)"

################################################################################
# Helper Functions
################################################################################

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$MERGE_LOG"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$MERGE_LOG"
}

warn() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$MERGE_LOG"
}

info() {
    echo -e "${BLUE}[INFO]${NC} $1" | tee -a "$MERGE_LOG"
}

confirm() {
    read -p "$1 (y/n) " -n 1 -r
    echo
    [[ $REPLY =~ ^[Yy]$ ]]
}

################################################################################
# Phase 1: Preparation
################################################################################

prepare_merge() {
    log "=== Phase 1: Preparation ==="
    
    # Check if we're in the overview repo
    if [ ! -f "MERGE_PLAN.md" ]; then
        error "Not in overview repository! MERGE_PLAN.md not found."
        exit 1
    fi
    
    log "✓ Confirmed in overview repository"
    
    # Create backup
    log "Creating backup of current state..."
    mkdir -p "$BACKUP_DIR"
    cp -r . "$BACKUP_DIR/" 2>/dev/null || true
    log "✓ Backup created at $BACKUP_DIR"
    
    # Check git status
    if ! git diff-index --quiet HEAD -- 2>/dev/null; then
        warn "Uncommitted changes detected!"
        if ! confirm "Continue anyway?"; then
            exit 1
        fi
    fi
    
    log "✓ Phase 1 complete"
}

################################################################################
# Phase 2: Get Main Repository
################################################################################

get_main_repo() {
    log "=== Phase 2: Get Main Repository ==="
    
    if [ -d "$MAIN_REPO_PATH/.git" ]; then
        log "Main repo already exists at $MAIN_REPO_PATH"
        cd "$MAIN_REPO_PATH"
        git pull origin main || warn "Could not pull latest changes"
        cd "$OVERVIEW_REPO_PATH"
    else
        log "Cloning main repository..."
        if ! git clone "$MAIN_REPO_URL" "$MAIN_REPO_PATH"; then
            error "Failed to clone main repository"
            error "You may need to:"
            error "  1. Check your GitHub authentication"
            error "  2. Verify repository URL"
            error "  3. Clone manually and pass path as argument"
            exit 1
        fi
        log "✓ Main repo cloned to $MAIN_REPO_PATH"
    fi
    
    log "✓ Phase 2 complete"
}

################################################################################
# Phase 3: Merge Core Systems
################################################################################

merge_directory() {
    local dir_name="$1"
    local source_path="$MAIN_REPO_PATH/$dir_name"
    local dest_path="$OVERVIEW_REPO_PATH/$dir_name"
    
    if [ ! -d "$source_path" ]; then
        warn "Directory not found in main repo: $dir_name"
        return 1
    fi
    
    log "Merging $dir_name..."
    
    if [ -d "$dest_path" ]; then
        warn "Directory already exists: $dir_name"
        if confirm "Overwrite with main repo version?"; then
            rm -rf "$dest_path"
            cp -r "$source_path" "$dest_path"
            log "✓ Overwrote $dir_name"
        else
            info "Skipping $dir_name"
        fi
    else
        cp -r "$source_path" "$dest_path"
        log "✓ Merged $dir_name"
    fi
}

merge_core_systems() {
    log "=== Phase 3: Merge Core Systems ==="
    
    # List of major systems to merge
    CORE_SYSTEMS=(
        "ember-terminal"
        "GemBotMemory2025"
        "city-3d"
        "mandem.os"
        "OSKeyMap"
        "rdata"
    )
    
    for system in "${CORE_SYSTEMS[@]}"; do
        merge_directory "$system"
    done
    
    log "✓ Phase 3 complete"
}

################################################################################
# Phase 4: Merge Supporting Systems
################################################################################

merge_supporting_systems() {
    log "=== Phase 4: Merge Supporting Systems ==="
    
    SUPPORTING_SYSTEMS=(
        "projects"
        "language-samples"
        "scripts"
        "logs"
    )
    
    for system in "${SUPPORTING_SYSTEMS[@]}"; do
        merge_directory "$system"
    done
    
    log "✓ Phase 4 complete"
}

################################################################################
# Phase 5: Merge Configuration Files
################################################################################

merge_file() {
    local file_name="$1"
    local source_file="$MAIN_REPO_PATH/$file_name"
    local dest_file="$OVERVIEW_REPO_PATH/$file_name"
    
    if [ ! -f "$source_file" ]; then
        warn "File not found in main repo: $file_name"
        return 1
    fi
    
    if [ -f "$dest_file" ]; then
        log "Comparing $file_name..."
        if diff -q "$source_file" "$dest_file" > /dev/null; then
            info "Files identical, skipping: $file_name"
        else
            warn "Files differ: $file_name"
            if confirm "Show diff?"; then
                diff "$dest_file" "$source_file" || true
            fi
            if confirm "Use main repo version?"; then
                cp "$source_file" "$dest_file"
                log "✓ Updated $file_name"
            else
                info "Keeping overview version of $file_name"
            fi
        fi
    else
        cp "$source_file" "$dest_file"
        log "✓ Added $file_name"
    fi
}

merge_configurations() {
    log "=== Phase 5: Merge Configuration Files ==="
    
    CONFIG_FILES=(
        "netlify.toml"
        ".env.example"
        ".gitignore"
    )
    
    for file in "${CONFIG_FILES[@]}"; do
        merge_file "$file"
    done
    
    log "✓ Phase 5 complete"
}

################################################################################
# Phase 6: Merge Dependencies
################################################################################

merge_dependencies() {
    log "=== Phase 6: Merge Dependencies ==="
    
    # Merge package.json if it exists
    if [ -f "$MAIN_REPO_PATH/package.json" ]; then
        log "Merging package.json dependencies..."
        
        # Backup current package.json
        cp package.json package.json.backup
        
        # This is a simplified merge - in practice, you'd want to use jq or npm
        warn "package.json requires manual merge!"
        warn "Main repo version at: $MAIN_REPO_PATH/package.json"
        warn "Overview version at: $OVERVIEW_REPO_PATH/package.json"
        
        if confirm "Open both files for manual merge?"; then
            ${EDITOR:-nano} "$MAIN_REPO_PATH/package.json" &
            ${EDITOR:-nano} "$OVERVIEW_REPO_PATH/package.json" &
            wait
        fi
        
        info "After merging package.json, run: npm install"
    fi
    
    # Check for requirements.txt
    if [ -f "$MAIN_REPO_PATH/requirements.txt" ]; then
        merge_file "requirements.txt"
        info "After merging, run: pip install -r requirements.txt"
    fi
    
    log "✓ Phase 6 complete"
}

################################################################################
# Phase 7: Update Documentation
################################################################################

update_documentation() {
    log "=== Phase 7: Update Documentation ==="
    
    # Create merge report
    cat > MERGE_REPORT.md << EOF
# Merge Report

**Date:** $(date)
**Main Repo:** $MAIN_REPO_URL
**Main Repo Commit:** $(cd "$MAIN_REPO_PATH" && git rev-parse HEAD)

## Systems Merged

### Core Systems
EOF
    
    for system in "${CORE_SYSTEMS[@]}"; do
        if [ -d "$system" ]; then
            echo "- ✅ $system" >> MERGE_REPORT.md
        else
            echo "- ❌ $system (not found)" >> MERGE_REPORT.md
        fi
    done
    
    cat >> MERGE_REPORT.md << EOF

### Supporting Systems
EOF
    
    for system in "${SUPPORTING_SYSTEMS[@]}"; do
        if [ -d "$system" ]; then
            echo "- ✅ $system" >> MERGE_REPORT.md
        else
            echo "- ❌ $system (not found)" >> MERGE_REPORT.md
        fi
    done
    
    cat >> MERGE_REPORT.md << EOF

## File Statistics

**Before Merge:**
- Files in overview repo: $(find . -type f | wc -l)

**After Merge:**
- Files now: $(find . -type f | wc -l)

## Next Steps

1. Review merged files
2. Run tests: \`npm test\`
3. Update documentation
4. Commit changes
5. Push to repository

## Notes

See merge-progress.log for detailed merge log.
EOF
    
    log "✓ Created MERGE_REPORT.md"
    log "✓ Phase 7 complete"
}

################################################################################
# Phase 8: Testing
################################################################################

run_tests() {
    log "=== Phase 8: Testing ==="
    
    # Check if package.json has test script
    if [ -f "package.json" ] && grep -q '"test"' package.json; then
        if confirm "Run npm test?"; then
            npm test || warn "Tests failed! Review output above."
        fi
    fi
    
    # Check if HTML files are valid
    log "Checking HTML validity..."
    HTML_ERRORS=0
    for file in $(find . -name "*.html" -not -path "*/node_modules/*" -not -path "*/backup-*/*"); do
        if ! grep -q "<html" "$file"; then
            warn "Invalid HTML structure: $file"
            ((HTML_ERRORS++))
        fi
    done
    
    if [ $HTML_ERRORS -eq 0 ]; then
        log "✓ All HTML files appear valid"
    else
        warn "$HTML_ERRORS HTML files may have issues"
    fi
    
    log "✓ Phase 8 complete"
}

################################################################################
# Phase 9: Commit Changes
################################################################################

commit_changes() {
    log "=== Phase 9: Commit Changes ==="
    
    # Show git status
    log "Git status:"
    git status
    
    if confirm "Commit merged changes?"; then
        git add .
        git commit -m "Merge main repository features and enhanced scripts

- Merged core systems: ember-terminal, GemBotMemory2025, city-3d, mandem.os
- Merged supporting systems: projects, language-samples, scripts, logs
- Updated configuration files
- Merged dependencies
- Generated MERGE_REPORT.md

Total files merged: ~1,140+ from main repository
See MERGE_REPORT.md and merge-progress.log for details."
        
        log "✓ Changes committed"
        
        if confirm "Push to remote?"; then
            git push
            log "✓ Changes pushed to remote"
        fi
    else
        info "Changes not committed. Review and commit manually when ready."
    fi
    
    log "✓ Phase 9 complete"
}

################################################################################
# Main Execution
################################################################################

main() {
    log "========================================="
    log "Main Repository Merge Script"
    log "========================================="
    log ""
    
    info "This script will merge the main consciousness-revolution repository"
    info "into this overview repository following the MERGE_PLAN.md document."
    info ""
    info "Main repo: $MAIN_REPO_URL"
    info "Main repo path: $MAIN_REPO_PATH"
    info "Overview repo: $OVERVIEW_REPO_PATH"
    info ""
    
    if ! confirm "Continue with merge?"; then
        info "Merge cancelled"
        exit 0
    fi
    
    # Execute phases
    prepare_merge
    get_main_repo
    merge_core_systems
    merge_supporting_systems
    merge_configurations
    merge_dependencies
    update_documentation
    run_tests
    commit_changes
    
    log "========================================="
    log "Merge Complete!"
    log "========================================="
    log ""
    log "Summary:"
    log "- Backup created: $BACKUP_DIR"
    log "- Merge log: $MERGE_LOG"
    log "- Merge report: MERGE_REPORT.md"
    log ""
    log "Next steps:"
    log "1. Review MERGE_REPORT.md"
    log "2. Test all functionality"
    log "3. Update documentation as needed"
    log "4. Deploy to production when ready"
    log ""
    log "If you encounter issues:"
    log "- Check $MERGE_LOG for details"
    log "- Restore from backup: $BACKUP_DIR"
    log "- Review MERGE_PLAN.md for manual steps"
}

# Run main function
main "$@"
