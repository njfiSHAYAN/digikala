{{/*
Create a default fully qualified app name for prometheus service.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "monitoring.nodeExporter.fullname" -}}
{{- if .Values.nodeExporter.fullnameOverride }}
{{- .Values.nodeExporter.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-node-exporter-monitoring" .Release.Name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}


{{/*
Selector labels
*/}}
{{- define "monitoring.nodeExporter.selectorLabels" -}}
app.kubernetes.io/name: {{ include "monitoring.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/monitoringTask: node-exporter
{{- end }}
