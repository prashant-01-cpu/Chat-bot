const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

// Prevent double triggers
sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") {
    e.preventDefault();
    sendMessage();
  }
});

// 🪄 Format bot reply (replace * or - with ➤)
function formatBotReply(text) {
  let formatted = text;

  // Convert markdown bold (**text**) to HTML <strong>
  formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

  // Convert markdown italic (*text*) to <em>
  formatted = formatted.replace(/\*(.*?)\*/g, '<em>$1</em>');

  // Replace bullet markers (* or -) at the start of lines with •
  formatted = formatted.replace(/^\s*([*-])\s+/gm, '• ');

  // Replace numbered list (1. 2. etc.) with clean list styling
  formatted = formatted.replace(/^(\d+)\.\s+/gm, '$1. ');

  return formatted;
}


// 💬 Append message to chat
function appendMessage(sender, content) {
  const messageDiv = document.createElement("div");
  messageDiv.classList.add("message", sender, "fade-in");

  const bubble = document.createElement("div");
  bubble.classList.add("bubble");

  if (sender === "bot") {
    bubble.innerHTML = formatBotReply(content);
  } else {
    bubble.textContent = content;
  }

  messageDiv.appendChild(bubble);
  chatBox.appendChild(messageDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// ✨ Show typing animation
function showTyping() {
  const bubble = document.createElement("div");
  bubble.classList.add("bubble");

  const typingIndicator = document.createElement("div");
  typingIndicator.classList.add("typing-indicator");

  for (let i = 0; i < 3; i++) {
    const dot = document.createElement("span");
    dot.classList.add("typing-dot");
    dot.textContent = "●";
    typingIndicator.appendChild(dot);
  }

  bubble.appendChild(typingIndicator);

  const botMsg = document.createElement("div");
  botMsg.classList.add("message", "bot", "typing");
  botMsg.appendChild(bubble);
  chatBox.appendChild(botMsg);
  chatBox.scrollTop = chatBox.scrollHeight;

  return botMsg;
}

// 🚀 Send message to backend
async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;

  appendMessage("user", message);
  userInput.value = "";

  const typing = showTyping();

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });
    const data = await response.json();

    chatBox.removeChild(typing); // Remove typing dots

    if (data.reply) appendMessage("bot", data.reply);

    if (data.image_url) {
      const img = document.createElement("img");
      img.src = data.image_url;
      img.classList.add("roadmap-image");
      chatBox.appendChild(img);
    }

    chatBox.scrollTop = chatBox.scrollHeight;
  } catch (err) {
    chatBox.removeChild(typing);
    appendMessage("bot", "⚠️ Something went wrong!");
  }
}

// 🌌 Animated background
particlesJS("particles-js", {
  particles: {
    number: { value: 80, density: { enable: true, value_area: 800 } },
    color: { value: "#5bc0de" },
    shape: { type: "circle" },
    opacity: { value: 0.6, random: true },
    size: { value: 2, random: true },
    move: { enable: true, speed: 1.5, random: true, out_mode: "out" },
  },
  interactivity: {
    detect_on: "canvas",
    events: { onhover: { enable: true, mode: "grab" }, onclick: { enable: true, mode: "push" } },
    modes: { grab: { distance: 140, line_linked: { opacity: 0.5 } }, push: { particles_nb: 4 } },
  },
  retina_detect: true,
});
