# Copyright (c) 2024 Robert Cronin
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import subprocess
from typing import List


class KubernetesClient:
    def __init__(self):
        self.kubectl_path = self._find_kubectl()

    def _find_kubectl(self):
        try:
            return subprocess.check_output(["which", "kubectl"]).decode().strip()
        except subprocess.CalledProcessError:
            raise Exception("kubectl not found in PATH")

    def _run_kubectl(self, args: List[str]) -> str:
        try:
            result = subprocess.run(
                [self.kubectl_path] + args, capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error executing kubectl command: {e.stderr}"

    def fetch_pod_logs(self, namespace: str, pod_name: str, container_name: str, limit: int = 1000) -> str:
        return self._run_kubectl(["logs", "-n", namespace, pod_name, "-c", container_name, f"--tail={limit}"])

    def fetch_events(self, namespace: str, limit: int = 100) -> str:
        kubectl_command = [
            "get", "events",
            "-n", namespace,
            "--sort-by=.metadata.creationTimestamp"
        ]
        full_command = [self.kubectl_path] + kubectl_command + \
            ["2>&1", "|", "head", "-n", str(limit)]
        try:
            result = subprocess.run(
                " ".join(full_command), shell=True, capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error executing kubectl command: {e.stderr}"

    def execute_kubectl_command(self, command: List[str]) -> str:
        return self._run_kubectl(command)
