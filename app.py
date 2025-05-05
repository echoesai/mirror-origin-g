
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv
import yaml

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

# Configure OpenAI (OpenRouter) API
openai.api_key = api_key
openai.api_base = "https://openrouter.ai/api/v1"

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json.get("message")

        if not user_input:
            return jsonify({"error": "Missing input"}), 400

        response = openai.ChatCompletion.create(
            model="openai/gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )

        reply = response["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/status")
def status():
    return "Service is running."

if __name__ == "__main__":
    app.run(debug=True)
