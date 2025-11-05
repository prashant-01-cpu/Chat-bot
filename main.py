from flask import Flask, render_template, request, jsonify
import matplotlib.pyplot as plt
import io
import base64
from groq import Groq

app = Flask(__name__, template_folder='templates', static_folder='static')

# Initialize Groq API client
client = Groq(api_key="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")  # 🔒 Replace with your actual API key

# Global conversation history
conversation_history = [
    {"role": "system", "content": "You are a friendly career guidance assistant. Your goal is to help students explore career paths that fit their interests and skills."}
]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    global conversation_history
    user_message = request.json["message"]
    conversation_history.append({"role": "user", "content": user_message})

    # 💬 Otherwise, use Groq model to respond normally
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=conversation_history
        )
        bot_reply = response.choices[0].message.content
        conversation_history.append({"role": "assistant", "content": bot_reply})
        return jsonify({"reply": bot_reply})

    except Exception as e:
        print("Error:", e)
        friendly_message = "Hmm, something went wrong. Let's try that again!"
        return jsonify({"reply": friendly_message})


if __name__ == "__main__":
    app.run(debug=True)
