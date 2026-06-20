"""Multilingual dubbing pipeline — един глас, много езици."""

from __future__ import annotations

import soundfile as sf
from pathlib import Path
from typing import Sequence
from .model import get_model, load_config
from .clone import controllable_clone


# Преводи, които трябва да подготвиш предварително (или интегрирай DeepL/GPT).
# Структурата: { "en": "...", "de": "...", ... }

def dub_multilingual(
    translations: dict[str, str],
    reference_wav: str | Path,
    output_dir: str | Path = "output/dub",
    style: str = "спокоен, ясен, авторитетен",
    prefix: str = "dub",
) -> dict[str, Path]:
    """
    Синтезира едно съдържание на няколко езика с един и същ клониран глас.

    `translations` е речник { "bg": "текст", "en": "text", "de": "Text", ... }
    Връща речник с пътищата до изходните файлове.
    """
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    results: dict[str, Path] = {}

    for lang, text in translations.items():
        out_path = out_dir / f"{prefix}_{lang}.wav"
        print(f"\n── Синтезирам [{lang}] ──────────────────")
        controllable_clone(
            text=text,
            reference_wav=reference_wav,
            output_path=out_path,
            style=style,
        )
        results[lang] = out_path

    print(f"\n✓ Дублажът завърши. Файлове в: {out_dir}")
    return results


def dub_integra_lesson(
    translations: dict[str, str],
    lesson_name: str = "lesson",
) -> dict[str, Path]:
    """Shortcut за обучителни материали на Integra Method."""
    cfg = load_config()
    ref = cfg["alex_voice"]["sample"]
    style = cfg["alex_voice"]["style"]
    return dub_multilingual(
        translations=translations,
        reference_wav=ref,
        output_dir=f"output/dub/{lesson_name}",
        style=style,
        prefix=lesson_name,
    )


if __name__ == "__main__":
    # Примерен урок на 4 езика
    example = {
        "bg": "Добре дошли в първи урок на Integra Method. Днес ще разгледаме основите.",
        "en": "Welcome to the first lesson of Integra Method. Today we cover the basics.",
        "de": "Willkommen zur ersten Lektion der Integra Method. Heute behandeln wir die Grundlagen.",
        "ru": "Добро пожаловать на первый урок метода Интегра. Сегодня мы рассмотрим основы.",
    }
    dub_integra_lesson(example, lesson_name="lesson_01")
