import pytest
from unittest.mock import patch, MagicMock
from jarvis.commands import stocks_commands

# Mock for speech_output.speak
@patch('jarvis.commands.stocks_commands.speak')
# Mock for requests.get
@patch('jarvis.commands.stocks_commands.requests.get')
def test_get_stock_price(mock_get, mock_speak):
    mock_response = MagicMock()
    mock_get.return_value = mock_response

    # Mock successful response from Alpha Vantage API
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'Global Quote': {'05. price': '135.67'}
    }
    stocks_commands.get_stock_price('AAPL')
    mock_speak.assert_called_with("The current price of AAPL is $135.67.")

    # Mock no price information case
    mock_response.json.return_value = {}
    stocks_commands.get_stock_price('AAPL')
    mock_speak.assert_called_with("Could not find price information for AAPL.")

    # Mock error case
    mock_response.status_code = 400
    stocks_commands.get_stock_price('AAPL')
    mock_speak.assert_called_with("Failed to fetch stock data due to an error with the API.")

@pytest.mark.parametrize("command, expected_symbol, expected_call", [
    ("get price of AAPL", "AAPL", "get_stock_price"),
    ("unknown command", None, None)
])
@patch('jarvis.commands.stocks_commands.get_stock_price')
def test_stock_commands(mock_get_stock_price, command, expected_symbol, expected_call):
    stocks_commands.stock_commands(command)

    if expected_call == "get_stock_price":
        mock_get_stock_price.assert_called_once_with(expected_symbol)
    else:
        assert not mock_get_stock_price.called
