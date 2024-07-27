# Copyright (c) 2024 Robert Cronin
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import shutil
import subprocess
from typing import List

from kubernetes import client, config


class KubernetesClient:
    def __init__(self):
        try:
            # Try to load in-cluster configuration
            config.load_incluster_config()
        except Exception as e:
            print(f"Error loading in-cluster configuration: {e}")
            # If that fails, try to load kubeconfig file
            kubeconfig = os.path.expanduser("~/.kube/config")
            if os.path.exists(kubeconfig):
                config.load_kube_config(kubeconfig)
            else:
                raise Exception(
                    "Cannot find Kubernetes configuration. Are you running inside a cluster?")

        self.v1 = client.CoreV1Api()
        self.kubectl_path = shutil.which('kubectl')
        if not self.kubectl_path:
            raise Exception("kubectl not found in PATH")

    def fetch_pod_logs(self, namespace: str, pod_name: str, container_name: str, limit: int = 1000) -> str:
        try:
            return self.v1.read_namespaced_pod_log(
                name=pod_name,
                namespace=namespace,
                container=container_name,
                tail_lines=limit
            )
        except client.exceptions.ApiException as e:
            return f"Error fetching logs: {e}"

    def fetch_events(self, namespace: str, limit: int = 100) -> str:
        try:
            events = self.v1.list_namespaced_event(
                namespace=namespace, limit=limit)
            return "\n".join([f"{event.last_timestamp} {event.type} {event.reason}: {event.message}" for event in events.items])
        except client.exceptions.ApiException as e:
            return f"Error fetching events: {e}"

    def execute_kubectl_command(self, command: List[str]) -> str:
        try:
            full_command = [self.kubectl_path] + command
            result = subprocess.run(
                full_command, capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error executing kubectl command: {e.stderr}"
        except Exception as e:
            return f"Error executing kubectl command: {str(e)}"
