import requests
from click.testing import CliRunner
from pytest_mock import MockerFixture

from simple_http_checker.cli import main


def test_no_ulrs():
    runner = CliRunner()
    result = runner.invoke(main, [], prog_name="check_urls")
    assert result.exit_code == 2
    assert "Usage: check_urls" in result.output


def test_check_urls_success(mocker: MockerFixture):
    # Mock the requests.get method to simulate a successful response
    mock_response = mocker.MagicMock(spec=requests.Response)
    mock_response.ok = True
    mock_response.status_code = 200
    mock_response.reason = "OK"
    mocker.patch(
        "simple_http_checker.checker.check_urls",
        return_value=mock_response,
    )

    runner = CliRunner()
    result = runner.invoke(
        main, ["http://example.com"], prog_name="check_urls"
    )

    assert result.exit_code == 0
    assert "http://example.com" in result.output
    assert "200" in result.output


def test_check_urls_failure(mocker: MockerFixture):
    # Mock the requests.get method to simulate a failed response
    mock_response = mocker.MagicMock(spec=requests.Response)
    mock_response.ok = False
    mock_response.status_code = 404
    mock_response.reason = "Not Found"
    mocker.patch(
        "simple_http_checker.checker.check_urls",
        return_value=mock_response,
    )

    runner = CliRunner()
    result = runner.invoke(
        main,
        ["http://example.com/nonexistent"],
        prog_name="check_urls",
    )

    assert result.exit_code == 1
    assert "http://example.com/nonexistent" in result.output
    assert "404 - Not Found" in result.output
