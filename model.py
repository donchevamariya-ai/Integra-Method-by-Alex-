"""Singleton loader for VoxCPM2 — call get_model() everywhere."""

from __future__ import annotations

import yaml
from pathlib import Path
from voxcpm import VoxCPM

_model: VoxCPM | None = None
_CONFIG = Path(__file__).parent.parent / "config" / "settings.yaml"


def load_config() -> dict:
    with open(_CONFIG) as f:
        return yaml.safe_load(f)


def get_model() -> VoxCPM:
    global _model
    if _model is None:
        cfg = load_config()
        _model = VoxCPM.from_pretrained(
            cfg["model"]["name"],
            device=cfg["model"].get("device", "cuda"),
        )
    return _model
