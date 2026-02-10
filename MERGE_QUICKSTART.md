# Quick Start: Merging Main Repository

This guide provides quick instructions for merging the main consciousness-revolution repository into this overview repository.

## Prerequisites

1. **Access to main repository**: You need access to `https://github.com/overkor-tek/consciousness-revolution`
2. **Git installed**: Version 2.x or higher
3. **GitHub credentials**: SSH key or personal access token configured
4. **Disk space**: At least 500MB free space
5. **Permissions**: Write access to this repository

## Quick Merge (Automated)

### Option 1: Using the Merge Script

```bash
# If main repo is not cloned yet
./merge-main-repo.sh

# If main repo is already cloned elsewhere
./merge-main-repo.sh /path/to/consciousness-revolution
```

The script will:
- Create a backup of current state
- Clone/pull main repository
- Merge all systems systematically
- Update configuration files
- Run tests
- Commit changes

### Option 2: Manual Merge (Step-by-Step)

```bash
# 1. Clone main repository (if not already done)
cd ..
git clone https://github.com/overkor-tek/consciousness-revolution.git consciousness-revolution-main
cd consciousness-revolution--AgentR-overview

# 2. Copy core systems
cp -r ../consciousness-revolution-main/ember-terminal ./
cp -r ../consciousness-revolution-main/GemBotMemory2025 ./
cp -r ../consciousness-revolution-main/city-3d ./
cp -r ../consciousness-revolution-main/mandem.os ./
cp -r ../consciousness-revolution-main/OSKeyMap ./
cp -r ../consciousness-revolution-main/rdata ./

# 3. Copy supporting systems
cp -r ../consciousness-revolution-main/projects ./
cp -r ../consciousness-revolution-main/language-samples ./
cp -r ../consciousness-revolution-main/scripts ./
cp -r ../consciousness-revolution-main/logs ./

# 4. Copy backend enhancements (if not exists)
if [ -d ../consciousness-revolution-main/backend ]; then
    cp -r ../consciousness-revolution-main/backend/* ./BACKEND/ 2>/dev/null || true
fi

# 5. Review and merge configuration files manually
# Compare and merge: package.json, .env.example, netlify.toml

# 6. Install dependencies
npm install

# 7. Run tests
npm test

# 8. Commit changes
git add .
git commit -m "Merge main repository features"
git push
```

## What Gets Merged

Based on `content_comparison_data.json`, approximately **1,140 files** will be added:

### Major Systems (~700 files)
- **ember-terminal** - Terminal interface system
- **GemBotMemory2025** - AI control and quantum visualization
- **city-3d** - 3D visualization tools
- **mandem.os** - Operating system interface
- **projects/** - Sub-projects including LINKt
- **language-samples** - Multi-language examples

### Supporting Files (~440 files)
- Backend scripts and services
- Configuration files
- Log management
- Utility scripts
- Documentation

## Quick Verification

After merge, verify these systems are present:

```bash
# Check core systems
ls -d ember-terminal GemBotMemory2025 city-3d mandem.os OSKeyMap rdata

# Check supporting systems
ls -d projects language-samples scripts logs

# Count total files
find . -type f | wc -l
# Should be around 1,890+ files (750 + 1,140)
```

## Quick Testing

```bash
# Test that key HTML files exist and are valid
for file in ember-terminal/index.html mandem.os/index.html city-3d/index.html; do
    if [ -f "$file" ]; then
        echo "✓ $file exists"
    else
        echo "✗ $file missing"
    fi
done

# Test npm dependencies
npm list --depth=0

# Test Python scripts (if applicable)
find . -name "*.py" -type f | head -10 | while read file; do
    python3 -m py_compile "$file" && echo "✓ $file" || echo "✗ $file"
done
```

## Common Issues

### Issue: Main repo clone fails
**Solution:**
```bash
# Use SSH instead of HTTPS
git clone git@github.com:overkor-tek/consciousness-revolution.git

# Or configure GitHub token
gh auth login
```

### Issue: Permission denied
**Solution:**
```bash
# Check if you have access to main repo
gh repo view overkor-tek/consciousness-revolution

# Or verify your SSH keys
ssh -T git@github.com
```

### Issue: Merge conflicts
**Solution:**
- Review `MERGE_PLAN.md` for conflict resolution strategies
- Use `git status` to identify conflicting files
- Manually resolve each conflict
- Test after resolution

### Issue: Dependencies conflict
**Solution:**
```bash
# Remove node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall with merged package.json
npm install

# Fix any audit issues
npm audit fix
```

## Post-Merge Checklist

- [ ] All core systems present
- [ ] All HTML pages load
- [ ] Navigation works
- [ ] No console errors
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Changes committed
- [ ] Changes pushed

## Rollback

If something goes wrong:

```bash
# If not yet committed
git reset --hard HEAD
git clean -fd

# If committed
git reset --hard <commit-before-merge>

# If pushed
git revert HEAD
```

## Need Help?

1. **Check logs**: `merge-progress.log` if using script
2. **Review plan**: `MERGE_PLAN.md` for detailed strategy
3. **Check report**: `MERGE_REPORT.md` after script runs
4. **Discord**: https://discord.gg/xHRXyKkzyg
5. **Email**: darrickpreble@proton.me

## Detailed Documentation

For comprehensive merge strategy and details, see:
- `MERGE_PLAN.md` - Complete 7-phase merge plan
- `content_comparison_data.json` - Detailed file comparison
- `SYSTEMS_AND_LINKS_CATALOG.md` - System documentation

---

**Estimated Time:** 2-4 hours (automated script)  
**Estimated Time:** 4-8 hours (manual merge)

**Last Updated:** 2026-02-10
