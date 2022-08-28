{{/*
Create a default fully qualified app name for prometheus service.
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


{{/*
prometheus web config
*/}}
{{- define "monitoring.alertManager.mainConfig" -}}
global:
  resolve_timeout: 5m

route:
  group_by: ['alertname']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 30m
  receiver: 'email'
receivers:
- name: 'email'
  email_configs:
  - to: 'sobhan.saf79@gmail.com'
    from: 'digiprojectalertmanager@gmail.com'
    smarthost: smtp.gmail.com:587
    auth_username: 'digiprojectalertmanager@gmail.com'
    auth_identity: 'digiprojectalertmanager@gmail.com'
    auth_password: 'tmdomrsefzgqrbpv'

{{- end }}