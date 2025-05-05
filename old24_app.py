
import os
import openai
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import yaml
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

# Load tone YAML
with open("tone.yaml", "r") as file:
    tone_config = yaml.safe_load(file)

def apply_tone_and_rhythm(text):
    if tone_config.get("style") == "G":
        text = text.replace(".", "").replace("--", "–").replace("-", "–")
        text = text.replace("...", "…")
    return text

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_message}],
            headers={
                "HTTP-Referer": "https://mirror.greg.app",
                "X-Title": "Mirror"
            }
        )
        reply = response.choices[0].message.content.strip()
        styled_reply = apply_tone_and_rhythm(reply)
        return jsonify({"reply": styled_reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
