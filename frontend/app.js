const API_URL = 'http://127.0.0.1:8000';

document.addEventListener('DOMContentLoaded', () => {
    const chatHistory = document.getElementById('chat-history');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const statusIndicator = document.getElementById('status-indicator');

    // Check backend status on load
    checkBackendStatus();

    // Auto-resize textarea
    messageInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
        if (this.value.trim() === '') {
             sendButton.disabled = true;
        } else {
             sendButton.disabled = false;
        }
    });

    // Initial button state
    sendButton.disabled = true;

    // Handle Enter key (send message) and Shift+Enter (new line)
    messageInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    sendButton.addEventListener('click', sendMessage);

    async function checkBackendStatus() {
        try {
            const response = await fetch(`${API_URL}/`);
            if (response.ok) {
                statusIndicator.classList.remove('offline');
                statusIndicator.classList.add('online');
                statusIndicator.title = "Backend is Online";
            } else {
                setOffline();
            }
        } catch (error) {
            setOffline();
        }
    }

    function setOffline() {
        statusIndicator.classList.remove('online');
        statusIndicator.classList.add('offline');
        statusIndicator.title = "Backend is Offline";
    }

    async function sendMessage() {
        const text = messageInput.value.trim();
        if (!text) return;

        // 1. Add User message to UI
        appendMessage('user', text);
        messageInput.value = '';
        messageInput.style.height = 'auto';
        sendButton.disabled = true;

        // 2. Add Loading indicator
        const loadingId = appendLoading();

        // 3. Call Backend API
        try {
            const response = await fetch(`${API_URL}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: text })
            });

            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }

            const data = await response.json();

            // 4. Remove loading and add AI response
            removeMessage(loadingId);
            appendMessage('ai', data.reply, data.sources);

            // Ensure status is online if successful
            statusIndicator.classList.remove('offline');
            statusIndicator.classList.add('online');

        } catch (error) {
            console.error('Error fetching response:', error);
            removeMessage(loadingId);
            appendMessage('ai', '⚠️ Connection Error: Unable to reach the `.ac` backend. Please ensure the server is running via Termux.', [], true);
            setOffline();
        }
    }

    function appendMessage(sender, text, sources = [], isError = false) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(sender === 'user' ? 'user-message' : 'ai-message');

        let contentHtml = `<div class="message-content" ${isError ? 'style="color: var(--error-color);"' : ''}>`;

        // Simple escaping to prevent HTML injection/swallowing
        const escapedText = text.replace(/&/g, "&amp;")
                                .replace(/</g, "&lt;")
                                .replace(/>/g, "&gt;")
                                .replace(/"/g, "&quot;")
                                .replace(/'/g, "&#039;");
        contentHtml += escapedText;

        contentHtml += `</div>`;

        if (sources && sources.length > 0) {
            // Filter out direct llm fallback string if present
             const validSources = sources.filter(s => !s.toLowerCase().includes('direct llm'));
             if(validSources.length > 0) {
                 const sourceString = validSources.map(s => s.split('/').pop()).join(', '); // Show only filenames
                 contentHtml += `<div class="sources-indicator">🔍 Sources: ${sourceString}</div>`;
             }
        }

        messageDiv.innerHTML = contentHtml;
        chatHistory.appendChild(messageDiv);
        scrollToBottom();
    }

    function appendLoading() {
        const id = 'loading-' + Date.now();
        const messageDiv = document.createElement('div');
        messageDiv.id = id;
        messageDiv.classList.add('message', 'ai-message');
        messageDiv.innerHTML = `<div class="message-content"><span class="loading-dots">Thinking</span></div>`;
        chatHistory.appendChild(messageDiv);
        scrollToBottom();
        return id;
    }

    function removeMessage(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    function scrollToBottom() {
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }
});
