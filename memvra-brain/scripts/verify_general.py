import requests
import json

API_URL = "http://localhost:8000/v1/logical/stream"

def test_general_knowledge():
    query = "Why is the sky blue?"
    print(f"Query: {query}")
    
    try:
        response = requests.post(
            API_URL,
            params={"query": query, "user_id": "test_user"},
            stream=True
        )
        response.raise_for_status()
        
        print("Response:", end=" ")
        for chunk in response.iter_content(chunk_size=None):
            if chunk:
                text = chunk.decode('utf-8')
                # Skip metadata
                if text.strip().startswith('{'):
                    continue
                print(text, end="", flush=True)
        print("\n")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_general_knowledge()
