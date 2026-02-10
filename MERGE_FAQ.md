# Merge FAQ (Frequently Asked Questions)

Common questions and answers about merging the main consciousness-revolution repository with this overview repository.

---

## General Questions

### Q: Why do we need to merge these repositories?

**A:** The main repository (`overkor-tek/consciousness-revolution`) contains ~1,140 files and enhanced features that aren't in this overview repository. These include:
- ember-terminal system
- GemBotMemory2025 AI control
- city-3d visualizations
- mandem.os interface
- Additional backend services
- Enhanced scripts and utilities

Merging brings all these features into one unified repository.

---

### Q: Will the merge break existing functionality?

**A:** No, if done correctly:
- The merge script creates automatic backups
- Each phase is tested before proceeding
- Existing files are only updated if beneficial
- Rollback procedures are documented
- The merge follows a systematic, tested approach

---

### Q: How long will the merge take?

**A:** Time estimates:
- **Automated (using script):** 2-4 hours
- **Manual (step-by-step):** 4-8 hours
- **Comprehensive (with full testing):** 14-21 hours

The automated script significantly reduces time and errors.

---

### Q: Can I merge only specific systems?

**A:** Yes! The merge plan supports selective merging:
```bash
# Merge only ember-terminal
cp -r ../consciousness-revolution-main/ember-terminal ./

# Merge only city-3d
cp -r ../consciousness-revolution-main/city-3d ./

# Test each system individually
```

See MERGE_PLAN.md for detailed instructions per system.

---

## Technical Questions

### Q: What if I don't have access to the main repository?

**A:** You need access to proceed. Options:
1. **GitHub access:** Request access from repository owner
2. **Clone URL:** Ask owner for clone URL if private
3. **Local copy:** If someone has cloned it, use their copy
4. **Zip archive:** Owner can provide a zip of the repo

Without access, you can still review the merge documentation to understand what will be merged.

---

### Q: How do I handle npm dependency conflicts?

**A:** The merge script handles this, but if doing manually:

```bash
# 1. Backup current package.json
cp package.json package.json.backup

# 2. Manually merge dependencies
# - Combine all unique packages
# - Use highest version numbers
# - Keep all scripts

# 3. Clean install
rm package-lock.json
rm -rf node_modules
npm install

# 4. Fix vulnerabilities
npm audit fix

# 5. Test
npm test
```

---

### Q: What about environment variables?

**A:** Environment variables are merged:

```bash
# .env.example will combine variables from both repos
# After merge, update your local .env with any new variables

# Check for new variables
diff .env .env.example

# Add missing variables to .env
```

Common new variables might include:
- Additional API keys
- Database URLs
- Feature flags
- Service endpoints

---

### Q: Will my local changes be overwritten?

**A:** No, with precautions:
1. **Backup created:** Script creates automatic backup
2. **Git status check:** Script warns if uncommitted changes
3. **Interactive prompts:** Script asks before overwriting
4. **Commit first:** Best practice - commit local changes before merge

---

### Q: Can I test the merge before committing?

**A:** Yes! The merge script:
1. Creates a backup first
2. Merges files
3. Runs tests
4. Shows git status
5. **Asks permission** before committing

You can review all changes before finalizing.

---

## File Conflict Questions

### Q: Why are there 244 file conflicts?

**A:** These files have the same name but different content in both repos. Each requires a decision:
- Use main repo version
- Use overview version
- Merge both versions
- Create new combined version

See MERGE_CONFLICT_RESOLUTION.md for detailed strategies.

---

### Q: How do I decide which version to keep?

**A:** Use this decision tree:

```
Is the file critical (index.html, package.json)?
├─ YES → Merge both versions carefully
└─ NO → Check which is newer/better
    ├─ Main repo newer → Use main repo
    ├─ Overview has unique features → Merge features
    └─ Functionally identical → Use either (prefer main)
```

---

### Q: Can I automate conflict resolution?

**A:** Partially. The merge script handles:
- ✅ Configuration files (.gitignore, .env)
- ✅ Non-critical HTML files
- ⚠️ Critical files (index.html, package.json) need manual review
- ⚠️ Files with unique features need manual merge

