def test_health(client):
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert set(body["tickers"]) == {"BBCA.JK", "BBRI.JK", "BMRI.JK"}


def test_tickers(client):
    r = client.get("/api/v1/tickers")
    assert r.status_code == 200
    assert set(r.json()) == {"BBCA.JK", "BBRI.JK", "BMRI.JK"}


def test_predict_returns_prediction(client):
    r = client.get("/api/v1/predict/BBCA.JK")
    assert r.status_code == 200
    body = r.json()
    assert body["ticker"] == "BBCA.JK"
    assert body["signal"] in ("BUY", "HOLD", "SELL")
    assert body["predicted_close"] == 9600.0
    assert body["narration"] is None


def test_predict_with_narrate_returns_narration(client):
    r = client.get("/api/v1/predict/BBCA.JK?narrate=true")
    assert r.status_code == 200
    assert r.json()["narration"] == "Narasi test prediksi"


def test_predict_invalid_ticker_returns_422(monkeypatch):
    def raise_value_error(ticker):
        raise ValueError(f"Unsupported ticker: {ticker}")

    monkeypatch.setattr("src.inference.preload_all", lambda: None)
    monkeypatch.setattr("src.inference.predict_next_day", raise_value_error)

    import main
    from fastapi.testclient import TestClient

    with TestClient(main.app) as c:
        r = c.get("/api/v1/predict/INVALID.JK")
    assert r.status_code == 422


def test_predict_missing_model_returns_503(monkeypatch):
    def raise_fnf(ticker):
        raise FileNotFoundError("Model not found")

    monkeypatch.setattr("src.inference.preload_all", lambda: None)
    monkeypatch.setattr("src.inference.predict_next_day", raise_fnf)

    import main
    from fastapi.testclient import TestClient

    with TestClient(main.app) as c:
        r = c.get("/api/v1/predict/BBCA.JK")
    assert r.status_code == 503


def test_predict_narration_graceful_on_gemini_error(monkeypatch):
    def raise_runtime(*args):
        raise RuntimeError("GEMINI_API_KEY not set")

    monkeypatch.setattr("src.inference.preload_all", lambda: None)
    monkeypatch.setattr(
        "src.inference.predict_next_day",
        lambda ticker: {
            "ticker": ticker, "signal_date": "2026-05-30",
            "base_close": 9500.0, "predicted_log_return": 0.010417,
            "predicted_close": 9600.0, "signal": "BUY",
        },
    )
    monkeypatch.setattr(
        "src.inference.get_metrics",
        lambda ticker: {"ticker": ticker, "mape": 1.2, "r2": 0.85,
                        "direction_accuracy": 71.0, "return_rmse": 0.005},
    )
    monkeypatch.setattr("src.gemini_narration.generate_prediction_narration", raise_runtime)

    import main
    from fastapi.testclient import TestClient

    with TestClient(main.app) as c:
        r = c.get("/api/v1/predict/BBCA.JK?narrate=true")
    assert r.status_code == 200
    assert "tidak tersedia" in r.json()["narration"]


def test_metrics_returns_metrics(client):
    r = client.get("/api/v1/metrics/BBCA.JK")
    assert r.status_code == 200
    body = r.json()
    assert body["ticker"] == "BBCA.JK"
    assert "mape" in body
    assert "direction_accuracy" in body


def test_metrics_not_found_returns_404(monkeypatch):
    monkeypatch.setattr("src.inference.preload_all", lambda: None)
    monkeypatch.setattr("src.inference.get_metrics", lambda ticker: {})

    import main
    from fastapi.testclient import TestClient

    with TestClient(main.app) as c:
        r = c.get("/api/v1/metrics/BBCA.JK")
    assert r.status_code == 404


def test_forecast_returns_30_points_by_default(client):
    r = client.get("/api/v1/forecast/BBCA.JK")
    assert r.status_code == 200
    body = r.json()
    assert isinstance(body, list)
    assert len(body) == 30
    first = body[0]
    assert "date" in first
    assert "predicted_close" in first
    assert "predicted_log_return" in first


def test_forecast_custom_days(client):
    r = client.get("/api/v1/forecast/BBCA.JK?days=7")
    assert r.status_code == 200
    assert len(r.json()) == 7


def test_forecast_days_below_minimum_returns_422(client):
    r = client.get("/api/v1/forecast/BBCA.JK?days=0")
    assert r.status_code == 422


def test_forecast_days_above_maximum_returns_422(client):
    r = client.get("/api/v1/forecast/BBCA.JK?days=91")
    assert r.status_code == 422
