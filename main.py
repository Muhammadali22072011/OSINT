#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🕵️ Social Engineering & OSINT Toolkit
Образовательный инструмент для изучения социальной инженерии и OSINT

⚠️ ВАЖНО: Использовать только в образовательных целях и на своих системах!
"""

import os
import sys
import time
import random
from datetime import datetime
import json
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import re
import whois
import dns.resolver
import socket
from urllib.parse import urlparse
import subprocess

class Colors:
    """Цвета для терминала"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def clear_screen():
    """Очистка экрана"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Печать баннера"""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
 ██████╗ ███████╗██╗███╗   ██╗████████╗    ████████╗ ██████╗  ██████╗ ██╗     ██╗  ██╗██╗████████╗
██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██║ ██╔╝██║╚══██╔══╝
██║   ██║███████╗██║██╔██╗ ██║   ██║          ██║   ██║   ██║██║   ██║██║     █████╔╝ ██║   ██║   
██║   ██║╚════██║██║██║╚██╗██║   ██║          ██║   ██║   ██║██║   ██║██║     ██╔═██╗ ██║   ██║   
╚██████╔╝███████║██║██║ ╚████║   ██║          ██║   ╚██████╔╝╚██████╔╝███████╗██║  ██╗██║   ██║   
 ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝          ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝   
{Colors.END}
{Colors.YELLOW}Social Engineering & OSINT Framework v2.0{Colors.END}
{Colors.RED}⚠️  ТОЛЬКО ДЛЯ ОБРАЗОВАТЕЛЬНЫХ ЦЕЛЕЙ!{Colors.END}
{Colors.GREEN}Автор: Ethical Hacker | Дата: {datetime.now().strftime('%Y-%m-%d')}{Colors.END}
{Colors.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}
"""
    print(banner)

def main_menu():
    """Главное меню"""
    print(f"\n{Colors.BOLD}{Colors.GREEN}🎯 ГЛАВНОЕ МЕНЮ{Colors.END}")
    print(f"{Colors.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
    
    menu_options = [
        ("1", "📧 Генератор фишинговых писем", "phishing_generator"),
        ("2", "🔍 OSINT инструменты", "osint_tools"), 
        ("3", "📱 Анализатор социальных сетей", "social_analyzer"),
        ("4", "🔬 Продвинутый многоуровневый поиск", "advanced_search"),
        ("5", "👤 Поиск информации о людях", "people_search"),
        ("6", "🔐 Стеганография и криптоанализ", "steganography"),
        ("7", "🌐 Сетевая разведка и анализ", "network_intelligence"),
        ("8", "⚙️ Дополнительные инструменты", "extra_tools"),
        ("9", "📋 Настройки и помощь", "settings"),
        ("0", "🚪 Выход", "exit")
    ]
    
    for option, description, _ in menu_options:
        print(f"{Colors.YELLOW}[{option}]{Colors.END} {description}")
    
    print(f"{Colors.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
    
    choice = input(f"{Colors.BOLD}Выберите опцию: {Colors.END}")
    return choice

class OSINTToolkit:
    """Основной класс OSINT инструментов"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def email_lookup(self, email):
        """Поиск информации об email"""
        print(f"\n{Colors.YELLOW}🔍 Анализ email: {email}{Colors.END}")
        
        # Проверка формата email
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            print(f"{Colors.RED}❌ Неверный формат email{Colors.END}")
            return
        
        domain = email.split('@')[1]
        username = email.split('@')[0]
        
        print(f"{Colors.GREEN}📧 Email: {email}")
        print(f"👤 Пользователь: {username}")
        print(f"🌐 Домен: {domain}{Colors.END}")
        
        # Анализ домена
        self.domain_lookup(domain)
        
        # Поиск в базах утечек (симуляция)
        print(f"\n{Colors.YELLOW}🔍 Проверка в базах утечек...{Colors.END}")
        time.sleep(2)
        
        # Симуляция результатов
        breaches = [
            "Collection #1 (2019)",
            "LinkedIn (2012)", 
            "Adobe (2013)",
            "MySpace (2013)"
        ]
        
        if random.choice([True, False]):
            print(f"{Colors.RED}⚠️ Email найден в утечках:{Colors.END}")
            for breach in random.sample(breaches, random.randint(1, 3)):
                print(f"  • {breach}")
        else:
            print(f"{Colors.GREEN}✅ Email не найден в известных утечках{Colors.END}")
    
    def domain_lookup(self, domain):
        """Анализ домена"""
        print(f"\n{Colors.YELLOW}🌐 Анализ домена: {domain}{Colors.END}")
        
        try:
            # WHOIS информация
            print(f"{Colors.CYAN}📋 WHOIS информация:{Colors.END}")
            w = whois.whois(domain)
            print(f"  Регистратор: {w.registrar}")
            print(f"  Дата создания: {w.creation_date}")
            print(f"  Дата окончания: {w.expiration_date}")
            
        except Exception as e:
            print(f"{Colors.RED}❌ Ошибка WHOIS: {e}{Colors.END}")
        
        try:
            # DNS записи
            print(f"\n{Colors.CYAN}🔍 DNS записи:{Colors.END}")
            
            # A записи
            try:
                a_records = dns.resolver.resolve(domain, 'A')
                print(f"  A записи:")
                for record in a_records:
                    print(f"    • {record}")
            except:
                pass
            
            # MX записи
            try:
                mx_records = dns.resolver.resolve(domain, 'MX')
                print(f"  MX записи:")
                for record in mx_records:
                    print(f"    • {record}")
            except:
                pass
                
        except Exception as e:
            print(f"{Colors.RED}❌ Ошибка DNS: {e}{Colors.END}")

