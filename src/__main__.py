"""
Including this file means that the application can be run
as an executable with: python -m application-tracker/src
"""

from src import cli, __app_name__


def main():
    cli.app(prog_name=__app_name__)


if __name__ == "__main__":
    main()

