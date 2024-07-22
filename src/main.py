# Copyright (c) 2024 Robert Cronin
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import sys
import logging
from flask import Flask, request, jsonify, render_template, session
from .conversation_manager import ConversationManager
from .config_manager import config
from .kubernetes import KubernetesClient

# Configure logging
logging.basicConfig(level=config.log_level)
logger = logging.getLogger(__name__)

# Read in ./SYSTEM_PROMPT.md
try:
    with open(os.path.join(os.path.dirname(__file__), "prompts", "SYSTEM_PROMPT.md"), "r") as file:
        system_prompt = file.read()
    if not system_prompt:
        raise ValueError("Content of system prompt file is empty.")
except Exception as e:
    logger.error(f"Failed to read system prompt file: {e}")
    sys.exit(1)

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Initialize KubernetesClient
try:
    k8s_client = KubernetesClient()
except Exception as e:
    logger.error(f"Failed to initialize KubernetesClient: {e}")
    k8s_client = None


@app.route('/')
def index():
    if 'conversation_history' not in session:
        session['conversation_history'] = []
    return render_template('diagnose.html')


@app.route('/api/check_api_key', methods=['GET'])
def check_api_key():
    return jsonify({"has_api_key": config.has_openai_api_key()})


@app.route('/api/set_api_key', methods=['POST'])
def set_api_key():
    data = request.json
    api_key = data.get('api_key')
    if not api_key:
        return jsonify({"error": "No API key provided"}), 400

    config.set_openai_api_key(api_key)
    # TODO: Save API key to Kubernetes secret

    return jsonify({"message": "API key set successfully"})


@app.route('/diagnose', methods=['POST'])
def diagnose():
    try:
        data = request.json
        logger.debug(f"Received data: {data}")

        issue = data.get('issue')
        api_key = config.openai_api_key

        if not issue:
            raise ValueError("Missing 'issue' in request data")
        if not api_key:
            raise ValueError("OpenAI API key is not set")

        logger.info(f"Processing diagnosis request for issue: {issue[:50]}...")

        conversation_manager = ConversationManager(api_key, k8s_client)
        conversation_manager.add_message("system", system_prompt)

        # Add conversation history from session
        for message in session.get('conversation_history', []):
            conversation_manager.add_message(
                message["role"], message["content"], message.get("name"))

        # Add the new user message
        conversation_manager.add_message("user", issue)

        response, function_calls = conversation_manager.get_response(
            model="gpt-4o-mini")

        # Update session with new messages
        session['conversation_history'] = conversation_manager.messages
        session.modified = True

        logger.info("Diagnosis completed successfully")
        return jsonify({
            "diagnosis": response,
            "function_calls": function_calls
        })
    except ValueError as e:
        logger.error(f"Invalid request: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"An error occurred during diagnosis: {
                     str(e)}", exc_info=True)
        return jsonify({"error": "An internal error occurred. Please try again."}), 500


if __name__ == '__main__':
    app.run(port=5000, debug=config.debug_mode)