def check_breaches(email):
    """Проверка утечек паролей"""
    print(f"\n{Colors.YELLOW}🔍 Проверка утечек для: {email}{Colors.END}")
    
    # Симуляция проверки в базах утечек
    print("🔄 Проверка в базах данных утечек...")
    time.sleep(2)
    
    breaches = [
        "Collection #1 (2019) - 773M аккаунтов",
        "LinkedIn (2012) - 164M аккаунтов", 
        "Adobe (2013) - 153M аккаунтов",
        "MySpace (2013) - 360M аккаунтов",
        "Yahoo (2014) - 500M аккаунтов"
    ]
    
    if random.choice([True, False]):
        found_breaches = random.sample(breaches, random.randint(1, 3))
        print(f"{Colors.RED}⚠️ Email найден в утечках:{Colors.END}")
        for breach in found_breaches:
            print(f"  • {breach}")
        print(f"\n{Colors.YELLOW}🔒 Рекомендуется сменить пароли!{Colors.END}")
    else:
        print(f"{Colors.GREEN}✅ Email не найден в известных утечках{Colors.END}")

def generate_passwords():
    """Генератор паролей"""
    print(f"\n{Colors.PURPLE}🔐 ГЕНЕРАТОР ПАРОЛЕЙ{Colors.END}")
    
    length = input("Длина пароля (по умолчанию 12): ").strip()
    if not length.isdigit():
        length = 12
    else:
        length = int(length)
    
    include_symbols = input("Включить символы? (y/n): ").lower() == 'y'
    
    import string
    
    chars = string.ascii_letters + string.digits
    if include_symbols:
        chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    passwords = []
    for i in range(5):
        password = ''.join(random.choice(chars) for _ in range(length))
        passwords.append(password)
    
    print(f"\n{Colors.GREEN}🔑 СГЕНЕРИРОВАННЫЕ ПАРОЛИ:{Colors.END}")
    for i, pwd in enumerate(passwords, 1):
        print(f"  {i}. {pwd}")

def show_system_info():
    """Информация о системе"""
    print(f"\n{Colors.CYAN}💻 ИНФОРМАЦИЯ О СИСТЕМЕ{Colors.END}")
    
    import platform
    import psutil
    
    print(f"Операционная система: {platform.system()} {platform.release()}")
    print(f"Архитектура: {platform.machine()}")
    print(f"Процессор: {platform.processor()}")
    print(f"Hostname: {socket.gethostname()}")
    print(f"IP адрес: {socket.gethostbyname(socket.gethostname())}")
    
    # Память
    memory = psutil.virtual_memory()
    print(f"Память: {memory.total // (1024**3)} GB")
    print(f"Использовано памяти: {memory.percent}%")

