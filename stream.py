"""Real-time streaming synthesis — за live гласови асистенти."""

from __future__ import annotations

import time
import sounddevice as sd
import numpy as np
from pathlib import Path
from .model import get_model, load_config


def stream_realtime(
    text_chunks: list[str],
    reference_wav: str | Path | None = None,
    style: str = "спокоен, ясен",
    measure_rtf: bool = True,
) -> float:
    """
    Стриймва синтезирана реч в реално време чрез sounddevice.
    Връща измерения RTF (Real-Time Factor).

    RTF < 1.0 = по-бърз от реално-временен (целта е ~0.3 на RTX 4090).
    """
    model = get_model()
    cfg = load_config()
    sr = cfg["output"]["sample_rate"]

    total_audio_sec = 0.0
    total_wall_sec = 0.0

    print("── Стрийминг старт ──────────────────────")
    for chunk in text_chunks:
        t0 = time.perf_counter()

        if reference_wav:
            audio = model.controllable_clone(
                text=chunk,
                reference=str(reference_wav),
                style=style,
                sample_rate=sr,
                stream=True,
            )
        else:
            audio = model.synthesize(text=chunk, sample_rate=sr, stream=True)

        audio_arr = np.array(audio, dtype=np.float32)
        sd.play(audio_arr, samplerate=sr)
        sd.wait()

        wall = time.perf_counter() - t0
        audio_sec = len(audio_arr) / sr
        total_audio_sec += audio_sec
        total_wall_sec += wall

        if measure_rtf:
            rtf = wall / audio_sec if audio_sec > 0 else 0
            print(f"  chunk RTF: {rtf:.3f}  ({audio_sec:.1f}s аудио / {wall:.1f}s стена)")

    rtf_overall = total_wall_sec / total_audio_sec if total_audio_sec > 0 else 0
    print(f"\n✓ Общ RTF: {rtf_overall:.3f}")
    print("─────────────────────────────────────────")
    return rtf_overall


if __name__ == "__main__":
    cfg = load_config()
    ref = cfg["alex_voice"]["sample"]

    stream_realtime(
        text_chunks=["Здравей,", " как", " си?"],
        reference_wav=ref,
        style="топъл, приятелски",
    )
