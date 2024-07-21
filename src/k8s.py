# Copyright (c) 2024 Robert Cronin
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import kubernetes.config
import kubernetes.client


def fetch_pod_logs(k8s_client, namespace):
    logs = ""
    pods = k8s_client.list_namespaced_pod(namespace)
    for pod in pods.items:
        log = k8s_client.read_namespaced_pod_log(
            name=pod.metadata.name, namespace=namespace)
        logs += f"Pod: {pod.metadata.name}\n{log}\n"
    return logs


def fetch_events(k8s_client, namespace):
    events = k8s_client.list_namespaced_event(namespace)
    event_details = ""
    for event in events.items:
        event_details += f"Event: {event.reason} - {event.message}\n"
    return event_details


def run_diagnose_loop():
    # Uses the Kubernetes service account token to authenticate
    kubernetes.config.load_incluster_config()

    v1 = kubernetes.client.CoreV1Api()

    # TODO: query the namespace that the LLM wants to diagnose
    namespace = "default"

    # Fetch logs and events
    pod_logs = fetch_pod_logs(v1, namespace)
    events = fetch_events(v1, namespace)

    return f"Logs:\n{pod_logs}\nEvents:\n{events}\n"
