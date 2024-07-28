from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from app.config import EXIT_COMMAND

console = Console()


def row_based_rich_menu(options: list) -> str:

    options.append(EXIT_COMMAND)

    menu_items = []
    for i, option in enumerate(options, 1):
        item = Text.assemble((f"{i}. ", "bold magenta"), (option, "cyan"))
        menu_items.append(item)

    console.print(
        Panel(
            "\n".join(str(item) for item in menu_items),
            title="[bold blue]Main Menu[/bold blue]",
            expand=False,
            border_style="bold green",
        )
    )

    choice = Prompt.ask(
        "[bold yellow]Enter your choice[/bold yellow]",
        choices=[str(i) for i in range(1, len(options) + 1)],
        show_choices=False,
    )

    return options[int(choice) - 1]
