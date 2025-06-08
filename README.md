# Intuitive Chatbot Backend 

This README provides an overview of the backend components for the Intuitive API, including setup instructions, configuration, and detailed descriptions of each module.

## Installation 
1. Clone the repo
```bash
git clone https://github.com/intuitivechatbot/intuitive_api.git
cd intuitive_api
```
2. Create a virtual environment and install dependencies:
```bash
pip install -r requirements.txt
```
## Configuration
Create a `.env` file in the project root with the following variables:
```txt
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=https://your-qdrant-instance
QDRANT_API_KEY=your_qdrant_api_key
```

## Project Strucure
```txt
intuitive_api/
├── app/
│   ├── app.py
│   ├── llm_chain.py
│   ├── query_engine.py
│   ├── retriever.py
│   └── config.py
├── Procfile
├── requirements.txt
└── runtime.txt
```
## File Descriptions
1. app.py
- Purpose: Entry point for the Flask API. Defines the /ask endpoin
- Key Functions: ask(): Handles POST /ask, validates input JSON (input, session_id), invokes the query engine, and returns an answer or error.
- Usage: 
```bash
flask run  # development
gunicorn app.app:app  # production
```
2. llm_chain.py
- Purpose: Configures and manages the memory-aware LangChain LLMChain for conversation handling.

- Key Components: 
create_chain(model_name): Builds a chain with a system prompt, retrieval context, and conversation memory.
get_chain(session_id): Returns a cached chain per session to preserve memory.

- Environment Variables: Reads OPENAI_API_KEY from .env.

3. query_engine.py
- Purpose: Orchestrates semantic retrieval and LLM response generation.

- Key Function:
ask_query(user_input, session_id): Retrieves relevant documents, builds context, and invokes the chain to generate the final answer.
Falls back to GPT-only responses if no vector results are found

4. retriever.py
- Purpose: Initializes and returns a Qdrant-based retriever for semantic search.
- Key Components:
get_retriever(): Creates a QdrantClient, sets up OpenAIEmbeddings, and returns a retriever with k=3 results.
- Environment Variables: Uses QDRANT_URL, QDRANT_API_KEY, and OPENAI_API_KEY.

5. config.py
- Purpose: Central location for configuration constants and settings.

6. Procfile
- Purpose: use this in render/heroku for deployment
- Content:
```Procfile
web: gunicorn app.app:app
```
7. requirments.txt
- Purpose: list all packages required to ru API
8. runtime.txt
- Purpose: Specifies the Python runtime version for deployment platforms.

## Usage
1. Set environment variables (either via .env or your deployment platform)
2. Start the API:
- Development: `FLASK_APP=app.app flask run --port 5000`
- Production: `gunicorn app.app:app --bind 0.0.0.0:$PORT`
3. Call API
- Postman and call `url/ask`





