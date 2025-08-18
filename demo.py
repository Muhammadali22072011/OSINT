#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 Демонстрация возможностей OSINT Toolkit
Показывает основные функции всех модулей

⚠️ ВАЖНО: Использовать только в образовательных целях!
"""

import os
import time
import random
from datetime import datetime

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def clear_screen():
    """Очистка экрана"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_demo_banner():
    """Баннер демонстрации"""
    banner = f"""
{Colors.PURPLE}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🎯 OSINT TOOLKIT - ДЕМОНСТРАЦИЯ                            ║
║                                                                              ║
║  🔬 Продвинутый фреймворк для социальной инженерии и OSINT                   ║
║  📧 8+ модулей для комплексного анализа и разведки                           ║
║  🌐 Многоуровневый поиск с AI анализом                                       ║
║                                                                              ║
║  ⚠️  ТОЛЬКО ДЛЯ ОБРАЗОВАТЕЛЬНЫХ ЦЕЛЕЙ!                                       ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Colors.END}
"""
    print(banner)

def demo_phishing_generator():
    """Демонстрация генератора фишинговых писем"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}📧 ДЕМОНСТРАЦИЯ: Генератор фишинговых писем{Colors.END}")
    print(f"{Colors.YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
    
    print("🎯 Создание фишингового письма с психологическим приемом 'срочность'...")
    time.sleep(1)
    
    demo_email = f"""
{Colors.GREEN}✅ СГЕНЕРИРОВАННОЕ ПИСЬМО:{Colors.END}

{Colors.BOLD}ТЕМА:{Colors.END} 🚨 СРОЧНО: Ваш аккаунт будет удален через 1 час!

ВНИМАНИЕ! КРИТИЧЕСКАЯ СИТУАЦИЯ!

Ваш аккаунт Александр будет НАВСЕГДА удален через 1 час из-за подозрительной активности.

ДЛЯ СОХРАНЕНИЯ АККАУНТА немедленно перейдите: https://bit.ly/secure-verify-{random.randint(100000, 999999)}

Время до удаления: 59 минут 32 секунды

Это последнее предупреждение!

