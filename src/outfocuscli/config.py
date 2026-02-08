import os

N8N_WEBHOOK_URL = os.getenv(
    "N8N_WEBHOOK_URL",
    "http://localhost:5678/webhook-test/cli-chat"
)

REQUEST_TIMEOUT = 120