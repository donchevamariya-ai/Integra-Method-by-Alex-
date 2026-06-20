#!/usr/bin/env bash
# Генерира медитация от скрипт файл (един ред = един сегмент)
# Употреба: ./scripts/generate_meditation.sh content/meditations/intro.txt
cd "$(dirname "$0")/.."

SCRIPT_FILE="${1:-content/meditations/intro.txt}"

if [[ ! -f "$SCRIPT_FILE" ]]; then
  echo "Файлът '$SCRIPT_FILE' не е намерен."
  exit 1
fi

python - <<EOF
from pathlib import Path
from src.meditate import generate_meditation
from src.model import load_config

cfg = load_config()
ref = cfg["alex_voice"]["sample"]

lines = [l.strip() for l in Path("$SCRIPT_FILE").read_text(encoding="utf-8").splitlines() if l.strip()]
name = Path("$SCRIPT_FILE").stem

generate_meditation(
    segments=lines,
    output_path=f"output/meditations/{name}.wav",
    reference_wav=ref,
    pause_between=4.0,
)
EOF
