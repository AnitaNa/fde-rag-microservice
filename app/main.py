from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.rag_service import RAGService

app = FastAPI(title="FDE Containerized RAG Microservice", version="1.0.0")

# Initialize RAG service
rag_service = RAGService()

class IngestRequest(BaseModel):
    text: str
    metadata: dict | None = None

class QueryRequest(BaseModel):
    query: str
    k: int | None = 3

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "rag-api"}

@app.post("/ingest")
def ingest_documents(payload: IngestRequest):
    try:
        chunk_count = rag_service.ingest_text(payload.text, payload.metadata)
        return {
            "status": "success", 
            "message": f"Successfully ingested text into {chunk_count} vector chunks."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
def query_vector_store(payload: QueryRequest):
    try:
        results = rag_service.search(payload.query, k=payload.k)
        return {
            "query": payload.query,
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))