For full automation, use:
```bash
# Accept main repo for all non-critical files
./merge-main-repo.sh --auto-resolve
```

(Note: `--auto-resolve` flag can be added to script if needed)

---

## System-Specific Questions

### Q: What is ember-terminal?

**A:** A terminal interface system from the main repo that provides:
- Command-line interface in browser
- Workspace management
- Task execution
- Developer tools

After merge, accessible at `/ember-terminal/index.html`

---

### Q: What is GemBotMemory2025?

**A:** An AI web control system including:
- Quantum neural network visualization (3D)
- AI-powered web automation
- Memory management for AI agents
- Advanced visualization tools

After merge, accessible at `/GemBotMemory2025/`

---

### Q: What is mandem.os?

**A:** A full operating system interface that provides:
- Workspace environment
- Application launcher
- File management
- User authentication
- Multi-window system

After merge, accessible at `/mandem.os/index.html`

---

### Q: Will these systems work with existing features?

**A:** Yes, they're designed to integrate:
- ember-terminal works with existing scripts
- GemBotMemory2025 integrates with AI orchestration
- mandem.os connects to Seven Domains
- All systems use sacred geometry theme

Integration points are documented in MERGE_PLAN.md

---

## Testing Questions

### Q: How do I test after merge?

**A:** Follow this checklist:

**Automated Tests:**
```bash
npm test              # Run test suite
npm run lint          # Check code quality
python -m pytest      # Python tests
```

**Manual Tests:**
- Open index.html → Check landing page
- Navigate to each new system → Verify loads
- Test existing features → Ensure still work
- Check mobile → Responsive design
- Open console → No errors
- Test ARAYA → Still functional
- Test pattern detectors → Still work

Detailed testing guide in MERGE_PLAN.md Phase 6.

---

### Q: What if tests fail after merge?

**A:** Troubleshooting steps:

1. **Check merge log:**
```bash
cat merge-progress.log  # Review what was merged
```

2. **Identify failing component:**
```bash
npm test -- --verbose  # See detailed test output
```

3. **Rollback if needed:**
```bash
# Restore from backup
cp -r backup-TIMESTAMP/* ./

# Or use git
git reset --hard HEAD~1
```

4. **Fix specific issue:**
- Review MERGE_CONFLICT_RESOLUTION.md
- Check file-specific merge decisions
- Verify dependencies installed

5. **Re-run tests:**
```bash
npm test
```

---

## Deployment Questions

### Q: Can I deploy during merge?

**A:** Not recommended:
- Merge on feature branch first
- Test thoroughly
- Only deploy after verification
- Use staging environment first

---

### Q: How do I deploy after merge?

**A:** Standard deployment:

```bash
# 1. Verify all tests pass
npm test

# 2. Build if needed
npm run build

# 3. Deploy to staging
netlify deploy

# 4. Test staging
# Visit staging URL and test

# 5. Deploy to production
netlify deploy --prod
```

Deployment checklist in MERGE_PLAN.md Phase 6.

---

### Q: What if deployment fails?

**A:** Rollback procedure:

```bash
# Quick rollback (if not committed)
git reset --hard HEAD

# Rollback specific commit
git revert <commit-hash>

# Deploy previous version
git checkout HEAD~1
netlify deploy --prod

# Or use Netlify's rollback feature
netlify rollback
```

---

## Security Questions

### Q: Are there security concerns with merging?

**A:** Security is maintained:
- ✅ API keys remain in .env (not committed)
- ✅ .gitignore prevents secret exposure
- ✅ All merged code is from trusted source
- ✅ Dependencies are audited (npm audit)
- ✅ Secrets are validated before merge

---

### Q: How are secrets handled in merge?

**A:** Secret management:

1. **Never committed:**
```bash
# .gitignore includes
.env
*.key
secrets/
```

2. **Environment variables:**
```bash
# Merge .env.example only (no actual secrets)
# Update local .env with new variables
```

3. **Validation:**
```bash
# Check no secrets in code
grep -r "sk_live\|pk_live\|api_key.*=" . --exclude-dir=node_modules
```

4. **After merge:**
- Rotate any exposed secrets
- Verify .env not committed
- Update secrets management docs

---

