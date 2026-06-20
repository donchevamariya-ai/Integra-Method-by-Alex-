"""Voice Design — създаване на нов глас от текстово описание."""

from __future__ import annotations

import soundfile as sf
from pathlib import Path
from .model import get_model, load_config


INTEGRA_VOICES = {
    "alex": (
        "Мъж на около 40 години, уверен и топъл глас, говори спокойно и ясно, "
        "авторитетен тембър с леко средиземноморско влияние"
    ),
    "meditation": (
        "Жена на около 35 години, много тих и бавен глас, дълбоко спокоен, "
        "медитативен, с паузи между изреченията"
    ),
    "guide": (
        "Мъж на около 45 години, уверен глас на учител, ясна дикция, "
        "умерено темпо, топъл и подкрепящ"
    ),
}


def design(
    text: str,
    description: str,
    output_path: str | Path,
) -> Path:
    """Синтезира `text` с глас, описан само с думи."""
    model = get_model()
    cfg = load_config()
    sr = cfg["output"]["sample_rate"]

    audio = model.design_voice(description=description, text=text, sample_rate=sr)

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(out), audio, sr)
    print(f"Записан: {out}")
    return out


def design_integra(
    text: str,
    voice_name: str = "alex",
    output_path: str | Path | None = None,
) -> Path:
    """Удобен shortcut за предефинираните гласове на Integra Method."""
    if voice_name not in INTEGRA_VOICES:
        raise ValueError(f"Непознат глас: {voice_name}. Избери от {list(INTEGRA_VOICES)}")
    desc = INTEGRA_VOICES[voice_name]
    out = output_path or Path("output") / f"{voice_name}_design.wav"
    return design(text, desc, out)


if __name__ == "__main__":
    design_integra(
        text="Добре дошли в Integra Method. Готови ли сте да започнем?",
        voice_name="alex",
        output_path="output/alex_design_test.wav",
    )
