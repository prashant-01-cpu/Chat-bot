from flask import Flask, render_template, request, jsonify
import io
import base64
import matplotlib
matplotlib.use("Agg")  # ✅ Fix: use non-interactive backend for Flask
import matplotlib.pyplot as plt
from groq import Groq
import random

app = Flask(__name__, template_folder="templates", static_folder="static")

# ✅ Replace with your valid Groq API key
client = Groq(api_key="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")

conversation_history = [
    {"role": "system", "content": "You are a friendly AI career mentor who creates creative visual and text roadmaps for users."}
]

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    global conversation_history
    user_message = request.json["message"].lower().strip()
    conversation_history.append({"role": "user", "content": user_message})

    try:
        # Detect roadmap image request
        image_keywords = [
            "image roadmap", "visual", "pictorial", "diagram",
            "picture", "roadmap image", "graph", "chart"
        ]
        text_keywords = ["text roadmap", "only text", "text only"]

        # ✅ IMAGE GENERATION
        if any(keyword in user_message for keyword in image_keywords):
            topic = user_message.replace("roadmap", "").strip().title() or "Career"

            # Generate a creative visual roadmap
            stages = ["Explore", "Learn", "Practice", "Network", "Achieve"]
            y_values = [random.randint(1, 10) for _ in stages]

            plt.figure(figsize=(8, 4))
            plt.plot(stages, y_values, marker="o", linewidth=4,
                     color="#1ABC9C", markerfacecolor="#16A085")
            plt.fill_between(stages, y_values, color="#16A085", alpha=0.3)
            plt.title(f"🌟 Your {topic} Roadmap", fontsize=16, color="#F4D03F", weight="bold")
            plt.gca().set_facecolor("#0E1A2B")
            plt.xticks(rotation=25, color="#FDFEFE", fontsize=10)
            plt.yticks([])
            plt.tight_layout()

            # Convert to base64
            buf = io.BytesIO()
            plt.savefig(buf, format="png", bbox_inches="tight", facecolor="#0E1A2B")
            buf.seek(0)
            image_base64 = base64.b64encode(buf.read()).decode("utf-8")
            plt.close()

            bot_reply = f"Here's your creative {topic} roadmap! 🎨"
            conversation_history.append({"role": "assistant", "content": bot_reply})
            return jsonify({"reply": bot_reply, "image": image_base64})

        # ✅ TEXT ROADMAP
        elif any(keyword in user_message for keyword in text_keywords) or user_message in ["no", "text"]:
            bot_reply = "Sure! Here’s your structured text-based roadmap. 🧭"
            conversation_history.append({"role": "assistant", "content": bot_reply})
            return jsonify({"reply": bot_reply})

        # ✅ Use Groq API for normal replies
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=conversation_history
        )
        bot_reply = response.choices[0].message.content
        conversation_history.append({"role": "assistant", "content": bot_reply})

        return jsonify({"reply": bot_reply})

    except Exception as e:
        # Print full traceback for debugging
        import traceback
        print("🔥 ERROR:", e)
        print(traceback.format_exc())
        return jsonify({"reply": "⚠️ Something went wrong while generating your roadmap. Check console logs for details."})


if __name__ == "__main__":
    app.run(debug=True)
