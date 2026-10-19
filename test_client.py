import requests

BASE_URL = "http://localhost:8000"

def test_workflow():
    # 1. Check health
    health = requests.get(f"{BASE_URL}/health")
    print("Health Check:", health.json())

    # 2. Ingest text
    ingest_payload = {
        "text": "Forward Deployed Engineers build resilient systems that integrate AI into existing customer workflows seamlessly using Docker and PostgreSQL.",
        "metadata": {"source": "portfolio_doc.txt"}
    }
    ingest_res = requests.post(f"{BASE_URL}/ingest", json=ingest_payload)
    print("Ingest Response:", ingest_res.json())

    # 3. Query vector store
    query_payload = {
        "query": "What do Forward Deployed Engineers build?",
        "k": 1
    }
    query_res = requests.post(f"{BASE_URL}/query", json=query_payload)
    print("Query Results:", query_res.json())

if __name__ == "__main__":
    test_workflow()