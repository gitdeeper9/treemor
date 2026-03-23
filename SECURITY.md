# Security Policy for TREEMOR

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | ✅                 |
| < 1.0   | ❌                 |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security issue, please:

1. **Do NOT** open a public GitHub issue
2. Email the maintainer directly: **gitdeeper@gmail.com**
3. Include as much information as possible:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

You can expect:
- Initial acknowledgment within 48 hours
- Regular updates on progress
- Credit for disclosure (if desired)

## Security Best Practices

### For TREEMOR Users

1. **API Keys**: Never commit `.env` files with real credentials. Use `.env.example` as template.

2. **Database**: Always change default passwords in production:
   ```bash
   # Never use default passwords in production!
   DB_PASSWORD=use_strong_random_password
```

1. Network: Deploy TREEMOR behind a firewall. Only expose necessary ports:
   · Dashboard: 8050 (internal) / 443 (HTTPS external)
   · Database: 5432 (internal only)
   · Metrics: 9090 (internal only)
2. SSL/TLS: Always use HTTPS in production. Example nginx configuration:
   ```nginx
   server {
       listen 443 ssl http2;
       ssl_certificate /etc/ssl/certs/treomor.crt;
       ssl_certificate_key /etc/ssl/private/treomor.key;
       # ... rest of configuration
   }
   ```
3. Authentication: Enable JWT authentication for API endpoints:
   ```bash
   JWT_SECRET_KEY=generate_strong_32_char_key
   ```

For TREEMOR Developers

1. Dependencies: Regularly update dependencies to patch known vulnerabilities:
   ```bash
   pip list --outdated
   safety check
   ```
2. Code Scanning: Use pre-commit hooks with bandit:
   ```bash
   pre-commit install
   pre-commit run --all-files
   ```
3. Secrets Scanning: Never commit secrets. Use tools like gitleaks or trufflehog:
   ```bash
   gitleaks detect --source . --verbose
   ```
4. Input Validation: Always validate user inputs, especially for:
   · Sensor data uploads (validate HDF5/NetCDF structure)
   · API parameters (use Pydantic models)
   · File paths (prevent path traversal)
5. Logging: Never log sensitive information (passwords, tokens). Use structured logging:
   ```python
   import structlog
   logger = structlog.get_logger()
   logger.info("User login", user_id=user.id, status="success")
   # Do NOT log: password, token, session_id
   ```

Data Privacy

TREEMOR may process:

· Seismic event locations (potentially near critical infrastructure)
· Sensor deployment coordinates (may indicate sensitive locations)
· Timestamps of events

Best Practices:

· Anonymize location data if sharing publicly
· Use aggregation for published datasets (e.g., 1km grid cells)
· Comply with local data protection regulations (GDPR, CCPA)

Known Vulnerabilities (None)

As of version 1.0.0, no known security vulnerabilities have been identified.

Responsible Disclosure

We follow responsible disclosure practices:

· Reporters will be acknowledged (if desired)
· Fixed will be released as patches
· CVEs will be assigned for critical issues

Contact

· Security issues: gitdeeper@gmail.com
· PGP Key: Available upon request

---

Last updated: 2026-03-23
