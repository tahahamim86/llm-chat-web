from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import json

db_location = os.path.join(os.path.dirname(__file__), "chroma_nhis_db")
json_path = r"C:\Users\bough\OneDrive\Desktop\restaurant review with llm and rag\nhis_data\transformed_chatbot_data.json"

add_documents = not os.path.exists(db_location)

embeddings = OllamaEmbeddings(model="mxbai-embed-large")

if add_documents:
    documents = []
    ids = []
    
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    for i, intent in enumerate(data.get("intents", [])):
        tag = intent.get("tag", "")
        patterns = " ".join(intent.get("patterns", []))
        responses = " ".join(intent.get("responses", []))
        
        content = f"Question/Symptom: {patterns}\nResponse/Info: {responses}"
        
        document = Document(
            page_content=content,
            metadata={"tag": tag},
            id=str(i)
        )
        ids.append(str(i))
        documents.append(document)

vector_store = Chroma(
    collection_name="nhis_medical_data",
    persist_directory=db_location,
    embedding_function=embeddings
)

if add_documents:
    print(f"Adding {len(documents)} documents to the vector store...")
    vector_store.add_documents(documents=documents, ids=ids)

retriever = vector_store.as_retriever(search_kwargs={"k": 5})
