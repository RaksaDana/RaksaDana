import pytest
from unittest.mock import MagicMock

from google.genai import errors


_PREDICTION = {
    "signal_date": "2026-05-30",
    "base_close": 9500.0,
    "predicted_log_return": 0.010417,
    "predicted_close": 9600.0,
    "signal": "BUY",
}
_METRICS = {
    "mape": 1.2,
    "r2": 0.85,
    "direction_accuracy": 71.0,
    "return_rmse": 0.005,
}
_PROFIT_LOSS = {
    "buy_price": 7600.0,
    "sell_price": 9600.0,
    "quantity": {"shares": 200, "lots": 2.0},
    "total_cost": 1522280.0,
    "net_profit_loss": 392920.0,
    "net_return_pct": 25.813,
    "status": "PROFIT",
    "breakeven_sell_price": 7630.48,
}


@pytest.fixture(autouse=True)
def reset_clients():
    """Keep the module-level client cache from leaking across tests."""
    import src.gemini_narration as gn
    gn._clients = None
    yield
    gn._clients = None


def test_get_clients_raises_without_api_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY_2", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY_3", raising=False)
    import src.gemini_narration as gn
    with pytest.raises(RuntimeError, match="GEMINI_API_KEY not set"):
        gn._get_clients()


def test_generate_prediction_narration_returns_model_text():
    import src.gemini_narration as gn

    mock_resp = MagicMock()
    mock_resp.text = "Narasi prediksi BBCA"
    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = mock_resp
    gn._clients = [mock_client]

    result = gn.generate_prediction_narration("BBCA.JK", _PREDICTION, _METRICS)

    assert result == "Narasi prediksi BBCA"
    call_kwargs = mock_client.models.generate_content.call_args.kwargs
    assert call_kwargs["model"] == "gemma-4-31b-it"
    assert "BBCA.JK" in call_kwargs["contents"]
    assert "BUY" in call_kwargs["contents"]


def test_generate_profit_loss_narration_returns_model_text():
    import src.gemini_narration as gn

    mock_resp = MagicMock()
    mock_resp.text = "Narasi profit loss BBCA"
    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = mock_resp
    gn._clients = [mock_client]

    result = gn.generate_profit_loss_narration("BBCA.JK", _PREDICTION, _METRICS, _PROFIT_LOSS)

    assert result == "Narasi profit loss BBCA"
    call_kwargs = mock_client.models.generate_content.call_args.kwargs
    assert "PROFIT" in call_kwargs["contents"]
    assert "7600" in call_kwargs["contents"]


def test_falls_back_to_second_key_on_rate_limit():
    import src.gemini_narration as gn

    rate_limited = MagicMock()
    rate_limited.models.generate_content.side_effect = errors.ClientError(429, {})
    ok_resp = MagicMock()
    ok_resp.text = "Narasi dari key kedua"
    healthy = MagicMock()
    healthy.models.generate_content.return_value = ok_resp
    gn._clients = [rate_limited, healthy]

    result = gn.generate_prediction_narration("BBCA.JK", _PREDICTION, _METRICS)

    assert result == "Narasi dari key kedua"
    rate_limited.models.generate_content.assert_called_once()
    healthy.models.generate_content.assert_called_once()


def test_falls_back_on_server_overload():
    import src.gemini_narration as gn

    overloaded = MagicMock()
    overloaded.models.generate_content.side_effect = errors.ServerError(503, {})
    ok_resp = MagicMock()
    ok_resp.text = "Narasi setelah overload"
    healthy = MagicMock()
    healthy.models.generate_content.return_value = ok_resp
    gn._clients = [overloaded, healthy]

    result = gn.generate_prediction_narration("BBCA.JK", _PREDICTION, _METRICS)

    assert result == "Narasi setelah overload"


def test_reraises_when_all_keys_rate_limited():
    import src.gemini_narration as gn

    c1 = MagicMock()
    c1.models.generate_content.side_effect = errors.ClientError(429, {})
    c2 = MagicMock()
    c2.models.generate_content.side_effect = errors.ClientError(429, {})
    gn._clients = [c1, c2]

    with pytest.raises(errors.ClientError):
        gn.generate_prediction_narration("BBCA.JK", _PREDICTION, _METRICS)


def test_non_rate_limit_client_error_not_retried():
    import src.gemini_narration as gn

    bad_request = MagicMock()
    bad_request.models.generate_content.side_effect = errors.ClientError(400, {})
    healthy = MagicMock()
    gn._clients = [bad_request, healthy]

    with pytest.raises(errors.ClientError):
        gn.generate_prediction_narration("BBCA.JK", _PREDICTION, _METRICS)
    healthy.models.generate_content.assert_not_called()


def test_raises_on_empty_response_text():
    import src.gemini_narration as gn

    mock_resp = MagicMock()
    mock_resp.text = None
    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = mock_resp
    gn._clients = [mock_client]

    with pytest.raises(ValueError, match="Empty response"):
        gn.generate_prediction_narration("BBCA.JK", _PREDICTION, _METRICS)


def test_raises_runtime_error_when_no_clients():
    import src.gemini_narration as gn

    gn._clients = []

    with pytest.raises(RuntimeError, match="No API clients available"):
        gn.generate_prediction_narration("BBCA.JK", _PREDICTION, _METRICS)
