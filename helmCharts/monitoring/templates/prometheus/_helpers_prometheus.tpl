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