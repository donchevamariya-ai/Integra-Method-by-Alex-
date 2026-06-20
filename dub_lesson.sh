#!/usr/bin/env bash
# Дублира урок на 4 езика с гласа на Алекс
# Употреба: ./scripts/dub_lesson.sh lesson_01
cd "$(dirname "$0")/.."

LESSON="${1:-lesson_01}"

python - <<EOF
from src.dub import dub_integra_lesson

# Попълни преводите тук или зареди от JSON файл
translations = {
    "bg": "Добре дошли в Integra Method. Днес ще разгледаме основите.",
    "en": "Welcome to Integra Method. Today we cover the basics.",
    "de": "Willkommen bei Integra Method. Heute behandeln wir die Grundlagen.",
    "ru": "Добро пожаловать в Integra Method. Сегодня мы рассмотрим основы.",
}

dub_integra_lesson(translations, lesson_name="$LESSON")
EOF
