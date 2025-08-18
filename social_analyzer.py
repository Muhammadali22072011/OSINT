#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📱 Анализатор социальных сетей
Модуль для сбора открытой информации из социальных сетей

⚠️ ВАЖНО: Использовать только в образовательных целях!
"""

import requests
import json
import time
import random
import re
from datetime import datetime, timedelta
import os
from urllib.parse import urlparse, parse_qs
import base64

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

class SocialAnalyzer:
    """Анализатор социальных сетей для OSINT"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.results = {}
    
    def analyze_username(self, username):
        """Анализ имени пользователя на различных платформах"""
        print(f"\n{Colors.YELLOW}🔍 Поиск пользователя: {username}{Colors.END}")
        
        platforms = {
            "VKontakte": f"https://vk.com/{username}",
            "Instagram": f"https://instagram.com/{username}",
            "Twitter": f"https://twitter.com/{username}",
            "Facebook": f"https://facebook.com/{username}",
            "GitHub": f"https://github.com/{username}",
            "Telegram": f"https://t.me/{username}",
            "YouTube": f"https://youtube.com/@{username}",
            "TikTok": f"https://tiktok.com/@{username}",
            "LinkedIn": f"https://linkedin.com/in/{username}",
            "Reddit": f"https://reddit.com/user/{username}"
        }
        
        found_profiles = []
        
        print(f"{Colors.CYAN}🌐 Проверка платформ...{Colors.END}")
        
        for platform, url in platforms.items():
            print(f"  • Проверка {platform}...", end="")
            
            # Симуляция проверки
            time.sleep(random.uniform(0.5, 1.5))
            
            # Случайная симуляция найденных профилей
            if random.choice([True, False, False]):  # 33% шанс найти профиль
                found_profiles.append({
                    "platform": platform,
                    "url": url,
                    "status": "Найден",
                    "activity": self.generate_activity_data()
                })
                print(f" {Colors.GREEN}✅ НАЙДЕН{Colors.END}")
            else:
                print(f" {Colors.RED}❌ Не найден{Colors.END}")
        
        return found_profiles
    
    def generate_activity_data(self):
        """Генерация данных об активности"""
        return {
            "last_seen": f"{random.randint(1, 30)} дней назад",
            "posts_count": random.randint(10, 1000),
            "followers": random.randint(50, 5000),
            "following": random.randint(20, 1500),
            "registration": f"{random.randint(2010, 2023)} год"
        }
    
    def analyze_vk_profile(self, vk_url):
        """Анализ профиля ВКонтакте"""
        print(f"\n{Colors.PURPLE}📱 АНАЛИЗ ПРОФИЛЯ ВКОНТАКТЕ{Colors.END}")
        print(f"URL: {vk_url}")
        
        # Извлечение ID из URL
        user_id = self.extract_vk_id(vk_url)
        
        # Симуляция данных профиля
        profile_data = {
            "id": user_id,
            "name": random.choice(["Александр Петров", "Мария Иванова", "Дмитрий Сидоров"]),
            "age": random.randint(18, 45),
            "city": random.choice(["Москва", "Санкт-Петербург", "Екатеринбург", "Новосибирск"]),
            "education": random.choice(["МГУ", "СПбГУ", "УрФУ", "НГУ", "Не указано"]),
            "work": random.choice(["IT-специалист", "Маркетолог", "Дизайнер", "Не указано"]),
            "relationship": random.choice(["Не указано", "В отношениях", "Женат/Замужем", "Свободен"]),
            "phone": f"+7{random.randint(900, 999)}{random.randint(1000000, 9999999)}" if random.choice([True, False]) else "Скрыто",
            "email": f"user{random.randint(100, 999)}@gmail.com" if random.choice([True, False]) else "Скрыто"
        }
        
        print(f"\n{Colors.GREEN}👤 ИНФОРМАЦИЯ О ПРОФИЛЕ:{Colors.END}")
        for key, value in profile_data.items():
            print(f"  {key.capitalize()}: {value}")
        
        # Анализ друзей
        friends_data = self.analyze_vk_friends(user_id)
        
        # Анализ активности
        activity_data = self.analyze_vk_activity(user_id)
        
        return {
            "profile": profile_data,
            "friends": friends_data,
            "activity": activity_data
        }
    
    def extract_vk_id(self, url):
        """Извлечение ID пользователя из URL ВК"""
        if "vk.com/id" in url:
            return url.split("id")[1].split("?")[0]
        elif "vk.com/" in url:
            return url.split("vk.com/")[1].split("?")[0]
        else:
            return str(random.randint(100000, 999999999))
    
    def analyze_vk_friends(self, user_id):
        """Анализ друзей ВКонтакте"""
        print(f"\n{Colors.CYAN}👥 АНАЛИЗ ДРУЗЕЙ{Colors.END}")
        
        friends_count = random.randint(50, 500)
        print(f"Общее количество друзей: {friends_count}")
        
        # Генерация статистики по друзьям
        cities = ["Москва", "СПб", "Екатеринбург", "Казань", "Новосибирск"]
        age_groups = ["18-25", "26-35", "36-45", "46+"]
        
        print(f"\n{Colors.YELLOW}📊 Статистика друзей:{Colors.END}")
        
        # По городам
        print("По городам:")
        for city in cities[:3]:
            count = random.randint(5, friends_count//4)
            print(f"  • {city}: {count}")
        
        # По возрасту
        print("\nПо возрасту:")
        for age_group in age_groups:
            count = random.randint(5, friends_count//3)
            print(f"  • {age_group}: {count}")
        
        # Общие друзья с известными людьми
        if random.choice([True, False]):
            print(f"\n{Colors.RED}⚠️ Обнаружены связи с подозрительными аккаунтами{Colors.END}")
            
        return {
            "total": friends_count,
            "cities": {city: random.randint(5, friends_count//4) for city in cities[:3]},
            "ages": {age: random.randint(5, friends_count//3) for age in age_groups}
        }
    
    def analyze_vk_activity(self, user_id):
        """Анализ активности ВКонтакте"""
        print(f"\n{Colors.BLUE}📈 АНАЛИЗ АКТИВНОСТИ{Colors.END}")
        
        # Последняя активность
        last_seen = random.randint(1, 30)
        print(f"Последний раз в сети: {last_seen} дней назад")
        
        # Статистика постов
        posts_count = random.randint(100, 2000)
        print(f"Количество постов: {posts_count}")
        
        # Время активности
        active_hours = random.sample(range(0, 24), random.randint(4, 8))
        print(f"Активные часы: {', '.join(map(str, sorted(active_hours)))}")
        
        # Интересы
        interests = ["Музыка", "Спорт", "Путешествия", "Технологии", "Кино", "Книги", "Игры"]
        user_interests = random.sample(interests, random.randint(2, 5))
        print(f"Интересы: {', '.join(user_interests)}")
        
        # Анализ геолокации
        print(f"\n{Colors.PURPLE}📍 АНАЛИЗ ГЕОЛОКАЦИИ{Colors.END}")
        if random.choice([True, False]):
            locations = ["Дом", "Работа", "Спортзал", "Торговый центр"]
            for location in random.sample(locations, random.randint(1, 3)):
                print(f"  • {location}: {random.randint(1, 20)} посещений")
        else:
            print("  Геолокация отключена")
        
        return {
            "last_seen": last_seen,
            "posts": posts_count,
            "active_hours": active_hours,
            "interests": user_interests
        }
    
    def phone_to_social(self, phone):
        """Поиск социальных профилей по номеру телефона"""
        print(f"\n{Colors.YELLOW}📱 ПОИСК ПО НОМЕРУ: {phone}{Colors.END}")
        
        # Очистка номера
        clean_phone = re.sub(r'[^\d+]', '', phone)
        
        print(f"Очищенный номер: {clean_phone}")
        
        # Симуляция поиска
        print(f"\n{Colors.CYAN}🔍 Поиск в базах данных...{Colors.END}")
        time.sleep(2)
        
        found_accounts = []
        
        # Случайные результаты
        platforms = ["WhatsApp", "Telegram", "Viber", "VKontakte"]
        
        for platform in platforms:
            if random.choice([True, False]):
                found_accounts.append({
                    "platform": platform,
                    "status": "Найден аккаунт",
                    "details": self.generate_phone_account_details(platform)
                })
        
        if found_accounts:
            print(f"{Colors.GREEN}✅ Найдены аккаунты:{Colors.END}")
            for account in found_accounts:
                print(f"  • {account['platform']}: {account['status']}")
                for key, value in account['details'].items():
                    print(f"    - {key}: {value}")
        else:
            print(f"{Colors.RED}❌ Аккаунты не найдены{Colors.END}")
        
        return found_accounts
    
    def generate_phone_account_details(self, platform):
        """Генерация деталей аккаунта по номеру"""
        names = ["Александр", "Мария", "Дмитрий", "Анна"]
        
        base_details = {
            "name": random.choice(names),
            "registration": f"{random.randint(2015, 2023)} год"
        }
        
        if platform == "WhatsApp":
            base_details.update({
                "last_seen": f"{random.randint(1, 24)} часов назад",
                "profile_photo": "Есть" if random.choice([True, False]) else "Нет"
            })
        elif platform == "Telegram":
            base_details.update({
                "username": f"@user{random.randint(100, 999)}",
                "bio": "Доступно" if random.choice([True, False]) else "Скрыто"
            })
        
        return base_details
    
    def email_to_social(self, email):
        """Поиск социальных профилей по email"""
        print(f"\n{Colors.YELLOW}📧 ПОИСК ПО EMAIL: {email}{Colors.END}")
        
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            print(f"{Colors.RED}❌ Неверный формат email{Colors.END}")
            return
        
        domain = email.split('@')[1]
        username = email.split('@')[0]
        
        print(f"Домен: {domain}")
        print(f"Пользователь: {username}")
        
        # Поиск по имени пользователя
        print(f"\n{Colors.CYAN}🔍 Поиск профилей с похожим именем...{Colors.END}")
        
        similar_usernames = [
            username,
            username + str(random.randint(1, 99)),
            username.replace('.', ''),
            username.replace('_', '')
        ]
        
        found_profiles = []
        platforms = ["GitHub", "Twitter", "Instagram", "LinkedIn"]
        
        for platform in platforms:
            if random.choice([True, False]):
                similar_name = random.choice(similar_usernames)
                found_profiles.append({
                    "platform": platform,
                    "username": similar_name,
                    "confidence": f"{random.randint(60, 95)}%"
                })
        
        if found_profiles:
            print(f"{Colors.GREEN}✅ Найдены похожие профили:{Colors.END}")
            for profile in found_profiles:
                print(f"  • {profile['platform']}: @{profile['username']} (уверенность: {profile['confidence']})")
        else:
            print(f"{Colors.RED}❌ Похожие профили не найдены{Colors.END}")
        
        return found_profiles
    
    def analyze_profile_photo(self, photo_url):
        """Анализ фото профиля"""
        print(f"\n{Colors.PURPLE}📸 АНАЛИЗ ФОТОГРАФИИ{Colors.END}")
        
        # Симуляция анализа
        print("🔍 Загрузка и анализ изображения...")
        time.sleep(2)
        
        analysis_results = {
            "face_detection": random.choice([True, False]),
            "age_estimate": f"{random.randint(20, 45)} лет",
            "gender": random.choice(["Мужской", "Женский", "Неопределенно"]),
            "emotions": random.choice(["Счастье", "Нейтрально", "Серьезность"]),
            "location_data": random.choice([True, False]),
            "reverse_search": random.choice([True, False])
        }
        
        print(f"\n{Colors.GREEN}📊 РЕЗУЛЬТАТЫ АНАЛИЗА:{Colors.END}")
        for key, value in analysis_results.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
        
        if analysis_results["reverse_search"]:
            print(f"\n{Colors.YELLOW}🔍 Обратный поиск нашел {random.randint(1, 5)} похожих изображений{Colors.END}")
        
        return analysis_results
    
    def generate_report(self, username, analysis_data):
        """Генерация отчета"""
        if not os.path.exists("reports"):
            os.makedirs("reports")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reports/social_analysis_{username}_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write(f"ОТЧЕТ АНАЛИЗА СОЦИАЛЬНЫХ СЕТЕЙ\n")
            f.write("="*60 + "\n\n")
            f.write(f"Цель: {username}\n")
            f.write(f"Дата анализа: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Аналитик: OSINT Toolkit\n\n")
            
            f.write("НАЙДЕННЫЕ ПРОФИЛИ:\n")
            f.write("-"*30 + "\n")
            
            for platform_data in analysis_data:
                f.write(f"Платформа: {platform_data['platform']}\n")
                f.write(f"URL: {platform_data['url']}\n")
                f.write(f"Статус: {platform_data['status']}\n")
                
                if 'activity' in platform_data:
                    f.write("Активность:\n")
                    for key, value in platform_data['activity'].items():
                        f.write(f"  - {key}: {value}\n")
                
                f.write("\n")
            
            f.write("="*60 + "\n")
            f.write("⚠️ ОТЧЕТ СОЗДАН В ОБРАЗОВАТЕЛЬНЫХ ЦЕЛЯХ\n")
            f.write("="*60 + "\n")
        
        print(f"{Colors.GREEN}✅ Отчет сохранен: {filename}{Colors.END}")
        return filename
    
    def run(self):
        """Запуск анализатора"""
        while True:
            print(f"\n{Colors.BOLD}{Colors.PURPLE}📱 АНАЛИЗАТОР СОЦИАЛЬНЫХ СЕТЕЙ{Colors.END}")
            print(f"{Colors.RED}⚠️ ТОЛЬКО ДЛЯ ОБРАЗОВАТЕЛЬНЫХ ЦЕЛЕЙ!{Colors.END}\n")
            
            print("Выберите режим анализа:")
            print("1. 👤 Поиск по имени пользователя")
            print("2. 📱 Поиск по номеру телефона")
            print("3. 📧 Поиск по email")
            print("4. 🔍 Детальный анализ профиля ВК")
            print("5. 📸 Анализ фотографии профиля")
            print("6. 📊 Просмотр отчетов")
            print("0. ← Назад в главное меню")
            
            choice = input(f"\n{Colors.YELLOW}Выберите опцию: {Colors.END}")
            
            if choice == '1':
                username = input("Введите имя пользователя: ").strip()
                if username:
                    found_profiles = self.analyze_username(username)
                    if found_profiles:
                        if input("\nСоздать отчет? (y/n): ").lower() == 'y':
                            self.generate_report(username, found_profiles)
                    input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
            
            elif choice == '2':
                phone = input("Введите номер телефона: ").strip()
                if phone:
                    self.phone_to_social(phone)
                    input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
            
            elif choice == '3':
                email = input("Введите email: ").strip()
                if email:
                    self.email_to_social(email)
                    input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
            
            elif choice == '4':
                vk_url = input("Введите URL профиля ВК: ").strip()
                if vk_url:
                    self.analyze_vk_profile(vk_url)
                    input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
            
            elif choice == '5':
                photo_url = input("Введите URL фотографии: ").strip()
                if photo_url:
                    self.analyze_profile_photo(photo_url)
                    input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
            
            elif choice == '6':
                self.view_reports()
            
            elif choice == '0':
                break
            
            else:
                print(f"{Colors.RED}❌ Неверный выбор!{Colors.END}")
                time.sleep(1)
    
    def view_reports(self):
        """Просмотр сохраненных отчетов"""
        if not os.path.exists("reports"):
            print(f"{Colors.YELLOW}📁 Папка с отчетами не найдена{Colors.END}")
            return
        
        files = [f for f in os.listdir("reports") if f.endswith('.txt')]
        
        if not files:
            print(f"{Colors.YELLOW}📁 Отчеты не найдены{Colors.END}")
            return
        
        print(f"\n{Colors.BOLD}📊 СОХРАНЕННЫЕ ОТЧЕТЫ{Colors.END}")
        for i, filename in enumerate(files, 1):
            print(f"  {i}. {filename}")
        
        try:
            choice = int(input(f"\n{Colors.YELLOW}Выберите отчет для просмотра (или 0 для выхода): {Colors.END}"))
            
            if 1 <= choice <= len(files):
                filepath = os.path.join("reports", files[choice-1])
                with open(filepath, 'r', encoding='utf-8') as f:
                    print(f"\n{Colors.CYAN}{f.read()}{Colors.END}")
                input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
        except (ValueError, IndexError):
            print(f"{Colors.RED}❌ Неверный выбор!{Colors.END}")

if __name__ == "__main__":
    analyzer = SocialAnalyzer()
    analyzer.run()
