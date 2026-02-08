import typer
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from .client import N8NChatClient
from .repl import start_repl

app = typer.Typer(
    help="CLI conversacional para workflow unico do n8n",
    invoke_without_command=True,
)
console = Console()
client = N8NChatClient()


@app.callback()
def main(
    ctx: typer.Context,
    conversation_id: str = typer.Option(
        None,
        "--conversation",
        "-c",
        help="ID da conversa (para memoria no n8n)",
    ),
):
    """
    OutfocusCLI - Interface conversacional para n8n.
    Sem subcomando, inicia uma sessao interativa (REPL).
    """
    if ctx.invoked_subcommand is None:
        start_repl(conversation_id=conversation_id)


@app.command()
def chat(
    text: str = typer.Argument(..., help="Texto enviado ao workflow do n8n"),
    conversation_id: str = typer.Option(
        None,
        "--conversation",
        "-c",
        help="ID da conversa (para memoria no n8n)",
    ),
):
    """
    Envia uma unica mensagem ao n8n (modo nao-interativo).
    """
    console.print(Panel.fit(text, title="Enviando para o n8n"))

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
        Panel(Markdown(output), title=f"Resposta do n8n (agente: {agent})")
    )

    if conv_id:
        console.print(f"[dim]conversation_id:[/dim] {conv_id}")


@app.command()
def workflows():
    """
    Lista todos os workflows cadastrados no n8n.
    """
    try:
        wfs = client.list_workflows()
    except Exception as e:
        console.print(f"[red]Erro ao listar workflows:[/red] {e}")
        raise typer.Exit(code=1)

    if not wfs:
        console.print("[yellow]Nenhum workflow encontrado.[/yellow]")
        raise typer.Exit()

    from rich.table import Table

    table = Table(title="Workflows do n8n")
    table.add_column("ID", style="dim")
    table.add_column("Nome", style="bold")
    table.add_column("Ativo", justify="center")

    for wf in wfs:
        active = "[green]Sim[/green]" if wf.get("active") else "[red]Nao[/red]"
        table.add_row(str(wf.get("id", "")), wf.get("name", ""), active)

    console.print(table)


if __name__ == "__main__":
    app()
