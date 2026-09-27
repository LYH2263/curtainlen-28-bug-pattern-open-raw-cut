"""Shape payloads for history open views (pattern repeat snap)."""

from __future__ import annotations

from copy import deepcopy

from app.engines.helpers import ceil_units


def has_pattern(result: dict) -> bool:
    return float(result.get("pattern_repeat_cm") or 0) > 0


def _raw_cut_height(result: dict, dims: dict | None = None) -> float | None:
    gross = result.get("gross_cut_height")
    if gross is not None:
        return float(gross)
    if dims and None not in (dims.get("height"), dims.get("hem_top"), dims.get("hem_bottom")):
        return float(dims["height"]) + float(dims["hem_top"]) + float(dims["hem_bottom"])
    return None


def open_as_raw_cut(result: dict, dims: dict | None = None) -> dict:
    """Keep pattern_repeat_cm, but set cut_height to gross (height+hems) and cascade meters."""
    if not isinstance(result, dict):
        return result
    out = deepcopy(result)
    if not has_pattern(out):
        return out
    cut_h = _raw_cut_height(out, dims)
    if cut_h is None:
        return out
    panels = int(out.get("panels") or 0)
    if panels <= 0 and dims and dims.get("width") is not None and dims.get("fabric_width"):
        fullness = float(dims.get("fullness") or 2.0)
        finished_w = float(dims["width"]) * fullness
        panels = max(1, ceil_units(finished_w / float(dims["fabric_width"])))
        out["finished_width"] = round(finished_w, 3)
        out["panels"] = panels
    if panels <= 0:
        return out
    out["cut_height"] = round(cut_h, 3)
    out["meters"] = round(panels * cut_h, 2)
    out["open_pattern_raw"] = True
    out["list_pattern_repeat_cm"] = out.get("pattern_repeat_cm")
    out["list_gross_cut_height"] = out.get("gross_cut_height")
    return out


def summarize_pattern(result: dict) -> dict:
    """Flat view of pattern / gross / cut / meters for open consumers."""
    if not isinstance(result, dict):
        return {}
    return {
        "pattern_repeat_cm": result.get("pattern_repeat_cm"),
        "gross_cut_height": result.get("gross_cut_height"),
        "cut_height": result.get("cut_height"),
        "meters": result.get("meters"),
        "open_pattern_raw": bool(result.get("open_pattern_raw")),
    }
