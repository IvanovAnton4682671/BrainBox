kubectl delete -n brainbox deployment brainbox-loki-deployment brainbox-grafana-deployment
kubectl delete -n brainbox daemonset brainbox-promtail-daemonset
kubectl delete -n brainbox service brainbox-loki-service brainbox-promtail-service brainbox-grafana-service
kubectl delete -n brainbox secret brainbox-grafana-secret
kubectl delete -n brainbox configmap brainbox-promtail-configmap brainbox-grafana-loki-dashboard brainbox-grafana-configmap
kubectl delete -n brainbox role brainbox-promtail-role
kubectl delete -n brainbox serviceaccount brainbox-promtail-serviceaccount
kubectl delete -n brainbox rolebinding brainbox-promtail-rolebinding