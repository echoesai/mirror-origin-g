
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import yaml
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

with open("tone.yaml", "r") as file:
    tone_config = yaml.safe_load(file)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_BASE = "https://openrouter.ai/api/v1"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        user_input = data.get("prompt", "")

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "openai/gpt-4",
            "messages": [
                {"role": "system", "content": tone_config.get("system", "")},
                {"role": "user", "content": user_input}
            ]
        }

        response = requests.post(
            f"{OPENROUTER_API_BASE}/chat/completions",
            headers=headers,
            json=payload
        )

        print("Status Code:", response.status_code)
        print("Response Text:", response.text)

        if response.status_code != 200:
            return jsonify({"response": f"API error: {response.status_code}"}), 500

        try:
            result = response.json()
            message = result["choices"][0]["message"]["content"]
        except Exception as e:
            print("Failed to parse response JSON:", e)
            return jsonify({"response": "Error parsing response"}), 500

        return jsonify({"response": message})

    except Exception as e:
        print("Server Error:", e)
        return jsonify({"response": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=True)
