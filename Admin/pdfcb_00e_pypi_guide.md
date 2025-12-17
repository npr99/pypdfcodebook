# PyPI Publishing Guide

This guide walks you through transitioning from TestPyPI to the main PyPI for public package distribution using GitHub Actions and trusted publishing.

## Prerequisites

- Existing package tested on TestPyPI
- GitHub repository with release workflow configured
- Ready for public distribution

## 1. Set Up Main PyPI Account

### Create PyPI Account
1. Go to [https://pypi.org/account/register/](https://pypi.org/account/register/)
2. Create account (separate from TestPyPI account)
3. Verify email address
4. **Enable 2FA (Required)**: Set up two-factor authentication using an authenticator app

### Why Separate Account?
- TestPyPI (`test.pypi.org`) and PyPI (`pypi.org`) are completely separate services
- Different credentials for different environments
- Enhanced security isolation

## 2. Configure Trusted Publishing

### Set Up Trusted Publisher on PyPI
1. Log into [https://pypi.org](https://pypi.org)
2. Navigate to "Your account" → "Publishing"
3. Click "Add a new trusted publisher"
4. Configure with **exact** details:
   - **PyPI Project Name**: `pypdfcodebook`
   - **Repository owner**: `npr99`
   - **Repository name**: `pypdfcodebook`
   - **Workflow filename**: `release.yml`
   - **Environment name**: `release` 

### Why Trusted Publishing?
- No API tokens to manage
- Enhanced security through OpenID Connect (OIDC)
- Automatic authentication via GitHub Actions
- Required for modern PyPI publishing

## 3. Create GitHub Release Environment

### Set Up Release Environment
1. Go to your repository: `https://github.com/npr99/pypdfcodebook/settings/environments`
2. Click "New environment"
3. Name: `release`
4. Click "Configure environment"
5. **Optional**: Add protection rules:
   - Require reviewers before deployment
   - Restrict to specific branches (main)
   - Add deployment delays

### Environment Benefits
- Additional security layer
- Audit trail for releases
- Controlled deployment process

## 4. Verify Release Workflow Configuration

Your workflow should be configured as:

```yaml
name: Release

on:
  release:
    types: [published]

jobs:
  build-and-publish:
    runs-on: ubuntu-latest
    environment: release
    permissions:
      id-token: write
    steps:
    - name: Checkout
      uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'
    - name: Install build dependencies
      run: python -m pip install -U setuptools wheel build
    - name: Build
      run: python -m build .
    - name: Publish
      uses: pypa/gh-action-pypi-publish@release/v1
      with:
        skip-existing: true
```

## 5. Pre-Release Checklist

### Version Management
- [ ] Update version in `pyproject.toml` (under `[project] version`)
- [ ] Update `__version__` in `src/pypdfcodebook/__init__.py`
- [ ] Ensure both versions match exactly
- [ ] Version should be higher than any TestPyPI versions

### Quality Checks
- [ ] Run full test suite: `pytest`
- [ ] Verify package builds: `python -m build`
- [ ] Check metadata: Review `pyproject.toml` completeness
- [ ] Update documentation if needed
- [ ] Clean build artifacts:
  ```powershell
  Remove-Item dist\* -Force -ErrorAction SilentlyContinue
  Remove-Item build\* -Recurse -Force -ErrorAction SilentlyContinue
  Get-ChildItem -Path . -Filter *.egg-info -Recurse | Remove-Item -Recurse -Force
  ```

## 6. Create Release

### Release Process
1. **Go to GitHub**: Navigate to your repository releases page
2. **Click "Create a new release"**
3. **Create new tag**: Use semantic versioning (e.g., `v0.4.6`)
4. **Release title**: Use same version (e.g., `v0.4.6`)
5. **Release notes**: Document changes, improvements, bug fixes
6. **Publish release**: Click "Publish release"

### Automatic Publishing
- GitHub Actions workflow automatically triggers
- Builds package using `python -m build`
- Publishes to PyPI using trusted publishing
- Monitor workflow progress in Actions tab

## 7. Verify Publication

### Check PyPI
- Visit [https://pypi.org/project/pypdfcodebook/](https://pypi.org/project/pypdfcodebook/)
- Verify correct version published
- Check metadata display correctly

### Test Installation
Create fresh environment and test:
```sh
# Create clean test environment
python -m venv test_env
test_env\Scripts\activate  # Windows
# source test_env/bin/activate  # macOS/Linux

# Install from main PyPI
pip install pypdfcodebook

# Test import and version
python -c "import pypdfcodebook; print(pypdfcodebook.__version__)"
```

## 8. Update Documentation

### README Updates
- [ ] Update installation instructions to use main PyPI
- [ ] Remove TestPyPI references
- [ ] Add badges for PyPI version, downloads
- [ ] Update examples if needed

### Example Installation Command
Users can now install with:
```sh
pip install pypdfcodebook
```

## 9. Maintenance

### Future Releases
1. Make changes to your code
2. Update version numbers
3. Create new GitHub release
4. Automatic publication to PyPI

### Version Strategy
- **Patch** (0.4.6 → 0.4.7): Bug fixes
- **Minor** (0.4.7 → 0.5.0): New features, backward compatible
- **Major** (0.5.0 → 1.0.0): Breaking changes

### Rollback Strategy
- PyPI doesn't allow overwriting published versions
- If issues found, publish new patch version
- Use `pip install pypdfcodebook==0.4.5` for specific versions

## Troubleshooting

### Trusted Publishing Errors
```
Publisher with matching claims was not found
```
**Solution**: Verify exact match between PyPI configuration and workflow:
- Repository owner/name
- Workflow filename
- Environment name

### Build Failures
**Check**: 
- Version numbers match in both files
- All dependencies specified correctly
- Tests passing before release

### Publication Delays
- PyPI indexing may take a few minutes
- Check workflow logs for detailed error messages
- Verify 2FA is properly configured

## Security Best Practices

- [ ] Never commit API tokens to repository
- [ ] Use trusted publishing instead of tokens
- [ ] Enable 2FA on PyPI account
- [ ] Review release environment settings
- [ ] Monitor package for unauthorized changes

### Trusted Publishing Security Model

**Package Ownership Protection**: Trusted publishers can only be configured for packages you own on PyPI. Others cannot hijack publishing to your existing packages.

**Key Security Features**:
- **Package names are globally unique** - first publisher owns the name
- **No account linking required** - GitHub and PyPI accounts remain separate  
- **OIDC token validation** - automatic cryptographic verification
- **Repository specificity** - only your exact repo/workflow combination can publish

**Potential Risks**:
- **Name squatting**: Register your package name early to prevent others claiming it
- **Typosquatting**: Monitor for similar package names (e.g., `pypdfcodbook`)
- **Account compromise**: Use strong 2FA and monitor account activity

**Best Practices**: Claim package name early, monitor for typosquats, secure PyPI account with 2FA.

## Differences from TestPyPI

| Aspect | TestPyPI | Main PyPI |
|--------|----------|-----------|
| URL | test.pypi.org | pypi.org |
| Authentication | API Tokens | Trusted Publishing (preferred) |
| Publishing | Manual uploads | GitHub Actions |
| Versioning | Can reuse versions | Immutable versions |
| Audience | Testing only | Public production |
| Dependencies | May be missing | Full ecosystem |

---
*Maintained by project admin. Last updated: 2025-12-17.*