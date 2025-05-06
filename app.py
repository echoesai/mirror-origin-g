
from flask import Flask, request, jsonify, render_template
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_input = data.get('message', '')

    if not user_input:
        return jsonify({'error': 'No input provided'}), 400

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return jsonify({'error': 'API key not found'}), 500

    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://mirror-origin-g.onrender.com",
        "X-Title": "Echoes"
    }

    payload = {
        "model": "openrouter/auto",
        "messages": [
            {"role": "user", "content": user_input}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions",
                                 headers=headers,
                                 json=payload)
        if response.status_code == 200:
            reply = response.json()["choices"][0]["message"]["content"]
            return jsonify({'response': reply})
        else:
            return jsonify({'error': f'API error: {response.status_code}'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
