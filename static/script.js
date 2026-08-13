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
        // 1. Send request to backend
        const response = await fetch("/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query: query })
        });

        // 2. Remove the "Thinking" indicator as soon as the connection opens
        const indicator = document.getElementById("thinking-indicator");
        if (indicator) indicator.remove();

        // 3. Create the empty message div where the stream will type out
        const botMessageDiv = document.createElement("div");
        botMessageDiv.className = "message bot-message";
        chatBox.appendChild(botMessageDiv);

        // 4. Read the stream chunk by chunk
        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");

        while (true) {
            const { done, value } = await reader.read();
            if (done) break; // Stream is finished

            // Decode the chunk of text and append it to the div
            const chunk = decoder.decode(value, { stream: true });
            botMessageDiv.textContent += chunk;
            
            // Auto-scroll as text generates
            chatBox.scrollTop = chatBox.scrollHeight;
        }

    } 

    catch (error) {
        // Remove thinking indicator on error
        const indicator = document.getElementById("thinking-indicator");
        if (indicator) {
            indicator.remove();
        }

        // Display error message
        const errorDiv = document.createElement("div");
        errorDiv.className = "message bot-message error-message";
        errorDiv.textContent = "Error: Could not process request. Please try again.";
        chatBox.appendChild(errorDiv);
    }

    // Scroll chat box to bottom
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Optional: Allow pressing "Enter" to send message
document.getElementById("query-input")?.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
        sendMessage();
    }
});