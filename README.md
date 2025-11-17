# Docker Container & Host Metrics — Grafana Dashboard

[English] | [Русский](README.ru.md)

Grafana dashboard for monitoring Docker hosts and containers with Prometheus, cAdvisor and node_exporter.

## Overview

This dashboard provides a **single view** of Docker host and container metrics using Prometheus as a data source, fed by cAdvisor and node_exporter. It offers a comprehensive monitoring solution for Docker environments with pre-configured panels for resource usage, performance metrics, and system information.

Typical use cases include:
* Home lab or small clusters where you need quick insights into Docker performance.
* Production Docker nodes where you want an opinionated, ready-to-use monitoring overview without extensive configuration.

The dashboard JSON in this repository is ready to import into any Grafana instance with a Prometheus datasource configured.

## Requirements

To use this dashboard, you need:

* **Prometheus** scraping metrics from:
  * **cAdvisor** on each Docker host (for container-level metrics)
  * **node_exporter** on each host (for node-level metrics)
* **Grafana** with a Prometheus datasource configured (default name `Prometheus`, or map via `DS_PROMETHEUS` on import)

### Example Prometheus scrape configuration

Add the following jobs to your Prometheus `scrape_configs`:

```yaml
scrape_configs:
  - job_name: 'cadvisor'
    static_configs:
      - targets: ['host1:8080', 'host2:8080']
  
  - job_name: 'node'
    static_configs:
      - targets: ['host1:9100', 'host2:9100']
```

Adjust the hostnames and ports to match your environment.

## Importing the dashboard

### Import via Grafana UI

1. Open Grafana and navigate to **Dashboards** → **Import**.
2. Upload the JSON file from this repository (`10619_rev2.json`).
3. Select the Prometheus datasource (or map `DS_PROMETHEUS` if prompted).
4. Click **Import** to save and open the dashboard.

The dashboard assumes Prometheus is reachable as configured in your datasource settings.

### Import via Grafana API

You can also import the dashboard programmatically using the Grafana API:

```bash
GRAFANA_URL="https://your-grafana-instance"
API_KEY="your-api-key"

curl -sS -X POST "$GRAFANA_URL/api/dashboards/db" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  --data-binary @10619_rev2.json
```

Replace `GRAFANA_URL` and `API_KEY` with your actual Grafana instance URL and API key.

## Variables

The dashboard uses the following variables to filter and customize the displayed data:

* **`job`** — Job label for cAdvisor metrics (default: `cadvisor`). Used to select the appropriate metric source.
* **`node`** — Host or node name. Supports `All` via regex to display metrics from all hosts simultaneously.
* **`port`** — Port number. Supports `All` via regex to aggregate metrics across different ports.
* **`interval`** — Query interval that controls the resolution of time-series data in panels.

These variables can be adjusted using the dropdown selectors at the top of the dashboard.

## Panels overview

The dashboard includes the following panels organized for efficient monitoring:

* **Running containers** — Displays the count of running containers based on `max_over_time(container_last_seen[5m])`.
* **CPU usage on node** — Shows total CPU usage across the Docker host.
* **CPU usage per container** — Breaks down CPU usage by individual containers.
* **Memory usage per container** — Displays memory consumption for each container.
* **Memory cache per container** — Shows cache memory usage by container.
* **Free/used disk space per mount** — Visualizes disk space utilization for each mounted filesystem.
* **Disk I/O per device** — Tracks read/write operations for storage devices.
* **Network traffic on node** — Shows network ingress/egress for the host.
* **Network traffic per container** — Displays network usage broken down by container.
* **Versions table** — Lists versions of cAdvisor, Prometheus, node_exporter, Docker, OS, and kernel for quick reference.

The layout starts with summary metrics at the top, resource usage details in the middle rows, and system information at the bottom.

## Notes on metric names

This dashboard is designed for **node_exporter >= 0.16**, which uses `_bytes` suffixes for memory and disk metrics. Key metrics expected by the dashboard include:

* `node_memory_MemAvailable_bytes` — Available memory in bytes
* `node_memory_MemTotal_bytes` — Total memory in bytes
* `node_disk_read_bytes_total` — Total bytes read from disk
* `node_disk_written_bytes_total` — Total bytes written to disk

If you're using an older version of node_exporter with different metric names, you may need to adjust the PromQL queries in the dashboard panels to match your metric naming scheme.

## Provisioning (optional)

For automated deployment, you can use Grafana's provisioning feature to automatically load the dashboard and datasource.

### Dashboards provisioning

Create a provisioning file at `/etc/grafana/provisioning/dashboards/docker.yaml`:

```yaml
apiVersion: 1
providers:
  - name: docker
    orgId: 1
    folder: Infrastructure
    type: file
    allowUiUpdates: true
    updateIntervalSeconds: 30
    options:
      path: /var/lib/grafana/dashboards
```

Place the dashboard JSON file at:
```
/var/lib/grafana/dashboards/docker-container-host-metrics.json
```

Adjust the `path` to match your Grafana configuration.

### Datasource provisioning

Create a datasource provisioning file for Prometheus:

```yaml
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: true
```

This configuration assumes Prometheus is available at `http://prometheus:9090`. Modify the URL to match your Prometheus instance.

## Troubleshooting

### No data in "Running containers" panel

* Verify dashboard variables: `job = cadvisor`, `node = All`, `port = All`.
* Check that the `container_last_seen` metric exists in Prometheus for the last 5 minutes.
* Query Prometheus directly: `container_last_seen{job="cadvisor"}` to confirm data availability.

### Empty memory or disk panels

* Ensure node_exporter is exposing metrics with `_bytes` suffixes.
* Verify node_exporter version is >= 0.16.
* Check metric names in Prometheus match the expected format.

### General checks

* Visit the Prometheus targets page at `http://prometheus:9090/targets`.
* Confirm that both `cadvisor` and `node` job targets show as **UP**.
* Verify the Grafana Prometheus datasource is configured correctly and can query Prometheus.
* Check Grafana logs for any datasource connection errors.

## Development

To contribute or modify this dashboard:

1. Create a feature branch:
   ```bash
   git checkout -b feat/grafana-docker-dashboard
   ```

2. Edit the dashboard JSON file (`10619_rev2.json`) or make changes directly in Grafana and export the updated JSON.

3. Commit and push your changes:
   ```bash
   git add 10619_rev2.json README.md
   git commit -m "Update dashboard: description of changes"
   git push -u origin feat/grafana-docker-dashboard
   ```

The dashboard JSON can be edited in Grafana's UI, then exported back to this repository to keep the dashboard as code.

## License

This project is licensed under the **Unlicense** (public domain equivalent). You are free to use, modify, and distribute this dashboard without any restrictions.

See the [LICENSE](LICENSE) file for full details.