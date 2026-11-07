import logging

import requests

logger = logging.getLogger(__name__)


def check_urls(
    urls: list[str], timeout: int = 5
) -> dict[str, str]:
    """
    Check the status of a list of URLs.

    Args:
        urls: A list of URLs to check.
        timeout: The timeout for each HTTP request, in seconds.

    Returns:
        A dictionary mapping each URL to its status
        (an HTTP status code, or a short error description).
    """
    logger.info(
        f"Checking {len(urls)} URLs with a timeout of {timeout} seconds."
    )
    results: dict[str, str] = {}

    for url in urls:
        try:
            logger.debug(f"Checking URL: {url}")
            response = requests.get(url, timeout=timeout)

            if response.ok:
                status = str(response.status_code)
            else:
                status = (
                    f"{response.status_code} - {response.reason}"
                )
        except requests.exceptions.Timeout:
            status = "TIMEOUT"
            logger.warning(f"Timeout occurred for URL: {url}")
        except requests.exceptions.ConnectionError:
            status = "CONNECTION ERROR"
            logger.warning(
                f"Connection error occurred for URL: {url}"
            )
        except requests.exceptions.RequestException as e:
            status = f"ERROR - {type(e).__name__}"
            logger.exception(f"Request exception for URL: {url}")

        results[url] = status
        logger.debug(f"Checked: {url:<40} Status: {status}")

    logger.info("URL checking completed.")
    return results
