{{/*
Create a default fully qualified app name for prometheus service.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "monitoring.prometheus.fullname" -}}
{{- if .Values.prometheus.fullnameOverride }}
{{- .Values.prometheus.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-prometheus-monitoring" .Release.Name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}


{{/*
Selector labels
*/}}
{{- define "monitoring.prometheus.selectorLabels" -}}
app.kubernetes.io/name: {{ include "monitoring.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/monitoringTask: prometheus
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "monitoring.prometheus.serviceAccountName" -}}
{{- if .Values.prometheus.serviceAccount.create }}
{{- default (include "monitoring.prometheus.fullname" .) .Values.prometheus.serviceAccount.name }}
{{- else }}
""
{{- end }}
{{- end }}


{{/*
define cluster role name
*/}}
{{- define "monitoring.prometheus.clusterRoleNmae" -}}
{{- default "prometheus-role" .Values.prometheus.clusterRole.name }}
{{- end }}

{{/*
prometheus config
*/}}
{{- define "monitoring.prometheus.mainConfig" -}}
global:
  scrape_interval: 5s
  evaluation_interval: 5s
rule_files:
  - {{ .Values.prometheus.configurations.config_dir }}{{ .Values.prometheus.configurations.rules.file_name }}
alerting:
  alertmanagers:
  - scheme: http
    static_configs:
    - targets:
      - "{{ .Values.alertManager.service.name }}.{{ .Values.namespace }}.svc:{{ .Values.alertManager.service.port }}"

scrape_configs:
  - job_name: 'node-exporter'
    kubernetes_sd_configs:
      - role: endpoints
    relabel_configs:
    - source_labels: [__meta_kubernetes_endpoints_name]
      regex: '.*node-exporter.*'
      action: keep
  
  - job_name: 'kubernetes-apiservers'

    kubernetes_sd_configs:
    - role: endpoints
    scheme: https

    tls_config:
      ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token

    relabel_configs:
    - source_labels: [__meta_kubernetes_namespace, __meta_kubernetes_service_name, __meta_kubernetes_endpoint_port_name]
      action: keep
      regex: default;kubernetes;https

  - job_name: 'kubernetes-nodes'

    scheme: https

    tls_config:
      ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token

    kubernetes_sd_configs:
    - role: node

    relabel_configs:
    - action: labelmap
      regex: __meta_kubernetes_node_label_(.+)
    - target_label: __address__
      replacement: kubernetes.default.svc:443
    - source_labels: [__meta_kubernetes_node_name]
      regex: (.+)
      target_label: __metrics_path__
      replacement: /api/v1/nodes/${1}/proxy/metrics     
  
  - job_name: 'kubernetes-pods'

    kubernetes_sd_configs:
    - role: pod

    relabel_configs:
    - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
      action: keep
      regex: true
    - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
      action: replace
      target_label: __metrics_path__
      regex: (.+)
    - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
      action: replace
      regex: ([^:]+)(?::\d+)?;(\d+)
      replacement: $1:$2
      target_label: __address__
    - action: labelmap
      regex: __meta_kubernetes_pod_label_(.+)
    - source_labels: [__meta_kubernetes_namespace]
      action: replace
      target_label: kubernetes_namespace
    - source_labels: [__meta_kubernetes_pod_name]
      action: replace
      target_label: kubernetes_pod_name

  - job_name: 'kubernetes-cadvisor'

    scheme: https

    tls_config:
      ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token

    kubernetes_sd_configs:
    - role: node

    relabel_configs:
    - action: labelmap
      regex: __meta_kubernetes_node_label_(.+)
    - target_label: __address__
      replacement: kubernetes.default.svc:443
    - source_labels: [__meta_kubernetes_node_name]
      regex: (.+)
      target_label: __metrics_path__
      replacement: /api/v1/nodes/${1}/proxy/metrics/cadvisor
  
  - job_name: 'kubernetes-service-endpoints'

    kubernetes_sd_configs:
    - role: endpoints

    relabel_configs:
    - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_scrape]
      action: keep
      regex: true
    - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_scheme]
      action: replace
      target_label: __scheme__
      regex: (https?)
    - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_path]
      action: replace
      target_label: __metrics_path__
      regex: (.+)
    - source_labels: [__address__, __meta_kubernetes_service_annotation_prometheus_io_port]
      action: replace
      target_label: __address__
      regex: ([^:]+)(?::\d+)?;(\d+)
      replacement: $1:$2
    - action: labelmap
      regex: __meta_kubernetes_service_label_(.+)
    - source_labels: [__meta_kubernetes_namespace]
      action: replace
      target_label: kubernetes_namespace
    - source_labels: [__meta_kubernetes_service_name]
      action: replace
      target_label: kubernetes_name

  - job_name: 'blackbox'
    metrics_path: /probe
    params:
      target: ['google.com']
      module: ["http_2xx"]

    kubernetes_sd_configs:
    - role: endpoints

    relabel_configs:
      - source_labels: [__meta_kubernetes_endpoints_name]
        action: keep
        regex: '.*blackbox.*'
      - source_labels: [__param_target]
        action: replace
        target_label: instance
        regex: (.*)
        replacement: $1

{{- end }}


{{/*
prometheus rules
*/}}
{{- define "monitoring.prometheus.rules" -}}
groups:
- name: Instances
  rules:
  - alert: InstanceDown
    expr: up == 0
    for: 2m
    labels:
      severity: page
    # Prometheus templates apply here in the annotation and label fields of the alert.
    annotations:
      description: '{{ `{{ $labels.instance }}` }} of job {{ `{{ $labels.job }}` }} has been down for more than 2 minutes.'
      summary: 'Instance {{ `{{ $labels.instance }}` }} down'

{{- end }}


{{/*
prometheus web config
*/}}
{{- define "monitoring.prometheus.webConfig" -}}
{{- with .Values.prometheus.configurations.webConfig.authentication }}
{{- if .enabled }}
basic_auth_users:
  {{ htpasswd .username .password | replace ":" ": "}}
{{- end }}
{{ end }}
{{- end }}


{{/*
configmap name for prometheus configs
*/}}
{{- define "monitoring.prometheus.cmname" -}}
{{ default (printf "%s-conf" (include "monitoring.prometheus.fullname" .)) .Values.prometheus.configurations.configMapName }}
{{- end }}

{{/*
liveness and readiness authorization headers.
if basic authentication is enabled authorization header will be set for liveness and
readiness checks
*/}}
{{- define "monitoring.prometheus.authHeaders" }}
{{- with .Values.prometheus.configurations.webConfig.authentication }}
{{- if .enabled }}
httpHeaders:
  - name: Authorization
    value: Basic {{ printf "%s:%s" .username .password | b64enc }}
{{- end }}
{{- end }}
{{- end }}