import csv
import json
import click

from .rle_decoder import RLE


__VERSION__ = "0.1.0"


VALID_METRICS = [
    "area",
    "perimeter",
    "compactness",
    "centroid",
    "moments",
    "contour",
    "rle",
    "bbox",
]


@click.group()
def cli():
    """🍇 🍇 RLE Decoder CLI Tool by Efrain@UCD."""


@cli.command("metrics")
@click.version_option(__VERSION__, prog_name="🍇 RLE-Decoder")
@click.option(
    "-s",
    "--size",
    nargs=2,
    type=click.INT,
    required=True,
    help="Image size, e.g. 600 500",
)
@click.option(
    "-c",
    "--counts",
    nargs=1,
    type=click.STRING,
    required=True,
    help="""
    RLE counts encoded string
    (e.g. '_lm26^b09I4L4M2M3N2O1N2N2O1N101N101O0O100000O1O100N2K6L3M3N2N2O2N1O3L5L3N2M`bb5')""",
)
@click.option(
    "-m",
    "--metrics",
    type=click.STRING,
    default="area,perimeter,centroid,compactness,contour",
    help=f"""
    Comma separated list of metrics to display.
    Valid options are: {",".join(VALID_METRICS)}""",
)
@click.option(
    "-o",
    "--output-file",
    type=click.File("w"),
    required=False,
    help="Output file to save the results. Default is stdout.",
)
def metrics(size, counts, metrics, output_file):  # pylint: disable=W0621
    """Get metrics from RLE encoded mask."""
    metrics = [o for o in metrics.split(",") if o in VALID_METRICS]
    rle = RLE(size=size, counts=counts)
    result = {o: getattr(rle, o) for o in metrics}
    if output_file:
        _, ext = output_file.name.split(".")
        if ext != "json":
            click.echo(
                click.style(
                    "Error: Only JSON format is supported ",
                    blink=True,
                    bold=True,
                    bg="red",
                    fg="white",
                ),
                err=True,
            )
        with open(str(output_file.name), "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
    else:
        click.echo(json.dumps(result, indent=2))


@cli.command("decode")
@click.version_option(__VERSION__, prog_name="🍇 RLE-Decoder")
@click.option(
    "-s",
    "--size",
    nargs=2,
    type=click.INT,
    required=True,
    help="Image size, e.g. 600 500",
)
@click.option(
    "-c",
    "--counts",
    nargs=1,
    type=click.STRING,
    required=True,
    help="""
    RLE counts encoded string
    (e.g. '_lm26^b09I4L4M2M3N2O1N2N2O1N101N101O0O100000O1O100N2K6L3M3N2N2O2N1O3L5L3N2M`bb5')""",
)
@click.option(
    "-o",
    "--output-file",
    type=click.File("w"),
    required=False,
    help="Output file to save the results",
)
def decode(size, counts, output_file):
    """Decode RLE encoded mask."""
    rle = RLE(size=size, counts=counts)

    if output_file:
        _, ext = output_file.name.split(".")
        if ext != "csv":
            click.echo(
                click.style(
                    "Error: Only CSV format is supported ",
                    blink=True,
                    bold=True,
                    bg="red",
                    fg="white",
                ),
                err=True,
            )
        else:
            with open(str(output_file.name), "w", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["x", "y"])
                writer.writerows(rle.contour)
    else:
        click.echo("x,y")
        for p in rle.contour:
            click.echo(f"{p[0]},{p[1]}")