## Maintenance Questions

### Q: How do I keep repos in sync after merge?

**A:** Post-merge sync strategy:

```bash
# Keep main repo as upstream
git remote add upstream https://github.com/overkor-tek/consciousness-revolution.git

# Periodically sync
git fetch upstream
git merge upstream/main

# Or cherry-pick specific commits
git cherry-pick <commit-hash>
```

---

### Q: Can I merge again in the future?

**A:** Yes! The merge tools are reusable:
```bash
# Run merge script again anytime
./merge-main-repo.sh

# It will detect existing files and handle conflicts
# Use for periodic syncs or new feature integration
```

---

### Q: What if main repo has breaking changes?

**A:** Handle carefully:
1. Review main repo changelog
2. Identify breaking changes
3. Test in feature branch first
4. Update overview code to handle breaks
5. Merge when compatible
6. Document migration guide

---

## Troubleshooting

### Q: Script fails with "permission denied"

**A:** Make script executable:
```bash
chmod +x merge-main-repo.sh
./merge-main-repo.sh
```

---

### Q: Git says "repository not found"

**A:** Check authentication:
```bash
# Test GitHub access
ssh -T git@github.com

# Or configure token
gh auth login

# Or clone with HTTPS
git clone https://github.com/overkor-tek/consciousness-revolution.git
```

---

### Q: npm install fails after merge

**A:** Fix dependencies:
```bash
# Clear cache
npm cache clean --force

# Remove and reinstall
rm -rf node_modules package-lock.json
npm install

# If still fails, check Node version
node --version  # Should be 18+
```

---

### Q: File conflicts I can't resolve

**A:** Get help:
1. Document the conflict
2. Check MERGE_CONFLICT_RESOLUTION.md for that file
3. Ask on Discord: https://discord.gg/xHRXyKkzyg
4. Open issue with details
5. Tag repository maintainer

---

## Performance Questions

### Q: Will merge slow down the repo?

**A:** Minimal impact:
- Git is optimized for large repos
- Only modified files affect performance
- Use .gitignore to exclude large files
- Assets can be optimized post-merge

---

### Q: How much disk space needed?

**A:** Space requirements:
- Main repo: ~200MB
- Backup: ~200MB (temporary)
- Merged repo: ~400MB
- With node_modules: ~600MB

**Minimum recommended:** 1GB free space

---

## Next Steps Questions

### Q: I've read all the docs, what now?

**A:** Ready to merge!

1. **Checklist:**
   - [ ] Understood merge scope
   - [ ] Have main repo access
   - [ ] Read MERGE_PLAN.md
   - [ ] Read MERGE_QUICKSTART.md
   - [ ] Backed up important work
   - [ ] Created feature branch

2. **Execute:**
   ```bash
   git checkout -b merge-main-repo
   ./merge-main-repo.sh
   ```

3. **Test and deploy:**
   - Follow testing checklist
   - Review all changes
   - Deploy when ready

---

### Q: Where can I get more help?

**A:** Support resources:
- 📖 **Documentation:** This repo's MD files
- 💬 **Discord:** https://discord.gg/xHRXyKkzyg
- 📧 **Email:** darrickpreble@proton.me
- 🐛 **Issues:** GitHub issues in this repo
- 📚 **Guides:** MERGE_PLAN.md and related docs

---

### Q: Can I contribute improvements to merge process?

**A:** Absolutely!
1. Test the merge process
2. Document any issues
3. Suggest improvements
4. Submit PR with enhancements
5. Help others in Discord

---

## Still Have Questions?

1. **Check documentation:**
   - MERGE_PLAN.md
   - MERGE_QUICKSTART.md
   - MERGE_CONFLICT_RESOLUTION.md

2. **Search existing issues:**
   - GitHub issues in this repo
   - GitHub issues in main repo

3. **Ask community:**
   - Discord: https://discord.gg/xHRXyKkzyg
   - Create GitHub issue

4. **Contact maintainer:**
   - Email: darrickpreble@proton.me
   - Tag in PR or issue

---

**Last Updated:** 2026-02-10  
**Maintained By:** Consciousness Revolution Team

*Have a question not listed here? Open an issue or PR to add it!*
