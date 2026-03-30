# DoctorSina - Medical AI Chatbot

DoctorSina is an intelligent virtual doctor and a cutting-edge telemedicine backend platform. It uses Retrieval-Augmented Generation (RAG) to answer medical questions based on a provided medical dataset. The project is built with FastAPI, LangChain, Ollama, and ChromaDB.

## Features

- **FastAPI Backend**: Provides a robust, high-performance API endpoint (`/chat`) for frontend applications to communicate with the chatbot.
- **RAG Architecture**: Reads from a medical JSON dataset with symptom patterns and informational responses, embeds the data, and stores it in a vector database for context-aware accurate answers.
- **Chat History Support**: Maintains conversational context by accepting and parsing chat history along with the user's current question.
- **Local Large Language Models**: Runs completely locally using Ollama. Uses `mxbai-embed-large` for vector embeddings and `llama3.2` as the core reasoning engine.
- **CORS Enabled**: Ready to be consumed by any modern frontend web or mobile client.

## Technologies Used

- **Python**
- **FastAPI** & **Uvicorn**
- **Pydantic** (Data validation)
- **LangChain** (`langchain_ollama`, `langchain_chroma`, `langchain_core`)
- **Ollama** (Local LLM `llama3.2` and Embeddings `mxbai-embed-large`)
- **ChromaDB** (Local Vector Store)

## Project Structure

- `app.py`: The FastAPI application file. It defines the `/chat` endpoint, sets up the LangChain prompt template, handles history parsing, and invokes the LLM chain.
- `nhis_vector.py`: Handles data ingestion and ChromaDB vector store creation. It parses intents from `transformed_chatbot_data.json`, creates searchable documents, and provides the retrieval interface for `app.py`.
- `chroma_nhis_db/`: Directory where the Chroma vector store is persistently saved on disk.
- `frontend/`: Directory meant for the frontend interface of the DoctorSina platform.

## Setup and Installation

1. **Install Python Dependencies**
   Ensure you have Python installed, then install the required packages:
   ```bash
   pip install fastapi uvicorn langchain-ollama langchain-chroma langchain-core
   ```

2. **Install and Setup Ollama**
   - Download and install [Ollama](https://ollama.ai/) for your operating system.
   - Pull the required machine learning models by running the following commands in your terminal:
     ```bash
     ollama pull llama3.2
     ollama pull mxbai-embed-large
     ```

3. **Configure Dataset Path**
   - Open `nhis_vector.py`.
   - Update `json_path` on line 8 to point to the actual location of your `transformed_chatbot_data.json` dataset.

## Usage

Start the FastAPI server using Uvicorn:

```bash
uvicorn app:app --reload
```

The server will typically start running on `http://127.0.0.1:8000`. 
On the first run, the vector database will be initialized from the JSON data.

### API Endpoint

**POST `/chat`**

Request Body:
```json
{
  "question": "What are the symptoms of the flu?",
  "history": [
    {
      "role": "user",
      "content": "Hello Doctor"
    },
    {
      "role": "ai",
      "content": "Hello, how can I help you today?"
    }
  ]
}
```

Response:
```json
{
  "reply": "Based on...",
}
```
