import collect
import dotenv
import scan
import typer

import init

dotenv.load_dotenv()
app = typer.Typer()
app.add_typer(collect.app, name="collect")
app.add_typer(scan.app, name="scan")
app.add_typer(init.app, name="init")

if __name__ == "__main__":
    app()
