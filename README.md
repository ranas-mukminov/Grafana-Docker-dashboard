# Grafana Docker Dashboard

**Production-ready Grafana dashboard for comprehensive Docker host and container monitoring**

[English] | [Русский](README.ru.md)

A complete monitoring solution for Docker environments using Prometheus, cAdvisor, and node_exporter. This dashboard provides real-time visibility into container and host metrics with pre-configured panels for resource usage, performance tracking, and system health monitoring.

## Key Features

* **Single-pane view** — Monitor all Docker hosts and containers from one dashboard
* **Comprehensive metrics** — CPU, memory, disk I/O, network traffic at both host and container levels
* **Resource tracking** — Real-time resource utilization with historical trends
* **Container lifecycle** — Track running containers, restarts, and health status
* **Multi-host support** — Monitor multiple Docker hosts simultaneously with variable-based filtering
* **System information** — Built-in version table showing Docker, OS, kernel, and exporter versions
* **Production-tested** — Battle-tested dashboard with normalized metrics and proper threshold alerts
* **Import-ready** — JSON configuration ready for immediate import into any Grafana instance
* **Flexible filtering** — Dynamic variables for job, node, port, and time interval selection

## Architecture

This dashboard uses a standard Prometheus monitoring stack:

```
┌─────────────────┐
│  Grafana        │ ← Visualizes metrics
│  (This Dashboard)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Prometheus     │ ← Scrapes and stores metrics
└────────┬────────┘
         │
         ├──────────────────┬─────────────────┐
         ▼                  ▼                 ▼
┌─────────────┐    ┌─────────────┐   ┌─────────────┐
│  cAdvisor   │    │ node_exporter│   │  cAdvisor   │
│  (Host 1)   │    │  (Host 1)   │   │  (Host 2)   │
└─────────────┘    └─────────────┘   └─────────────┘
       │                   │                  │
       ▼                   ▼                  ▼
  Docker Engine      System Metrics     Docker Engine
```

**Data sources:**
* **cAdvisor** — Provides container-level metrics (CPU, memory, network, filesystem)
* **node_exporter** — Provides host-level metrics (system resources, hardware info)
* **Prometheus** — Aggregates, stores, and serves time-series data
* **Grafana** — Visualizes metrics through this dashboard

![Dashboard Preview](./images/dashboard-preview.png)

## Quick Start

### Prerequisites

You need the following components running:

1. **Prometheus** (version 2.x or higher)
2. **cAdvisor** on each Docker host (typically on port 8080)
3. **node_exporter** on each host (typically on port 9100)
4. **Grafana** (version 5.x or higher)

### Step 1: Deploy Exporters

On each Docker host, run cAdvisor and node_exporter:

```bash
# Run cAdvisor
docker run -d \
  --name=cadvisor \
  --restart=always \
  --volume=/:/rootfs:ro \
  --volume=/var/run:/var/run:ro \
  --volume=/sys:/sys:ro \
  --volume=/var/lib/docker/:/var/lib/docker:ro \
  --volume=/dev/disk/:/dev/disk:ro \
  --publish=8080:8080 \
  --privileged \
  gcr.io/cadvisor/cadvisor:latest

# Run node_exporter
docker run -d \
  --name=node_exporter \
  --restart=always \
  --net="host" \
  --pid="host" \
  --volume=/:/host:ro,rslave \
  quay.io/prometheus/node-exporter:latest \
  --path.rootfs=/host
```

### Step 2: Configure Prometheus

Add scrape configurations to your `prometheus.yml`:

```yaml
scrape_configs:
  - job_name: 'cadvisor'
    static_configs:
      - targets:
          - 'docker-host-1:8080'
          - 'docker-host-2:8080'
    
  - job_name: 'node'
    static_configs:
      - targets:
          - 'docker-host-1:9100'
          - 'docker-host-2:9100'
```

Reload Prometheus configuration:

```bash
curl -X POST http://prometheus:9090/-/reload
```

Verify targets are up: `http://prometheus:9090/targets`

### Step 3: Import Dashboard to Grafana

**Option A: Import via Grafana UI**

1. Download `10619_rev2.json` from this repository
2. Open Grafana → **Dashboards** → **Import**
3. Upload the JSON file
4. Select your Prometheus datasource
5. Click **Import**

