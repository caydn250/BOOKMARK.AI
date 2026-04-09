// Configuration
const API_BASE = 'http://localhost:5000/api';

// State
let currentDocId = null;
let currentSessionId = generateSessionId();

// DOM elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const uploadBtn = document.getElementById('uploadBtn');
const uploadStatus = document.getElementById('uploadStatus');
const documentInfo = document.getElementById('documentInfo');
const fileName = document.getElementById('fileName');
const sentenceCount = document.getElementById('sentenceCount');
const summaryBtn = document.getElementById('summaryBtn');
const summary = document.getElementById('summary');
const chatBox = document.getElementById('chatBox');
const questionInput = document.getElementById('questionInput');
const askBtn = document.getElementById('askBtn');
const qaStatus = document.getElementById('qaStatus');
const clearBtn = document.getElementById('clearBtn');

// Utility functions
function generateSessionId() {
    return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

function showStatus(elementId, message, type) {
    const element = document.getElementById(elementId);
    element.className = `status ${type}`;
    
    if (type === 'loading') {
        element.innerHTML = `<span class="loading-spinner"></span>${message}`;
    } else {
        element.textContent = message;
    }
    element.style.display = 'block';
}

function clearStatus(elementId) {
    const element = document.getElementById(elementId);
    element.style.display = 'none';
}

function addMessage(role, content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    messageDiv.textContent = content;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Upload handling
uploadArea.addEventListener('click', () => fileInput.click());

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.style.background = '#e6ecff';
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.style.background = '#f0f4ff';
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.style.background = '#f0f4ff';
    fileInput.files = e.dataTransfer.files;
    uploadBtn.disabled = false;
});

fileInput.addEventListener('change', () => {
    uploadBtn.disabled = fileInput.files.length === 0;
});

uploadBtn.addEventListener('click', async () => {
    if (!fileInput.files.length) return;
    
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);
    
    showStatus('uploadStatus', 'Uploading and processing PDF...', 'loading');
    uploadBtn.disabled = true;
    
    try {
        const response = await fetch(`${API_BASE}/upload`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            showStatus('uploadStatus', `Error: ${data.error}`, 'error');
            uploadBtn.disabled = false;
            return;
        }
        
        currentDocId = data.doc_id;
        fileName.textContent = data.filename;
        sentenceCount.textContent = data.num_sentences;
        documentInfo.style.display = 'block';
        
        showStatus('uploadStatus', '✓ PDF uploaded successfully!', 'success');
        
        // Enable QA controls
        summaryBtn.disabled = false;
        questionInput.disabled = false;
        askBtn.disabled = false;
        
        // Clear chat for new document
        chatBox.innerHTML = '';
        currentSessionId = generateSessionId();
        
        // Reset file input
        fileInput.value = '';
        uploadBtn.disabled = true;
        
        setTimeout(() => clearStatus('uploadStatus'), 3000);
    } catch (error) {
        showStatus('uploadStatus', `Error: ${error.message}`, 'error');
        uploadBtn.disabled = false;
    }
});

// Summarization
summaryBtn.addEventListener('click', async () => {
    if (!currentDocId) return;
    
    showStatus('uploadStatus', 'Generating summary...', 'loading');
    summaryBtn.disabled = true;
    
    try {
        const response = await fetch(`${API_BASE}/summarize/${currentDocId}`);
        const data = await response.json();
        
        if (!response.ok) {
            showStatus('uploadStatus', `Error: ${data.error}`, 'error');
            summaryBtn.disabled = false;
            return;
        }
        
        summary.textContent = data.summary;
        summary.classList.add('show');
        
        showStatus('uploadStatus', '✓ Summary generated!', 'success');
        setTimeout(() => clearStatus('uploadStatus'), 3000);
    } catch (error) {
        showStatus('uploadStatus', `Error: ${error.message}`, 'error');
    } finally {
        summaryBtn.disabled = false;
    }
});

// Question answering
askBtn.addEventListener('click', askQuestion);
questionInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !askBtn.disabled) {
        askQuestion();
    }
});

async function askQuestion() {
    const question = questionInput.value.trim();
    
    if (!question || !currentDocId) return;
    
    // Add user message
    addMessage('user', question);
    questionInput.value = '';
    askBtn.disabled = true;
    
    showStatus('qaStatus', 'Finding relevant information...', 'loading');
    
    try {
        const response = await fetch(`${API_BASE}/ask`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                doc_id: currentDocId,
                question: question,
                session_id: currentSessionId
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            addMessage('assistant', `Error: ${data.error}`);
            showStatus('qaStatus', `Error: ${data.error}`, 'error');
            askBtn.disabled = false;
            return;
        }
        
        // Add assistant message
        addMessage('assistant', data.answer);
        
        currentSessionId = data.session_id;
        
        showStatus('qaStatus', '✓ Answer generated!', 'success');
        setTimeout(() => clearStatus('qaStatus'), 3000);
    } catch (error) {
        addMessage('assistant', `Error: ${error.message}`);
        showStatus('qaStatus', `Error: ${error.message}`, 'error');
    } finally {
        askBtn.disabled = false;
        questionInput.focus();
    }
}

// Clear session
clearBtn.addEventListener('click', async () => {
    if (confirm('Clear conversation history? This will start a new session.')) {
        chatBox.innerHTML = '';
        currentSessionId = generateSessionId();
        questionInput.value = '';
        
        try {
            await fetch(`${API_BASE}/clear-session/${currentSessionId}`, {
                method: 'POST'
            });
        } catch (error) {
            console.error('Error clearing session:', error);
        }
    }
});

// Initial state
console.log('NotebookLM initialized');
console.log('Session ID:', currentSessionId);
