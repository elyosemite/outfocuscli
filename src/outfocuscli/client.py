import requests
from .config import N8N_WEBHOOK_URL, N8N_API_URL, N8N_API_KEY, REQUEST_TIMEOUT

class N8NChatClient:
    def __init__(self, webhook_url: str = N8N_WEBHOOK_URL, api_url: str = N8N_API_URL, api_key: str = N8N_API_KEY):
        self.webhook_url = webhook_url
        self.api_url = api_url
        self.api_key = api_key
    
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
            return {
                "output": data.get("output", ""),
                "conversation_id": data.get("conversation_id"),
                "agent_used": data.get("agent_used"),
            }
        except requests.exceptions.JSONDecodeError:
            return {"output": response.text.strip() or "(resposta vazia do n8n)"}

    def list_workflows(self) -> list[dict]:
        response = requests.get(
            f"{self.api_url}/workflows",
            headers={"X-N8N-API-KEY": self.api_key},
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("data", [])