#!/bin/bash

# OSINT Toolkit - Social Engineering Framework
# Скрипт запуска для Linux/macOS

clear

echo "=================================================================="
echo "  🕵️ OSINT Toolkit - Social Engineering Framework"
echo "=================================================================="
echo ""

# Проверка наличия Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден!"
    echo "Пожалуйста, установите Python 3.7+ "
    exit 1
fi

echo "✅ Python3 найден"

# Проверка версии Python
python3 -c "import sys; exit(0 if sys.version_info >= (3, 7) else 1)"
if [ $? -ne 0 ]; then
    echo "❌ Требуется Python 3.7 или выше!"
    exit 1
fi

echo "✅ Версия Python подходит"

# Запуск программы
echo "🚀 Запуск OSINT Toolkit..."
echo ""

python3 run.py

echo ""
echo "👋 Программа завершена"
