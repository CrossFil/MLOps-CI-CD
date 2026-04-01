#!/bin/bash

LOG_FILE="install.log"
exec > >(tee -a "$LOG_FILE") 2>&1

echo "--- Начинаем проверку среды: $(date) ---"

# Функция для проверки и установки через Brew (для macOS)
check_brew_install() {
    if command -v $1 &> /dev/null; then
        echo "✅ $1 уже установлен: $($1 --version | head -n 1)"
    else
        echo "⏳ Устанавливаю $1..."
        brew install $1
    fi
}

# 1. Проверка Homebrew (фундамент для Mac)
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew не найден. Установи его с https://brew.sh/"
    exit 1
fi

# 2. Проверка Docker
if command -v docker &> /dev/null; then
    echo "✅ Docker найден: $(docker --version)"
else
    echo "ℹ️ Docker Desktop лучше установить вручную с сайта docker.com"
fi

# 3. Проверка Python >= 3.9
PYTHON_VER=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))' 2>/dev/null)
if [[ $(echo "$PYTHON_VER >= 3.9" | bc -l) -eq 1 ]]; then
    echo "✅ Python $PYTHON_VER подходит."
else
    echo "⏳ Обновляю Python через brew..."
    brew install python@3.11
fi

# 4. Проверка pip
python3 -m pip install --upgrade pip &> /dev/null
echo "✅ pip обновлен."

# 5. Установка ML-библиотек и Django
echo "📦 Устанавливаю Python-зависимости..."
libs=(django torch torchvision pillow)
for lib in "${libs[@]}"; do
    if python3 -c "import $lib" &> /dev/null; then
        echo "✅ Библиотека $lib уже есть."
    else
        echo "⏳ Устанавливаю $lib..."
        python3 -m pip install $lib
    fi
done

echo "--- Проверка завершена успешно! Подробности в $LOG_FILE ---"
