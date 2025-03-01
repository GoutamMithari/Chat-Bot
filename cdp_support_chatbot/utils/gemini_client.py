import google.generativeai as genai

class GeminiClient:
    def __init__(self, api_key):
        """Initialize the Gemini client with the provided API key"""
        # Configure the API key globally
        genai.configure(api_key=api_key)
        # Initialize the model (adjust model name as per availability)
        self.model = genai.GenerativeModel("gemini-1.5-flash")  # Updated to a likely valid model name

    def generate_response(self, user_message, system_context=None):
        """
        Generate a response using the Gemini API
        
        Args:
            user_message (str): The user's query
            system_context (str, optional): System context to prepend to the request
            
        Returns:
            str: The generated response text
        """
        try:
            # Combine system context and user message if context is provided
            if system_context:
                prompt = f"{system_context}\n\n{user_message}"
            else:
                prompt = user_message

            # Generate content using the model
            response = self.model.generate_content(prompt)
            
            return response.text
        except Exception as e:
            print(f"Error generating response: {e}")
            return "I'm having trouble processing your request right now. Please try again later."