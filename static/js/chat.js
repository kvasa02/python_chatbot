// Enhanced Chatbot JavaScript
class ChatbotInterface {
    constructor() {
        this.chatBox = document.getElementById('chat-box');
        this.chatForm = document.getElementById('chat-form');
        this.userInput = document.getElementById('user-input');
        this.sendBtn = document.getElementById('send-btn');
        this.typingIndicator = document.getElementById('typing-indicator');
        
        this.isTyping = false;
        this.messageCount = 0;
        
        this.initializeEventListeners();
        this.setWelcomeTime();
    }
    
    initializeEventListeners() {
        // Form submission
        this.chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleUserMessage();
        });
        
        // Enter key handling
        this.userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.handleUserMessage();
            }
        });
        
        // Input focus and typing
        this.userInput.addEventListener('input', () => {
            this.updateSendButton();
        });
        
        this.userInput.addEventListener('focus', () => {
            this.userInput.parentElement.style.borderColor = '#667eea';
        });
        
        this.userInput.addEventListener('blur', () => {
            this.userInput.parentElement.style.borderColor = '#e1e5e9';
        });
    }
    
    setWelcomeTime() {
        const welcomeTime = document.getElementById('welcome-time');
        if (welcomeTime) {
            welcomeTime.textContent = this.getCurrentTime();
        }
    }
    
    getCurrentTime() {
        const now = new Date();
        return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
    
    updateSendButton() {
        const hasText = this.userInput.value.trim().length > 0;
        this.sendBtn.disabled = !hasText;
    }
    
    showTypingIndicator() {
        this.typingIndicator.style.display = 'flex';
        this.scrollToBottom();
    }
    
    hideTypingIndicator() {
        this.typingIndicator.style.display = 'none';
    }
    
    scrollToBottom() {
        setTimeout(() => {
            this.chatBox.scrollTop = this.chatBox.scrollHeight;
        }, 100);
    }
    
    createMessageElement(message, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-msg`;
        
        const avatar = document.createElement('div');
        avatar.className = `avatar ${sender}-avatar`;
        
        if (sender === 'user') {
            avatar.innerHTML = '<i class="fas fa-user"></i>';
        } else {
            avatar.innerHTML = '<i class="fas fa-robot"></i>';
        }
        
        const bubble = document.createElement('div');
        bubble.className = `message-bubble ${sender}-bubble`;
        
        // Handle multiline messages and preserve formatting
        const formattedMessage = this.formatMessage(message);
        bubble.innerHTML = formattedMessage;
        
        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = this.getCurrentTime();
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(bubble);
        bubble.appendChild(timeDiv);
        
        return messageDiv;
    }
    
    formatMessage(message) {
        // Convert line breaks to <br> tags
        let formatted = message.replace(/\n/g, '<br>');
        
        // Add emoji support
        formatted = formatted.replace(/🌤️/g, '<span style="font-size: 1.2em;">🌤️</span>');
        formatted = formatted.replace(/📰/g, '<span style="font-size: 1.2em;">📰</span>');
        formatted = formatted.replace(/📚/g, '<span style="font-size: 1.2em;">📚</span>');
        formatted = formatted.replace(/😄/g, '<span style="font-size: 1.2em;">😄</span>');
        
        return formatted;
    }
    
    appendMessage(message, sender) {
        const messageElement = this.createMessageElement(message, sender);
        this.chatBox.appendChild(messageElement);
        this.scrollToBottom();
        
        // Add animation delay for bot messages
        if (sender === 'bot') {
            messageElement.style.opacity = '0';
            messageElement.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                messageElement.style.transition = 'all 0.3s ease-out';
                messageElement.style.opacity = '1';
                messageElement.style.transform = 'translateY(0)';
            }, 100);
        }
    }
    
    async handleUserMessage() {
        const message = this.userInput.value.trim();
        if (!message || this.isTyping) return;
        
        // Clear input and disable send button
        this.userInput.value = '';
        this.updateSendButton();
        
        // Add user message
        this.appendMessage(message, 'user');
        
        // Show typing indicator
        this.isTyping = true;
        this.showTypingIndicator();
        
        try {
            // Send message to backend
            const response = await this.sendMessageToBackend(message);
            
            // Hide typing indicator
            this.hideTypingIndicator();
            
            // Add bot response
            this.appendMessage(response, 'bot');
            
        } catch (error) {
            console.error('Error sending message:', error);
            this.hideTypingIndicator();
            this.appendMessage('Sorry, I encountered an error. Please try again.', 'bot');
        } finally {
            this.isTyping = false;
        }
    }
    
    async sendMessageToBackend(message) {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data.response;
    }
    
    // Function to handle suggestion button clicks
    sendSuggestion(suggestion) {
        this.userInput.value = suggestion;
        this.handleUserMessage();
    }
}

// Initialize the chatbot interface when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.chatbot = new ChatbotInterface();
});

// Global function for suggestion buttons
function sendSuggestion(suggestion) {
    if (window.chatbot) {
        window.chatbot.sendSuggestion(suggestion);
    }
}

// Add some keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter to send message
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        if (window.chatbot) {
            window.chatbot.handleUserMessage();
        }
    }
    
    // Escape to clear input
    if (e.key === 'Escape') {
        if (window.chatbot && window.chatbot.userInput) {
            window.chatbot.userInput.value = '';
            window.chatbot.updateSendButton();
            window.chatbot.userInput.focus();
        }
    }
});

// Add some visual feedback for suggestion buttons
document.addEventListener('DOMContentLoaded', () => {
    const suggestionBtns = document.querySelectorAll('.suggestion-btn');
    
    suggestionBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Add a small animation
            btn.style.transform = 'scale(0.95)';
            setTimeout(() => {
                btn.style.transform = 'scale(1)';
            }, 150);
        });
    });
});