
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    prompt = data.get("prompt", "")
    
    # Temporary placeholder response
    response = f"You said: {prompt}"

    return jsonify({"response": response})

@app.route("/", methods=["GET"])
def index():
    return "Echoes backend is live."

if __name__ == "__main__":
    app.run(debug=True)
