import requests
from .config import N8N_WEBHOOK_URL, REQUEST_TIMEOUT

class N8NChatClient:
    def __init__(self, webhook_url: str = N8N_WEBHOOK_URL):
        self.webhook_url = webhook_url
    
    def send_message(
        self,
        text: str,
        conversation_id: str | None = None,
        metadata: dict | None = None,
    ):
        payload = {
            "chatInput": text,
            "metadata": {
                "source": "cli",
                **(metadata or {})
            }
        }

        headers = {
            "Content-Type": "application/json"
        }

        if conversation_id:
            payload["metadata"]["conversation_id"] = conversation_id
        
        response = requests.post(
            self.webhook_url,
            json=payload,
            headers=headers,
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        try:
            data = response.json()
            return {"output": data.get("output", "")}
        except requests.exceptions.JSONDecodeError:
            return {"output": response.text.strip() or "(resposta vazia do n8n)"}