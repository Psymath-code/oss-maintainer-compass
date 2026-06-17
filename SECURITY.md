# Security Policy

## Supported Versions

We release security updates for:

- Current stable release (latest)
- Previous stable release (patch fixes only)

Version 0.x releases are supported for critical security issues only.

## Reporting Security Issues

**Please do not open public GitHub issues for security vulnerabilities.** Instead:

1. Email security details to the project maintainer privately
2. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)
3. Allow 7-14 days for a response before public disclosure

We take all security reports seriously and will:
- Acknowledge receipt within 24 hours
- Work on a fix
- Release a patched version
- Credit the reporter (unless requested otherwise)

## Security Considerations

### Input Validation

This tool processes GitHub issue/PR data. When using:

- **Local JSON files** – Validate source and ensure files aren't modified
- **GitHub API** – Use authenticated requests with minimal scopes
- **Agent handoff reports** – Review AI-generated content before trusting it

### GitHub API Credentials

If extended to support live API pulls:

- Use GitHub Personal Access Tokens (PATs) with minimal scopes
- Never commit credentials to version control
- Use environment variables or `.env` files (not in git)
- Rotate tokens regularly
- Use organization-level secrets for CI/CD

### Data Privacy

- Issue/PR data may contain sensitive information (security reports, internal discussions)
- Do not share generated reports publicly without review
- Maintain appropriate access controls on export files
- Be cautious when feeding reports to external AI services

### Dependency Safety

This project has zero runtime dependencies (intentionally). When adding dependencies:

- Evaluate for security track record
- Check for known vulnerabilities: [PyPI Safety Check](https://safety.pypa.io/)
- Prefer well-maintained, widely-used libraries
- Consider maintenance burden
- Document rationale

### Code Review

- All changes go through pull request review
- At least one maintainer approval required
- Security-sensitive changes may need additional scrutiny

## Known Limitations

1. **JSON parsing** – Malformed GitHub exports may cause crashes (should be caught by tests)
2. **Large datasets** – Very large repositories may have performance issues
3. **Rate limiting** – Future API integration should handle GitHub rate limits
4. **File permissions** – Ensure generated reports have appropriate access controls

## Responsible Disclosure

We appreciate security researchers who:

- Report vulnerabilities responsibly
- Give us time to fix before disclosure
- Avoid data destruction or privacy violations
- Avoid spamming or social engineering

Thank you for helping keep this project secure!
