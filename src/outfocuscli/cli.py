import typer
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from .client import N8NChatClient

app = typer.Typer(help="CLI conversacional para workflow único do n8n")
console = Console()
client = N8NChatClient()

@app.command()
def chat(
    text: str = typer.Argument(..., help="Texto enviado ao workflow do n8n"),
    conversation_id: str = typer.Option(
        None,
        "--conversation",
        "-c",
        help="ID da conversa (para memória no n8n)",
    ),
):
    """
    Envia texto para o workflow conversacional do n8n
    e imprime a resposta final.
    """

    console.print(
        Panel.fit(
            text,
            title="🧠 Enviando para o n8n",
        )
    )

    try:
        result = client.send_message(
            text=text,
            conversation_id=conversation_id,
        )
    except Exception as e:
        console.print(f"[red]Erro ao chamar o n8n:[/red] {e}")
        raise typer.Exit(code=1)
    
    output = result.get("output", "")
    agent = result.get("agent_used", "desconhecido")
    conv_id = result.get("conversation_id")

    console.print(
        Panel(
            Markdown(output),
            title=f"🤖 Resposta do n8n (agente: {agent})",
        )
    )

    if conv_id:
        console.print(f"[dim]conversation_id:[/dim] {conv_id}")
    
if __name__ == "__main__":
    app()