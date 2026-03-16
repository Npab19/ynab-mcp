# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please **do not open a public GitHub issue**.

Instead, report it privately by opening a [GitHub Security Advisory](https://github.com/Npab19/ynab-mcp/security/advisories/new).

Please include:
- A description of the vulnerability
- Steps to reproduce
- Potential impact
- Any suggested fixes (optional)

You can expect an initial response within 48 hours.

## Scope

This project is a self-hosted MCP server. The following are in scope:

- Authentication bypass vulnerabilities
- Injection vulnerabilities in MCP tool handlers
- Container escape or privilege escalation issues
- Credential exposure risks

## Out of Scope

- Vulnerabilities in the YNAB API itself — report those to YNAB directly
- Issues requiring physical access to the host machine
- Social engineering attacks
