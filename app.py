from flask import Flask, render_template, request, jsonify
import os
import requests

app = Flask(__name__)

# Load OpenRouter API key from environment variable
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.json
        user_input = data.get("prompt", "")
        if not user_input:
            return jsonify({"error": "No prompt provided"}), 400

        print(f"Received prompt: {user_input}")

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://mirror-origin-g.onrender.com",
            "X-Title": "Echoes"
        }

        payload = {
            "model": "openrouter/openai/gpt-4",
            "messages": [
                {"role": "system", "content": "You are Echoes, a warm, emotionally intelligent conversational partner."},
                {"role": "user", "content": user_input}
            ]
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        response_data = response.json()

        reply = response_data["choices"][0]["message"]["content"].strip()
        print(f"Generated reply: {reply}")
        return jsonify({"response": reply})

    except Exception as e:
        print(f"Error in /ask: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
