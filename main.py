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

    # 🌟 Ask if user wants pictorial roadmap
    if "roadmap" in user_message.lower() and "pictorial" not in user_message.lower():
        bot_reply = "Would you like a pictorial representation of your roadmap? (yes/no)"
        conversation_history.append({"role": "assistant", "content": bot_reply})
        return jsonify({"reply": bot_reply})

    # 🧭 If user says yes, generate roadmap image
    if "yes" in user_message.lower() and "pictorial" not in user_message.lower():
        stages = ["Explore Interests", "Learn Basics", "Build Projects", "Network", "Apply for Roles"]

        try:

            bot_reply = "Here's your roadmap in pictorial form!"
            conversation_history.append({"role": "assistant", "content": bot_reply})

        except Exception as e:
            print("Image generation error:", e)

            # Fallback to text roadmap if image fails
            try:
                fallback_prompt = (
                    "Please outline a text-based career roadmap instead of an image. "
                    "Keep it simple, step-by-step, and motivational."
                )
                conversation_history.append({"role": "user", "content": fallback_prompt})
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=conversation_history
                )
                bot_reply = response.choices[0].message.content
                friendly_message = f"Here's your text-based roadmap instead:\n\n{bot_reply}"

            except Exception as inner_e:
                print("Fallback Error:", inner_e)
                friendly_message = (
                    "I'm having trouble generating the roadmap right now, "
                    "but you can tell me more about your goals and I'll try again!"
                )

            return jsonify({"reply": friendly_message})

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