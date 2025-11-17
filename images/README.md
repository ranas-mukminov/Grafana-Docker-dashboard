# Images Directory

This directory contains screenshots and diagrams for the Grafana Docker Dashboard documentation.

## Files

- `dashboard-preview.png` — Main dashboard screenshot showing all panels (to be added by maintainer)

## Adding Images

When adding screenshots:

1. **Use descriptive names** — `feature-name.png` or `panel-cpu-usage.png`
2. **Optimize images** — Use PNG for screenshots, compress to reduce file size
3. **Update README** — Reference new images in README.md
4. **Recommended size** — 1920x1080 or scaled down to < 500KB

## Current Status

⚠️ **Placeholder**: The `dashboard-preview.png` file referenced in README.md needs to be added.

To generate the preview screenshot:
1. Import the dashboard into Grafana
2. Configure Prometheus datasource with live data
3. Take a full-page screenshot (or use Grafana's render API)
4. Save as `images/dashboard-preview.png`
5. Commit and push the image

Example Grafana render command:
```bash
curl -o dashboard-preview.png \
  "http://admin:admin@grafana:3000/render/d-solo/YOUR-DASHBOARD-ID?orgId=1&width=1920&height=1080"
```
