import typer
import scan
import init

app = typer.Typer()
app.add_typer(scan.app, name="scan")
app.add_typer(init.app, name="init")
if __name__ == "__main__":
    app()
