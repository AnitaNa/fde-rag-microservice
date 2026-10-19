import os
import sqlalchemy
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

class RAGService:
    def __init__(self):
        self.connection_string = os.getenv("POSTGRES_CONNECTION_STRING")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        # Initialize OpenAI embeddings
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=self.openai_api_key
        )
        
        self._init_vector_extension()
        
        # Initialize PGVector store (removed invalid arguments like use_duplication)
        self.collection_name = "fde_documents"
        self.vector_store = PGVector(
            embeddings=self.embeddings,
            collection_name=self.collection_name,
            connection=self.connection_string,
            use_jsonb=True,
        )

    def _init_vector_extension(self):
        engine = sqlalchemy.create_engine(self.connection_string)
        with engine.begin() as conn:
            conn.execute(sqlalchemy.text("CREATE EXTENSION IF NOT EXISTS vector;"))

    def ingest_text(self, text: str, metadata: dict = None) -> int:
        doc = Document(page_content=text, metadata=metadata or {})
        self.vector_store.add_documents([doc])
        return 1

    def search(self, query: str, k: int = 3):
        results = self.vector_store.similarity_search_with_score(query, k=k)
        formatted_results = []
        for doc, score in results:
            formatted_results.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": float(score)
            })
        return formatted_results