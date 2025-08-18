#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Скрипт запуска OSINT Toolkit
Проверяет зависимости и запускает основную программу
"""

import sys
import subprocess
import importlib.util
import os

def check_python_version():
    """Проверка версии Python"""
    if sys.version_info < (3, 7):
        print("❌ Требуется Python 3.7 или выше!")
        print(f"Текущая версия: {sys.version}")
        sys.exit(1)
    else:
        print(f"✅ Python {sys.version.split()[0]} - OK")

def check_dependencies():
    """Проверка зависимостей"""
    required_packages = [
        'requests', 'whois', 'dns', 'bs4', 'colorama', 'psutil'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        spec = importlib.util.find_spec(package)
        if spec is None:
            missing_packages.append(package)
        else:
            print(f"✅ {package} - установлен")
    
    if missing_packages:
        print(f"\n❌ Отсутствуют пакеты: {', '.join(missing_packages)}")
        print("\n🔧 Установите зависимости командой:")
        print("pip install -r requirements.txt")
        
        install = input("\nУстановить автоматически? (y/n): ").lower()
        if install == 'y':
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
                print("✅ Зависимости установлены!")
            except subprocess.CalledProcessError:
                print("❌ Ошибка установки зависимостей")
                sys.exit(1)
        else:
            sys.exit(1)

def create_directories():
    """Создание необходимых директорий"""
    dirs = ['generated_emails', 'reports', 'osint_reports', 'people_reports']
    
    for dir_name in dirs:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print(f"📁 Создана директория: {dir_name}")

def show_disclaimer():
    """Показать дисклеймер"""
    disclaimer = """
╔══════════════════════════════════════════════════════════════╗
║                    ⚠️  ВАЖНОЕ ПРЕДУПРЕЖДЕНИЕ  ⚠️                  ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Данный инструмент создан ИСКЛЮЧИТЕЛЬНО в образовательных    ║
║  целях для изучения методов социальной инженерии и OSINT.    ║
║                                                              ║
║  🔴 ЗАПРЕЩЕНО использовать для:                               ║
║     • Реальных фишинговых атак                               ║
║     • Преследования людей                                    ║
║     • Нарушения приватности                                  ║
║     • Любой незаконной деятельности                          ║
║                                                              ║
║  ✅ РАЗРЕШЕНО использовать для:                               ║
║     • Изучения кибербезопасности                             ║
║     • Тестирования собственных систем                        ║
║     • Образовательных исследований                           ║
║     • Повышения осведомленности о безопасности               ║
║                                                              ║
║  Автор не несет ответственности за неправомерное             ║
║  использование данного инструмента!                          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
    
    print(disclaimer)
    
    agreement = input("\nВы согласны с условиями использования? (yes/no): ").lower()
    if agreement not in ['yes', 'y', 'да']:
        print("❌ Использование отклонено.")
        sys.exit(0)

def main():
    """Главная функция запуска"""
    print("🕵️ OSINT Toolkit - Инициализация...")
    print("="*50)
    
    # Проверки
    check_python_version()
    check_dependencies()
    create_directories()
    
    print("\n" + "="*50)
    show_disclaimer()
    
    print("\n🚀 Запуск OSINT Toolkit...")
    print("="*50)
    
    # Запуск основной программы
    try:
        from main import main as main_program
        main_program()
    except KeyboardInterrupt:
        print("\n\n⚠️ Программа прервана пользователем")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        print("Обратитесь к разработчикам за помощью")
    finally:
        print("\n👋 До свидания!")

if __name__ == "__main__":
    main()
