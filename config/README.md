# Configuration Directory

This directory contains configuration files for the Newsletter Manager system.

## Configuration Files

### 1. Environment Variables
**File:** [.env.template](\.env.template)

Template for environment-specific settings (API keys, database URLs, secrets).

**Usage:**
1. Copy to `.env` in project root
2. Fill in actual values
3. Never commit `.env` to version control

**Categories:**
- Database configuration
- Channel credentials (Slack, Email)
- AI service API keys
- Storage settings
- Application settings
- Security configuration
- Feature flags

---

### 2. Application Settings
**File:** [settings.json](settings.json)

Application behavior configuration (non-sensitive settings).

**Categories:**
- Agent behavior defaults
- Channel configurations
- Content generation parameters
- Image generation settings
- Article defaults
- Confirmation requirements
- Bulk operation limits
- Context resolution settings
- Memory TTL settings
- Rate limits
- Error handling
- Workflow settings
- Logging and monitoring

---

## Environment-Specific Configurations

### Development
- `DATABASE_URL`: Local database
- `LOG_LEVEL`: debug
- `FEATURE_FLAGS`: All enabled for testing
- Relaxed rate limits

### Staging
- `DATABASE_URL`: Staging database
- `LOG_LEVEL`: info
- `FEATURE_FLAGS`: Match production
- Production-like rate limits

### Production
- `DATABASE_URL`: Production database
- `LOG_LEVEL`: warn
- `FEATURE_FLAGS`: Stable features only
- Strict rate limits
- Enhanced security settings

---

## Configuration Best Practices

### Security
1. Never commit sensitive values to git
2. Use `.env` for secrets (excluded in `.gitignore`)
3. Rotate API keys regularly
4. Use different credentials per environment
5. Limit API key permissions to minimum required

### Organization
1. Group related settings together
2. Use clear, descriptive names
3. Include units in names (e.g., `_seconds`, `_mb`)
4. Document non-obvious settings
5. Use consistent naming conventions

### Defaults
1. Provide sensible defaults in code
2. Make common cases easy to configure
3. Validate configuration on startup
4. Fail fast on missing required settings
5. Log configuration warnings

---

## Loading Configuration

Recommended loading order:
1. Default values (hardcoded in application)
2. `settings.json` (general application config)
3. `.env` file (environment-specific overrides)
4. Environment variables (highest priority, useful for container deployments)

---

## Adding New Configuration

When adding new configuration:

1. **Determine sensitivity**
   - Sensitive (API keys, secrets) → `.env.template`
   - Non-sensitive (behavior settings) → `settings.json`

2. **Choose appropriate default**
   - Fail-safe default when possible
   - No default for required critical settings

3. **Document the setting**
   - Add comment explaining purpose
   - Document valid values/ranges
   - Note any dependencies

4. **Consider environment differences**
   - May need different values in dev/staging/prod
   - Document recommended values per environment

---

## Configuration Validation

On application startup, validate:
- Required settings are present
- Values are within acceptable ranges
- Dependent settings are compatible
- API credentials are valid (optional pre-flight check)

Log warnings for:
- Using default values
- Deprecated settings
- Unusual value combinations

---

## Future Enhancements

Potential configuration improvements:
- **Dynamic config updates** - Reload without restart
- **Feature flags service** - Centralized feature toggle
- **Secrets management** - Integration with HashiCorp Vault, AWS Secrets Manager
- **Config validation schema** - JSON Schema or similar
- **Multi-tenant support** - Per-organization settings
