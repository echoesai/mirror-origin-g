
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import yaml
import os

app = Flask(__name__, static_url_path='/static')
CORS(app)

# Load tone config
with open("tone.yaml", "r") as file:
    tone_config = yaml.safe_load(file)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_ID = "openai/gpt-4"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("prompt", "")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://mirror-origin-g.onrender.com",
        "X-Title": "Echoes",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_ID,
        "messages": [
            {"role": "system", "content": tone_config["system"]},
            {"role": "user", "content": user_input}
        ]
    }

    try:
        response = requests.post(OPENROUTER_BASE_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        reply = data["choices"][0]["message"]["content"]
        return jsonify({"response": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
