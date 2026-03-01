import httpx
import json
from typing import Optional
from config import config


class LMStudioService:
    
    def __init__(self):
        self.api_url = config.LM_STUDIO_API_URL
        self.model = config.LM_STUDIO_MODEL
        self.client = httpx.Client(timeout=120.0)
    
    def health_check(self) -> bool:
        try:
            response = self.client.get(f"{self.api_url}/models")
            return response.status_code == 200
        except Exception as e:
            print(f"Health check failed: {e}")
            return False
    
    def analyze_document(self, text: str, query: str) -> Optional[str]:
        try:
            prompt = f"""Analyze the following document and answer the query:

DOCUMENT:
{text}

QUERY:
{query}

ANALYSIS:"""
            
            response = self.client.post(
                f"{self.api_url}/chat/completions",
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": "You are a helpful document analysis assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 1024
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                return f"Error: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Error analyzing document: {str(e)}"
    
    def summarize(self, text: str) -> Optional[str]:
        query = "Provide a concise summary of this document in 3-5 sentences."
        return self.analyze_document(text, query)
    
    def extract_key_points(self, text: str) -> Optional[str]:
        query = "Extract and list the main key points from this document."
        return self.analyze_document(text, query)
    
    def __del__(self):
        try:
            self.client.close()
        except:
            pass
