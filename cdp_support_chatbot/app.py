import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from utils.gemini_client import GeminiClient
from utils.document_indexer import DocumentIndexer
from utils.cdp_knowledge import CDPKnowledgeBase

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Load API key from environment variable
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set. Please set it in your .env file or system environment.")

# Initialize Gemini client
gemini_client = GeminiClient(api_key=api_key)

# Initialize the document indexer with CDP documentation
cdp_knowledge = CDPKnowledgeBase()
document_indexer = DocumentIndexer(cdp_knowledge)

@app.route('/')
def index():
    """Render the main chat interface"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Process chat requests and generate responses"""
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    # Check if the question is CDP-related
    if cdp_knowledge.is_cdp_related(user_message):
        # Get relevant documentation snippets
        relevant_docs = document_indexer.retrieve_relevant_documents(user_message)
        
        # Build context-enriched prompt
        system_context = f"""You are a helpful Customer Data Platform (CDP) support agent. 
        Answer the user's question about {', '.join(cdp_knowledge.platforms)} based on the following documentation:
        
        {relevant_docs}
        
        If the question asks for a comparison between CDPs, highlight the key differences.
        If you don't know the answer, say so honestly and suggest where they might find more information.
        Your response should be clear, concise, and directly address the user's question.
        Format your response with markdown to improve readability when appropriate.
        """
        
        # Generate response with Gemini
        response_text = gemini_client.generate_response(
            user_message, 
            system_context=system_context
        )
    else:
        # For non-CDP related questions
        response_text = "I'm a CDP support agent focused on Segment, mParticle, Lytics, and Zeotap. I can help with questions about these platforms. Is there something specific about these CDPs you'd like to know?"
    
    return jsonify({
        'response': response_text,
        'source': 'gemini'
    })

if __name__ == '__main__':
    app.run(debug=True)