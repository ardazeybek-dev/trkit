"""``trkit`` command line interface."""

from __future__ import annotations

from typing import Annotated

import typer

from . import __version__, plates, text, validate

app = typer.Typer(
    name="trkit",
    help="Turkish text utilities and Türkiye-specific validators.",
    no_args_is_help=True,
    add_completion=False,
)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(__version__)
        raise typer.Exit()


@app.callback()
def _root(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            "-V",
            callback=_version_callback,
            is_eager=True,
            help="Print the version and exit.",
        ),
    ] = False,
) -> None:
    """Turkish text utilities and Türkiye-specific validators."""


def _report(ok: bool) -> None:
    """Print the validation result; exit with code 1 when invalid.

    The exit code is meaningful so the tool can be used directly in shell
    scripts, e.g. ``if trkit tckn "$VALUE"; then ...``.
    """
    typer.echo("valid" if ok else "invalid")
    raise typer.Exit(code=0 if ok else 1)


@app.command()
def slug(
    text_: Annotated[str, typer.Argument(metavar="TEXT", help="Text to slugify.")],
    separator: Annotated[str, typer.Option("--separator", "-s", help="Word separator.")] = "-",
) -> None:
    """Convert text into a URL-safe slug."""
    typer.echo(text.slugify(text_, separator=separator))


@app.command()
def upper(
    text_: Annotated[str, typer.Argument(metavar="TEXT", help="Text to upper-case.")],
) -> None:
    """Upper-case text using Turkish rules."""
    typer.echo(text.upper(text_))


@app.command()
def lower(
    text_: Annotated[str, typer.Argument(metavar="TEXT", help="Text to lower-case.")],
) -> None:
    """Lower-case text using Turkish rules."""
    typer.echo(text.lower(text_))


@app.command()
def title(
    text_: Annotated[str, typer.Argument(metavar="TEXT", help="Text to title-case.")],
) -> None:
    """Capitalise the first letter of each word using Turkish rules."""
    typer.echo(text.title(text_))


@app.command(name="ascii")
def ascii_(
    text_: Annotated[str, typer.Argument(metavar="TEXT", help="Text to fold to ASCII.")],
) -> None:
    """Replace Turkish letters with their ASCII counterparts."""
    typer.echo(text.asciify(text_))


@app.command()
def tckn(number: Annotated[str, typer.Argument(help="11-digit Turkish national ID.")]) -> None:
    """Validate a Turkish national ID (TCKN). Exit code is 1 when invalid."""
    _report(validate.is_valid_tckn(number))


@app.command()
def iban(number: Annotated[str, typer.Argument(help="IBAN starting with TR.")]) -> None:
    """Validate a Türkiye IBAN. Exit code is 1 when invalid."""
    _report(validate.is_valid_iban(number))


def _plate_lookup(value: str) -> None:
    value = value.strip()
    if value.isdigit():
        city = plates.city_from_plate(value)
        if city is None:
            typer.echo(f"'{value}' is not a valid plate code.", err=True)
            raise typer.Exit(code=1)
        typer.echo(city)
    else:
        code = plates.plate_from_city(value)
        if code is None:
            typer.echo(f"No province named '{value}'.", err=True)
            raise typer.Exit(code=1)
        typer.echo(str(code))


@app.command()
def plate(
    value: Annotated[str, typer.Argument(help="Plate code (35) or province name (İzmir).")],
) -> None:
    """Look up a province from its plate code, or a plate code from a province."""
    _plate_lookup(value)


# 0.1.0 shipped this command under its Turkish name; kept as a hidden alias so
# existing scripts keep working. Prefer ``plate``.
@app.command(name="plaka", hidden=True)
def plaka(
    value: Annotated[str, typer.Argument(help="Plate code (35) or province name (İzmir).")],
) -> None:
    """Deprecated alias for ``plate``."""
    _plate_lookup(value)


def main() -> None:
    """Console script entry point."""
    app()


if __name__ == "__main__":  # pragma: no cover
    main()
