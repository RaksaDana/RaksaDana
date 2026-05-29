import src.inference as inf


def test_cache_hit_returns_cached_artifacts():
    inf._ARTIFACT_CACHE.clear()
    fake = ([], object(), object(), [], 30)
    inf._ARTIFACT_CACHE["BBCA.JK"] = fake

    result = inf._load_artifacts("BBCA.JK")

    assert result is fake


def test_preload_all_calls_load_for_all_tickers(monkeypatch):
    inf._ARTIFACT_CACHE.clear()
    called = []

    def fake_load(ticker):
        called.append(ticker)
        fake = ([], object(), object(), [], 30)
        inf._ARTIFACT_CACHE[ticker] = fake
        return fake

    monkeypatch.setattr(inf, "_load_artifacts", fake_load)
    inf.preload_all()

    assert set(called) == set(inf.SUPPORTED_TICKERS)
