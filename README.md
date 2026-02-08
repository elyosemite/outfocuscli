# OutfocusCLI

[![Python](https://img.shields.io/badge/Python-3.14%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![n8n](https://img.shields.io/badge/n8n-Workflow%20Automation-orange?logo=n8n&logoColor=white)](https://n8n.io/)
[![Typer](https://img.shields.io/badge/Typer-CLI%20Framework-green)](https://typer.tiangolo.com/)
[![Rich](https://img.shields.io/badge/Rich-Terminal%20UI-purple)](https://rich.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

A conversational CLI that connects to [n8n](https://n8n.io/) workflows, providing an interactive REPL experience similar to Gemini CLI, Claude CLI, and Codex.

## Features

- **Interactive REPL** — Start a chat session with your n8n workflow, with persistent conversation context
- **Animated spinner** — Fun, rotating nerd jokes and tech phrases while waiting for responses
- **Single-shot mode** — Send a one-off message via the `chat` command for scripting and pipes
- **List workflows** — View all workflows registered in your n8n instance

## Installation

```bash
poetry install
```

## Configuration

Set the following environment variables:

| Variable | Description | Default |
|---|---|---|
| `N8N_WEBHOOK_URL` | Webhook URL for the chat workflow | `http://localhost:5678/webhook-test/cli-chat` |
| `N8N_API_URL` | n8n REST API base URL | `http://localhost:5678/api/v1` |
| `N8N_API_KEY` | API key for n8n (required for `workflows` command) | — |

## Usage

### Interactive session (REPL)

```bash
poetry run python -m outfocuscli.cli
```

### Single message

```bash
poetry run python -m outfocuscli.cli chat "Hello, how are you?"
```

### List workflows

```bash
poetry run python -m outfocuscli.cli workflows
```
