import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.db import connect
from app import seed


@pytest.fixture(scope="module")
def client():
    seed.init_db()
    with TestClient(app) as c:
        yield c


def count_runs():
    conn = connect()
    try:
        return conn.execute("SELECT COUNT(*) c FROM calc_runs").fetchone()["c"]
    finally:
        conn.close()


def test_estimate_zero_repeat_legacy(client):
    r = client.get("/api/estimate", params={"window_id": 1, "fabric_id": 1})
    assert r.status_code == 200
    d = r.json()
    assert d["cut_height"] == 2.85
    assert d["gross_cut_height"] == 2.85
    assert d["pattern_repeat_cm"] == 0


def test_estimate_preview_with_repeat_not_persisted(client):
    before = count_runs()
    r = client.get("/api/estimate", params={"window_id": 1, "fabric_id": 1, "pattern_repeat_cm": 64})
    assert r.status_code == 200
    d = r.json()
    assert d["gross_cut_height"] == 2.85
    assert d["cut_height"] == 3.2
    assert d["meters"] == 16.0
    assert d["run_id"] is None
    assert count_runs() == before


def test_negative_repeat_get_rejected_without_row(client):
    before = count_runs()
    r = client.get("/api/estimate", params={"window_id": 1, "fabric_id": 1, "pattern_repeat_cm": -5})
    assert r.status_code == 422
    assert count_runs() == before


def test_negative_repeat_post_rejected_without_row(client):
    before = count_runs()
    r = client.post("/api/estimate", json={"window_id": 1, "fabric_id": 1, "save": True, "pattern_repeat_cm": -5})
    assert r.status_code == 422
    assert count_runs() == before


def test_save_freezes_repeat_and_later_default_change_does_not_rewrite(client):
    # 用花高 64cm 真正写入
    r = client.post("/api/estimate", json={"window_id": 1, "fabric_id": 1, "save": True, "pattern_repeat_cm": 64})
    assert r.status_code == 200
    run_id = r.json()["run_id"]
    assert run_id is not None

    saved = client.get("/api/runs").json()["items"]
    row = next(x for x in saved if x["id"] == run_id)
    assert row["result"]["pattern_repeat_cm"] == 64
    assert row["result"]["gross_cut_height"] == 2.85
    assert row["result"]["cut_height"] == 3.2
    assert row["result"]["meters"] == 16.0

    # 事后改布料默认花高：只影响之后的试算，旧编号回看裁高不变
    p = client.patch(f"/api/fabrics/1", json={"pattern_repeat_cm": 80})
    assert p.status_code == 200
    assert p.json()["pattern_repeat_cm"] == 80

    saved = client.get("/api/runs").json()["items"]
    row = next(x for x in saved if x["id"] == run_id)
    assert row["result"]["cut_height"] == 3.2
    assert row["result"]["pattern_repeat_cm"] == 64

    later = client.get("/api/estimate", params={"window_id": 1, "fabric_id": 1})
    assert later.json()["pattern_repeat_cm"] == 80


def test_patch_negative_repeat_rejected(client):
    r = client.patch("/api/fabrics/1", json={"pattern_repeat_cm": -1})
    assert r.status_code == 422


def test_patch_missing_fabric_404(client):
    r = client.patch("/api/fabrics/9999", json={"pattern_repeat_cm": 10})
    assert r.status_code == 404
