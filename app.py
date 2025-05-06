
import os
import json
import requests
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        prompt = data.get("prompt", "").strip()

        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400

        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            return jsonify({"error": "API key not set in environment"}), 500

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "openrouter/mistral",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, data=json.dumps(payload))

        if response.status_code != 200:
            return jsonify({"error": f"API error: {response.status_code}", "details": response.text}), 500

        result = response.json()
        message = result.get("choices", [{}])[0].get("message", {}).get("content", "")

        return jsonify({"response": message})

    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
