const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
});

function appendMessage(sender, content) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", sender, "fade-in");  // <-- add fade-in here

    const bubble = document.createElement("div");
    bubble.classList.add("bubble");

    if (typeof content === "string") {
        bubble.textContent = content;
    } else {
        bubble.appendChild(content);
    }

    messageDiv.appendChild(bubble);
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function showTyping() {
    const bubble = document.createElement("div");
    bubble.classList.add("bubble");
    
    // Create typing dots container
    const typingIndicator = document.createElement("div");
    typingIndicator.classList.add("typing-indicator");
    
    // Add 3 animated dots
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
        typing.querySelector(".bubble").textContent = data.reply;
    } catch {
        typing.querySelector(".bubble").textContent = "⚠️ Something went wrong!";
    }
}
if (data.image) {
  const img = document.createElement("img");
  img.src = "data:image/png;base64," + data.image;
  img.classList.add("roadmap-image");
  appendMessage("bot", img);
  if (data.image) {
  const img = document.getElementById("roadmap-img");
  img.src = `data:image/png;base64,${data.image}`;
  img.style.display = "block";
}
fetch("/chat", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ message: userMessage })
})
.then(response => response.json())
.then(data => {
  const chatBox = document.getElementById("chat-box");

  // Add the text response
  const botMsg = document.createElement("div");
  botMsg.classList.add("bot-message");
  botMsg.innerHTML = `<p>${data.reply}</p>`;
  chatBox.appendChild(botMsg);

  // If image exists, show it
  if (data.image) {
    const img = document.createElement("img");
    img.src = "data:image/png;base64," + data.image;
    img.classList.add("roadmap-image");
    img.style.maxWidth = "100%";
    img.style.borderRadius = "12px";
    img.style.marginTop = "8px";
    chatBox.appendChild(img);
  }

  chatBox.scrollTop = chatBox.scrollHeight;
});


} else {
  appendMessage("bot", data.reply);
}




