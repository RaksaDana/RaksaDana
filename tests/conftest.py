import pytest


MOCK_PREDICTION = {
    "ticker": "BBCA.JK",
    "signal_date": "2026-05-30",
    "base_close": 9500.0,
    "predicted_log_return": 0.010417,
    "predicted_close": 9600.0,
    "signal": "BUY",
}

MOCK_METRICS = {
    "ticker": "BBCA.JK",
    "mape": 1.2,
    "r2": 0.85,
    "direction_accuracy": 71.0,
    "return_rmse": 0.005,
}

MOCK_FORECAST = [
    {
        "date": f"2026-06-{i + 1:02d}",
        "predicted_close": round(9500.0 + i * 10, 2),
        "predicted_log_return": 0.001050,
    }
    for i in range(30)
]

MOCK_PROFIT_LOSS = {
    "ticker": "BBCA.JK",
    "price_source": "model_next_day",
    "exit_date": "2026-05-30",
    "quantity": {"shares": 200, "lots": 2.0, "lot_size": 100},
    "buy_price": 7600.0,
    "sell_price": 9600.0,
    "gross_buy_value": 1520000.0,
    "buy_fee": 2280.0,
    "total_cost": 1522280.0,
    "gross_sell_value": 1920000.0,
    "sell_fee": 4800.0,
    "net_proceeds": 1915200.0,
    "gross_profit_loss": 400000.0,
    "net_profit_loss": 392920.0,
    "net_return_pct": 25.8130,
    "price_change_pct": 26.3158,
    "breakeven_sell_price": 7630.48,
    "status": "PROFIT",
    "assumptions": {"buy_fee_rate": 0.0015, "sell_fee_rate": 0.0025},
}


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr("src.inference.preload_all", lambda: None)
    monkeypatch.setattr("src.inference.predict_next_day", lambda ticker: MOCK_PREDICTION.copy())
    monkeypatch.setattr("src.inference.forecast_30d", lambda ticker, days=30: MOCK_FORECAST[:days])
    monkeypatch.setattr("src.inference.get_metrics", lambda ticker: MOCK_METRICS.copy())
    monkeypatch.setattr(
        "src.inference.calculate_profit_loss",
        lambda ticker, buy_price, **kwargs: MOCK_PROFIT_LOSS.copy(),
    )
    monkeypatch.setattr(
        "src.gemini_narration.generate_prediction_narration",
        lambda ticker, pred, met: "Narasi test prediksi",
    )
    monkeypatch.setattr(
        "src.gemini_narration.generate_profit_loss_narration",
        lambda ticker, pred, met, pl: "Narasi test profit loss",
    )

    import main
    from fastapi.testclient import TestClient

    with TestClient(main.app) as c:
        yield c
