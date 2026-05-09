import pandas as pd
from unittest.mock import patch, MagicMock
from volsurface.data.fetch_yahoo import fetch_option_chain, load_all_expiries

@patch("volsurface.data.fetch_yahoo.yf.Ticker")
def test_fetch_option_chain(mock_ticker_class):
    # Setup mock
    mock_ticker_instance = MagicMock()
    mock_ticker_class.return_value = mock_ticker_instance

    mock_chain = MagicMock()
    # Create a dummy dataframe for calls
    dummy_calls = pd.DataFrame({
        "strike": [100, 110],
        "lastPrice": [5.5, 2.1]
    })
    mock_chain.calls = dummy_calls
    mock_ticker_instance.option_chain.return_value = mock_chain

    # Call the function
    ticker = "AAPL"
    expiry = "2024-01-19"
    result = fetch_option_chain(ticker, expiry)

    # Verify calls
    mock_ticker_class.assert_called_once_with(ticker)
    mock_ticker_instance.option_chain.assert_called_once_with(expiry)

    # Verify result
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    assert "type" in result.columns
    assert "expiry" in result.columns
    assert (result["type"] == "call").all()
    assert (result["expiry"] == expiry).all()

@patch("volsurface.data.fetch_yahoo.fetch_option_chain")
@patch("volsurface.data.fetch_yahoo.yf.Ticker")
def test_load_all_expiries(mock_ticker_class, mock_fetch_option_chain):
    # Setup mock Ticker
    mock_ticker_instance = MagicMock()
    mock_ticker_class.return_value = mock_ticker_instance
    mock_ticker_instance.options = ("2024-01-19", "2024-02-16")

    # Setup mock fetch_option_chain
    df1 = pd.DataFrame({
        "strike": [100],
        "lastPrice": [5.5],
        "type": ["call"],
        "expiry": ["2024-01-19"]
    })
    df2 = pd.DataFrame({
        "strike": [110],
        "lastPrice": [2.1],
        "type": ["call"],
        "expiry": ["2024-02-16"]
    })
    mock_fetch_option_chain.side_effect = [df1, df2]

    # Call the function
    ticker = "AAPL"
    result = load_all_expiries(ticker)

    # Verify calls
    mock_ticker_class.assert_called_once_with(ticker)
    assert mock_fetch_option_chain.call_count == 2
    mock_fetch_option_chain.assert_any_call(ticker, "2024-01-19")
    mock_fetch_option_chain.assert_any_call(ticker, "2024-02-16")

    # Verify result
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    assert list(result["expiry"]) == ["2024-01-19", "2024-02-16"]
