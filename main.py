from flask import Flask, render_template, request, jsonify
import matplotlib
matplotlib.use("Agg")  # Fix: use non-interactive backend for Flask
import matplotlib.pyplot as plt
import io
import base64
from groq import Groq
import traceback

app = Flask(__name__, template_folder="templates", static_folder="static")

# Groq API client
client = Groq(api_key="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")

conversation_history = [
    {"role": "system", "content": "You are a friendly AI career mentor who creates creative visual and text roadmaps for users."}
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json["message"].lower().strip()
        conversation_history.append({"role": "user", "content": user_message})

        # Determine if image roadmap or text roadmap
        image_keywords = ["visual", "pictorial", "diagram", "roadmap image", "graph", "chart"]
        text_keywords = ["text", "write", "only text", "text only"]

        # --- Generate Image Roadmap ---
        if any(keyword in user_message for keyword in image_keywords):
            stages = ["Learn Python", "Master Statistics", "Explore ML", "Build Projects", "Get Hired"]

            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(range(len(stages)), [1]*len(stages), 'o-', color='#6A0D91', linewidth=3)
            for i, stage in enumerate(stages):
                ax.text(i, 1.05, stage, ha='center', fontsize=10, fontweight='bold')
            ax.set_title("AI Career Roadmap", fontsize=14, color="#6A0D91", fontweight="bold")
            ax.axis("off")

            plt.tight_layout()
            buf = io.BytesIO()
            plt.savefig(buf, format="png", bbox_inches="tight", facecolor="#161A3F")
            buf.seek(0)
            image_base64 = base64.b64encode(buf.read()).decode("utf-8")
            buf.close()

            bot_reply = "Here's your generated AI Career Roadmap image!"
            conversation_history.append({"role": "assistant", "content": bot_reply})
            return jsonify({"reply": bot_reply, "image": image_base64})

        # --- Generate Text Roadmap ---
        else:
            response = client.chat.completions.create(
                model="llama3-8b-8192",  # Groq-compatible model
                messages=conversation_history
            )

            bot_reply = response.choices[0].message.content
            conversation_history.append({"role": "assistant", "content": bot_reply})

            return jsonify({"reply": bot_reply})

    except Exception as e:
        print("🔥 ERROR:", e)
        print(traceback.format_exc())
        return jsonify({
            "reply": "⚠️ Something went wrong while generating your roadmap. Check console logs for details."
        })

if __name__ == "__main__":
    app.run(debug=True)
