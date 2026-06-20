"""Meditation & practice audio generator за Integra Method."""

from __future__ import annotations

import soundfile as sf
import numpy as np
from pathlib import Path
from .model import get_model, load_config
from .clone import controllable_clone
from .design import design


MEDITATION_STYLE = "много тих и бавен глас, дълбоко спокоен, медитативен, с паузи между изреченията"

SILENCE_SEC = 3.0  # пауза между блокове (секунди)


def _silence(sample_rate: int, seconds: float) -> np.ndarray:
    return np.zeros(int(sample_rate * seconds), dtype=np.float32)


def generate_meditation(
    segments: list[str],
    output_path: str | Path,
    reference_wav: str | Path | None = None,
    pause_between: float = SILENCE_SEC,
) -> Path:
    """
    Синтезира медитация от списък с текстови сегменти.
    Между всеки сегмент се добавя тишина `pause_between` секунди.

    Ако `reference_wav` е подаден — използва Controllable Cloning.
    Иначе — Voice Design с медитативен профил.
    """
    model = get_model()
    cfg = load_config()
    sr = cfg["output"]["sample_rate"]

    parts: list[np.ndarray] = []

    for i, segment in enumerate(segments, 1):
        print(f"  [{i}/{len(segments)}] {segment[:60]}…")
        if reference_wav:
            audio = model.controllable_clone(
                text=segment,
                reference=str(reference_wav),
                style=MEDITATION_STYLE,
                sample_rate=sr,
            )
        else:
            audio = model.design_voice(
                description=MEDITATION_STYLE,
                text=segment,
                sample_rate=sr,
            )
        parts.append(audio)
        if i < len(segments):
            parts.append(_silence(sr, pause_between))

    combined = np.concatenate(parts)
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(out), combined, sr)
    print(f"\n✓ Медитация записана: {out}  ({len(combined)/sr:.1f} сек)")
    return out


if __name__ == "__main__":
    cfg = load_config()
    ref = cfg["alex_voice"]["sample"]

    script = [
        "Затвори очи. Поеми дълбоко въздух.",
        "Усети как тялото ти се отпуска с всяко издишване.",
        "Ти си в безопасност. Ти си тук. Ти си достатъчен.",
        "Остани в тази тишина за момент.",
        "Когато си готов, бавно отвори очи.",
    ]

    generate_meditation(
        segments=script,
        output_path="output/meditations/integra_intro.wav",
        reference_wav=ref,
        pause_between=4.0,
    )
