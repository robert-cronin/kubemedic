# Copyright (c) 2024 Robert Cronin
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import json
import logging
from typing import Dict, List, Tuple

import openai

from .kubernetes import KubernetesClient
from .tool_specs import tool_specs

logger = logging.getLogger(__name__)


class ConversationManager:
    def __init__(self, api_key: str, k8s_client: KubernetesClient):
        self.client = openai.OpenAI(api_key=api_key)
        self.messages: List[Dict[str, str]] = []
        self.function_calls: List[Dict[str, str]] = []
        self.k8s_client = k8s_client

    def add_message(self, role: str, content: str, name: str = None):
        message = {"role": role, "content": content}
        if role == "function" and name:
            message["name"] = name
        self.messages.append(message)

    def truncate_result(self, result: str, max_length: int = 2000) -> str:
        if len(result) > max_length:
            return result[:max_length] + "... (truncated)"
        return result

    def get_response(self, model: str = "gpt-4o-mini", max_iterations: int = 5) -> Tuple[str, List[Dict[str, str]]]:
        self.function_calls = []
        for _ in range(max_iterations):
            try:
                logger.debug(f"Sending request to OpenAI API with {
                             len(self.messages)} messages")
                response = self.client.chat.completions.create(
                    model=model,
                    messages=self.messages,
                    temperature=0.7,
                    max_tokens=1000,
                    tools=tool_specs
                )
                logger.debug("Received response from OpenAI API")

                message = response.choices[0].message

                # Check if the model wants to call a function
                if message.tool_calls:
                    for tool_call in message.tool_calls:
                        function_name = tool_call.function.name
                        function_args = json.loads(
                            tool_call.function.arguments)

                        if self.k8s_client is None:
                            result = "Error: Kubernetes client is not initialized. Unable to fetch cluster information."
                        else:
                            # Call the appropriate function
                            if function_name == "fetch_events":
                                result = self.k8s_client.fetch_events(
                                    function_args.get("namespace", "default"),
                                    # Add a default limit
                                    function_args.get("limit", 100)
                                )
                            elif function_name == "fetch_pod_logs":
                                result = self.k8s_client.fetch_pod_logs(
                                    function_args.get("namespace", "default"),
                                    function_args.get("pod_name"),
                                    function_args.get("container_name"),
                                    # Add a default limit
                                    function_args.get("limit", 1000)
                                )
                            elif function_name == "execute_kubectl_command":
                                result = self.k8s_client.execute_kubectl_command(
                                    function_args.get("command", [])
                                )
                            else:
                                result = f"Error: Unknown function {
                                    function_name}"

                        # Truncate the result
                        truncated_result = self.truncate_result(result)

                        # Add the function call and truncated result to the messages and function_calls list
                        self.add_message("function", f"Function {function_name} was called with args: {
                                         function_args}", name=function_name)
                        self.add_message("function", f"Result: {
                                         truncated_result}", name=function_name)
                        self.function_calls.append({
                            "name": function_name,
                            "args": function_args,
                            "result": truncated_result
                        })

                    # Continue the conversation
                    continue

                # If no function was called, return the message content and function calls
                return message.content, self.function_calls

            except Exception as e:
                logger.error(f"Error in get_response: {str(e)}")
                raise

        return "Max iterations reached without a final response. Please try rephrasing your question.", self.function_calls

    def clear_conversation(self):
        self.messages = []
        self.function_calls = []
