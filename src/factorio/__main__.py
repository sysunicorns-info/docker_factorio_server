# pylint: disable=C0103
"""
Entry point for the Factorio CLI application.
"""

from .commands import typer_application

if __name__ == "__main__":
    typer_application()
