# Copyright (c) 2024 Robert Cronin
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import openai
import kubernetes.client
import kubernetes.config
import subprocess
import click
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/diagnose', methods=['POST'])
def diagnose():
    data = request.json
    api_key = data['api_key']
    kubeconfig = data['kubeconfig']
    namespace = data['namespace']
    issue = data['issue']

    # Configure OpenAI API key
    openai.api_key = api_key

    # Load Kubernetes configuration
    kubernetes.config.load_kube_config(config_file=kubeconfig)

    v1 = kubernetes.client.CoreV1Api()

    # Get pod logs
    logs = ""
    pods = v1.list_namespaced_pod(namespace)
    for pod in pods.items:
        pod_logs = v1.read_namespaced_pod_log(
            name=pod.metadata.name, namespace=namespace)
        logs += f"Pod: {pod.metadata.name}\n{pod_logs}\n"

    # Get events
    events = v1.list_namespaced_event(namespace)
    event_details = ""
    for event in events.items:
        event_details += f"Event: {event.reason} - {event.message}\n"

    # Combine logs and events into the prompt for OpenAI
    full_prompt = f"Issue: {issue}\n\nPod Logs:\n{
        logs}\n\nEvents:\n{event_details}"

    # Call OpenAI API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=full_prompt,
        max_tokens=100
    )

    return jsonify({"diagnosis": response.choices[0].text.strip()})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
