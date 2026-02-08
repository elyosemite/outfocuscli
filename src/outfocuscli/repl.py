import uuid
import threading

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from .client import N8NChatClient
from .spinner_messages import get_random_message

console = Console()

EXIT_COMMANDS = {"exit", "quit", "sair", "q"}
SPINNER_INTERVAL = 2.5


def _print_welcome_banner(conversation_id: str) -> None:
    banner_text = (
        "[bold green]OutfocusCLI[/bold green] - Sessao Interativa\n\n"
        f"[dim]Sessao:[/dim] {conversation_id}\n"
        "[dim]Comandos:[/dim] digite [bold]exit[/bold], [bold]quit[/bold], "
        "[bold]sair[/bold] ou pressione [bold]Ctrl+C[/bold] para sair"
    )
    console.print(Panel(banner_text, title=">> Outfocus <<", border_style="green"))
    console.print()


def _send_with_spinner(client: N8NChatClient, text: str, conversation_id: str) -> dict:
    result = {}
    error = None
    finished = threading.Event()

    def _do_request():
        nonlocal result, error
        try:
            result = client.send_message(text=text, conversation_id=conversation_id)
        except Exception as e:
            error = e
        finally:
            finished.set()

    thread = threading.Thread(target=_do_request, daemon=True)
    thread.start()

    try:
        with console.status(get_random_message(), spinner="dots") as status:
            while not finished.is_set():
                finished.wait(timeout=SPINNER_INTERVAL)
                if not finished.is_set():
                    status.update(get_random_message())
    except KeyboardInterrupt:
        console.print("\n[yellow]Requisicao cancelada.[/yellow]")
        raise

    if error:
        raise error

    return result


def start_repl(conversation_id: str | None = None) -> None:
    if conversation_id is None:
        conversation_id = uuid.uuid4().hex[:12]

    client = N8NChatClient()
    _print_welcome_banner(conversation_id)

    while True:
        try:
            user_input = console.input("[bold blue]voce >[/bold blue] ")
        except (KeyboardInterrupt, EOFError):
            console.print("\n[green]Ate mais![/green]")
            break

        user_input = user_input.strip()

        if not user_input:
            continue

        if user_input.lower() in EXIT_COMMANDS:
            console.print("[green]Ate mais![/green]")
            break

        try:
            result = _send_with_spinner(client, user_input, conversation_id)
        except KeyboardInterrupt:
            continue
        except Exception as e:
            console.print(f"[red]Erro ao chamar o n8n:[/red] {e}")
            continue

        output = result.get("output", "")
        agent = result.get("agent_used")

        title = "Outfocus"
        if agent:
            title += f" (agente: {agent})"

        console.print(Panel(Markdown(output), title=title, border_style="cyan"))
        console.print()

        server_conv_id = result.get("conversation_id")
        if server_conv_id:
            conversation_id = server_conv_id
