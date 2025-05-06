from flask import Flask, request, jsonify, send_from_directory
import os
import requests

app = Flask(__name__, static_folder='static', static_url_path='/static')

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    user_input = data.get('message')

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "openrouter/auto",
        "messages": [
            {"role": "user", "content": user_input}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)

    if response.status_code != 200:
        return jsonify({"error": f"API error: {response.status_code}", "details": response.text}), 500

    try:
        reply = response.json()["choices"][0]["message"]["content"]
        return jsonify({"response": reply})
    except Exception as e:
        return jsonify({"error": "Invalid response structure", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
