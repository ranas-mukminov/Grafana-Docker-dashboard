# Security Policy

## Reporting Security Vulnerabilities

We take security seriously. If you discover a security vulnerability in this dashboard, please report it responsibly.

### How to Report

**Please do NOT open public GitHub issues for security vulnerabilities.**

Instead, report security issues privately via email:

📧 **Email:** [security@run-as-daemon.ru](mailto:security@run-as-daemon.ru)

### What to Include

When reporting a security issue, please provide:

* **Description** — Clear description of the vulnerability
* **Impact** — Potential impact if exploited
* **Steps to reproduce** — Detailed steps to reproduce the issue
* **Affected versions** — Dashboard version(s) affected
* **Environment** — Prometheus, Grafana, and exporter versions (if relevant)
* **Proof of concept** — PoC code or screenshots (if applicable)
* **Suggested fix** — If you have ideas on how to fix it

### What to Expect

* **Acknowledgment** — We'll acknowledge receipt of your report within 3-5 business days
* **Updates** — We'll keep you informed about progress on the issue
* **Credit** — If you wish, we'll credit you for the discovery when announcing the fix
* **No SLA** — This is a community project; we can't guarantee specific response times

### Security Scope

This project is a **Grafana dashboard configuration** (JSON file) and documentation. Potential security concerns include:

* **PromQL injection** — If dashboard variables allow arbitrary PromQL queries
* **XSS vulnerabilities** — If user input is reflected without sanitization
* **Information disclosure** — If the dashboard exposes sensitive system information inappropriately
* **Authentication bypass** — Issues with Grafana datasource authentication

**Out of scope:**
* Security issues in Prometheus itself
* Security issues in Grafana itself
* Security issues in cAdvisor or node_exporter
* Infrastructure-specific security misconfigurations
* General security best practices (unless they're specific to this dashboard)

### Security Best Practices

When using this dashboard:

1. **Secure Grafana access** — Use authentication and HTTPS
2. **Limit Prometheus access** — Don't expose Prometheus publicly without authentication
3. **Network segmentation** — Keep monitoring infrastructure on secure networks
4. **Regular updates** — Keep Grafana, Prometheus, and exporters updated
5. **Review permissions** — Limit who can edit dashboards and datasources
6. **Monitor access logs** — Track who accesses monitoring systems

### Known Limitations

This dashboard:
* Requires access to Prometheus metrics (ensure Prometheus is secured)
* Uses dashboard variables that should be validated (we've applied regex filters, see CODE_QUALITY.md)
* Displays system metrics that may be sensitive (use Grafana RBAC to control access)

### Security Updates

Security fixes will be:
* Released as soon as possible after verification
* Documented in the commit message and release notes
* Announced in the repository README (if significant)

### Questions?

For non-security questions, see [SUPPORT.md](SUPPORT.md).

---

**Maintained by [run-as-daemon](https://run-as-daemon.ru)**
