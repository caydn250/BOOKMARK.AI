"""
Rule-based summarization module
"""
import nltk
from collections import Counter


def get_important_words(text, top_n=10):
    """
    Get the most important words from text (excluding stopwords).
    
    Args:
        text: Raw text
        top_n: Number of top words to consider
        
    Returns:
        set: Set of important words
    """
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)
    
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('english'))
    
    words = text.lower().split()
    words = [w for w in words if w.isalnum() and w not in stop_words and len(w) > 3]
    
    word_freq = Counter(words)
    important_words = set([word for word, _ in word_freq.most_common(top_n)])
    
    return important_words


def score_sentences(sentences, text):
    """
    Score sentences based on important word frequency.
    
    Args:
        sentences: List of sentences
        text: Full text for context
        
    Returns:
        list: List of (score, sentence) tuples
    """
    important_words = get_important_words(text)
    
    scored_sentences = []
    for s in sentences:
        score = sum(1 for word in important_words if word.lower() in s.lower())
        score += len(s.split()) / 100  # Prefer longer sentences slightly
        scored_sentences.append((score, s))
    
    return scored_sentences


def summarize_document(text, num_sentences=3):
    """
    Generate a rule-based summary of a document.
    
    Args:
        text: Document text
        num_sentences: Number of sentences in summary
        
    Returns:
        str: Summary text
    """
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
    
    sentences = nltk.sent_tokenize(text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
    
    if len(sentences) <= num_sentences:
        return ' '.join(sentences)
    
    # Score and select top sentences
    scored = score_sentences(sentences, text)
    top_sentences = sorted(scored, key=lambda x: x[0], reverse=True)[:num_sentences]
    
    # Sort by original order
    top_sentences = sorted(top_sentences, key=lambda x: sentences.index(x[1]))
    
    summary = ' '.join([s for _, s in top_sentences])
    return summary


def generate_answer(passages, query):
    """
    Generate an answer from retrieved passages.
    
    Args:
        passages: List of relevant passages
        query: User query
        
    Returns:
        str: Generated answer
    """
    if not passages:
        return "I couldn't find relevant information to answer your question."
    
    # Simple answer generation: combine top passages with context
    answer = "Based on the document: " + " ".join(passages)
    
    # Limit length
    if len(answer) > 500:
        answer = answer[:497] + "..."
    
    return answer
