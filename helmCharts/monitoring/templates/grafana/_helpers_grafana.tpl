{{/*
Create a default fully qualified app name for grafana service.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "monitoring.grafana.fullname" -}}
{{- if .Values.grafana.fullnameOverride }}
{{- .Values.grafana.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-grafana-monitoring" .Release.Name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}


{{/*
Selector labels
*/}}
{{- define "monitoring.grafana.selectorLabels" -}}
app.kubernetes.io/name: {{ include "monitoring.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/monitoringTask: grafana
{{- end }}


{{/*
grafana config
*/}}
{{- define "monitoring.grafana.mainConfig" -}}
modules:
  http_2xx:
    prober: http
    http:
      preferred_ip_protocol: "ip4"

{{- end }}


{{/*
configmap name for grafana configs
*/}}
{{- define "monitoring.grafana.cmname" -}}
{{ default (printf "%s-conf" (include "monitoring.grafana.fullname" .)) .Values.grafana.configurations.configMapName }}
{{- end }}