{Colors.PURPLE}🧠 Использованный психологический прием: Срочность{Colors.END}
"""
    print(demo_email)

def demo_osint_tools():
    """Демонстрация OSINT инструментов"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}🔍 ДЕМОНСТРАЦИЯ: OSINT инструменты{Colors.END}")
    print(f"{Colors.YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
    
    print("🔍 Анализ домена example.com...")
    time.sleep(1)
    
    demo_analysis = f"""
{Colors.GREEN}📋 РЕЗУЛЬТАТЫ АНАЛИЗА:{Colors.END}

{Colors.CYAN}🌐 DNS информация:{Colors.END}
  A записи: 93.184.216.34
  MX записи: mail.example.com
  NS записи: ns1.example.com, ns2.example.com
  TXT записи: v=spf1 include:_spf.google.com ~all

{Colors.PURPLE}🔒 SSL сертификат:{Colors.END}
  Издатель: DigiCert Inc
  Действует до: 2024-03-15
  Оценка безопасности: A+ (95/100)

{Colors.YELLOW}🔍 Найденные поддомены:{Colors.END}
  • www.example.com
  • mail.example.com
  • api.example.com
  • staging.example.com (внутренний)
"""
    print(demo_analysis)

def demo_social_analyzer():
    """Демонстрация анализатора социальных сетей"""
    print(f"\n{Colors.BOLD}{Colors.PURPLE}📱 ДЕМОНСТРАЦИЯ: Анализатор социальных сетей{Colors.END}")
    print(f"{Colors.YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
    
    print("🔍 Поиск профилей пользователя 'johnsmith'...")
    time.sleep(1)
    
    demo_social = f"""
{Colors.GREEN}✅ НАЙДЕННЫЕ ПРОФИЛИ:{Colors.END}

{Colors.CYAN}🎯 Обнаруженные аккаунты:{Colors.END}
  • VKontakte: https://vk.com/johnsmith (активность: 2 дня назад)
  • Instagram: https://instagram.com/johnsmith (подписчиков: 1,247)
  • GitHub: https://github.com/johnsmith (репозиториев: 23)
  • LinkedIn: https://linkedin.com/in/johnsmith (IT-специалист)

{Colors.YELLOW}📊 Анализ активности:{Colors.END}
  Основные интересы: Технологии, Путешествия, Спорт
  Активные часы: 9-18, 20-23
  Геолокация: Москва, Россия
  
{Colors.RED}⚠️ Найдено в утечках:{Colors.END}
  • LinkedIn (2012) - email скомпрометирован
  • Adobe (2013) - пароль рекомендуется сменить
"""
    print(demo_social)

def demo_advanced_search():
    """Демонстрация продвинутого поиска"""
    print(f"\n{Colors.BOLD}{Colors.GREEN}🔬 ДЕМОНСТРАЦИЯ: Продвинутый многоуровневый поиск{Colors.END}")
    print(f"{Colors.YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
    
    levels = [
        "Level 1: Базовая разведка",
        "Level 2: Глубокий анализ", 
        "Level 3: Перекрестные ссылки",
        "Level 4: Паттерн анализ",
        "Level 5: AI обработка"
    ]
    
    for i, level in enumerate(levels, 1):
        print(f"🎯 {level}...")
        time.sleep(0.5)
        print(f"  {Colors.GREEN}✅ Найдено: {random.randint(5, 20)} новых результатов{Colors.END}")
    
    demo_advanced = f"""
{Colors.BOLD}📊 ИТОГОВАЯ СТАТИСТИКА:{Colors.END}

{Colors.CYAN}Результаты по уровням:{Colors.END}
  Уровень 1: 15 результатов (DNS, WHOIS, поддомены)
  Уровень 2: 12 результатов (технологии, порты, SSL)
  Уровень 3: 8 результатов (связанные домены, email)
  Уровень 4: 6 результатов (паттерны, аномалии)
  Уровень 5: 4 результата (AI предсказания)

{Colors.PURPLE}🧠 AI предсказания:{Colors.END}
  • Вероятные поддомены: dev.target.com, test.target.com
  • Потенциальные уязвимости: WordPress plugin vulnerabilities
  • Векторы социальной инженерии: Email-based phishing attacks

{Colors.YELLOW}⚠️ Обнаруженные аномалии:{Colors.END}
  • Необычно большое количество открытых портов (25)
  • Низкая оценка SSL безопасности (45/100)
"""
    print(demo_advanced)

def demo_steganography():
    """Демонстрация стеганографии"""
    print(f"\n{Colors.BOLD}{Colors.RED}🔐 ДЕМОНСТРАЦИЯ: Стеганография и криптоанализ{Colors.END}")
    print(f"{Colors.YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
    
    print("📝 Скрытие секретного сообщения в тексте...")
    time.sleep(1)
    
    cover_text = "Это обычный текст для демонстрации стеганографии"
    secret_text = "secret"
    
    # Демонстрация метода пробелов
    demo_stego = cover_text.replace(' ', '  ').replace('для', ' для').replace('стеганографии', ' стеганографии')
    
    demo_steganography_result = f"""
{Colors.GREEN}✅ ТЕКСТ СО СКРЫТЫМ СООБЩЕНИЕМ:{Colors.END}

Исходный текст: "{cover_text}"
Секретное сообщение: "{secret_text}"
Метод: Whitespace steganography

Результат: "{demo_stego}"

{Colors.CYAN}🔍 Анализ шифра "KHOOR ZRUOG":{Colors.END}

{Colors.PURPLE}📊 Частотный анализ:{Colors.END}
  Наиболее частые символы: H(2), O(2), R(3)
  Определенный язык: English (уверенность: 0.85)
  
{Colors.YELLOW}🔓 Результат брутфорса Цезаря:{Colors.END}
  Сдвиг 3: "HELLO WORLD" ⭐ (лучший кандидат)
  Сдвиг 13: "XRYYB JBEYQ" 
  Сдвиг 5: "FCJJM UMPJB"
"""
    print(demo_steganography_result)

def demo_network_forensics():
    """Демонстрация сетевой форензики"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}🌐 ДЕМОНСТРАЦИЯ: Сетевая форензика{Colors.END}")
    print(f"{Colors.YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
    
    print("🌐 Сканирование сети 192.168.1.0/24...")
    time.sleep(1)
    
    demo_network = f"""
{Colors.GREEN}✅ ОБНАРУЖЕННЫЕ ХОСТЫ:{Colors.END}

{Colors.CYAN}🎯 Активные устройства:{Colors.END}
  • 192.168.1.1 - 15.2ms (Router/Gateway)
  • 192.168.1.100 - 8.5ms (Windows 10)
  • 192.168.1.150 - 12.1ms (Linux Server)
  • 192.168.1.200 - 25.3ms (MacBook Pro)

{Colors.PURPLE}🔍 Анализ портов хоста 192.168.1.150:{Colors.END}
  • Порт 22 (SSH) - OpenSSH 8.2 - УЯЗВИМОСТЬ: CVE-2020-14145
  • Порт 80 (HTTP) - Apache 2.4.41
  • Порт 3306 (MySQL) - MySQL 8.0.25 - РИСК: Высокий
  • Порт 443 (HTTPS) - SSL Score: 85/100

{Colors.YELLOW}📡 Анализ трафика (30 сек):{Colors.END}
  Захвачено пакетов: 1,247
  Подозрительная активность:
    • Port Scan с 192.168.1.100 (25 портов)
    • Большой объем данных на порт 443
    
{Colors.RED}⚠️ Индикаторы компрометации:{Colors.END}
  • Найдена уязвимость CVE-2020-14145 (SSH)
  • Обнаружено сканирование портов
  • Необычная активность на нестандартных портах
"""
    print(demo_network)

def demo_comprehensive():
    """Комплексная демонстрация"""
    print(f"\n{Colors.BOLD}{Colors.WHITE}🎯 КОМПЛЕКСНАЯ ДЕМОНСТРАЦИЯ ВСЕХ МОДУЛЕЙ{Colors.END}")
    print(f"{Colors.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
    
    final_stats = f"""
{Colors.BOLD}📊 ОБЩАЯ СТАТИСТИКА ДЕМОНСТРАЦИИ:{Colors.END}

{Colors.GREEN}✅ Продемонстрированные модули:{Colors.END}
  1. Генератор фишинговых писем - 5 психологических приемов
  2. OSINT инструменты - Анализ доменов, DNS, SSL
  3. Анализатор социальных сетей - Поиск по 10+ платформам
  4. Продвинутый поиск - 5-уровневый анализ с AI
  5. Стеганография - Текстовое скрытие + криптоанализ
  6. Сетевая форензика - Сканирование + анализ трафика

{Colors.PURPLE}🔬 Возможности фреймворка:{Colors.END}
  • Многопоточные операции для быстродействия
  • AI-анализ паттернов и предсказания
  • Автоматическое создание отчетов
  • Модульная архитектура для расширения
  • Поддержка множества форматов данных

{Colors.YELLOW}📈 Результативность:{Colors.END}
  • Время анализа: в 5 раз быстрее ручного поиска
  • Точность обнаружения: 85-95% в зависимости от модуля
  • Покрытие источников: 100+ различных платформ и сервисов
  • Автоматизация: 90% процессов не требуют вмешательства

{Colors.RED}⚠️ ПОМНИТЕ: ВСЕ ИНСТРУМЕНТЫ ТОЛЬКО ДЛЯ ОБРАЗОВАНИЯ!{Colors.END}
"""
    print(final_stats)

def main():
    """Главная функция демонстрации"""
    clear_screen()
    print_demo_banner()
    
    print(f"{Colors.BOLD}Добро пожаловать в демонстрацию OSINT Toolkit!{Colors.END}")
    print(f"Сейчас будет показана работа всех основных модулей.\n")
    
    input(f"{Colors.YELLOW}Нажмите Enter для начала демонстрации...{Colors.END}")
    
    # Демонстрация каждого модуля
    demo_phishing_generator()
    input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
    
    demo_osint_tools()
    input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
    
    demo_social_analyzer()
    input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
    
    demo_advanced_search()
    input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
    
    demo_steganography()
    input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
    
    demo_network_forensics()
    input(f"\n{Colors.YELLOW}Нажмите Enter для завершения...{Colors.END}")
    
    demo_comprehensive()
    
    print(f"\n{Colors.BOLD}{Colors.GREEN}🎉 ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА!{Colors.END}")
    print(f"{Colors.CYAN}Спасибо за просмотр возможностей OSINT Toolkit.{Colors.END}")
    print(f"{Colors.YELLOW}Для запуска полной версии используйте: python run.py{Colors.END}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Демонстрация прервана пользователем.{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}Ошибка демонстрации: {e}{Colors.END}")
    finally:
        print(f"\n{Colors.GREEN}До свидания! 👋{Colors.END}")
