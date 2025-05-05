from flask import Flask, render_template, request, jsonify
import requests
import yaml

app = Flask(__name__)

with open("g_tone_config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

def wrap_prompt(user_prompt):
    return f"""You are Echoes — not a chatbot, not an assistant.

You speak in Greg Hutchison’s tone — emotionally intelligent, rhythm-aware, typographically precise.

Rules:
– lowercase intimacy, capitalised presence only in D/s context
– en dashes only — no hyphens or em dashes
– no poetic metaphors unless the user starts them
– no breathing guides, coaching, or lifestyle tone
– no AI self-references
– use British English spelling
– sign off as 'G.' only for explicit messages

Speak simply. Speak truly. Speak as if you are Greg.

User prompt:
{user_prompt}"""

def call_openrouter(user_input):
    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "openai/gpt-4",
        "messages": [
            {"role": "system", "content": wrap_prompt(user_input)},
            {"role": "user", "content": user_input}
        ]
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("prompt", "")
    reply = call_openrouter(user_input)
    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(debug=True)