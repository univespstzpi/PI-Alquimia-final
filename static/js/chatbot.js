document.addEventListener("DOMContentLoaded", function() {
  const chatContainer = document.getElementById("chat-container");
  const userInput = document.getElementById("user-input");

  function sendMessage() {
      let message = userInput.value.trim();
      if (message === "") return;

      appendMessage("Você: " + message, "user");
      userInput.value = "";

      setTimeout(() => {
          let response = getResponse(message);
          appendMessage("Bot: " + response, "bot");
      }, 500);
  }

  function appendMessage(text, sender) {
      let msg = document.createElement("div");
      msg.classList.add(sender);
      msg.textContent = text;
      chatContainer.appendChild(msg);
      chatContainer.scrollTop = chatContainer.scrollHeight;
  }

  function getResponse(userMessage) {
      const responses = {
          "olá": "Olá! Bem-vindo à Cervejaria Alquimia! Como posso te ajudar?", "oi": "Oi! Bem-vindo à Cervejaria Alquimia! Como posso te ajudar?", "oi tudo bem": "Oi! Tudo ótimo, e você? Como posso te ajudar?", "tudo bem": "Que bom saber que está tudo bem! Como posso te ajudar?", "tudo certo": "Que bom saber que está tudo certo! Como posso te ajudar?", "tudo tranquilo": "Que bom saber que está tudo tranquilo! Como posso te ajudar?", "tudo beleza": "Que bom saber que está tudo beleza! Como posso te ajudar?", "tudo ok": "Que bom saber que está tudo ok! Como posso te ajudar?", "tipos de cervejas": "Temos cervejas do tipo Pilsen, Trigo, Stout, Sour, Red Ale e IPA", "horário de funcionamento": "Estamos abertos de terça a domingo das 15h às 22h.", "horário funcionamento": "Estamos abertos de terça a domingo das 15h às 22h.", "horário": "Estamos abertos de terça a domingo das 15h às 22h.", "onde fica": "Nossa cervejaria está localizada na Avenida Maria Aparecida Andrade, 342, no bairro Jd. Veneto II, na cidade de Sertãozinho-SP. Clique no link e Venha nos visitar!", "onde fica a cervejaria": "Nossa cervejaria está localizada na Avenida Maria Aparecida Andrade, 342, no bairro Jd. Veneto II, na cidade de Sertãozinho-SP. Clique no link e Venha nos visitar!", "obrigado":" De nada! Se precisar de mais alguma coisa, é só perguntar.", "tchau": "Tchau! Volte sempre!", "até logo": "Até logo! Volte sempre!", "valeu": "De nada! Se precisar de mais alguma coisa, é só perguntar.", "tá bom": "Que bom saber que está tudo bem! Fico feliz em ajudar?", "tá tranquilo": "Que bom saber que está tudo tranquilo! Como posso te ajudar?", "tá beleza": "Que bom saber que está tudo beleza! Como posso te ajudar?", "tá ok": "Que bom saber que está tudo ok! Como posso te ajudar?", "tá certo": "Que bom saber que está tudo certo! Como posso te ajudar?", "tá de boa": "Que bom saber que está tudo de boa! Como posso te ajudar?", "bom dia": "Bom dia! Como posso lhe ajudar?", "boa tarde": "Boa Tarde! Em que posso lhe ajudar?", "boa noite":"Boa noite! Em que posso lhe ajudar?",
      };

      return responses[userMessage.toLowerCase()] || "Desculpe, não entendi. Você quer saber quais os nossos 'tipos de cervejas', 'horário funcionamento' ou 'onde fica a cervejaria'?";
  }

  window.sendMessage = sendMessage;
});
