import pytest
import requests
from pytest_mock import MockerFixture, mocker

from simple_http_checker.checker import check_urls

def test_check_urls_success(mocker: MockerFixture):
    # Mock the requests.get method to simulate a successful response
    mock_response = mocker.MagicMock(spec=requests.Response)
    mock_response.ok = True
    mock_response.status_code = 200
    mock_response.reason = "OK"
    mocker.patch("simple_http_checker.checker.requests.get", return_value=mock_response)

    urls = ["http://example.com"]
    results = check_urls(urls)

    assert results == {"http://example.com": "200"}


def test_check_urls_client_error(mocker: MockerFixture):
    # Mock the requests.get method to simulate a client error response
    mock_response = mocker.MagicMock(spec=requests.Response)
    mock_response.ok = False
    mock_response.status_code = 404
    mock_response.reason = "Not Found"
    mocker.patch("simple_http_checker.checker.requests.get", return_value=mock_response)

    urls = ["http://example.com/nonexistent"]
    results = check_urls(urls)

    assert results == {"http://example.com/nonexistent": "404 - Not Found"}

@pytest.mark.parametrize(
    "error_exception, expected_status",
    [
        (requests.exceptions.Timeout, "TIMEOUT"),
        (requests.exceptions.ConnectionError, "CONNECTION ERROR"),
        (requests.exceptions.RequestException, "ERROR - RequestException"),
    ],
)

def test_check_urls_exception(mocker: MockerFixture, error_exception: Exception, expected_status: str):
    # Mock the requests.get method to raise a RequestException
    mocker.patch("simple_http_checker.checker.requests.get", side_effect=requests.exceptions.RequestException)

    urls = ["http://MYDOG.com"]
    results = check_urls(urls)

    assert results == {"http://MYDOG.com": "ERROR - RequestException"}

def test_check_urls_with_multiple_urls(mocker: MockerFixture):
    # Mock the requests.get method to simulate successful responses
    mock_response = mocker.MagicMock(spec=requests.Response)
    mock_response.ok = True
    mock_response.status_code = 200
    mock_response.reason = "OK"
    mocker.patch("simple_http_checker.checker.requests.get", return_value=mock_response)

    urls = ["http://example.com", "http://mydog.com"]
    results = check_urls(urls)

    assert results == {"http://example.com": "200", "http://mydog.com": "200"}

def test_check_urls_empty_list(mocker: MockerFixture):
    # Test with an empty list of URLs
    urls = []
    results = check_urls(urls)

    assert results == {}
def test_check_urls_timeout(mocker: MockerFixture):
    # Mock the requests.get method to raise a Timeout exception
    mocker.patch("simple_http_checker.checker.requests.get", side_effect=requests.exceptions.Timeout)

    urls = ["http://example.com"]
    results = check_urls(urls)

    assert results == {"http://example.com": "TIMEOUT"}   

    