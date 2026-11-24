# Handles all communictaion with the AI model.


import requests, json
from backend.fastapi_app.app.config import settings

class LLMService():
    def __init__(self):
        self.model = settings.OPENAI_MODEL_NAME
        self.endpoint_url = settings.OPENAI_API_URL
        self.headers = {
            "Content-Type": "application/json",
            "X-API-KEY": settings.OPENAI_API_KEY
        }
        self.temperature = 0.4
        self.top_p = 1.0
        self.max_tokens = 800

    def generate_answer(self, prompt: str) -> str:
        print(f"PROMPT LENGTH: {len(prompt)}")
        payload = {
            "model": self.model,
            "messages": [{"role": "system", "content": "You are an expert senior DevOps Engineer"},{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            "top_p": self.top_p,
            "max_tokens": self.max_tokens
        }
        response = requests.post(self.endpoint_url, headers=self.headers, json=payload, timeout=120)
        if not response.ok:
            print("\n" + "=" * 80)
            print("API FAILURE")
            print("=" * 80)
            print("Status Code:", response.status_code)
            print("Response Text:", response.text)
            print("\nPrompt Length:", len(prompt))
            print(prompt[:2000])
            print("\nPayload:")
            print(json.dumps(payload, indent=2)[:3000])
            print("=" * 80)
            response.raise_for_status()
        data = response.json()
        return data['choices'][0]['message']['content']