#!/usr/bin/env bash
# Клонира гласа на Алекс върху произволен текст
# Употреба: ./scripts/clone_alex.sh "Текстът, който искаш да озвучиш" [controllable|ultimate]
cd "$(dirname "$0")/.."

TEXT="${1:-Добре дошли в Integra Method.}"
MODE="${2:-controllable}"

python - <<EOF
from src.clone import clone_for_integra
clone_for_integra(
    text="""$TEXT""",
    mode="$MODE",
    output_name="alex_output.wav",
)
EOF

echo "Готово: output/alex_output.wav"
