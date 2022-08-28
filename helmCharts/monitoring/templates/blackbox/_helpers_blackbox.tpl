{{/*
Create a default fully qualified app name for blackbox service.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "monitoring.blackbox.fullname" -}}
{{- if .Values.blackbox.fullnameOverride }}
{{- .Values.blackbox.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-blackbox-monitoring" .Release.Name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}


{{/*
Selector labels
*/}}
{{- define "monitoring.blackbox.selectorLabels" -}}
app.kubernetes.io/name: {{ include "monitoring.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/monitoringTask: blackbox
{{- end }}


{{/*
blackbox config
*/}}
{{- define "monitoring.blackbox.mainConfig" -}}
modules:
  http_2xx:
    prober: http
    http:
      preferred_ip_protocol: "ip4"

{{- end }}


{{/*
configmap name for blackbox configs
*/}}
{{- define "monitoring.blackbox.cmname" -}}
{{ default (printf "%s-conf" (include "monitoring.blackbox.fullname" .)) .Values.blackbox.configurations.configMapName }}
{{- end }}