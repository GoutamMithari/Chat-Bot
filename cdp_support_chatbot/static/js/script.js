document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');
    
    // Function to create a message element
    function createMessageElement(content, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(isUser ? 'user-message' : 'bot-message');
        
        const messageContent = document.createElement('div');
        messageContent.classList.add('message-content');
        
        // If it's a bot message and content contains markdown, render it as markdown
        if (!isUser && (content.includes('*') || content.includes('```') || content.includes('#'))) {
            messageContent.innerHTML = md.render(content);
        } else {
            const paragraph = document.createElement('p');
            paragraph.textContent = content;
            messageContent.appendChild(paragraph);
        }
        
        messageDiv.appendChild(messageContent);
        return messageDiv;
    }
    
    // Function to add a message to the chat
    function addMessage(content, isUser = false) {
        const messageElement = createMessageElement(content, isUser);
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Function to show typing indicator
    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.classList.add('message', 'bot-message', 'typing-indicator-container');
        typingDiv.id = 'typing-indicator';
        
        const typingContent = document.createElement('div');
        typingContent.classList.add('typing-indicator');
        
        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('span');
            typingContent.appendChild(dot);
        }
        
        typingDiv.appendChild(typingContent);
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Function to remove typing indicator
    function removeTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    // Function to handle the chat form submission
    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const message = userInput.value.trim();
        if (!message) return;
        
        // Add user message to chat
        addMessage(message, true);
        
        // Clear input field
        userInput.value = '';
        
        // Show typing indicator
        showTypingIndicator();
        
        // Send message to server
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            // Remove typing indicator
            removeTypingIndicator();
            
            // Add bot response to chat
            addMessage(data.response, false);
            
            // Highlight code blocks if any
            document.querySelectorAll('pre code').forEach((block) => {
                hljs.highlightElement(block);
            });
        })
        .catch(error => {
            console.error('Error:', error);
            removeTypingIndicator();
            addMessage('Sorry, there was an error processing your request. Please try again.', false);
        });
    });
    
    // Function to set question from examples
    window.setQuestion = function(element) {
        userInput.value = element.textContent;
        userInput.focus();
    };
    
    // Initial focus on input field
    userInput.focus();
    
    // Add event listener for Enter key in input field
    userInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            chatForm.dispatchEvent(new Event('submit'));
        }
    });
    
    // Function to handle viewport changes
    function handleViewportChange() {
        if (window.innerWidth <= 768) {
            chatMessages.style.maxHeight = '50vh';
        } else {
            chatMessages.style.maxHeight = '60vh';
        }
    }
    
    // Call once on load and add event listener
    handleViewportChange();
    window.addEventListener('resize', handleViewportChange);
    
    // Highlight code blocks on initial load
    document.querySelectorAll('pre code').forEach((block) => {
        hljs.highlightElement(block);
    });
});