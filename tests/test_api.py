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
