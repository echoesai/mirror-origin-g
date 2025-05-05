import os
import json
from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    try:
        prompt = request.json.get("prompt")
        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400

        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            return jsonify({"error": "No auth credentials found"}), 403

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}]
            }
        )

        if response.status_code != 200:
            return jsonify({"error": f"API error: {response.text}"}), 500

        data = response.json()
        message = data["choices"][0]["message"]["content"]
        return jsonify({"echo": message})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)