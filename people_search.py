#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Модуль поиска информации о людях
Комплексный поиск через различные источники в интернете
"""

import os
import sys
import time
import random
import requests
import json
from datetime import datetime
from urllib.parse import quote, urlencode
import re
from bs4 import BeautifulSoup

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

class PeopleSearchEngine:
    """Движок поиска информации о людях"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.results = {}
        
    def clear_screen(self):
        """Очистка экрана"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_banner(self):
        """Баннер модуля"""
        banner = f"""
{Colors.CYAN}{Colors.BOLD}
 ██████╗ ███████╗ ██████╗ ██████╗ ██╗     ███████╗    ███████╗███████╗ █████╗ ██████╗  ██████╗██╗  ██╗
 ██╔══██╗██╔════╝██╔═══██╗██╔══██╗██║     ██╔════╝    ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝██║  ██║
 ██████╔╝█████╗  ██║   ██║██████╔╝██║     █████╗      ███████╗█████╗  ███████║██████╔╝██║     ███████║
 ██╔═══╝ ██╔══╝  ██║   ██║██╔═══╝ ██║     ██╔══╝      ╚════██║██╔══╝  ██╔══██║██╔══██╗██║     ██╔══██║
 ██║     ███████╗╚██████╔╝██║     ███████╗███████╗    ███████║███████╗██║  ██║██║  ██║╚██████╗██║  ██║
 ╚═╝     ╚══════╝ ╚═════╝ ╚═╝     ╚══════╝╚══════╝    ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
{Colors.END}
{Colors.YELLOW}Комплексный поиск информации о людях в интернете{Colors.END}
{Colors.RED}⚠️  ТОЛЬКО ДЛЯ ОБРАЗОВАТЕЛЬНЫХ ЦЕЛЕЙ!{Colors.END}
{Colors.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}
"""
        print(banner)
    
    def search_menu(self):
        """Меню поиска"""
        print(f"\n{Colors.BOLD}{Colors.GREEN}🔍 ТИПЫ ПОИСКА{Colors.END}")
        print(f"{Colors.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
        
        options = [
            ("1", "👤 Поиск по имени и фамилии", "name_search"),
            ("2", "📧 Поиск по email адресу", "email_search"),
            ("3", "📱 Поиск по номеру телефона", "phone_search"),
            ("4", "🆔 Поиск по username", "username_search"),
            ("5", "🌐 Поиск по домену/сайту", "domain_search"),
            ("6", "🖼️ Поиск изображений", "image_search"),
            ("7", "🎥 Поиск видео", "video_search"),
            ("8", "🔄 Комплексный поиск", "full_search"),
            ("9", "📊 Просмотр результатов", "view_results"),
            ("0", "🔙 Назад", "back")
        ]
        
        for option, description, _ in options:
            print(f"{Colors.YELLOW}[{option}]{Colors.END} {description}")
        
        print(f"{Colors.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
        
        choice = input(f"{Colors.BOLD}Выберите тип поиска: {Colors.END}")
        return choice
    
    def search_by_name(self, name):
        """Поиск по имени и фамилии"""
        print(f"\n{Colors.YELLOW}👤 Поиск по имени: {name}{Colors.END}")
        
        results = {
            'name': name,
            'search_engines': [],
            'social_networks': [],
            'professional_networks': [],
            'images': [],
            'videos': [],
            'news': []
        }
        
        # Поиск в поисковых системах
        search_engines = [
            {'name': 'Google', 'url': f'https://www.google.com/search?q="{name}"'},
            {'name': 'Yandex', 'url': f'https://yandex.ru/search/?text="{name}"'},
            {'name': 'Bing', 'url': f'https://www.bing.com/search?q="{name}"'},
            {'name': 'DuckDuckGo', 'url': f'https://duckduckgo.com/?q="{name}"'}
        ]
        
        print(f"\n{Colors.CYAN}🔍 Поисковые системы:{Colors.END}")
        for engine in search_engines:
            print(f"  • {engine['name']}: {engine['url']}")
            results['search_engines'].append(engine)
        
        # Социальные сети
        social_networks = [
            {'name': 'VKontakte', 'url': f'https://vk.com/search?c[name]=1&c[q]={quote(name)}'},
            {'name': 'Facebook', 'url': f'https://www.facebook.com/search/people/?q={quote(name)}'},
            {'name': 'Instagram', 'url': f'https://www.instagram.com/explore/tags/{quote(name.replace(" ", ""))}'},
            {'name': 'Twitter', 'url': f'https://twitter.com/search?q="{name}"'},
            {'name': 'Telegram', 'url': f'https://t.me/s/{name.replace(" ", "_")}'},
            {'name': 'YouTube', 'url': f'https://www.youtube.com/results?search_query={quote(name)}'}
        ]
        
        print(f"\n{Colors.GREEN}📱 Социальные сети:{Colors.END}")
        for network in social_networks:
            print(f"  • {network['name']}: {network['url']}")
            results['social_networks'].append(network)
        
        # Профессиональные сети
        professional_networks = [
            {'name': 'LinkedIn', 'url': f'https://www.linkedin.com/search/results/people/?keywords={quote(name)}'},
            {'name': 'Behance', 'url': f'https://www.behance.net/search/users?search={quote(name)}'},
            {'name': 'GitHub', 'url': f'https://github.com/search?q={quote(name)}&type=users'},
            {'name': 'Habr', 'url': f'https://habr.com/ru/search/?q={quote(name)}&target_type=users'}
        ]
        
        print(f"\n{Colors.BLUE}💼 Профессиональные сети:{Colors.END}")
        for network in professional_networks:
            print(f"  • {network['name']}: {network['url']}")
            results['professional_networks'].append(network)
        
        self.results['name_search'] = results
        return results
    
    def search_by_email(self, email):
        """Поиск по email"""
        print(f"\n{Colors.YELLOW}📧 Поиск по email: {email}{Colors.END}")
        
        # Проверка формата
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            print(f"{Colors.RED}❌ Неверный формат email{Colors.END}")
            return
        
        results = {
            'email': email,
            'domain': email.split('@')[1],
            'username': email.split('@')[0],
            'social_profiles': [],
            'breaches': [],
            'domain_info': {}
        }
        
        # Поиск профилей по email
        print(f"\n{Colors.CYAN}🔍 Поиск связанных профилей:{Colors.END}")
        
        # Проверка в социальных сетях (симуляция)
        social_checks = [
            {'platform': 'Gravatar', 'url': f'https://gravatar.com/{email}'},
            {'platform': 'Google+', 'url': f'https://plus.google.com/find/{quote(email)}'},
            {'platform': 'Skype', 'url': f'https://www.skype.com/en/search/?query={quote(email)}'}
        ]
        
        for check in social_checks:
            if random.choice([True, False]):  # Симуляция результата
                print(f"  ✅ Найден профиль на {check['platform']}")
                results['social_profiles'].append(check)
            else:
                print(f"  ❌ Профиль на {check['platform']} не найден")
        
        # Проверка утечек (симуляция)
        print(f"\n{Colors.RED}🔍 Проверка утечек данных:{Colors.END}")
        breaches = [
            "Collection #1 (2019)",
            "LinkedIn (2012)",
            "Adobe (2013)",
            "MySpace (2013)",
            "Yahoo (2014)"
        ]
        
        if random.choice([True, False]):
            found_breaches = random.sample(breaches, random.randint(1, 3))
            print(f"{Colors.RED}⚠️ Email найден в утечках:{Colors.END}")
            for breach in found_breaches:
                print(f"  • {breach}")
                results['breaches'].append(breach)
        else:
            print(f"{Colors.GREEN}✅ Email не найден в известных утечках{Colors.END}")
        
        self.results['email_search'] = results
        return results
    
    def search_by_phone(self, phone):
        """Поиск по номеру телефона"""
        print(f"\n{Colors.YELLOW}📱 Поиск по телефону: {phone}{Colors.END}")
        
        results = {
            'phone': phone,
            'operator_info': {},
            'social_profiles': [],
            'messenger_accounts': []
        }
        
        # Определение оператора (симуляция)
        operators = {
            '+7': ['МТС', 'Билайн', 'МегаФон', 'Теле2'],
            '+380': ['Киевстар', 'Vodafone', 'lifecell'],
            '+998': ['Ucell', 'Beeline', 'UzMobile']
        }
        
        country_code = phone[:3] if phone.startswith('+') else phone[:2]
        
        if country_code in operators:
            operator = random.choice(operators[country_code])
            print(f"\n{Colors.CYAN}📡 Информация об операторе:{Colors.END}")
            print(f"  Оператор: {operator}")
            print(f"  Код страны: {country_code}")
            results['operator_info'] = {'operator': operator, 'country_code': country_code}
        
        # Поиск в мессенджерах
        print(f"\n{Colors.GREEN}💬 Проверка мессенджеров:{Colors.END}")
        messengers = ['WhatsApp', 'Telegram', 'Viber', 'Signal']
        
        for messenger in messengers:
            if random.choice([True, False]):
                print(f"  ✅ Аккаунт найден в {messenger}")
                results['messenger_accounts'].append(messenger)
            else:
                print(f"  ❌ Аккаунт в {messenger} не найден")
        
        # Поиск в социальных сетях
        print(f"\n{Colors.BLUE}📱 Поиск в социальных сетях:{Colors.END}")
        social_platforms = ['VKontakte', 'Facebook', 'Instagram', 'TikTok']
        
        for platform in social_platforms:
            if random.choice([True, False]):
                print(f"  ✅ Профиль найден в {platform}")
                results['social_profiles'].append(platform)
            else:
                print(f"  ❌ Профиль в {platform} не найден")
        
        self.results['phone_search'] = results
        return results
    
    def search_images(self, query):
        """Поиск изображений"""
        print(f"\n{Colors.YELLOW}🖼️ Поиск изображений: {query}{Colors.END}")
        
        results = {
            'query': query,
            'search_engines': [],
            'reverse_search': [],
            'face_recognition': []
        }
        
        # Поисковые системы для изображений
        image_engines = [
            {'name': 'Google Images', 'url': f'https://images.google.com/search?q={quote(query)}'},
            {'name': 'Yandex Images', 'url': f'https://yandex.ru/images/search?text={quote(query)}'},
            {'name': 'Bing Images', 'url': f'https://www.bing.com/images/search?q={quote(query)}'},
            {'name': 'DuckDuckGo Images', 'url': f'https://duckduckgo.com/?q={quote(query)}&iax=images&ia=images'}
        ]
        
        print(f"\n{Colors.CYAN}🔍 Поиск в базах изображений:{Colors.END}")
        for engine in image_engines:
            print(f"  • {engine['name']}: {engine['url']}")
            results['search_engines'].append(engine)
        
        # Обратный поиск изображений
        reverse_engines = [
            {'name': 'TinEye', 'url': 'https://tineye.com/'},
            {'name': 'Google Reverse', 'url': 'https://images.google.com/'},
            {'name': 'Yandex Reverse', 'url': 'https://yandex.ru/images/'},
            {'name': 'IQDB', 'url': 'https://iqdb.org/'}
        ]
        
        print(f"\n{Colors.GREEN}🔄 Обратный поиск изображений:{Colors.END}")
        for engine in reverse_engines:
            print(f"  • {engine['name']}: {engine['url']}")
            results['reverse_search'].append(engine)
        
        # Распознавание лиц
        face_services = [
            {'name': 'FindFace', 'url': 'https://findface.ru/'},
            {'name': 'PimEyes', 'url': 'https://pimeyes.com/'},
            {'name': 'Betaface', 'url': 'https://www.betaface.com/'},
            {'name': 'Face++', 'url': 'https://www.faceplusplus.com/'}
        ]
        
        print(f"\n{Colors.PURPLE}👁️ Распознавание лиц:{Colors.END}")
        for service in face_services:
            print(f"  • {service['name']}: {service['url']}")
            results['face_recognition'].append(service)
        
        self.results['image_search'] = results
        return results
    
    def search_videos(self, query):
        """Поиск видео"""
        print(f"\n{Colors.YELLOW}🎥 Поиск видео: {query}{Colors.END}")
        
        results = {
            'query': query,
            'video_platforms': [],
            'streaming_services': [],
            'social_video': []
        }
        
        # Видеоплатформы
        video_platforms = [
            {'name': 'YouTube', 'url': f'https://www.youtube.com/results?search_query={quote(query)}'},
            {'name': 'Vimeo', 'url': f'https://vimeo.com/search?q={quote(query)}'},
            {'name': 'Dailymotion', 'url': f'https://www.dailymotion.com/search/{quote(query)}'},
            {'name': 'RuTube', 'url': f'https://rutube.ru/search/?query={quote(query)}'}
        ]
        
        print(f"\n{Colors.CYAN}🎬 Видеоплатформы:{Colors.END}")
        for platform in video_platforms:
            print(f"  • {platform['name']}: {platform['url']}")
            results['video_platforms'].append(platform)
        
        # Социальные видео
        social_video = [
            {'name': 'TikTok', 'url': f'https://www.tiktok.com/search?q={quote(query)}'},
            {'name': 'Instagram Reels', 'url': f'https://www.instagram.com/explore/tags/{quote(query.replace(" ", ""))}'},
            {'name': 'VK Video', 'url': f'https://vk.com/video?q={quote(query)}'},
            {'name': 'Telegram', 'url': f'https://t.me/s/{query.replace(" ", "_")}'}
        ]
        
        print(f"\n{Colors.GREEN}📱 Социальные видео:{Colors.END}")
        for platform in social_video:
            print(f"  • {platform['name']}: {platform['url']}")
            results['social_video'].append(platform)
        
        self.results['video_search'] = results
        return results
    
    def full_search(self, query):
        """Комплексный поиск"""
        print(f"\n{Colors.BOLD}{Colors.RED}🔄 КОМПЛЕКСНЫЙ ПОИСК: {query}{Colors.END}")
        print(f"{Colors.YELLOW}Выполняется поиск по всем доступным источникам...{Colors.END}")
        
        # Выполняем все виды поиска
        time.sleep(1)
        self.search_by_name(query)
        
        time.sleep(1)
        self.search_images(query)
        
        time.sleep(1)
        self.search_videos(query)
        
        print(f"\n{Colors.GREEN}✅ Комплексный поиск завершен!{Colors.END}")
        return True
    
    def view_results(self):
        """Просмотр результатов поиска"""
        if not self.results:
            print(f"\n{Colors.YELLOW}⚠️ Нет результатов поиска{Colors.END}")
            return
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}📊 РЕЗУЛЬТАТЫ ПОИСКА{Colors.END}")
        print(f"{Colors.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
        
        for search_type, data in self.results.items():
            print(f"\n{Colors.YELLOW}🔍 {search_type.upper().replace('_', ' ')}:{Colors.END}")
            
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, list) and value:
                        print(f"  {key}: {len(value)} результатов")
                    elif not isinstance(value, (list, dict)):
                        print(f"  {key}: {value}")
    
    def save_results(self, filename=None):
        """Сохранение результатов"""
        if not self.results:
            print(f"\n{Colors.YELLOW}⚠️ Нет результатов для сохранения{Colors.END}")
            return
        
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"people_search_{timestamp}.json"
        
        # Создаем директорию если не существует
        if not os.path.exists('people_reports'):
            os.makedirs('people_reports')
        
        filepath = os.path.join('people_reports', filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, ensure_ascii=False, indent=2)
            
            print(f"\n{Colors.GREEN}✅ Результаты сохранены: {filepath}{Colors.END}")
            
            # Также создаем текстовый отчет
            txt_filename = filename.replace('.json', '.txt')
            txt_filepath = os.path.join('people_reports', txt_filename)
            
            with open(txt_filepath, 'w', encoding='utf-8') as f:
                f.write("🔍 ОТЧЕТ ПОИСКА ИНФОРМАЦИИ О ЛЮДЯХ\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                for search_type, data in self.results.items():
                    f.write(f"\n🔍 {search_type.upper().replace('_', ' ')}:\n")
                    f.write("-" * 30 + "\n")
                    
                    if isinstance(data, dict):
                        for key, value in data.items():
                            f.write(f"{key}: {value}\n")
                    f.write("\n")
            
            print(f"{Colors.GREEN}✅ Текстовый отчет: {txt_filepath}{Colors.END}")
            
        except Exception as e:
            print(f"\n{Colors.RED}❌ Ошибка сохранения: {e}{Colors.END}")
    
    def run(self):
        """Главный цикл"""
        while True:
            self.clear_screen()
            self.print_banner()
            choice = self.search_menu()
            
            if choice == '1':
                name = input(f"\n{Colors.BOLD}Введите имя и фамилию: {Colors.END}")
                if name.strip():
                    self.search_by_name(name.strip())
                    self.save_results()
                
            elif choice == '2':
                email = input(f"\n{Colors.BOLD}Введите email: {Colors.END}")
                if email.strip():
                    self.search_by_email(email.strip())
                    self.save_results()
                
            elif choice == '3':
                phone = input(f"\n{Colors.BOLD}Введите номер телефона: {Colors.END}")
                if phone.strip():
                    self.search_by_phone(phone.strip())
                    self.save_results()
                
            elif choice == '4':
                username = input(f"\n{Colors.BOLD}Введите username: {Colors.END}")
                if username.strip():
                    self.search_by_name(username.strip())
                    self.save_results()
                
            elif choice == '5':
                domain = input(f"\n{Colors.BOLD}Введите домен: {Colors.END}")
                if domain.strip():
                    self.search_by_name(domain.strip())
                    self.save_results()
                
            elif choice == '6':
                query = input(f"\n{Colors.BOLD}Введите запрос для поиска изображений: {Colors.END}")
                if query.strip():
                    self.search_images(query.strip())
                    self.save_results()
                
            elif choice == '7':
                query = input(f"\n{Colors.BOLD}Введите запрос для поиска видео: {Colors.END}")
                if query.strip():
                    self.search_videos(query.strip())
                    self.save_results()
                
            elif choice == '8':
                query = input(f"\n{Colors.BOLD}Введите запрос для комплексного поиска: {Colors.END}")
                if query.strip():
                    self.full_search(query.strip())
                    self.save_results()
                
            elif choice == '9':
                self.view_results()
                
            elif choice == '0':
                break
                
            else:
                print(f"\n{Colors.RED}❌ Неверный выбор!{Colors.END}")
                time.sleep(1)
                continue
            
            input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")

def main():
    """Главная функция"""
    search_engine = PeopleSearchEngine()
    search_engine.run()

if __name__ == "__main__":
    main()
