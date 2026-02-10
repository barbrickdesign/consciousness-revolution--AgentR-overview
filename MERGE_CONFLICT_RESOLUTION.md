# Merge Conflict Resolution Guide

This document provides detailed guidance for resolving the 244 files that have matching names between the main repository and overview repository.

## Overview

According to `content_comparison_data.json`:
- **244 files** have matching names
- **0 files** are exact matches (all have different content)
- These files require manual review and decision-making

## Resolution Strategy

### General Principle
1. **Main repo is source of truth** for core features
2. **Overview repo enhancements** should be preserved if unique
3. **Merge both** when they have complementary features
4. **Test thoroughly** after each resolution

---

## High-Priority Files

### 1. index.html
**Location:** Root directory  
**Conflict:** Both repos have landing pages with different content

**Resolution Steps:**
```bash
# Compare both versions
diff index.html ../consciousness-revolution-main/index.html

# Review key differences
# - Navigation structure
# - Feature listings
# - Styling/theming
# - Call-to-action buttons
```

**Decision Matrix:**
- If main repo has newer design → Use main repo
- If overview has better navigation → Merge nav from overview
- If both have unique features → Merge manually

**Recommended Approach:**
```bash
# Back up overview version
cp index.html index.html.overview-backup

# Use main repo as base
cp ../consciousness-revolution-main/index.html ./

# Extract unique elements from overview backup
# - Copy any unique <section> elements
# - Merge navigation menus
# - Preserve any overview-specific features
```

**Test:**
- Load in browser
- Check all links work
- Verify responsive design
- Test on mobile

---

### 2. dashboard.html
**Location:** Root directory  
**Conflict:** Different dashboard layouts and features

**Resolution Steps:**
```bash
# Compare features
grep -o '<section[^>]*>' dashboard.html
grep -o '<section[^>]*>' ../consciousness-revolution-main/dashboard.html
```

**Merge Strategy:**
1. Identify unique dashboard widgets in each version
2. Create unified dashboard with all widgets
3. Ensure consistent styling
4. Test all interactive elements

---

### 3. package.json
**Location:** Root directory  
**Conflict:** Different dependencies and scripts

**Critical File:** Requires careful merge to avoid breaking dependencies

**Resolution Steps:**
```bash
# Install jq for JSON manipulation
# Option 1: Manual merge
code package.json ../consciousness-revolution-main/package.json

# Option 2: Use npm-merge (if available)
npx npm-merge package.json ../consciousness-revolution-main/package.json
```

**Merge Checklist:**
- [ ] Merge `dependencies` - keep all unique packages
- [ ] Merge `devDependencies` - keep all unique packages
- [ ] Merge `scripts` - combine all scripts
- [ ] Keep highest version numbers
- [ ] Update `name`, `version`, `description` as needed
- [ ] Preserve both `repository` URLs if different

**After Merge:**
```bash
# Remove lockfile and node_modules
rm package-lock.json
rm -rf node_modules

# Clean install
npm install

# Audit for vulnerabilities
npm audit fix

# Test scripts
npm test
npm run build  # if available
```

---

### 4. netlify.toml
**Location:** Root directory  
**Conflict:** Different deployment configurations

**Resolution:**
```bash
# Compare configurations
diff netlify.toml ../consciousness-revolution-main/netlify.toml
```

**Merge Strategy:**
```toml
[build]
  # Use main repo build settings
  command = "npm run build"
  publish = "dist"
  
  # Add overview repo functions if unique
  functions = "netlify/functions"

[build.environment]
  # Merge all environment variables from both
  
[[redirects]]
  # Combine redirects from both versions
```

**Test:**
```bash
# Test locally with Netlify CLI
netlify dev

# Check all routes work
# Verify functions respond
```

---

### 5. README.md
**Location:** Root directory  
**Conflict:** Different documentation content

**Resolution Strategy:**
1. **Structure:** Use main repo structure as base
2. **Content:** Merge unique sections from both
3. **Links:** Verify all links work
4. **Examples:** Include examples from both

**Merge Sections:**
```markdown
# From main repo:
- Project description
- Core features
- Installation instructions

# From overview repo:
- Additional integrations
- Overview-specific features
- Extended documentation

# Combined:
- All repository links
- All feature lists
- Complete quick start guide
```

---

### 6. login.html
**Location:** Root and mandem.os/workspace/  
**Conflict:** Different authentication flows

**Resolution:**
- Use main repo version as authoritative
- Preserve any Supabase integration from overview
- Ensure Stripe integration works
- Test authentication flow

---

### 7. Configuration Files

#### .gitignore
**Strategy:** Merge all ignore patterns
```bash
# Combine unique entries from both
cat .gitignore > .gitignore.merged
cat ../consciousness-revolution-main/.gitignore >> .gitignore.merged
sort -u .gitignore.merged > .gitignore
rm .gitignore.merged
```

#### .env.example
**Strategy:** Merge all environment variables
```bash
# Combine and sort unique entries
cat .env.example ../consciousness-revolution-main/.env.example | sort -u > .env.example.new
mv .env.example.new .env.example
```

---

## Medium-Priority Files

