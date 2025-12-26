# Security Policy

## Supported Versions

This website is continuously updated. Only the latest version deployed to GitHub Pages is supported.

## Security Best Practices

This website implements the following security best practices:

### External Links
- All external links opening in new tabs include `rel="noopener noreferrer"` to prevent tab-nabbing attacks

### Content Security
- HTML sanitization is enabled in Hugo configuration
- User-generated content is properly escaped
- No inline JavaScript execution from user content

### HTTPS
- Site is served exclusively over HTTPS via GitHub Pages
- All external resources are loaded over HTTPS

### Dependencies
- Bootstrap 5.3.3 loaded from official CDN with SRI (Subresource Integrity) hashes
- Google Fonts loaded from official sources
- Regular updates to dependencies

## Recommended HTTP Security Headers

When deploying this site, consider adding the following HTTP security headers (via GitHub Pages settings or reverse proxy):

```
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://www.googletagmanager.com; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com https://cdn.jsdelivr.net; img-src 'self' data: https:; connect-src 'self' https://www.google-analytics.com;
X-Frame-Options: SAMEORIGIN
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=(), camera=()
```

## Reporting a Vulnerability

If you discover a security vulnerability in this website, please report it by:

1. **Email**: Send details to ywchoi02@sogang.ac.kr
2. **Subject**: Include "[SECURITY]" in the email subject
3. **Details**: Provide:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### Response Timeline

- **Initial Response**: Within 48 hours
- **Assessment**: Within 1 week
- **Fix**: Critical issues patched within 2 weeks

## Responsible Disclosure

We appreciate responsible disclosure and will:
- Acknowledge your contribution (if desired)
- Keep you informed of the fix progress
- Credit you in the changelog (unless you prefer to remain anonymous)

## Out of Scope

The following are considered out of scope:
- Social engineering attacks
- Physical attacks
- Denial of service attacks
- Issues in third-party services (Google Analytics, CDNs)

Thank you for helping keep our website secure!
