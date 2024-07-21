# Copyright (c) 2024 Robert Cronin
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

# Function definitions
tool_specs = [
    {
        "type": "function",
        "function": {
            "name": "execute_kubectl_command",
            "parameters": {
                "type": "object",
                "required": [
                    "command"
                ],
                "properties": {
                    "command": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "The kubectl command to execute, split into arguments."
                    }
                }
            },
            "description": "Execute a custom kubectl command and return the output."
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_events",
            "parameters": {
                "type": "object",
                "required": [
                    "namespace"
                ],
                "properties": {
                    "namespace": {
                        "type": "string",
                        "description": "The namespace to retrieve events from."
                    }
                }
            },
            "description": "Retrieve all events in a given namespace."
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_pod_logs",
            "parameters": {
                "type": "object",
                "required": [
                    "namespace",
                    "pod_name",
                    "container_name"
                ],
                "properties": {
                    "pod_name": {
                        "type": "string",
                        "description": "The name of the pod to fetch logs from."
                    },
                    "namespace": {
                        "type": "string",
                        "description": "The namespace where the pod is located."
                    },
                    "container_name": {
                        "type": "string",
                        "description": "The name of the container to fetch logs from."
                    }
                }
            },
            "description": "Fetch logs from a specific pod and container in a given namespace."
        }
    }
]
