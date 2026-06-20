"""Voice Cloning — Controllable и Ultimate режими."""

from __future__ import annotations

import soundfile as sf
from pathlib import Path
from .model import get_model, load_config


def controllable_clone(
    text: str,
    reference_wav: str | Path,
    output_path: str | Path,
    style: str = "спокоен, ясен, авторитетен",
) -> Path:
    """
    Клонира глас от референтен клип.
    `style` насочва интонацията без да пренаписва идентичността на гласа.
    Ползвай за озвучаване на обучения — контролирано темпо и тон.
    """
    model = get_model()
    cfg = load_config()
    sr = cfg["output"]["sample_rate"]

    audio = model.controllable_clone(
        text=text,
        reference=str(reference_wav),
        style=style,
        sample_rate=sr,
    )

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(out), audio, sr)
    print(f"Controllable clone записан: {out}")
    return out


def ultimate_clone(
    text: str,
    reference_wav: str | Path,
    output_path: str | Path,
) -> Path:
    """
    Пълно клониране — копира тембър, ритъм, емоция и стил без корекции.
    Ползвай когато верността на оригиналния глас е критична
    (напр. официални материали с гласа на Алекс).
    """
    model = get_model()
    cfg = load_config()
    sr = cfg["output"]["sample_rate"]

    audio = model.ultimate_clone(
        text=text,
        reference=str(reference_wav),
        sample_rate=sr,
    )

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(out), audio, sr)
    print(f"Ultimate clone записан: {out}")
    return out


def clone_for_integra(
    text: str,
    mode: str = "controllable",
    output_name: str = "output.wav",
) -> Path:
    """Shortcut: използва samples/alex_reference.wav от config."""
    cfg = load_config()
    ref = Path(cfg["alex_voice"]["sample"])
    style = cfg["alex_voice"]["style"]
    out = Path("output") / output_name

    if mode == "ultimate":
        return ultimate_clone(text, ref, out)
    return controllable_clone(text, ref, out, style=style)


if __name__ == "__main__":
    clone_for_integra(
        text="Integra Method е система за трансформация, изградена върху реални резултати.",
        mode="controllable",
        output_name="alex_clone_test.wav",
    )
