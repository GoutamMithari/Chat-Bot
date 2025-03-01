# CDP Support Chatbot

A Flask-based chatbot application that answers "how-to" questions related to Customer Data Platforms (CDPs): Segment, mParticle, Lytics, and Zeotap.

## Features

- Answers "how-to" questions about CDP platforms
- Extracts relevant information from official documentation
- Handles variations in question phrasing
- Provides cross-CDP comparisons
- Supports advanced platform-specific questions
- User-friendly chat interface

## Supported CDPs

- [Segment](https://segment.com/docs/?ref=nav)
- [mParticle](https://docs.mparticle.com/)
- [Lytics](https://docs.lytics.com/)
- [Zeotap](https://docs.zeotap.com/home/en-us/)

## Technologies Used

- **Backend**: Flask, Google Generative AI (Gemini)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **NLP**: NLTK, scikit-learn for document indexing and retrieval
- **Documentation Processing**: BeautifulSoup for document scraping

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/cdp-support-chatbot.git
   cd cdp-support-chatbot
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   FLASK_ENV=development
   FLASK_DEBUG=1
   ```

## Usage

1. Start the Flask server:
   ```
   python app.py
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

3. Start asking questions about the supported CDP platforms!

## Example Questions

- "How do I set up a new source in Segment?"
- "How can I create a user profile in mParticle?"
- "How do I build an audience segment in Lytics?"
- "How can I integrate my data with Zeotap?"
- "How does Segment's audience creation process compare to Lytics'?"

## Project Structure

```
cdp_support_chatbot/
├── .env                     # Environment variables
├── app.py                   # Main Flask application
├── requirements.txt         # Dependencies
├── README.md                # Project documentation
├── config.py                # Configuration settings
├── static/                  # Static files
│   ├── css/
│   │   └── style.css        # Custom styling
│   ├── js/
│   │   └── script.js        # Frontend JavaScript
│   └── img/
│       └── logo.png         # Company logo
├── templates/               # HTML templates
│   ├── index.html           # Main chat interface
│   └── layout.html          # Base template
└── utils/                   # Utility modules
    ├── __init__.py
    ├── gemini_client.py     # Gemini API wrapper
    ├── document_indexer.py  # Document indexing utilities
    └── cdp_knowledge.py     # CDP documentation knowledge base
```

## Extending the Chatbot

To add support for more CDP platforms:

1. Add the platform and documentation URL to the `platforms` and `doc_urls` in `cdp_knowledge.py`.
2. Update the placeholder documentation or implement the document scraping functionality.
3. Add relevant keywords to the `cdp_keywords` list to improve detection of platform-related questions.

## License

MIT

---

## Notes

This project was developed as an assignment to demonstrate a support agent chatbot for Customer Data Platforms.