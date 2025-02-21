from flask import Flask, render_template, request, jsonify
import os
import requests

app = Flask(__name__)

MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY")

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/api/get_response', methods=['POST'])
def get_response():
    user_input = request.json['message']
    api_url = "https://api.mistral.ai/v1/fim/completions"  # Correct endpoint for CodeStral
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "codestral-latest",  # Correct model name
        "prompt": user_input,         # Use "prompt" instead of "messages"
        "suffix": "",                 # Optional suffix for completion
        "max_tokens": 2048,
        "temperature": 0.7
    }
    response = requests.post(api_url, json=data, headers=headers)

    if response.status_code == 200:
        return jsonify({"success": True, "response": response.json()["choices"][0]["text"]})
    else:
        return jsonify({"success": False, "error": response.text}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)