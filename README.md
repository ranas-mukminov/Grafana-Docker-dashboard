
Docker Container & Host Metrics — Grafana Dashboard
Monitor Docker hosts and containers with Prometheus + cAdvisor + node_exporter. Works with Prometheus at [http://prometheus:9090](http://prometheus:9090).

Files
grafana/dashboards/docker-container-host-metrics.json   # dashboard
grafana/README.md                                        # this file

Requirements

* Prometheus scraping:

  * cAdvisor on each host
  * node_exporter on each host
* Grafana with Prometheus datasource (name: Prometheus) or map via DS_PROMETHEUS on import.

Example Prometheus scrape config
scrape_configs:

* job_name: 'cadvisor'
  static_configs:

  * targets: ['host1:8080','host2:8080']
* job_name: 'node'
  static_configs:

  * targets: ['host1:9100','host2:9100']

Importing the dashboard (UI)
Grafana -> Dashboards -> Import -> Upload grafana/dashboards/docker-container-host-metrics.json -> select datasource Prometheus.

Importing the dashboard (API)
GRAFANA_URL="https://<grafana>"
API_KEY="<api-key>"
curl -sS -X POST "$GRAFANA_URL/api/dashboards/db" 
-H "Authorization: Bearer $API_KEY" 
-H "Content-Type: application/json" 
--data-binary @grafana/dashboards/docker-container-host-metrics.json

Variables

* job — default cadvisor
* node — host, supports All via regex
* port — port, supports All via regex
* interval — query interval

Panels

* Running containers (max_over_time(container_last_seen[5m]))
* CPU usage on node and per container
* Memory usage and cache per container
* Free/used disk space per mount
* Disk I/O per device
* Network traffic on node and per container
* Versions table (cAdvisor, Prometheus, node_exporter, Docker, OS, kernel)

Notes on metrics names

* node_exporter >= 0.16 uses _bytes suffixes:

  * node_memory_MemAvailable_bytes
  * node_memory_MemTotal_bytes
  * node_disk_read_bytes_total
  * node_disk_written_bytes_total

Provisioning (optional)
Dashboards provisioning file: /etc/grafana/provisioning/dashboards/docker.yaml
apiVersion: 1
providers:

* name: docker
  orgId: 1
  folder: Infrastructure
  type: file
  allowUiUpdates: true
  updateIntervalSeconds: 30
  options:
  path: /var/lib/grafana/dashboards

Place the JSON at:
/var/lib/grafana/dashboards/docker-container-host-metrics.json

Datasource provisioning (Prometheus at [http://prometheus:9090](http://prometheus:9090)):
apiVersion: 1
datasources:

* name: Prometheus
  type: prometheus
  access: proxy
  url: [http://prometheus:9090](http://prometheus:9090)
  isDefault: true
  editable: true

Development
git checkout -b feat/grafana-docker-dashboard
git add grafana/dashboards/docker-container-host-metrics.json grafana/README.md
git commit -m "Add Grafana dashboard: Docker Container & Host Metrics"
git push -u origin feat/grafana-docker-dashboard

Troubleshooting

* No data in Running containers:

  * Set Job = cadvisor, Host = All, Port = All
  * Confirm container_last_seen exists in Prometheus over last 5m
* Empty memory/disk panels:

  * Ensure _bytes metrics are exposed by node_exporter
* Check Prometheus targets:

  * [http://prometheus:9090/targets](http://prometheus:9090/targets)
  * cadvisor and node targets should be UP
