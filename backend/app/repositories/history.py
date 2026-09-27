import json
from datetime import datetime, timezone
from app.db import connect

def insert_run(window_id, fabric_id, result, note=""):
    c = connect()
    try:
        cur = c.execute(
            "INSERT INTO calc_runs(window_id,fabric_id,result_json,note,created_at) VALUES (?,?,?,?,?)",
            (window_id, fabric_id, json.dumps(result, ensure_ascii=False), note, datetime.now(timezone.utc).isoformat()),
        )
        c.commit()
        return int(cur.lastrowid)
    finally:
        c.close()

def list_runs(limit=50):
    from app.services.pattern_open import open_as_raw_cut

    c = connect()
    try:
        rows = c.execute(
            """SELECT r.*, w.name window_name, f.name fabric_name,
                   w.width window_width, w.height window_height, w.fullness window_fullness,
                   f.fabric_width fabric_width, f.hem_top hem_top, f.hem_bottom hem_bottom
            FROM calc_runs r
            LEFT JOIN windows w ON w.id=r.window_id LEFT JOIN fabrics f ON f.id=r.fabric_id
            ORDER BY r.id DESC LIMIT ?""", (limit,)).fetchall()
        out = []
        for row in rows:
            d = dict(row)
            dims = {
                "width": d.get("window_width"),
                "height": d.get("window_height"),
                "fullness": d.get("window_fullness"),
                "fabric_width": d.get("fabric_width"),
                "hem_top": d.get("hem_top"),
                "hem_bottom": d.get("hem_bottom"),
            }
            raw = json.loads(d.pop("result_json"))
            d["result"] = open_as_raw_cut(raw, dims)
            out.append(d)
        return out
    finally:
        c.close()
