# Support

Looking for help with Grafana Docker Dashboard? Here's how to get support.

## Documentation

Before opening an issue, please check the documentation:

* **[README.md](README.md)** — Full setup guide, usage instructions, and troubleshooting
* **[README.ru.md](README.ru.md)** — Russian version of the documentation
* **[CODE_QUALITY.md](CODE_QUALITY.md)** — Details on dashboard improvements and fixes

## Community Support

### GitHub Issues

For bug reports and feature requests, use GitHub Issues:

* **Bug Reports** — Use the [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.yml)
  - Dashboard not displaying data
  - Metrics showing incorrect values
  - Import errors or compatibility issues
  
* **Feature Requests** — Use the [Feature Request template](.github/ISSUE_TEMPLATE/feature_request.yml)
  - New panels or visualizations
  - Additional metrics or data sources
  - Dashboard improvements

### GitHub Discussions

For general questions, ideas, and community discussions:

* Setup and configuration questions
* Best practices for Docker monitoring
* Sharing your experience with the dashboard
* Ideas that aren't yet fully formed feature requests

**Note:** This repository may not have Discussions enabled yet. If not available, use Issues for questions.

## When to Open an Issue

**DO open an issue if:**

* ✅ The dashboard shows "No data" or errors when it should work
* ✅ You found a bug or incorrect behavior
* ✅ You have a well-defined feature request
* ✅ Documentation is unclear or incorrect
* ✅ You want to suggest an improvement

**DON'T open an issue if:**

* ❌ You need help setting up Prometheus, Grafana, cAdvisor, or node_exporter (check their respective documentation)
* ❌ You have general Prometheus or PromQL questions (use Prometheus community resources)
* ❌ You have Grafana usage questions (use Grafana community resources)
* ❌ The issue is with your specific infrastructure configuration

## Response Time

This is a community-maintained open-source project. Response times vary:

* **Simple questions**: Usually within a few days
* **Bug reports**: Reviewed as soon as possible, fixes depend on complexity
* **Feature requests**: May take time to evaluate and implement

## Professional Support

Need faster response times or hands-on help?

**run-as-daemon** offers professional SRE/DevOps services:

* **Priority support** — Guaranteed response times for production issues
* **Setup assistance** — Complete monitoring stack deployment and configuration
* **Custom development** — Tailored dashboards and monitoring solutions
* **Training** — Team training on Prometheus, Grafana, and Docker monitoring
* **Infrastructure consulting** — Architecture review and optimization

**Contact:** [https://run-as-daemon.ru](https://run-as-daemon.ru)

We provide commercial support contracts for organizations that need:
- Production-grade monitoring setup
- 24/7 on-call support
- Custom SLA agreements
- Dedicated technical account management

## Self-Help Resources

### Troubleshooting Steps

1. **Verify Prometheus targets** are up: `http://prometheus:9090/targets`
2. **Check metrics exist** in Prometheus:
   ```promql
   container_last_seen{job="cadvisor"}
   node_memory_MemTotal_bytes
   ```
3. **Test Grafana datasource** connection in Grafana UI
4. **Check dashboard variables** — Ensure `job`, `node`, `port` are set correctly
5. **Review logs**:
   - Prometheus logs for scraping errors
   - Grafana logs for datasource errors
   - cAdvisor logs for container discovery issues

### Common Issues

See the **Troubleshooting** section in [README.md](README.md) for solutions to:
- No data displayed / "N/A" values
- "Running containers" panel shows 0
- Memory or disk panels are empty
- High CPU values / percentages over 100%
- Grafana datasource connection errors
- Variables not loading
- IPv6 address issues

### External Resources

* **Prometheus Documentation**: https://prometheus.io/docs/
* **Grafana Documentation**: https://grafana.com/docs/
* **cAdvisor GitHub**: https://github.com/google/cadvisor
* **node_exporter GitHub**: https://github.com/prometheus/node_exporter
* **PromQL Tutorial**: https://prometheus.io/docs/prometheus/latest/querying/basics/

## Contributing

Want to improve this dashboard? See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## Security Issues

**Do not open public issues for security vulnerabilities.**

See [SECURITY.md](SECURITY.md) for instructions on reporting security issues privately.

---

**Maintained by [run-as-daemon](https://run-as-daemon.ru)**
