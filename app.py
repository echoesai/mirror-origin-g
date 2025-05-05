import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mistralai/mixtral-8x7b",
                "messages": [
                    {"role": "system", "content": "Respond in G. style — emotionally intelligent, rhythm-aware, no excessive poetry, no preambles, and no generic platitudes. Speak like you *know* them."},
                    {"role": "user", "content": user_input}
                ]
            }
        )
        data = response.json()
        output = data["choices"][0]["message"]["content"]
        return jsonify({"response": output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)