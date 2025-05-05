
from flask import Flask, request, render_template, jsonify
import requests
import os
import yaml

app = Flask(__name__)

# Load G-style tone config from YAML
with open("tone.yaml", "r") as file:
    tone_config = yaml.safe_load(file)

# Load OpenRouter API key from environment variable
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/echo", methods=["POST"])
def echo():
    user_input = request.json.get("prompt", "")
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://echoes.greg.app",
        "X-Title": "Echoes",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openrouter/gpt-4",
        "messages": [
            {"role": "system", "content": tone_config["system_prompt"]},
            {"role": "user", "content": user_input}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        output = response.json()["choices"][0]["message"]["content"]
        return jsonify({"reply": post_process(output)})
    except Exception as e:
        return jsonify({"reply": "Echoes couldn’t reach the stars just now – try again?"})

def post_process(text):
    # Basic G-style formatter: trim, replace unwanted patterns, etc
    text = text.strip()
    if text.lower().startswith("echoes:"):
        text = text.split(":", 1)[-1].strip()
    if text.startswith("–"):
        text = text[1:].strip()
    return text

if __name__ == "__main__":
    app.run(debug=True)
