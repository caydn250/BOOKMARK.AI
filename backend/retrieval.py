"""
BM25-based document retrieval module
"""
from rank_bm25 import BM25Okapi
import nltk


def preprocess_text(text):
    """
    Preprocess text for BM25 indexing.
    
    Args:
        text: Raw text
        
    Returns:
        list: List of preprocessed tokens
    """
    # Simple tokenization and lowercasing
    tokens = text.lower().split()
    # Remove common stopwords manually or with NLTK
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)
    
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [t for t in tokens if t.isalnum() and t not in stop_words]
    return tokens


def create_bm25_index(sentences):
    """
    Create a BM25 index from sentences.
    
    Args:
        sentences: List of sentences
        
    Returns:
        tuple: (BM25Okapi object, list of sentences)
    """
    # Tokenize sentences
    tokenized_sentences = [preprocess_text(s) for s in sentences]
    
    # Create BM25 index
    bm25 = BM25Okapi(tokenized_sentences)
    
    return bm25, sentences


def retrieve_relevant_passages(query, bm25, sentences, top_k=3):
    """
    Retrieve top-k relevant passages for a query using BM25.
    
    Args:
        query: User query
        bm25: BM25Okapi object
        sentences: List of sentences
        top_k: Number of top passages to retrieve
        
    Returns:
        list: List of relevant sentences
    """
    query_tokens = preprocess_text(query)
    
    if not query_tokens:
        return []
    
    # Get BM25 scores
    scores = bm25.get_scores(query_tokens)
    
    # Get indices of top-k sentences
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
    
    # Sort by original position to maintain document flow
    top_indices = sorted(top_indices)
    
    # Return relevant sentences
    relevant = [sentences[i] for i in top_indices]
    return relevant
