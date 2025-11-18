# Contributing to Grafana Docker Dashboard

Thank you for considering contributing to this project! We welcome contributions from the community.

## How to Contribute

### Reporting Issues

If you find a bug or have a feature request:

1. **Search existing issues** — Check if the issue has already been reported
2. **Create a new issue** — Use the appropriate issue template:
   - [Bug Report](.github/ISSUE_TEMPLATE/bug_report.yml) for bugs
   - [Feature Request](.github/ISSUE_TEMPLATE/feature_request.yml) for new features
3. **Provide details** — Include as much relevant information as possible:
   - Dashboard version (check the JSON file revision)
   - Prometheus version
   - Grafana version
   - cAdvisor and node_exporter versions
   - Steps to reproduce (for bugs)
   - Expected vs. actual behavior

### Submitting Pull Requests

We welcome code contributions! Here's how to submit a pull request:

1. **Fork the repository** — Create your own fork on GitHub
2. **Create a branch** — Use a descriptive branch name:
   ```bash
   git checkout -b feat/improve-cpu-panel
   git checkout -b fix/memory-metrics-display
   ```
3. **Make your changes** — Edit the dashboard JSON file or documentation
   - For dashboard changes: Edit in Grafana UI, then export to JSON
   - For documentation: Edit markdown files directly
4. **Test your changes** — Verify the dashboard works correctly:
   - Run `python tests/validate_dashboard.py` to statically validate the JSON
   - Import the updated JSON into Grafana
   - Check all panels display data correctly
   - Test with different variable combinations
5. **Commit your changes** — Use clear, descriptive commit messages:
   ```bash
   git add 10619_rev2.json README.md
   git commit -m "Fix memory panel not displaying cache metrics"
   ```
6. **Push to your fork**:
   ```bash
   git push origin feat/improve-cpu-panel
   ```
7. **Open a pull request** — Submit a PR from your fork to the main repository
   - Use the PR template
   - Reference any related issues
   - Describe what changed and why

### Dashboard Editing Guidelines

When modifying the dashboard JSON:

* **Test thoroughly** — Ensure all panels work with real Prometheus data
* **Maintain compatibility** — Keep support for node_exporter >= 0.16 and cAdvisor
* **Document changes** — Update README.md if you add/change functionality
* **Keep it production-ready** — Avoid experimental features that may break in production
* **Follow PromQL best practices** — Use efficient queries that scale
* **Preserve variables** — Don't remove or rename existing dashboard variables
* **Version compatibility** — Ensure changes work with Grafana 5.x and higher

### Documentation Guidelines

When updating documentation:

* **Be clear and concise** — Technical but readable
* **Include examples** — Provide command-line examples where relevant
* **Update both languages** — If editing README.md, also update README.ru.md
* **Verify links** — Ensure all links work correctly
* **Maintain formatting** — Follow existing markdown structure

### Code Style

This repository primarily contains JSON configuration and markdown documentation:

* **JSON**: Follow the existing Grafana dashboard JSON structure
* **Markdown**: Use standard markdown formatting
* **Shell examples**: Use `bash` for code blocks with shell commands
* **YAML examples**: Use proper YAML indentation (2 spaces)

## Development Workflow

### Setting up a test environment

1. Start Prometheus with cAdvisor and node_exporter:
   ```bash
   # See README.md Quick Start section for setup instructions
   ```

2. Import the dashboard into Grafana:
   ```bash
   # Use Grafana UI or API import method
   ```

3. Make changes in Grafana UI

4. Export the updated dashboard:
   - Grafana → Dashboard Settings → JSON Model
   - Copy the JSON
   - Update `10619_rev2.json`

### Testing checklist

Before submitting a PR, verify:

- [ ] `python tests/validate_dashboard.py` passes
- [ ] Dashboard imports successfully without errors
- [ ] All panels display data (not "No data" or errors)
- [ ] Variables work correctly (job, node, port, interval)
- [ ] CPU metrics show 0-100% range (not over 100%)
- [ ] Memory and disk metrics display in readable units
- [ ] Network metrics show ingress/egress correctly
- [ ] Versions table populates with system information
- [ ] Dashboard works with both single and multiple hosts
- [ ] Changes are documented in README.md
- [ ] README.ru.md is updated (if documentation changed)

## Community Standards

* **Be respectful** — Follow our [Code of Conduct](CODE_OF_CONDUCT.md)
* **Be patient** — Maintainers review contributions as time permits
* **Be collaborative** — Work with others to improve the project

## Questions?

If you have questions about contributing:

* **GitHub Issues** — Open a discussion issue
* **Support** — See [SUPPORT.md](SUPPORT.md) for help channels

## License

By contributing to this project, you agree that your contributions will be licensed under the Unlicense (public domain equivalent).

---

**Maintained by [run-as-daemon](https://run-as-daemon.ru)**
