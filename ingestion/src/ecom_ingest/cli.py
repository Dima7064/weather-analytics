import logging
import sys

import typer
from rich.console import Console

from ecom_ingest.data_gen import generate_csv_data
from ecom_ingest.db import init_db, load_csv_to_raw

app = typer.Typer(help="E-commerce Analytics Ingestion CLI")
console = Console()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("ecom-ingest")


@app.callback()  # type: ignore[misc]
def main() -> None:
    pass


@app.command()  # type: ignore[misc]
def generate_data() -> None:
    """Генерирует фейковые CSV-файлы в папке data/."""
    console.print("[yellow]Генерация данных...[/yellow]")
    generate_csv_data()
    console.print("[green]Данные успешно сгенерированы в папке data/![/green]")


@app.command()  # type: ignore[misc]
def ingest() -> None:
    """Загружает CSV из папки data/ в базу Postgres."""
    try:
        console.print("[yellow]Инициализация БД...[/yellow]")
        init_db()

        tables = ["customers", "products", "orders"]
        for table in tables:
            path = f"data/{table}.csv"
            load_csv_to_raw(path, table)

        console.print("[bold green]Все данные успешно загружены в Postgres![/bold green]")
    except Exception as e:
        logger.error(f"Ошибка выполнения: {e}", exc_info=True)
        raise typer.Exit(code=1) from e


if __name__ == "__main__":
    app()