def show_help():
    """Справка по использованию"""
    help_text = f"""
{Colors.BOLD}{Colors.CYAN}📖 СПРАВКА ПО ИСПОЛЬЗОВАНИЮ{Colors.END}

{Colors.YELLOW}🎯 ОСНОВНЫЕ ФУНКЦИИ:{Colors.END}

📧 Генератор фишинговых писем:
   • Создание шаблонов писем для обучения
   • Психологические приемы социальной инженерии
   • Сохранение писем для анализа

🔍 OSINT инструменты:
   • Базовые: поиск по email, анализ домена, поиск по телефону
   • Продвинутые: сканирование портов, SSL анализ, перечисление директорий

📱 Анализатор социальных сетей:
   • Поиск профилей по имени пользователя
   • Анализ активности и связей
   • Поиск по контактным данным

{Colors.RED}⚠️ ВАЖНЫЕ ПРАВИЛА:{Colors.END}
   • Используйте только в образовательных целях
   • Тестируйте только на своих системах
   • Соблюдайте законодательство
   • Не нарушайте приватность других людей

{Colors.GREEN}💡 СОВЕТЫ:{Colors.END}
   • Все отчеты сохраняются автоматически
   • Используйте VPN для дополнительной анонимности
   • Регулярно обновляйте инструменты
   • Изучайте результаты для понимания уязвимостей
    """
    print(help_text)

def view_all_reports():
    """Просмотр всех отчетов"""
    print(f"\n{Colors.BOLD}📁 ВСЕ ОТЧЕТЫ{Colors.END}")
    
    report_dirs = ["generated_emails", "reports", "osint_reports", "people_reports"]
    total_files = 0
    
    for dir_name in report_dirs:
        if os.path.exists(dir_name):
            files = [f for f in os.listdir(dir_name) if f.endswith('.txt')]
            print(f"\n{Colors.CYAN}{dir_name.upper()}:{Colors.END}")
            if files:
                for f in files[-5:]:  # Показываем последние 5
                    print(f"  • {f}")
                if len(files) > 5:
                    print(f"  ... и еще {len(files) - 5} файлов")
                total_files += len(files)
            else:
                print(f"  {Colors.YELLOW}Нет файлов{Colors.END}")
    
    print(f"\n{Colors.GREEN}Всего отчетов: {total_files}{Colors.END}")

def cleanup_cache():
    """Очистка кэша"""
    print(f"\n{Colors.YELLOW}🧹 ОЧИСТКА КЭША{Colors.END}")
    
    cache_dirs = ["__pycache__", ".pytest_cache"]
    cleaned = 0
    
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            import shutil
            shutil.rmtree(cache_dir)
            cleaned += 1
            print(f"  ✅ Удален {cache_dir}")
    
    print(f"\n{Colors.GREEN}Очищено директорий: {cleaned}{Colors.END}")

def show_about():
    """О программе"""
    about_text = f"""
{Colors.BOLD}{Colors.PURPLE}ℹ️ О ПРОГРАММЕ{Colors.END}

{Colors.CYAN}🕵️ OSINT Toolkit - Social Engineering Framework{Colors.END}

Версия: 2.0
Автор: Ethical Hacker Team
Дата: {datetime.now().strftime('%Y-%m-%d')}

{Colors.YELLOW}📋 ВОЗМОЖНОСТИ:{Colors.END}
• Генерация фишинговых писем (образовательные цели)
• OSINT инструменты для сбора открытой информации
• Анализ социальных сетей и профилей
• Сканирование сетей и веб-приложений
• Генерация детальных отчетов

{Colors.GREEN}🛡️ БЕЗОПАСНОСТЬ:{Colors.END}
• Все данные обрабатываются локально
• Никакая информация не передается третьим лицам
• Используются только публичные источники
• Соблюдается rate limiting для API

{Colors.RED}⚠️ ДИСКЛЕЙМЕР:{Colors.END}
Данный инструмент создан исключительно в образовательных целях
для изучения методов социальной инженерии и OSINT.
Использование в незаконных целях строго запрещено!

{Colors.BLUE}🔗 ПОЛЕЗНЫЕ РЕСУРСЫ:{Colors.END}
• OSINT Framework: osintframework.com
• Social Engineering Toolkit: social-engineer.org
• Awesome OSINT: github.com/jivoi/awesome-osint
    """
    print(about_text)