**Option B: Import via API**

```bash
GRAFANA_URL="http://your-grafana:3000"
API_KEY="your-api-key"

curl -X POST "$GRAFANA_URL/api/dashboards/db" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d @10619_rev2.json
```

**Option C: Automated Provisioning**

Create `/etc/grafana/provisioning/dashboards/docker.yaml`:

```yaml
apiVersion: 1
providers:
  - name: docker
    orgId: 1
    folder: Infrastructure
    type: file
    allowUiUpdates: true
    options:
      path: /var/lib/grafana/dashboards
```

Copy `10619_rev2.json` to `/var/lib/grafana/dashboards/` and restart Grafana.

## Run with Docker Compose

If you prefer to spin everything up locally, the repository includes a `docker-compose.yml` file that wires Prometheus, Grafana, cAdvisor, and node_exporter together. Make sure Docker Engine and the Docker Compose plugin (v2+) are installed before running the stack.

```bash
# Start the monitoring stack
docker compose up -d

# Stop and remove the stack
docker compose down
```

Grafana will be available at [http://localhost:3000](http://localhost:3000) with the default `admin` / `admin` credentials (be sure to change the password on first login). The dashboard is auto-provisioned into the **Infrastructure** folder, so you can open Grafana → **Dashboards** → **Infrastructure** → **Docker** to start exploring metrics right away.

## CI / Validation

Every pull request runs a GitHub Actions workflow that keeps the dashboard artifacts healthy:

* **JSON integrity check** — Confirms `10619_rev2.json` is valid JSON and not empty, preventing corrupt dashboard exports from being merged.
* **docker-compose lint** — Uses `docker compose config` to validate the Compose file syntax so contributors do not break the local demo stack.

These gates catch formatting mistakes before they reach production users, ensuring the dashboard can always be imported and the demo environment remains runnable.

## Usage

### Dashboard Variables

Use the dropdown selectors at the top of the dashboard to filter data:

* **job** — Select the cAdvisor job name (default: `cadvisor`)
* **node** — Filter by specific host or select `All` to view all hosts
* **port** — Filter by port or select `All` for aggregated view
* **interval** — Adjust time-series resolution (auto, 1m, 5m, etc.)

### Key Metrics Explained

**Running Containers**
* Shows active container count in the last 5 minutes
* Based on `container_last_seen` metric from cAdvisor

**CPU Usage**
* Node CPU usage shows aggregate CPU utilization (0-100%)
* Container CPU usage normalized by available CPU cores
* Thresholds: Warning at 70%, Critical at 85%

**Memory Usage**
* Working set memory (actual memory used by containers)
* Cache memory (filesystem cache, reclaimable)
* Host memory available vs. total

**Disk Metrics**
* Free/used space per mount point
* Read/write bytes per device
* I/O operations per second

**Network Traffic**
* Ingress/egress on host interfaces
* Per-container network usage
* Cumulative bandwidth over time

### Best Practices

1. **Set up alerting** — Create Prometheus alerts for critical thresholds (CPU > 85%, Memory > 90%, Disk > 90%)
2. **Regular review** — Check the versions table to ensure exporters and Docker are up-to-date
3. **Capacity planning** — Monitor trends over 7-30 days to predict resource needs
4. **Container optimization** — Use per-container metrics to identify resource-heavy workloads
5. **Retention tuning** — Adjust Prometheus retention based on your monitoring requirements

## Troubleshooting

### No data displayed / "N/A" values

**Check Prometheus targets:**
```bash
curl http://prometheus:9090/api/v1/targets | jq '.data.activeTargets[] | select(.health != "up")'
```

**Verify metrics exist:**
```bash
# Check cAdvisor metrics
curl http://prometheus:9090/api/v1/query?query=container_last_seen

# Check node_exporter metrics
curl http://prometheus:9090/api/v1/query?query=node_memory_MemTotal_bytes
```

**Solution:** Ensure cAdvisor and node_exporter are running and accessible from Prometheus.

### "Running containers" panel shows 0

**Verify dashboard variables:**
* Set `job = cadvisor` (or your cAdvisor job name)
* Set `node = All` and `port = All`

**Check the metric directly in Prometheus:**
```promql
container_last_seen{job="cadvisor",image!=""}
```

**Solution:** If no results, verify cAdvisor is scraping containers correctly. Check cAdvisor logs.

### Memory or disk panels are empty

**Issue:** Metric naming mismatch with node_exporter version

**Check your node_exporter version:**
```bash
curl http://node-exporter:9100/metrics | grep node_exporter_build_info
```

**Solution:** 
* This dashboard requires node_exporter >= 0.16 (uses `_bytes` suffix)
* Older versions use different metric names (e.g., `node_memory_MemAvailable` vs. `node_memory_MemAvailable_bytes`)
* Update node_exporter or adjust PromQL queries in dashboard panels

### High CPU values / percentages over 100%

**Cause:** Multi-core systems without CPU normalization

**Solution:** The dashboard already includes CPU normalization. If you still see issues:
1. Verify the query uses `rate()` or `irate()` with appropriate intervals
2. Check that container CPU is normalized by `machine_cpu_cores`
3. Review CODE_QUALITY.md for detailed fixes applied

### Grafana datasource connection errors

**Check datasource configuration:**
1. Go to Grafana → **Configuration** → **Data Sources**
2. Test the Prometheus datasource connection
3. Verify URL is correct (e.g., `http://prometheus:9090`)

**Check network connectivity:**
```bash
# From Grafana container/host
curl http://prometheus:9090/api/v1/status/config
```

**Solution:** Ensure Prometheus is accessible from Grafana. Check firewall rules and DNS resolution.

### Variables not loading

**Symptom:** Dropdown variables are empty or show "No data"

**Check Prometheus label values:**
```promql
# Check job labels
label_values(container_last_seen, job)

# Check instance labels
label_values(container_last_seen, instance)
```

**Solution:** 
* Verify metrics have the expected labels
* Check variable regex patterns in dashboard settings
* Ensure Prometheus datasource is selected correctly

### IPv6 addresses cause issues

**Issue:** Dashboard was updated to support both IPv4 and IPv6

**Verify:** Check CODE_QUALITY.md for IPv6 compatibility fixes

**Solution:** The latest dashboard version uses `label_replace` to extract host/port without assuming IPv4 format.

## Professional SRE/DevOps Services

This dashboard is maintained by **run-as-daemon** — a professional SRE/DevOps services provider specializing in production monitoring, high availability, and infrastructure automation.

Need help beyond this dashboard? We offer:

* **Production monitoring setup** — Complete observability stack deployment (Prometheus, Grafana, Alertmanager, Loki)
* **Custom dashboards and alerts** — Tailored monitoring solutions for your infrastructure
* **High availability configuration** — HA Prometheus, Grafana clustering, disaster recovery
* **Performance tuning** — Optimize Docker, Kubernetes, and database workloads for high load
* **Infrastructure as Code** — Terraform, Ansible automation for monitoring infrastructure
* **On-call support** — 24/7 incident response and troubleshooting

**Contact us:** [https://run-as-daemon.ru](https://run-as-daemon.ru)

Whether you need a one-time consultation or ongoing infrastructure management, we provide expert-level SRE services to keep your systems reliable and performant.

## Support / Sponsorship

If this dashboard saves you time or helps monitor your infrastructure:

### Free Support
* ⭐ **Star this repository** — Help others discover this dashboard
* 🔗 **Share it** — Spread the word on social media, blog posts, or with colleagues
* 💬 **Contribute** — Report issues, suggest features, or submit improvements

### Financial Support
* 💰 **GitHub Sponsors** — Use the "Sponsor" button at the top of this repository
* ☕ **Buy me a coffee** — Support ongoing maintenance and updates
* 🎯 **Hire for projects** — Commission custom dashboards or monitoring solutions

Your support helps maintain this project and create more open-source monitoring tools for the community.

**Sponsorship options:** See [.github/FUNDING.yml](.github/FUNDING.yml) for all available channels.

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
* Reporting bugs and requesting features
* Submitting pull requests
* Code style and testing expectations

## License

This project is licensed under the **Unlicense** (public domain equivalent).

You are free to use, modify, and distribute this dashboard without any restrictions. See the [LICENSE](LICENSE) file for details.

---

**Maintained by [run-as-daemon](https://run-as-daemon.ru)** | **Questions?** See [SUPPORT.md](SUPPORT.md)