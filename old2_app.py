from flask import Flask, render_template, request, jsonify
import openai
import os

app = Flask(__name__)

# Load your OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

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

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are Echoes, a warm, emotionally intelligent conversational partner."},
                {"role": "user", "content": user_input}
            ]
        )

        reply = response['choices'][0]['message']['content'].strip()
        print(f"Generated reply: {reply}")
        return jsonify({"response": reply})

    except Exception as e:
        print(f"Error in /ask: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
