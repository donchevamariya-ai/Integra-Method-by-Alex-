# VoxCPM2 — Integra Method Voice Studio

TTS проект за клониране, дизайн и многоезично дублиране на глас, базиран на [VoxCPM2](https://github.com/OpenBMB/VoxCPM).

---

## Структура

```
Voice/VoxCPM2/
├── config/
│   └── settings.yaml          # модел, пътища, описание на гласа на Алекс
├── src/
│   ├── model.py               # singleton loader
│   ├── diagnose.py            # проверка на системните изисквания
│   ├── design.py              # Voice Design от текстово описание
│   ├── clone.py               # Controllable + Ultimate Cloning
│   ├── dub.py                 # многоезичен дублажен pipeline
│   ├── meditate.py            # генератор на медитации с паузи
│   └── stream.py              # real-time стрийминг + RTF измерване
├── scripts/
│   ├── run_diagnose.sh        # проверка на системата
│   ├── clone_alex.sh          # клониране на текст с гласа на Алекс
│   ├── dub_lesson.sh          # дублиране на урок на 4 езика
│   └── generate_meditation.sh # генерира медитация от .txt скрипт
├── content/
│   ├── meditations/           # текстови скриптове за медитации
│   └── lessons/               # текстове на уроци по езици
├── samples/                   # референтни WAV файлове (виж samples/README.txt)
├── output/                    # генерирано аудио (не се commit-ва)
└── requirements.txt
```

---

## Бърз старт

### 1. Провери системата
```bash
bash scripts/run_diagnose.sh
```

### 2. Инсталирай зависимостите
```bash
pip install -r requirements.txt
```

### 3. Постави референтен клип
Копирай WAV файл с гласа на Алекс в `samples/alex_reference.wav`.  
Виж `samples/README.txt` за изисквания.

### 4. Клонирай глас
```bash
bash scripts/clone_alex.sh "Текстът, който искаш да озвучиш"
# Изход: output/alex_output.wav
```

### 5. Генерирай медитация
```bash
bash scripts/generate_meditation.sh content/meditations/intro.txt
# Изход: output/meditations/intro.wav
```

### 6. Дублирай урок на 4 езика
```bash
bash scripts/dub_lesson.sh lesson_01
# Изход: output/dub/lesson_01/lesson_01_bg.wav, _en.wav, _de.wav, _ru.wav
```

---

## Режими на клониране

| Режим | Кога | Точност |
|-------|------|---------|
| **Voice Design** | Нямаш аудио семпъл | Средна — от описание |
| **Controllable Cloning** | Имаш 5–15 сек клип, искаш контрол | Висока |
| **Ultimate Cloning** | Официални материали, максимална вярност | Максимална |

---

## Производителност (RTX 4090)

- Стандартен режим: RTF ~0.3
- С vLLM-Omni: RTF ~0.13

---

## Системни изисквания

- Python 3.10–3.12
- PyTorch ≥ 2.5.0
- CUDA ≥ 12.0
- GPU VRAM ≥ 8 GB

---

## Тест без инсталация

Playground: https://huggingface.co/spaces/OpenBMB/VoxCPM-Demo
