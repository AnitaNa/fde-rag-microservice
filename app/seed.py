import os
from app.rag_service import RAGService

INITIAL_DOCUMENTS = [
    {
        "text": "Forward Deployed Engineers bridge the gap between complex AI systems and real-world client infrastructure, ensuring seamless integration, robust containerization, and reliable database performance using technologies like Docker, PostgreSQL, and LangChain.",
        "metadata": {"source": "fde_handbook.txt", "category": "overview"}
    },
    {
        "text": "Containerization with Docker Compose allows multi-container microservices to manage dependencies using health checks, ensuring the database is fully healthy and ready before the FastAPI backend boots up.",
        "metadata": {"source": "infrastructure_guide.md", "category": "devops"}
    },
    {
        "text": "PostgreSQL with the pgvector extension enables high-performance vector similarity search directly within a relational database, supporting efficient embedding storage and retrieval for RAG applications.",
        "metadata": {"source": "database_specs.pdf", "category": "database"}
    }
]

def seed_database():
    print("🌱 Starting database seeding...")
    rag = RAGService()
    
    for doc in INITIAL_DOCUMENTS:
        try:
            rag.ingest_text(doc["text"], doc["metadata"])
            print(f" Ingested: {doc['metadata']['source']}")
        except Exception as e:
            print(f" Failed to ingest {doc['metadata']['source']}: {e}")
            
    print("✨ Seeding complete! Your RAG store is ready.")

if __name__ == "__main__":
    seed_database()