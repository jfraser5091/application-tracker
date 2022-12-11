from pathlib import Path
from typing import Optional, List
import typer
from src import __app_name__, __version__, ERRORS, config, database, tracker

# Initialise application
app = typer.Typer()


@app.command()
def init(
        db_path: str = typer.Option(
            str(database.DEFAULT_DB_FILE_PATH),
            "--db-path",
            "-db",
            prompt="application tracker database location"
        )
) -> None:
    """
    This function initialises the database.
    """
    app_init_error = config.init_app(db_path)
    if app_init_error:
        typer.secho(
            f'Creating config file failed with "{ERRORS[app_init_error]}"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    db_init_error = database.init_database(Path(db_path))
    if db_init_error:
        typer.secho(
            f'Creating database failed with "{ERRORS[db_init_error]}"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f'The database is located in {db_path}',
            fg=typer.colors.GREEN
        )


def get_applier() -> tracker.Applier:
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
    else:
        typer.secho(
            'Config file not found. Please run "src.init".',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    if db_path.exists():
        return tracker.Applier(db_path)
    else:
        typer.secho(
            'Database not found. Please run "src.init".',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)


@app.command(name="add")
def add(
        title: str,
        description: List[str] = typer.Argument(...)
) -> None:
    """
    This function adds a new application to the list.
    """
    applier = get_applier()
    application, error = applier.add(title, description)
    if error:
        typer.secho(
            f'Adding application failed with {ERRORS[error]}',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            'Application added to list.',
            fg=typer.colors.GREEN
        )


@app.command(name='remove')
def remove(
        app_id: int = typer.Argument(...),
        force: bool = typer.Option(
            False,
            "--force",
            "-f",
            help="Force deletion without confirmation."
        )
) -> None:
    applier = get_applier()

    def _remove():
        application, error = applier.remove(app_id)
        if error:
            typer.secho(
                f'Removing application #{app_id} failed with {ERRORS[error]}',
                fg=typer.colors.RED
            )
            raise typer.Exit(1)
        else:
            typer.secho(
                f'Application #{app_id}: {application["title"]} removed.',
                fg=typer.colors.GREEN
            )

    if force:
        _remove()
    else:
        application_list = applier.get_application_list()
        try:
            application = application_list[app_id - 1]
        except IndexError:
            typer.secho('Invalid application ID', fg=typer.colors.RED)
            raise typer.Exit(1)
        delete = typer.confirm(
            f"Delete application #{app_id}?"
        )
        if delete:
            _remove()
        else:
            typer.echo("Operation cancelled.")

    return
@app.command(name='list')
def list_all() -> None:
    """
    This function lists all applications in the database.
    """
    applier = get_applier()
    application_list = applier.get_application_list()
    if len(application_list) == 0:
        typer.secho(
            'There are no applications in the list yet.',
            fg=typer.colors.RED
        )
        raise typer.Exit()
    typer.secho("\nApplication list:\n", fg=typer.colors.BLUE, bold=True)
    columns = (
        "ID. ",
        "| Title ",
        "| Description "
    )
    headers = "".join(columns)
    typer.secho(headers, fg=typer.colors.BLUE, bold=True)
    typer.secho("-" * len(headers), fg=typer.colors.BLUE)
    for id, application in enumerate(application_list, 1):
        title, desc = application.values()
        typer.secho(
            f"{id}{(len(columns[0]) - len(str(id))) * ' '}"
            f"| {title}"
            f"| {desc}",
            fg=typer.colors.BLUE,
            bold=True
        )
    typer.secho("-" * len(headers) + "\n", fg=typer.colors.BLUE)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f'{__app_name__} v{__version__}')
        raise typer.Exit()


@app.callback()
def main(
        version: Optional[bool] = typer.Option(
            None,
            '--version',
            '-v',
            help="Display the application's version and exit.",
            callback=_version_callback,
            is_eager=True
        )
) -> None:
    return
