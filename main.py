from fastapi import FastAPI
import chromadb
import ollama
import os

app = FastAPI()
chroma = chromadb.PersistentClient(path="./db")
collection = chroma.get_or_create_collection("docs")

# ----- api running in docker container + ollama runing local
# ollama_client = ollama.Client(host="http://host.docker.internal:11434")

# ----- api running in k8s + ollama runing local
# ollama_client = ollama.Client(host="http://host.kubernetes.internal:11434")
# ollama_client = ollama.Client(host="http://host.minikube.internal:11434")

# ------ api + ollama both running local (below 2 works)
ollama_client = ollama.Client()
# ollama_client = ollama.Client(host="http://localhost:11434")


@app.get('/')
def main():
    return "Hello from rag-api!"


@app.post("/query")
def query(q: str):
    results = collection.query(query_texts=[q], n_results=1)
    context = results["documents"][0][0] if results["documents"] else ""

    # Check if mock mode is enabled
    use_mock = os.getenv("USE_MOCK_LLM", "0") == "1"
    # print(f'use_mock..................: {use_mock}')    
    
    if use_mock:
        # Return retrieved context directly (deterministic!)
        return {"answer": context}
    else:
        # Use real LLM (production mode)
        answer = ollama_client.generate(model="tinyllama", prompt=f"Context:\n{context}\n\nQuestion: {q}\n\nAnswer clearly and concisely:")

        return {"answer": answer["response"]}    
