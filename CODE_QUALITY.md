# Code Quality Review

## Summary
- Corrected the PromQL expression for host CPU usage to track actual node utilization via `node_cpu_seconds_total`.
- Normalized container CPU graphs so percentages stay within 0-100% even on multi-core hosts.
- Replaced IPv4-only templating regex with label extraction that works for IPv4 and IPv6 instances alike.
- Hardened dashboard variables with allow-list regexes to prevent unexpected label payloads from being interpolated into PromQL queries.
- Enhanced CPU visualizations with thresholds, clearer legends, and clamp logic so operators can spot saturation and query jitter immediately.

## Findings

### 1. Host CPU panel uses exporter process metric
- **Location:** `10619_rev2.json`, lines 70-91.
- **Fix:** Updated the "CPU Usage on Node" panel to query `node_cpu_seconds_total` and compute `100 - idle%`, ensuring the graph reflects real node utilization instead of exporter process usage.

### 2. Container CPU percentages not normalized
- **Location:** `10619_rev2.json`, lines 198-212.
- **Fix:** Normalize `container_cpu_usage_seconds_total` by the aggregated per-instance CPU core count, add clamp guards, and enforce 0-100% bounds so stacked usage reflects the true share across the selected hosts.

### 3. Host/Port template regex breaks IPv6 targets
- **Location:** `10619_rev2.json`, lines 333-364.
- **Fix:** Generate Host and Port template variables with `label_replace`, extracting the components from `instance` without assuming IPv4 formatting so IPv6 targets are fully supported.

### 4. Dashboard variables accepted unsanitized values
- **Location:** `10619_rev2.json`, lines 320-368.
- **Fix:** Applied Grafana regex filters to the Job, Host, and Port template variables so only expected tokens reach PromQL, reducing the blast radius of a malicious metrics payload.

### 5. CPU panels lacked operational context
- **Location:** `10619_rev2.json`, lines 70-118 and 196-216.
- **Fix:** Added clamp logic, percent bounds, thresholds, and richer legends/colours to the CPU panels so jitter-induced negatives are suppressed and critical utilisation stands out visually.

