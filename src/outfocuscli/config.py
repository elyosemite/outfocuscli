import os

N8N_WEBHOOK_URL = os.getenv(
    "N8N_WEBHOOK_URL",
    "http://localhost:5678/webhook-test/cli-chat"
)

N8N_API_URL = os.getenv(
    "N8N_API_URL",
    "http://localhost:5678/api/v1"
)

N8N_API_KEY = os.getenv("N8N_API_KEY", "")

REQUEST_TIMEOUT = 120