{{/*
Create a default fully qualified app name for prometheus service.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "monitoring.prometheus.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
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
{{- if .Values.serviceAccount.create }}
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