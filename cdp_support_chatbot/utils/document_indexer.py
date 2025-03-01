import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

class DocumentIndexer:
    """Class for indexing and retrieving relevant documentation"""
    
    def __init__(self, cdp_knowledge_base):
        """
        Initialize the document indexer
        
        Args:
            cdp_knowledge_base: An instance of CDPKnowledgeBase containing documentation
        """
        self.cdp_knowledge = cdp_knowledge_base
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.document_vectors = None
        self.documents = []
        
        # Index the documents from all platforms
        self._index_documents()
    
    def _index_documents(self):
        """Build the document index from all CDP platforms"""
        # Collect all documentation chunks
        for platform in self.cdp_knowledge.platforms:
            platform_docs = self.cdp_knowledge.get_documentation(platform)
            # Add platform information to each document chunk
            for doc in platform_docs:
                self.documents.append({
                    'platform': platform,
                    'content': doc,
                    'combined': f"{platform}: {doc}"  # For vector calculation
                })
        
        # Create document vectors
        if self.documents:
            combined_texts = [doc['combined'] for doc in self.documents]
            self.document_vectors = self.vectorizer.fit_transform(combined_texts)
    
    def _preprocess_query(self, query):
        """Preprocess the user query"""
        # Tokenize and remove stopwords
        tokens = word_tokenize(query.lower())
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [w for w in tokens if w not in stop_words]
        return ' '.join(filtered_tokens)
    
    def retrieve_relevant_documents(self, query, top_n=5):
        """
        Retrieve the most relevant documentation for the given query
        
        Args:
            query (str): The user query
            top_n (int): Number of most relevant documents to return
            
        Returns:
            str: A concatenated string of relevant documentation
        """
        if not self.documents or self.document_vectors is None:
            return "Documentation not available."
        
        # Preprocess the query
        processed_query = self._preprocess_query(query)
        
        # Transform the query into the same vector space
        query_vector = self.vectorizer.transform([processed_query])
        
        # Calculate similarities
        similarities = cosine_similarity(query_vector, self.document_vectors).flatten()
        
        # Get indices of top similar documents
        top_indices = np.argsort(similarities)[-top_n:][::-1]
        
        # Extract relevant documentation
        relevant_docs = []
        for idx in top_indices:
            if similarities[idx] > 0.1:  # Threshold to ensure some relevance
                doc = self.documents[idx]
                relevant_docs.append(f"**{doc['platform']}**:\n{doc['content']}\n")
        
        # Join the relevant documentation
        if relevant_docs:
            return "\n".join(relevant_docs)
        else:
            return "No specific documentation found for this query."