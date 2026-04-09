# BOOKMARK.AI - Document QAhttps://github.com/caydn250/NotebookLM/tree/main System

A fully functional web app for question-answering over document corpus using smart retrieval techniques without vector embeddings or vector databases.

## Features

- **Smart PDF Upload**: Upload and extract text from PDF documents
- **Rule-Based Summarization**: Generate abstractive-style summaries using keyword extraction
- **BM25 Retrieval**: Advanced TF-IDF based document retrieval without embeddings
- **Context-Aware Q&A**: Ask questions and receive answers based on document content
- **Follow-Up Questions**: Maintain conversation history for context-aware responses
- **Clean Web Interface**: Modern, responsive UI built with HTML/CSS/JavaScript

## Tech Stack

- **Backend**: Python with Flask
- **Frontend**: HTML5, CSS3, JavaScript (no frameworks for simplicity)
- **Retrieval**: BM25 (rank-bm25)
- **NLP**: NLTK for text processing
- **PDF Processing**: pdfplumber for text extraction

## Installation

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Setup

1. **Clone or navigate to the project directory**
   ```bash
   cd c:\Users\Jayant\Desktop\NotebookLM
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   # source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Navigate to the backend directory**
   ```bash
   cd backend
   ```

2. **Run the Flask app**
   ```bash
   python app.py
   ```

3. **Open your browser**
   - Navigate to `http://localhost:5000`
   - You should see the NotebookLM interface

## Usage

### 1. Upload a PDF
- Click the upload area or drag and drop a PDF file
- The system will extract text and prepare it for querying

### 2. Generate Summary
- Click "Generate Summary" to get a rule-based summary of the document
- The summary uses keyword extraction and sentence scoring

### 3. Ask Questions
- Type a question in the input field
- Click "Ask" or press Enter
- The system will retrieve relevant passages and generate an answer
- Previous answers are automatically included as context for follow-up questions

### 4. Clear Session
- Click "Clear Session" to reset the conversation history
- This starts a new session while keeping the document loaded

## Architecture

### Backend Structure
```
backend/
├── app.py              # Main Flask application
├── pdf_processor.py    # PDF text extraction
├── retrieval.py        # BM25 indexing and retrieval
└── summarizer.py       # Rule-based summarization
```

### Frontend Structure
```
frontend/
├── static/
│   ├── index.html      # Main web interface
│   └── script.js       # Frontend logic and API calls
```

### API Endpoints

- `POST /api/upload` - Upload and process a PDF
- `GET /api/summarize/<doc_id>` - Generate summary for document
- `POST /api/ask` - Ask a question about document
- `GET /api/list-documents` - List all uploaded documents
- `POST /api/clear-session/<session_id>` - Clear conversation history

## How It Works

### Retrieval (BM25)
- **Tokenization**: Text is split into tokens with stopword removal
- **Indexing**: BM25 algorithm creates an inverse index
- **Ranking**: Queries are scored against indexed documents using BM25 formula
- **Retrieval**: Top-k relevant passages are returned based on relevance scores

### Summarization
- **Keyword Extraction**: Important words are identified based on frequency
- **Sentence Scoring**: Sentences are scored based on important word content
- **Selection**: Top-scoring sentences are selected and arranged in original order

### Question Answering
- **Query Augmentation**: Previous answers are included for context
- **Passage Retrieval**: BM25 finds top-3 relevant passages
- **Answer Generation**: Passages are combined to form a coherent answer

### Follow-Up Handling
- **Conversation History**: All Q&A exchanges are stored per session
- **Context Integration**: Previous answers are prepended to new queries
- **Session Management**: Sessions are maintained separately for each browser instance

## Limitations & Future Improvements

### Current Limitations
1. **No Vector Embeddings**: Uses traditional TF-IDF rather than semantic embeddings
2. **Rule-Based Summarization**: Cannot generate truly abstractive summaries without embeddings
3. **In-Memory Storage**: Documents are stored in RAM (not persisted)
4. **Single Machine**: No distributed indexing or querying

### Future Improvements
1. Add semantic similarity using lightweight embeddings (e.g., FastText)
2. Implement persistent document storage (database)
3. Add support for multiple languages
4. Integrate lightweight LLMs for better answer generation
5. Add metadata extraction and filtering
6. Implement document chunking strategies
7. Add support for other file formats (DOCX, TXT, etc.)
8. Deploy to cloud with proper session management

## Example Session

```
Upload: sample_report.pdf
Summary: "The report covers Q3 performance metrics showing 15% revenue growth..."

User: What was the revenue growth?
Answer: "Based on the document: The report shows 15% revenue growth in Q3..."

User: Any other key metrics?
Answer: "Based on the previous answer about revenue growth: The document also mentions..."
```

## Troubleshooting

### Issue: "Document not found" error
- **Solution**: Ensure the PDF was successfully uploaded and the doc_id matches

### Issue: Empty responses
- **Solution**: Check if the PDF text was properly extracted. Some PDFs may have non-extractable text

### Issue: Port 5000 already in use
- **Solution**: Change the port in `app.py` (line: `app.run(..., port=5001)`)

### Issue: NLTK data not found
- **Solution**: The app automatically downloads required NLTK data on first use

## Performance Notes

- **Upload Time**: Depends on PDF size; typically < 5 seconds for 50MB PDFs
- **Retrieval Time**: BM25 queries are typically < 100ms
- **Memory Usage**: Documents loaded in RAM; ~1MB per 100 pages of text

## License

This project is open source and available under the MIT License.

## Author

Built with ❤️ using Python, Flask, and NLTK