### HTML Pattern Detectors
Files like:
- `GASLIGHTING_DETECTOR.html`
- `LOVE_BOMBING_DETECTOR.html`
- `EMOTIONAL_BLACKMAIL_DETECTOR.html`

**Resolution:**
- Compare AI integration features
- Use version with better UI/UX
- Preserve any unique pattern detection logic
- Ensure ARAYA integration works

**Test Each:**
```bash
# Open in browser
# Enter test data
# Verify pattern detection works
# Check results display correctly
# Test mobile responsiveness
```

---

### Dashboard Files
- `admin-dashboard.html`
- `analytics_dashboard.html`
- `builder-dashboard.html`

**Resolution:**
1. Identify unique features in each version
2. Merge dashboards to include all features
3. Ensure consistent styling
4. Test all data connections

---

### ARAYA System Files
- `araya-chat.html`
- `araya-light.html`
- `ARAYA_BRIDGE.py`

**Critical:** These are core to the system

**Resolution:**
- Use main repo as base (likely more up-to-date)
- Preserve any overview-specific enhancements
- Test ARAYA functionality thoroughly
- Ensure file writing works

---

## Low-Priority Files

### Duplicate index.html Files
Main repo has many nested `index.html` files in subdirectories:
- `ember-terminal/index.html`
- `mandem.os/index.html`
- `city-3d/index.html`

**Resolution:**
- These are different systems, not conflicts
- Keep all versions in their respective directories
- Ensure navigation between them works

---

## Automation Script for Conflicts

Create a helper script for common conflicts:

```bash
#!/bin/bash
# merge-conflicts.sh - Helper for resolving merge conflicts

resolve_config_files() {
    echo "Resolving configuration files..."
    
    # Merge .gitignore
    cat .gitignore ../consciousness-revolution-main/.gitignore | \
        sort -u > .gitignore.tmp && \
        mv .gitignore.tmp .gitignore
    
    # Merge .env.example
    cat .env.example ../consciousness-revolution-main/.env.example | \
        sort -u > .env.example.tmp && \
        mv .env.example.tmp .env.example
    
    echo "✓ Config files merged"
}

resolve_package_json() {
    echo "Resolving package.json..."
    echo "⚠ Requires manual review!"
    echo "Opening both files..."
    
    ${EDITOR:-code} package.json &
    ${EDITOR:-code} ../consciousness-revolution-main/package.json &
    
    echo "Merge manually, then run: npm install"
}

resolve_readme() {
    echo "Resolving README.md..."
    
    # Create merged README
    {
        head -n 1 README.md  # Keep title from overview
        echo ""
        echo "## From Main Repository"
        tail -n +2 ../consciousness-revolution-main/README.md
        echo ""
        echo "## Overview Repository Features"
        tail -n +2 README.md
    } > README.md.merged
    
    echo "✓ Created README.md.merged - review and rename to README.md"
}

# Run functions
resolve_config_files
resolve_package_json
resolve_readme
```

---

## Testing After Resolution

### Automated Tests
```bash
# HTML validation
for file in *.html; do
    echo "Validating $file..."
    # Use HTML validator
done

# JavaScript linting
npm run lint

# Python linting
find . -name "*.py" -exec pylint {} \;

# Run test suites
npm test
python -m pytest
```

### Manual Tests
- [ ] All pages load without errors
- [ ] Navigation works between all sections
- [ ] Login/authentication works
- [ ] ARAYA chat responds
- [ ] Pattern detectors work
- [ ] Dashboards display data
- [ ] Mobile responsive design works
- [ ] No console errors

---

## Conflict Resolution Log

Keep track of decisions made:

```markdown
## Conflict Resolution Log

### index.html
- **Date:** 2026-02-10
- **Decision:** Used main repo version
- **Reason:** Newer design, better mobile support
- **Preserved:** Navigation menu from overview
- **Tested:** ✓ Works on desktop and mobile

### package.json
- **Date:** 2026-02-10
- **Decision:** Merged dependencies from both
- **Reason:** Both had unique packages needed
- **Version conflicts:** Resolved by using latest versions
- **Tested:** ✓ npm install successful, tests pass

[Continue for each conflict...]
```

---

## Emergency Rollback

If conflict resolution breaks something:

```bash
# Restore specific file from backup
cp backup-20260210-HHMMSS/path/to/file ./path/to/file

# Or restore entire backup
rm -rf *
cp -r backup-20260210-HHMMSS/* ./

# Or use git
git checkout HEAD -- path/to/file
```

---

## Best Practices

1. **One conflict at a time** - Don't rush
2. **Test after each resolution** - Catch issues early
3. **Document decisions** - Keep conflict log updated
4. **Back up everything** - Before making changes
5. **Ask for help** - If unsure, consult team
6. **Review with fresh eyes** - Take breaks

---

## Success Criteria

- [ ] All 244 conflicts resolved
- [ ] No duplicate files with different names
- [ ] All tests passing
- [ ] Documentation updated
- [ ] Deployment successful
- [ ] No broken links
- [ ] Mobile responsive
- [ ] Accessible (WCAG AA)

---

**Last Updated:** 2026-02-10  
**Next Review:** After completing conflict resolution
