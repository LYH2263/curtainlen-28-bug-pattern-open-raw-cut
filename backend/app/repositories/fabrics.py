from app.db import connect

def list_fabrics():
    c = connect()
    try:
        return [dict(r) for r in c.execute("SELECT * FROM fabrics ORDER BY id").fetchall()]
    finally:
        c.close()

def get_fabric(fid: int):
    c = connect()
    try:
        r = c.execute("SELECT * FROM fabrics WHERE id=?", (fid,)).fetchone()
        return dict(r) if r else None
    finally:
        c.close()

def update_pattern_repeat(fid: int, pattern_repeat_cm: float):
    c = connect()
    try:
        cur = c.execute("UPDATE fabrics SET pattern_repeat_cm=? WHERE id=?", (float(pattern_repeat_cm), fid))
        c.commit()
        if cur.rowcount == 0:
            return None
        return get_fabric(fid)
    finally:
        c.close()
