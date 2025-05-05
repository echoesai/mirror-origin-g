
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder="static")
CORS(app)

API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    print("Received message:", user_message)

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openrouter/auto",
        "messages": [{"role": "user", "content": user_message}]
    }

    try:
        print("Sending request to OpenRouter...")
        response = requests.post(API_URL, headers=headers, json=payload)
        print("OpenRouter response status:", response.status_code)
        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"]
        print("Reply from OpenRouter:", reply)
        return jsonify({"response": reply})
    except Exception as e:
        print("Error occurred:", e)
        return jsonify({"response": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
