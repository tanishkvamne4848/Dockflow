import logging
from rich.console import Console
from rich.logging import RichHandler

console = Console()


def setup_logger():
    """Configure rich logging for clean CLI output."""
    root_logger = logging.getLogger()
    if root_logger.handlers:
        return

    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[
            RichHandler(
                console=console,
                rich_tracebacks=True,
                show_time=True,
                show_path=False,
            )
        ],
    )


def log_step(message):
    console.print(f"[bold cyan]▶ {message}[/bold cyan]")


def log_success(message):
    console.print(f"[bold green]✔ {message}[/bold green]")


def log_error(message):
    console.print(f"[bold red]✖ {message}[/bold red]")


def log_warning(message):
    console.print(f"[bold yellow]⚠ {message}[/bold yellow]")


def log_info(message):
    console.print(f"[bold white]{message}[/bold white]")
