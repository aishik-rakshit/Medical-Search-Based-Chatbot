let thinkingAudio;

function playSound(soundFile, callback) {
    const audio = new Audio(soundFile);
    audio.play();
    audio.onended = callback;
    return audio;  // Return the audio object for control
}

function stopSound(audio) {
    if (audio) {
        audio.pause();
        audio.currentTime = 0;
    }
}

function sendMessage() {
    const userInput = document.getElementById('user-input');
    const userMessage = userInput.value.trim();
    
    if (userMessage === '') {
        return;
    }

    // Display user message in the chat window
    const chatWindow = document.getElementById('chat-window');
    const userMessageDiv = document.createElement('div');
    userMessageDiv.className = 'chat-message user-message';
    userMessageDiv.innerHTML = `<div class="chat-bubble">${userMessage}</div><img src="static/user.png" alt="User">`;
    chatWindow.appendChild(userMessageDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;

    // Play outgoing message sound
    playSound('static/message_outgoing.mp3', () => {
        // Show thinking bubble
        const thinkingBubble = document.createElement('div');
        thinkingBubble.className = 'chat-message thinking-bubble';
        thinkingBubble.innerHTML = '<img src="static/ai.png" alt="AI"><div class="chat-bubble"><div class="dots"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div></div>';
        chatWindow.appendChild(thinkingBubble);
        chatWindow.scrollTop = chatWindow.scrollHeight;

        // Play thinking sound continuously
        thinkingAudio = playSound('static/thinking.mp3');
        thinkingAudio.loop = true;

        // Send message to the Flask web app
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query: userMessage,
                conversation_history: getConversationHistory(),
                context_message: ""
            })
        })
        .then(response => response.json())
        .then(data => {
            // Remove thinking bubble and stop thinking sound
            chatWindow.removeChild(thinkingBubble);
            stopSound(thinkingAudio);

            // Display assistant response in the chat window with proper formatting
            const assistantMessageDiv = document.createElement('div');
            assistantMessageDiv.className = 'chat-message assistant-message';
            assistantMessageDiv.innerHTML = `<img src="static/ai.png" alt="AI"><div class="chat-bubble">${formatMessage(data.response)}</div>`;
            chatWindow.appendChild(assistantMessageDiv);
            chatWindow.scrollTop = chatWindow.scrollHeight;

            // Play incoming message sound
            playSound('static/message_incoming.mp3');
        })
        .catch(error => {
            console.error('Error:', error);
            // Remove thinking bubble and stop thinking sound if there's an error
            chatWindow.removeChild(thinkingBubble);
            stopSound(thinkingAudio);
        });
    });

    // Clear input
    userInput.value = '';
}

function formatMessage(message) {
    // Remove numbered points and convert to paragraphs
    const pointsRegex = /\d+\.\s+/g;
    message = message.replace(pointsRegex, '');

    // Convert new lines to HTML paragraphs
    message = message.replace(/\n/g, '</p><p>');

    // Wrap the content in <p> tags appropriately
    message = `<p>${message}</p>`;

    return message;
}

function getConversationHistory() {
    const chatWindow = document.getElementById('chat-window');
    const messages = chatWindow.getElementsByClassName('chat-message');
    const conversationHistory = [];

    for (const message of messages) {
        const role = message.className.includes('user-message') ? 'user' : 'assistant';
        conversationHistory.push({ role, content: message.textContent });
    }

    return conversationHistory;
}

// Add event listener for Enter key
document.getElementById('user-input').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});