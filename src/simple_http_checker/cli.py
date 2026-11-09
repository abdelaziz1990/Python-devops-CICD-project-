import logging
import sys
from _collections_abc import Collection

import click

from simple_http_checker.checker import check_urls

logger = logging.getLogger(__name__)


@click.command(
    name="check_urls",
    help="Check the status of one or more URLs.",
)
@click.argument("urls", nargs=-1, required=True)
@click.option(
    "--timeout",
    type=click.IntRange(min=1),
    default=5,
    show_default=True,
    help="Timeout for each request, in seconds.",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Show detailed debug logs.",
)
def main(urls: Collection[str], timeout: int, verbose: bool):
    """Check the status of one or more URLs."""
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.WARNING,
        format="%(levelname)s:%(name)s:%(message)s",
        force=True,
    )
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Verbose mode enabled.")
    logger.debug(f"Received urls: {urls}")
    logger.debug(f"Received timeout: {timeout} seconds")
    logger.debug(f"Received verbose flag: {verbose}")
    if not urls:
        logger.error("No URLs provided.")
        click.echo("Error: No URLs provided.", err=True)
        sys.exit(1)
    results = check_urls(list(urls), timeout=timeout)

    failed = 0
    for url, status in results.items():
        ok = status.isdigit()
        if not ok:
            failed += 1
        click.secho(
            f"{url:<40} {status}", fg="green" if ok else "red"
        )

    click.echo(
        f"\n{len(results) - failed}/{len(results)} URLs OK"
    )

    if failed:
        sys.exit(1)
