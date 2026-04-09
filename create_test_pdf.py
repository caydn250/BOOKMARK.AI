"""
Test PDF generator for NotebookLM testing
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from pathlib import Path

def create_test_pdf():
    """Create a sample PDF for testing the QA system."""
    
    pdf_path = Path(__file__).parent / "data" / "test_document.pdf"
    pdf_path.parent.mkdir(exist_ok=True)
    
    # Create PDF document
    doc = SimpleDocTemplate(str(pdf_path), pagesize=letter)
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor='#1f4788',
        spaceAfter=30,
        alignment=1
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        alignment=4,
        spaceAfter=12,
        leading=16
    )
    
    # Content
    content = []
    
    content.append(Paragraph("Artificial Intelligence in Modern Business", title_style))
    content.append(Spacer(1, 20))
    
    paragraphs = [
        "Artificial Intelligence (AI) has become one of the most transformative technologies of the 21st century. From healthcare to finance, AI is revolutionizing how businesses operate and serve their customers. Machine learning algorithms, a subset of AI, enable systems to learn from data without being explicitly programmed.",
        
        "The global AI market was valued at approximately $136.55 billion in 2022 and is expected to grow at a compound annual growth rate (CAGR) of 38.1% from 2023 to 2030. This rapid growth is driven by increased adoption across various industries including retail, healthcare, finance, and manufacturing.",
        
        "One of the key applications of AI is in customer service. Companies are increasingly using AI-powered chatbots to handle customer inquiries 24/7. These systems can understand natural language, provide instant responses, and escalate complex issues to human agents when necessary. This has resulted in improved customer satisfaction and reduced operational costs.",
        
        "In the healthcare industry, AI is being used for diagnostic imaging, drug discovery, and personalized treatment plans. Machine learning models can analyze medical images with accuracy comparable to or exceeding that of experienced radiologists. This allows for earlier detection of diseases like cancer and other critical conditions.",
        
        "Natural Language Processing (NLP), another important AI technology, enables computers to understand and generate human language. This technology powers translation services, sentiment analysis, and text summarization tools. NLP is crucial for building more intuitive and user-friendly interfaces.",
        
        "Data security is a major concern when implementing AI systems. Organizations must ensure that sensitive data used for training AI models is protected from unauthorized access. Privacy-preserving machine learning techniques are being developed to address these concerns while maintaining model effectiveness.",
        
        "The future of AI looks promising with emerging technologies like quantum computing and edge AI. Quantum computing could solve complex optimization problems much faster than classical computers, while edge AI brings computational power closer to data sources for real-time processing.",
        
        "However, the widespread adoption of AI also raises ethical questions about bias in algorithms, job displacement, and the need for regulatory frameworks. Responsible AI development requires collaboration between technologists, policymakers, and ethicists to ensure AI benefits society as a whole.",
        
        "In conclusion, Artificial Intelligence continues to reshape industries and create new opportunities for businesses. Organizations that successfully integrate AI into their operations will likely gain competitive advantages in their respective markets. As AI technology continues to evolve, staying informed about its capabilities and limitations will be crucial for business leaders.",
    ]
    
    for para in paragraphs:
        content.append(Paragraph(para, body_style))
        content.append(Spacer(1, 12))
    
    # Build PDF
    doc.build(content)
    print(f"✓ Test PDF created: {pdf_path}")
    return str(pdf_path)

if __name__ == "__main__":
    create_test_pdf()
