#!/usr/bin/env bash
# Проверява системните изисквания преди инсталация на VoxCPM2
cd "$(dirname "$0")/.."
python -m src.diagnose
