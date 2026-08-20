let chatHistory = [];

async function sendMessage() {
    const input = document.getElementById("query-input");
    const chatBox = document.getElementById("chat-box");
    const query = input.value.trim();

    if (!query) return;

    // 1. Display the User's message
    const userMessageDiv = document.createElement("div");
    userMessageDiv.className = "message user-message";
    userMessageDiv.textContent = query;
    chatBox.appendChild(userMessageDiv);

    // Clear input field & scroll down
    input.value = "";
    chatBox.scrollTop = chatBox.scrollHeight;

    // 2. Display the temporary "Thinking" indicator
    const thinkingDiv = document.createElement("div");
    thinkingDiv.className = "message bot-message thinking";
    thinkingDiv.id = "thinking-indicator";
    thinkingDiv.innerHTML = "<span>Analyzing...</span>";
    chatBox.appendChild(thinkingDiv);
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        // 3. Send request to backend with history
        const response = await fetch("/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
                query: query,
                history: chatHistory
            })
        });

        // 4. Remove the "Thinking" indicator once the response starts
        const indicator = document.getElementById("thinking-indicator");
        if (indicator) indicator.remove();

        // 5. Create the message container for the streaming response
        const botMessageDiv = document.createElement("div");
        botMessageDiv.className = "message bot-message";
        chatBox.appendChild(botMessageDiv);

        // 6. Read and render the stream chunk by chunk
        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");
        let rawMarkdown = "";

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value, { stream: true });
            rawMarkdown += chunk;
            
            // Parse Markdown to HTML in real-time
            botMessageDiv.innerHTML = marked.parse(rawMarkdown);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        // 7. Save conversation to history for subsequent turns
        chatHistory.push({ role: "user", content: query });
        chatHistory.push({ role: "assistant", content: rawMarkdown });

    } catch (error) {
        // Remove thinking indicator on error
        const indicator = document.getElementById("thinking-indicator");
        if (indicator) indicator.remove();

        // Display error message
        const errorDiv = document.createElement("div");
        errorDiv.className = "message bot-message error-message";
        errorDiv.textContent = "Error: Could not process request. Please try again.";
        chatBox.appendChild(errorDiv);
    }

    // Ensure final scroll position is at the bottom
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Allow pressing "Enter" to send message
document.getElementById("query-input")?.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
        sendMessage();
    }
});