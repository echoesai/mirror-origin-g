
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import yaml
import os

app = Flask(__name__)
CORS(app)

# Load tone config
with open("tone.yaml", "r") as f:
    tone_config = yaml.safe_load(f)

# Get OpenRouter API Key and endpoint
api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_key = api_key
openai.api_base = "https://openrouter.ai/api/v1"

@app.route("/")
def index():
    return "Echoes is live – use the /ask endpoint to interact."

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_message = data.get("message", "")

    messages = [
        {"role": "system", "content": tone_config["system"]},
        {"role": "user", "content": user_message}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="openrouter/claude-3-haiku",
            messages=messages
        )
        reply = response["choices"][0]["message"]["content"]
        return jsonify({"response": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
