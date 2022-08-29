{{/*
Create a default fully qualified app name for alertManager service.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "monitoring.alertManager.fullname" -}}
{{- if .Values.alertManager.fullnameOverride }}
{{- .Values.alertManager.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-alert-manager-monitoring" .Release.Name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}


{{/*
Selector labels
*/}}
{{- define "monitoring.alertManager.selectorLabels" -}}
app.kubernetes.io/name: {{ include "monitoring.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/monitoringTask: alert-manager
{{- end }}


{{/*
configmap name for alertManager configs
*/}}
{{- define "monitoring.alertManager.cmname" -}}
{{ default (printf "%s-conf" (include "monitoring.alertManager.fullname" .)) .Values.alertManager.configurations.configMapName }}
{{- end }}

