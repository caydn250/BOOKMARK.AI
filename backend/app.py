"""
Main Flask application for Document QA system
"""
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
import json
from pathlib import Path
from datetime import datetime
import uuid

from pdf_processor import extract_text_from_pdf, extract_sentences
from retrieval import create_bm25_index, retrieve_relevant_passages
from summarizer import summarize_document, generate_answer

# Setup paths
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR / 'frontend' / 'templates'
STATIC_DIR = BASE_DIR / 'frontend' / 'static'

app = Flask(__name__, static_folder=str(STATIC_DIR), static_url_path='/static')
CORS(app)

# Configuration
UPLOAD_FOLDER = Path(__file__).parent.parent / 'data'
UPLOAD_FOLDER.mkdir(exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# In-memory storage for documents and conversation history
documents_store = {}  # {doc_id: {text, sentences, bm25, filename}}
conversation_history = {}  # {session_id: [{role, content}]}


@app.route('/')
def index():
    """Serve the frontend."""
    return send_from_directory(STATIC_DIR, 'index.html')


@app.route('/api/upload', methods=['POST'])
def upload_pdf():
    """Handle PDF upload and processing."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.endswith('.pdf'):
        return jsonify({'error': 'Only PDF files are allowed'}), 400
    
    try:
        # Save file temporarily
        doc_id = str(uuid.uuid4())
        file_path = app.config['UPLOAD_FOLDER'] / file.filename
        file.save(file_path)
        
        # Extract text from PDF
        text = extract_text_from_pdf(file_path)
        
        if not text.strip():
            return jsonify({'error': 'Could not extract text from PDF'}), 400
        
        # Extract sentences
        sentences = extract_sentences(text)
        
        # Create BM25 index
        bm25, _ = create_bm25_index(sentences)
        
        # Store in memory
        documents_store[doc_id] = {
            'text': text,
            'sentences': sentences,
            'bm25': bm25,
            'filename': file.filename,
            'upload_time': datetime.now().isoformat()
        }
        
        # Clean up uploaded file
        file_path.unlink()
        
        return jsonify({
            'status': 'success',
            'doc_id': doc_id,
            'filename': file.filename,
            'num_sentences': len(sentences)
        }), 200
    
    except Exception as e:
        print(f"Error uploading file: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/summarize/<doc_id>', methods=['GET'])
def summarize(doc_id):
    """Generate a summary of the uploaded document."""
    if doc_id not in documents_store:
        return jsonify({'error': 'Document not found'}), 404
    
    try:
        doc = documents_store[doc_id]
        summary = summarize_document(doc['text'], num_sentences=5)
        
        return jsonify({
            'status': 'success',
            'summary': summary,
            'doc_id': doc_id
        }), 200
    
    except Exception as e:
        print(f"Error summarizing: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/ask', methods=['POST'])
def ask_question():
    """Answer a question about the document."""
    data = request.json
    doc_id = data.get('doc_id')
    question = data.get('question', '').strip()
    session_id = data.get('session_id', str(uuid.uuid4()))
    
    if not doc_id or not question:
        return jsonify({'error': 'Missing doc_id or question'}), 400
    
    if doc_id not in documents_store:
        return jsonify({'error': 'Document not found'}), 404
    
    try:
        doc = documents_store[doc_id]
        
        # Initialize session if needed
        if session_id not in conversation_history:
            conversation_history[session_id] = []
        
        # Build augmented query with conversation context
        augmented_query = question
        if conversation_history[session_id]:
            # Get last answer for context
            last_exchanges = conversation_history[session_id][-2:]
            context = " ".join([exc.get('content', '') for exc in last_exchanges])
            augmented_query = f"{context} {question}"
        
        # Retrieve relevant passages
        passages = retrieve_relevant_passages(
            augmented_query,
            doc['bm25'],
            doc['sentences'],
            top_k=3
        )
        
        # Generate answer
        answer = generate_answer(passages, question)
        
        # Store in conversation history
        conversation_history[session_id].append({
            'role': 'user',
            'content': question,
            'timestamp': datetime.now().isoformat()
        })
        conversation_history[session_id].append({
            'role': 'assistant',
            'content': answer,
            'timestamp': datetime.now().isoformat()
        })
        
        return jsonify({
            'status': 'success',
            'answer': answer,
            'session_id': session_id,
            'doc_id': doc_id,
            'passages_used': passages[:2]  # Return top 2 passages for reference
        }), 200
    
    except Exception as e:
        print(f"Error answering question: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/list-documents', methods=['GET'])
def list_documents():
    """List all uploaded documents."""
    docs = [
        {
            'doc_id': doc_id,
            'filename': doc['filename'],
            'upload_time': doc['upload_time'],
            'num_sentences': len(doc['sentences'])
        }
        for doc_id, doc in documents_store.items()
    ]
    return jsonify({'documents': docs}), 200


@app.route('/api/clear-session/<session_id>', methods=['POST'])
def clear_session(session_id):
    """Clear conversation history for a session."""
    if session_id in conversation_history:
        del conversation_history[session_id]
    return jsonify({'status': 'success'}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