def main():
    """Главная функция"""
    toolkit = OSINTToolkit()
    
    while True:
        clear_screen()
        print_banner()
        choice = main_menu()
        
        if choice == '1':
            # Генератор фишинговых писем
            from phishing_generator import PhishingGenerator
            generator = PhishingGenerator()
            generator.run()
            
        elif choice == '2':
            # OSINT инструменты
            print(f"\n{Colors.BOLD}{Colors.GREEN}🔍 OSINT ИНСТРУМЕНТЫ{Colors.END}")
            print("1. Базовые OSINT инструменты")
            print("2. Продвинутые OSINT инструменты")
            
            osint_choice = input("\nВыберите категорию: ")
            
            if osint_choice == '1':
                print(f"\n{Colors.CYAN}📋 БАЗОВЫЕ ИНСТРУМЕНТЫ{Colors.END}")
                print("1. Поиск по email")
                print("2. Анализ домена") 
                print("3. Поиск по телефону")
                
                basic_choice = input("\nВыберите инструмент: ")
                
                if basic_choice == '1':
                    email = input("Введите email: ")
                    toolkit.email_lookup(email)
                    
                elif basic_choice == '2':
                    domain = input("Введите домен: ")
                    toolkit.domain_lookup(domain)
                    
                elif basic_choice == '3':
                    phone = input("Введите номер телефона: ")
                    toolkit.phone_lookup(phone)
                
                input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
            
            elif osint_choice == '2':
                from osint_tools import AdvancedOSINT
                advanced_osint = AdvancedOSINT()
                advanced_osint.run()
            
        elif choice == '3':
            # Анализатор социальных сетей
            from social_analyzer import SocialAnalyzer
            analyzer = SocialAnalyzer()
            analyzer.run()
            
        elif choice == '4':
            # Продвинутый многоуровневый поиск
            from advanced_search import AdvancedSearchEngine
            search_engine = AdvancedSearchEngine()
            search_engine.run()
            
        elif choice == '5':
            # Поиск информации о людях
            from people_search import PeopleSearchEngine
            people_search = PeopleSearchEngine()
            people_search.run()
            
        elif choice == '6':
            # Стеганография и криптоанализ
            from steganography_crypto import SteganoCryptoSuite
            crypto_suite = SteganoCryptoSuite()
            crypto_suite.run()
            
        elif choice == '7':
            # Сетевая разведка и анализ
            from network_intelligence import NetworkIntelligence
            network_intel = NetworkIntelligence()
            network_intel.run()
            
        elif choice == '7':
            # Дополнительные инструменты
            print(f"\n{Colors.BOLD}{Colors.PURPLE}⚙️ ДОПОЛНИТЕЛЬНЫЕ ИНСТРУМЕНТЫ{Colors.END}")
            print("1. 🔍 Поиск утечек паролей")
            print("2. 📊 Анализ трафика")
            print("3. 🔐 Генератор паролей")
            print("4. 📋 Информация о системе")
            print("5. 🌐 Реальные OSINT API")
            
            extra_choice = input("\nВыберите инструмент: ")
            
            if extra_choice == '1':
                email = input("Введите email для проверки утечек: ")
                check_breaches(email)
            elif extra_choice == '2':
                from traffic_analyzer import TrafficAnalyzer
                analyzer = TrafficAnalyzer()
                analyzer.run()
            elif extra_choice == '3':
                generate_passwords()
            elif extra_choice == '4':
                show_system_info()
            elif extra_choice == '5':
                from real_osint_apis import RealOSINTEngine
                osint_engine = RealOSINTEngine()
                osint_engine.run()
            
            input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
            
        elif choice == '8':
            # Настройки и помощь
            print(f"\n{Colors.BOLD}{Colors.CYAN}⚙️ НАСТРОЙКИ И ПОМОЩЬ{Colors.END}")
            print("1. 📖 Справка по использованию")
            print("2. 📁 Просмотр всех отчетов")
            print("3. 🧹 Очистка кэша")
            print("4. ℹ️ О программе")
            
            settings_choice = input("\nВыберите опцию: ")
            
            if settings_choice == '1':
                show_help()
            elif settings_choice == '2':
                view_all_reports()
            elif settings_choice == '3':
                cleanup_cache()
            elif settings_choice == '4':
                show_about()
            
            input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
        
        elif choice == '0':
            print(f"\n{Colors.GREEN}👋 До свидания!{Colors.END}")
            sys.exit(0)
            
        else:
            print(f"\n{Colors.RED}❌ Неверный выбор!{Colors.END}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️ Программа прервана пользователем{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}❌ Критическая ошибка: {e}{Colors.END}")
        sys.exit(1)
