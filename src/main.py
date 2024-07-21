# Copyright (c) 2024 Robert Cronin
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import sys
from openai import OpenAI
from .tool_specs import tool_specs
from flask import Flask, request, jsonify, render_template

# Read in ./SYSTEM_PROMPT.md
try:
    with open(os.path.join(os.path.dirname(__file__), "prompts", "SYSTEM_PROMPT.md"), "r") as file:
        system_prompt = file.read()
    if not system_prompt:
        raise Exception("Content of system prompt file is empty.")
except Exception as e:
    print(f"Failed to read system prompt file: {e}")
    sys.exit(1)



app = Flask(__name__)


@app.route('/')
def index():
    return render_template('diagnose.html')

# Function to call OpenAI API


def call_openai(api_key, prompt):
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        engine="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "text": system_prompt,
                        "type": "text"
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "text": prompt,
                        "type": "text"
                    }
                ]
            }
        ],
        temperature=0.7,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        max_tokens=512,
        tools=[tool_specs]
    )
    return response.choices[0].message.content[0].text

# Flask route for diagnosis


@app.route('/diagnose', methods=['POST'])
def diagnose():
    data = request.json
    issue = data['issue']
    api_key = data['api_key']
    # Call GP-4o-mini to diagnose
    diagnosis = call_openai(api_key, issue)

    return jsonify({"diagnosis": diagnosis})


if __name__ == '__main__':
    app.run(port=5000)
