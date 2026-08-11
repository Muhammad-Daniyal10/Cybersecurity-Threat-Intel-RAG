async function sendMessage(){
    const input = document.getElementById('query-input');
    const chatBox = document.getElementById('chat-box');
    const query = input.value.trim();


if(!query){
    return false;
}

function appendMessage(text, className, isError = false){
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', className);

    if(isError){
        msgDiv.style.color = 'red';
    }

    msgDiv.textContent = text;
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

appendMessage(query, 'user-msg');
input.value = '';

try{
    const response = await fetch('/ask',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({query: query})
    });

    if(response.ok){
        const data = await response.json();

        appendMessage(data.answer, 'bot-msg');
    }
    else{
        appendMessage(`Error: backend returned status ${response.status}`, `bot-msg`, true);
    }
}

catch(error){
    appendMessage(`Error: ${error.message}`, `bot-msg`, true);
}
}

document.getElementById('query-input').addEventListener('keypress', function (e){
    if(e.key === "Enter"){
        sendMessage();
    }
});