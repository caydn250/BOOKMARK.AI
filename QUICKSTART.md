# Quick Start Guide - NotebookLM

## 🚀 Getting Started in 5 Minutes

### Prerequisites
- Python 3.7+
- All dependencies installed

### Step 1: Navigate to Project Directory
```bash
cd c:\Users\Jayant\Desktop\NotebookLM
```

### Step 2: Activate Virtual Environment
```bash
.\venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On macOS/Linux
```

### Step 3: Start the Flask Server
```bash
cd backend
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

### Step 4: Open Web Browser
Navigate to: **http://localhost:5000**

You should see the NotebookLM interface with:
- 📄 Upload & Summarize section on the left
- 💬 Question & Answer section on the right

## 📖 Using the Application

### Upload a PDF
1. Click the upload area or drag-and-drop a PDF
2. Click "Upload PDF"
3. Wait for processing (usually 1-5 seconds)
4. You'll see: "Document Loaded" with file info

**Example**: Use the pre-created test PDF at `data/test_document.pdf`

### Generate Summary
1. Click "Generate Summary"
2. A 3-5 sentence summary appears
3. Summary uses keyword extraction from the document

**Example Output**: "AI has become transformative... Machine learning algorithms enable systems... The global AI market was valued..."

### Ask Questions
1. Type a question in the input field
2. Press Enter or click "Ask"
3. The system retrieves relevant passages and generates an answer

**Example Questions**:
- "What is artificial intelligence?"
- "What are the applications of AI in healthcare?"
- "What is the expected growth rate of AI?"

### Follow-Up Questions
Ask follow-up questions naturally - the system remembers previous context!

**Example**:
- User: "What are the applications of AI in healthcare?"
- Assistant: "AI is used for diagnostic imaging, drug discovery..."
- User: "How accurate are these systems?" (system includes previous answer as context)

### Clear Session
- Click "Clear Session" to reset the conversation history
- Document remains loaded, so you can ask new questions

## 📁 Project Structure

```
NotebookLM/
├── backend/
│   ├── app.py                 # Flask main app
│   ├── pdf_processor.py       # Extract text from PDFs
│   ├── retrieval.py           # BM25 indexing & retrieval
│   └── summarizer.py          # Rule-based summarization
├── frontend/
│   └── static/
│       ├── index.html         # Web interface
│       └── script.js          # Frontend logic
├── data/
│   └── test_document.pdf      # Sample PDF
├── requirements.txt            # Python dependencies
├── README.md                   # Full documentation
└── create_test_pdf.py         # Test PDF generator
```

## 🔧 Key Components Explained

### PDF Processor (`pdf_processor.py`)
- Extracts text from PDF using pdfplumber
- Splits text into sentences using NLTK
- Handles multi-page documents

### Retrieval Engine (`retrieval.py`)
- **BM25 Algorithm**: Advanced TF-IDF ranking
- **Tokenization**: Breaks text into tokens, removes stopwords
- **Indexing**: Creates inverted index for fast retrieval
- **Top-K Retrieval**: Returns 3 most relevant passages

### Summarization (`summarizer.py`)
- **Keyword Extraction**: Identifies important words
- **Sentence Scoring**: Ranks sentences by importance
- **Selection**: Picks top sentences in original order
- **Output**: 3-5 sentence summary

### Flask Backend (`app.py`)
- `POST /api/upload` - Upload and process PDF
- `GET /api/summarize/<doc_id>` - Generate summary
- `POST /api/ask` - Answer questions
- `GET /api/list-documents` - List all documents
- `POST /api/clear-session/<session_id>` - Clear history

### Frontend (`script.js`)
- Drag-and-drop file upload
- Real-time chat interface
- Conversation history management
- API integration with backend

## 💡 Tips & Tricks

### For Better Results:
1. **Upload clear text PDFs** - Scanned images may not extract well
2. **Ask specific questions** - "What is machine learning?" works better than "Tell me everything"
3. **Use follow-ups** - The system is designed for conversational Q&A
4. **Check the summary first** - It gives you an overview of document content

### Troubleshooting:

| Problem | Solution |
|---------|----------|
| "Document not found" | Reload page or upload PDF again |
| Empty responses | PDF may have non-extractable text; try another PDF |
| Port 5000 in use | Stop other Flask apps or change port in `app.py` |
| JavaScript not loading | Check browser console (F12) for errors |
| Slow response | This is normal for large PDFs on first query |

## 🎯 Example Workflow

```
1. Open http://localhost:5000
   ↓
2. Upload test_document.pdf from data/
   ↓
3. Click "Generate Summary"
   Output: "AI has transformed industries... ML enables learning from data..."
   ↓
4. Ask: "What is the AI market size?"
   Output: "The global AI market was valued at $136.55B in 2022..."
   ↓
5. Follow-up: "What is the expected growth rate?"
   Output: "Based on the market size we discussed... CAGR of 38.1% from 2023-2030..."
   ↓
6. Ask: "Name applications in healthcare"
   Output: "Healthcare applications include diagnostic imaging, drug discovery..."
   ↓
7. Click "Clear Session" to reset conversation
```

## 🚀 Next Steps / Enhancements

1. **Try with your own PDFs** - Upload documents from work or research
2. **Test with multiple documents** - Load different PDFs and compare answers
3. **Test edge cases** - Try short questions, ambiguous questions, questions unrelated to document
4. **Review logs** - Check browser console and flask terminal for detailed logs

## ⚙️ Configuration

### Modify Response Behavior:
Edit `backend/summarizer.py` to adjust:
- Number of sentences in summary (line: `num_sentences=5`)
- Number of retrieved passages (line: `top_k=3`)
- Number of important keywords (line: `top_n=10`)

Edit `backend/retrieval.py`:
- Stopwords for tokenization
- Tokenization strategy

## 📞 Support

**For issues or questions:**
1. Check the full README.md for detailed documentation
2. Look at terminal output for error messages
3. Check browser console (F12) for JavaScript errors
4. Review the code comments in Python modules

---

**Happy Question-Answering! 🎉**
