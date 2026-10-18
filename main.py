"""Flask backend for the AI Career Guidance Chatbot."""

import os
import secrets
from threading import Lock

from cachetools import TTLCache
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request, session
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
secret_key = os.getenv("FLASK_SECRET_KEY")
if not api_key or api_key.startswith("replace_with_"):
    raise RuntimeError("GROQ_API_KEY is missing. Add your new key to the .env file.")
if not secret_key or secret_key.startswith("replace_with_"):
    raise RuntimeError("FLASK_SECRET_KEY is missing. Set it in your .env file.")

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config.update(
    SECRET_KEY=secret_key,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    # Set SESSION_COOKIE_SECURE=True when serving over HTTPS in production.
)

client = Groq(api_key=api_key)
model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

SYSTEM_MESSAGE = {
    "role": "system",
    "content": (
        "You are a friendly career guidance assistant. Help students explore "
        "career paths that fit their interests and skills. Provide realistic, "
        "practical, and clear next steps."
    ),
}
ROADMAP_STAGES = [
    "Explore your interests and strengths",
    "Learn the foundational skills",
    "Build practical projects",
    "Network with people in your field",
    "Apply for internships and entry-level roles",
]
MAX_MESSAGE_LENGTH = 4000
MAX_HISTORY_MESSAGES = 20

# A small, per-browser, in-memory conversation cache for local/demo use.
# Use a shared store (e.g., Redis) for multiple production workers/instances.
conversations = TTLCache(maxsize=1000, ttl=3600)
conversations_lock = Lock()


def get_conversation():
    conversation_id = session.get("conversation_id")
    if not conversation_id:
        conversation_id = secrets.token_urlsafe(32)
        session["conversation_id"] = conversation_id

    with conversations_lock:
        state = conversations.get(conversation_id)
        if state is None:
            state = {"messages": [], "awaiting_roadmap_confirmation": False}
        # Work on a copy so an API request does not hold the cache lock.
        state = {
            "messages": list(state["messages"]),
            "awaiting_roadmap_confirmation": state["awaiting_roadmap_confirmation"],
        }
    return conversation_id, state


def save_conversation(conversation_id, state):
    with conversations_lock:
        conversations[conversation_id] = state


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/chat")
def chat():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": "Send JSON with a 'message' field."}), 400

    user_message = payload.get("message")
    if not isinstance(user_message, str) or not user_message.strip():
        return jsonify({"error": "Message must be a non-empty string."}), 400

    user_message = user_message.strip()
    if len(user_message) > MAX_MESSAGE_LENGTH:
        return jsonify({"error": "Message is too long."}), 400

    conversation_id, state = get_conversation()
    lower_message = user_message.lower()

    if state["awaiting_roadmap_confirmation"]:
        if lower_message in {"yes", "y", "sure", "okay", "ok"}:
            state["awaiting_roadmap_confirmation"] = False
            roadmap = "Here's a simple career roadmap:\n" + "\n".join(
                f"{number}. {stage}"
                for number, stage in enumerate(ROADMAP_STAGES, start=1)
            )
            state["messages"].extend(
                [
                    {"role": "user", "content": user_message},
                    {"role": "assistant", "content": roadmap},
                ]
            )
            state["messages"] = state["messages"][-MAX_HISTORY_MESSAGES:]
            save_conversation(conversation_id, state)
            return jsonify({"reply": roadmap})
        if lower_message in {"no", "n"}:
            state["awaiting_roadmap_confirmation"] = False
            reply = "No problem! What career question can I help you with?"
            save_conversation(conversation_id, state)
            return jsonify({"reply": reply})
        state["awaiting_roadmap_confirmation"] = False

    if "roadmap" in lower_message and "pictorial" not in lower_message:
        reply = "Would you like a step-by-step career roadmap? (yes/no)"
        state["awaiting_roadmap_confirmation"] = True
        state["messages"].extend(
            [
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": reply},
            ]
        )
        state["messages"] = state["messages"][-MAX_HISTORY_MESSAGES:]
        save_conversation(conversation_id, state)
        return jsonify({"reply": reply})

    messages = [SYSTEM_MESSAGE] + state["messages"][-MAX_HISTORY_MESSAGES:] + [
        {"role": "user", "content": user_message}
    ]
    try:
        response = client.chat.completions.create(model=model, messages=messages)
        bot_reply = response.choices[0].message.content or "I couldn't generate a reply."
    except Exception:
        app.logger.exception("Groq chat request failed")
        return jsonify({"reply": "I'm having trouble responding right now. Please try again."}), 502

    state["messages"] = (
        state["messages"]
        + [
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": bot_reply},
        ]
    )[-MAX_HISTORY_MESSAGES:]
    save_conversation(conversation_id, state)
    return jsonify({"reply": bot_reply})


if __name__ == "__main__":
    # Local development only. Use a production WSGI server for hosting.
    app.run(debug=False)
