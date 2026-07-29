"""``trkit`` komut satırı arayüzü."""

from __future__ import annotations

from typing import Annotated

import typer

from . import __version__, plates, text, validate

app = typer.Typer(
    name="trkit",
    help="Türkçe metin araçları ve Türkiye'ye özgü doğrulayıcılar.",
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
            help="Sürümü yazdırıp çıkar.",
        ),
    ] = False,
) -> None:
    """Türkçe metin araçları ve Türkiye'ye özgü doğrulayıcılar."""


def _report(ok: bool) -> None:
    """Doğrulama sonucunu yazar; geçersizse çıkış kodu 1 olur.

    Çıkış kodu, aracın kabuk betiklerinde ``if trkit tckn ...`` şeklinde
    kullanılabilmesi için anlamlıdır.
    """
    typer.echo("geçerli" if ok else "geçersiz")
    raise typer.Exit(code=0 if ok else 1)


@app.command()
def slug(
    metin: Annotated[str, typer.Argument(help="Slug'a çevrilecek metin.")],
    ayirici: Annotated[str, typer.Option("--ayirici", "-a", help="Kelime ayırıcı.")] = "-",
) -> None:
    """Metni URL'de kullanılabilir slug'a çevirir."""
    typer.echo(text.slugify(metin, separator=ayirici))


@app.command()
def upper(metin: Annotated[str, typer.Argument(help="Büyütülecek metin.")]) -> None:
    """Metni Türkçe kurallarına göre BÜYÜK harfe çevirir."""
    typer.echo(text.upper(metin))


@app.command()
def lower(metin: Annotated[str, typer.Argument(help="Küçültülecek metin.")]) -> None:
    """Metni Türkçe kurallarına göre küçük harfe çevirir."""
    typer.echo(text.lower(metin))


@app.command()
def title(metin: Annotated[str, typer.Argument(help="Başlık formatına çevrilecek metin.")]) -> None:
    """Her kelimenin ilk harfini Türkçe kurallarına göre büyütür."""
    typer.echo(text.title(metin))


@app.command(name="ascii")
def ascii_(metin: Annotated[str, typer.Argument(help="ASCII'ye indirgenecek metin.")]) -> None:
    """Türkçe harfleri ASCII karşılıklarına çevirir."""
    typer.echo(text.asciify(metin))


@app.command()
def tckn(numara: Annotated[str, typer.Argument(help="11 haneli TC kimlik numarası.")]) -> None:
    """TC kimlik numarasını doğrular. Geçersizse çıkış kodu 1'dir."""
    _report(validate.is_valid_tckn(numara))


@app.command()
def iban(numara: Annotated[str, typer.Argument(help="TR ile başlayan IBAN.")]) -> None:
    """Türkiye IBAN'ını doğrular. Geçersizse çıkış kodu 1'dir."""
    _report(validate.is_valid_iban(numara))


@app.command()
def plaka(
    deger: Annotated[str, typer.Argument(help="Plaka kodu (35) veya il adı (İzmir).")],
) -> None:
    """Plaka kodundan il adını, il adından plaka kodunu bulur."""
    deger = deger.strip()
    if deger.isdigit():
        city = plates.city_from_plate(deger)
        if city is None:
            typer.echo(f"'{deger}' geçerli bir plaka kodu değil.", err=True)
            raise typer.Exit(code=1)
        typer.echo(city)
    else:
        code = plates.plate_from_city(deger)
        if code is None:
            typer.echo(f"'{deger}' adında bir il bulunamadı.", err=True)
            raise typer.Exit(code=1)
        typer.echo(str(code))


def main() -> None:
    """Konsol betiği giriş noktası."""
    app()


if __name__ == "__main__":  # pragma: no cover
    main()
