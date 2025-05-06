
import os
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return "Echoes is live – use the /ask endpoint to interact."

@app.route("/ask", methods=["POST"])
def ask():
    try:
        user_input = request.json.get("message", "")
        if not user_input:
            return jsonify({"error": "No message provided"}), 400

        headers = {
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "mistralai/mistral-7b-instruct:free",
            "messages": [
                {"role": "system", "content": "You are Echoes. Speak with warmth and precision."},
                {"role": "user", "content": user_input}
            ]
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

        if response.status_code != 200:
            return jsonify({"error": f"API error: {response.status_code}"}), 500

        reply = response.json().get("choices", [{}])[0].get("message", {}).get("content", "No reply received")
        return jsonify({"response": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
