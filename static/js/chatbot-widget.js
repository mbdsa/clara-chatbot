document.addEventListener("DOMContentLoaded", function () {
    const chatbotAvatar = document.querySelector(".chatbot-avatar");
    const chatbotWidget = document.querySelector(".chatbot-widget");
    const chatbotMessages = document.querySelector(".chatbot-messages");
    const chatbotInput = document.getElementById("chatbot-input");
    const chatbotSend = document.getElementById("chatbot-send");
  
    // Ouvre/ferme le widget
    chatbotAvatar.addEventListener("click", () => {
      chatbotWidget.style.display = chatbotWidget.style.display === "flex" ? "none" : "flex";
    });
  
    // Gère l'envoi du message
    chatbotSend.addEventListener("click", sendMessage);
    chatbotInput.addEventListener("keydown", function (event) {
      if (event.key === "Enter") sendMessage();
    });
  
    function sendMessage() {
      const message = chatbotInput.value.trim();
      if (message === "") return;
  
      addMessage("user", message);
      chatbotInput.value = "";
  
      fetch("/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: message })
      })
      .then(response => response.json())
      .then(data => {
        addMessage("bot", data.answer);
      })
      .catch(error => {
        addMessage("bot", "Une erreur est survenue. Réessaie plus tard.");
        console.error("Erreur lors de la requête :", error);
      });
    }
  
    function addMessage(sender, text) {
      const messageElem = document.createElement("div");
      messageElem.className = `message ${sender}`;
      messageElem.textContent = text;
      chatbotMessages.appendChild(messageElem);
      chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }
  });
  