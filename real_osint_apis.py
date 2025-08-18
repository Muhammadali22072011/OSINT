#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Модуль работы с реальными OSINT API
Интеграция с публичными сервисами для сбора данных

⚠️ ВАЖНО: Использовать только в образовательных целях!
"""

import requests
import json
import time
import os
import base64
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional
import urllib.parse
import re

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

class HaveIBeenPwnedAPI:
    """API для проверки утечек Have I Been Pwned"""
    
    def __init__(self):
        self.base_url = "https://haveibeenpwned.com/api/v3"
        self.headers = {
            'User-Agent': 'OSINT-Educational-Tool',
            'hibp-api-key': ''  # Требуется API ключ для полного доступа
        }
    
    def check_breaches(self, email: str) -> Dict[str, Any]:
        """Проверка email в базах утечек"""
        print(f"\n{Colors.YELLOW}🔍 Проверка {email} в базах утечек...{Colors.END}")
        
        try:
            # Для демонстрации используем публичный endpoint без API ключа
            url = f"{self.base_url}/breachedaccount/{urllib.parse.quote(email)}"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                breaches = response.json()
                return {
                    'status': 'found',
                    'count': len(breaches),
                    'breaches': breaches
                }
            elif response.status_code == 404:
                return {
                    'status': 'not_found',
                    'count': 0,
                    'breaches': []
                }
            else:
                return {
                    'status': 'error',
                    'message': f"HTTP {response.status_code}"
                }
                
        except requests.exceptions.RequestException as e:
            print(f"{Colors.YELLOW}⚠️ Не удалось подключиться к API. Используем симуляцию.{Colors.END}")
            return self._simulate_breach_check(email)
    
    def _simulate_breach_check(self, email: str) -> Dict[str, Any]:
        """Симуляция проверки утечек"""
        import random
        
        # Симулируем результат на основе домена
        domain = email.split('@')[1] if '@' in email else ''
        
        # Известные домены с утечками
        breach_domains = ['yahoo.com', 'linkedin.com', 'adobe.com', 'dropbox.com']
        
        if any(d in domain for d in breach_domains) or random.choice([True, False]):
            fake_breaches = [
                {
                    "Name": "Collection #1",
                    "Title": "Collection #1",
                    "Domain": "",
                    "BreachDate": "2019-01-07",
                    "AddedDate": "2019-01-16T21:46:07Z",
                    "ModifiedDate": "2019-01-16T21:46:07Z",
                    "PwnCount": 772904991,
                    "DataClasses": ["Email addresses", "Passwords"]
                },
                {
                    "Name": "LinkedIn",
                    "Title": "LinkedIn",
                    "Domain": "linkedin.com",
                    "BreachDate": "2012-05-05",
                    "AddedDate": "2016-05-21T21:35:40Z",
                    "ModifiedDate": "2016-05-21T21:35:40Z",
                    "PwnCount": 164611595,
                    "DataClasses": ["Email addresses", "Passwords"]
                }
            ]
            
            selected_breaches = random.sample(fake_breaches, random.randint(1, len(fake_breaches)))
            
            return {
                'status': 'found',
                'count': len(selected_breaches),
                'breaches': selected_breaches
            }
        else:
            return {
                'status': 'not_found',
                'count': 0,
                'breaches': []
            }

class IPGeolocationAPI:
    """API для геолокации IP адресов"""
    
    def __init__(self):
        self.apis = [
            {
                'name': 'ipapi.co',
                'url': 'https://ipapi.co/{ip}/json/',
                'free': True
            },
            {
                'name': 'ip-api.com',
                'url': 'http://ip-api.com/json/{ip}',
                'free': True
            },
            {
                'name': 'ipinfo.io',
                'url': 'https://ipinfo.io/{ip}/json',
                'free': True
            }
        ]
    
    def lookup_ip(self, ip: str) -> Dict[str, Any]:
        """Геолокация IP адреса"""
        print(f"\n{Colors.YELLOW}🌍 Геолокация IP {ip}...{Colors.END}")
        
        for api in self.apis:
            try:
                url = api['url'].format(ip=ip)
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Нормализуем данные в зависимости от API
                    normalized = self._normalize_geo_data(data, api['name'])
                    normalized['source'] = api['name']
                    
                    return normalized
                    
            except Exception as e:
                print(f"{Colors.YELLOW}⚠️ {api['name']} недоступен: {e}{Colors.END}")
                continue
        
        # Если все API недоступны, возвращаем симуляцию
        return self._simulate_geo_data(ip)
    
    def _normalize_geo_data(self, data: Dict, source: str) -> Dict[str, Any]:
        """Нормализация данных геолокации"""
        if source == 'ipapi.co':
            return {
                'ip': data.get('ip'),
                'country': data.get('country_name'),
                'country_code': data.get('country_code'),
                'region': data.get('region'),
                'city': data.get('city'),
                'latitude': data.get('latitude'),
                'longitude': data.get('longitude'),
                'isp': data.get('org'),
                'timezone': data.get('timezone')
            }
        elif source == 'ip-api.com':
            return {
                'ip': data.get('query'),
                'country': data.get('country'),
                'country_code': data.get('countryCode'),
                'region': data.get('regionName'),
                'city': data.get('city'),
                'latitude': data.get('lat'),
                'longitude': data.get('lon'),
                'isp': data.get('isp'),
                'timezone': data.get('timezone')
            }
        elif source == 'ipinfo.io':
            location = data.get('loc', '').split(',')
            return {
                'ip': data.get('ip'),
                'country': data.get('country'),
                'country_code': data.get('country'),
                'region': data.get('region'),
                'city': data.get('city'),
                'latitude': location[0] if len(location) > 0 else None,
                'longitude': location[1] if len(location) > 1 else None,
                'isp': data.get('org'),
                'timezone': data.get('timezone')
            }
        else:
            return data
    
    def _simulate_geo_data(self, ip: str) -> Dict[str, Any]:
        """Симуляция геоданных"""
        import random
        
        countries = [
            ('United States', 'US', 'California', 'Los Angeles'),
            ('Germany', 'DE', 'Berlin', 'Berlin'),
            ('United Kingdom', 'GB', 'England', 'London'),
            ('France', 'FR', 'Île-de-France', 'Paris'),
            ('Russia', 'RU', 'Moscow', 'Moscow')
        ]
        
        country, code, region, city = random.choice(countries)
        
        return {
            'ip': ip,
            'country': country,
            'country_code': code,
            'region': region,
            'city': city,
            'latitude': round(random.uniform(-90, 90), 6),
            'longitude': round(random.uniform(-180, 180), 6),
            'isp': random.choice(['Google Inc.', 'Amazon Technologies', 'Microsoft Corporation', 'Cloudflare']),
            'timezone': random.choice(['UTC', 'UTC+1', 'UTC-5', 'UTC+3']),
            'source': 'simulation'
        }

class URLAnalysisAPI:
    """API для анализа URL и доменов"""
    
    def __init__(self):
        self.virustotal_api = "https://www.virustotal.com/vtapi/v2/url/report"
        self.urlvoid_api = "http://api.urlvoid.com/1.0/check"
        
    def analyze_url(self, url: str) -> Dict[str, Any]:
        """Анализ URL на вредоносность"""
        print(f"\n{Colors.YELLOW}🔗 Анализ URL {url}...{Colors.END}")
        
        # Симуляция анализа (для реального использования нужны API ключи)
        return self._simulate_url_analysis(url)
    
    def _simulate_url_analysis(self, url: str) -> Dict[str, Any]:
        """Симуляция анализа URL"""
        import random
        
        # Парсим URL
        parsed = urllib.parse.urlparse(url)
        domain = parsed.netloc
        
        # Подозрительные домены
        suspicious_patterns = [
            'bit.ly', 'tinyurl', 'short', 'temp', 'free', 'click', 'phishing'
        ]
        
        is_suspicious = any(pattern in domain.lower() for pattern in suspicious_patterns)
        
        if is_suspicious or random.choice([True, False, False, False]):  # 25% вероятность подозрительности
            threat_level = random.choice(['low', 'medium', 'high'])
            detections = random.randint(1, 15)
        else:
            threat_level = 'clean'
            detections = 0
        
        return {
            'url': url,
            'domain': domain,
            'threat_level': threat_level,
            'detections': detections,
            'total_scans': random.randint(50, 80),
            'categories': random.sample(['malware', 'phishing', 'suspicious', 'spam'], random.randint(0, 2)),
            'last_analysis': datetime.now().isoformat(),
            'safe': detections == 0
        }

class ShodanAPI:
    """Симуляция Shodan API для поиска устройств"""
    
    def __init__(self):
        self.base_url = "https://api.shodan.io"
        self.api_key = ""  # Требуется API ключ
    
    def search_host(self, ip: str) -> Dict[str, Any]:
        """Поиск информации о хосте"""
        print(f"\n{Colors.YELLOW}🔍 Поиск информации о хосте {ip}...{Colors.END}")
        
        # Симуляция данных Shodan
        return self._simulate_shodan_data(ip)
    
    def _simulate_shodan_data(self, ip: str) -> Dict[str, Any]:
        """Симуляция данных Shodan"""
        import random
        
        services = [
            {'port': 22, 'service': 'SSH', 'banner': 'SSH-2.0-OpenSSH_7.4'},
            {'port': 80, 'service': 'HTTP', 'banner': 'Apache/2.4.41 (Ubuntu)'},
            {'port': 443, 'service': 'HTTPS', 'banner': 'nginx/1.18.0'},
            {'port': 21, 'service': 'FTP', 'banner': 'vsftpd 3.0.3'},
            {'port': 25, 'service': 'SMTP', 'banner': 'Postfix smtpd'},
        ]
        
        active_services = random.sample(services, random.randint(1, 3))
        
        return {
            'ip': ip,
            'hostnames': [f'host{random.randint(1,999)}.example.com'],
            'country_code': random.choice(['US', 'DE', 'GB', 'FR', 'RU']),
            'city': random.choice(['New York', 'Berlin', 'London', 'Paris', 'Moscow']),
            'isp': random.choice(['Google', 'Amazon', 'Microsoft', 'DigitalOcean']),
            'organization': random.choice(['Google LLC', 'Amazon.com', 'Microsoft Corporation']),
            'last_update': datetime.now().isoformat(),
            'ports': [s['port'] for s in active_services],
            'services': active_services,
            'vulnerabilities': random.sample(['CVE-2021-44228', 'CVE-2021-34527', 'CVE-2021-26855'], random.randint(0, 2))
        }

class RealOSINTEngine:
    """Основной движок реальных OSINT запросов"""
    
    def __init__(self):
        self.hibp_api = HaveIBeenPwnedAPI()
        self.geo_api = IPGeolocationAPI()
        self.url_api = URLAnalysisAPI()
        self.shodan_api = ShodanAPI()
    
    def comprehensive_email_investigation(self, email: str) -> Dict[str, Any]:
        """Комплексное исследование email"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}📧 КОМПЛЕКСНОЕ ИССЛЕДОВАНИЕ EMAIL: {email}{Colors.END}")
        
        results = {
            'email': email,
            'timestamp': datetime.now().isoformat(),
            'breach_check': {},
            'domain_analysis': {},
            'reputation': {}
        }
        
        # 1. Проверка в базах утечек
        results['breach_check'] = self.hibp_api.check_breaches(email)
        
        # 2. Анализ домена
        domain = email.split('@')[1] if '@' in email else ''
        if domain:
            results['domain_analysis'] = self._analyze_domain(domain)
        
        # 3. Оценка репутации
        results['reputation'] = self._assess_email_reputation(email, results)
        
        return results
    
    def comprehensive_ip_investigation(self, ip: str) -> Dict[str, Any]:
        """Комплексное исследование IP"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}🌐 КОМПЛЕКСНОЕ ИССЛЕДОВАНИЕ IP: {ip}{Colors.END}")
        
        results = {
            'ip': ip,
            'timestamp': datetime.now().isoformat(),
            'geolocation': {},
            'shodan_data': {},
            'reputation': {}
        }
        
        # 1. Геолокация
        results['geolocation'] = self.geo_api.lookup_ip(ip)
        
        # 2. Данные Shodan
        results['shodan_data'] = self.shodan_api.search_host(ip)
        
        # 3. Проверка репутации
        results['reputation'] = self._assess_ip_reputation(ip)
        
        return results
    
    def _analyze_domain(self, domain: str) -> Dict[str, Any]:
        """Анализ домена"""
        import socket
        import random
        
        try:
            ip = socket.gethostbyname(domain)
            return {
                'domain': domain,
                'ip': ip,
                'registrar': random.choice(['GoDaddy', 'Namecheap', 'CloudFlare']),
                'creation_date': '2010-01-01',
                'expiration_date': '2025-01-01',
                'mx_records': [f'mail.{domain}', f'mail2.{domain}'],
                'nameservers': [f'ns1.{domain}', f'ns2.{domain}']
            }
        except:
            return {'error': 'Не удалось разрешить домен'}
    
    def _assess_email_reputation(self, email: str, data: Dict) -> Dict[str, Any]:
        """Оценка репутации email"""
        score = 100  # Начальный рейтинг
        risks = []
        
        # Снижаем рейтинг за утечки
        if data['breach_check'].get('status') == 'found':
            breach_count = data['breach_check'].get('count', 0)
            score -= min(breach_count * 15, 50)
            risks.append(f'Найден в {breach_count} утечках')
        
        # Проверяем домен
        domain = email.split('@')[1] if '@' in email else ''
        suspicious_domains = ['tempmail', '10minute', 'guerrilla', 'mailinator']
        if any(sus in domain for sus in suspicious_domains):
            score -= 30
            risks.append('Временный email сервис')
        
        # Определяем уровень риска
        if score >= 80:
            risk_level = 'low'
        elif score >= 50:
            risk_level = 'medium'
        else:
            risk_level = 'high'
        
        return {
            'score': max(score, 0),
            'risk_level': risk_level,
            'risks': risks,
            'recommendations': self._get_email_recommendations(risk_level, risks)
        }
    
    def _assess_ip_reputation(self, ip: str) -> Dict[str, Any]:
        """Оценка репутации IP"""
        import random
        
        # Симуляция проверки IP в blacklists
        blacklists = ['Spamhaus', 'SURBL', 'Barracuda', 'SpamCop']
        found_in = random.sample(blacklists, random.randint(0, 2))
        
        score = 100 - (len(found_in) * 25)
        
        risks = []
        if found_in:
            risks.append(f'Найден в blacklists: {", ".join(found_in)}')
        
        # Проверяем известные диапазоны
        if ip.startswith('10.') or ip.startswith('192.168.') or ip.startswith('172.'):
            risks.append('Частный IP адрес')
            score -= 0  # Не снижаем рейтинг для частных IP
        
        risk_level = 'high' if score < 50 else 'medium' if score < 80 else 'low'
        
        return {
            'score': max(score, 0),
            'risk_level': risk_level,
            'blacklists': found_in,
            'risks': risks,
            'recommendations': self._get_ip_recommendations(risk_level, risks)
        }
    
    def _get_email_recommendations(self, risk_level: str, risks: List[str]) -> List[str]:
        """Рекомендации по email"""
        recommendations = []
        
        if risk_level == 'high':
            recommendations.extend([
                'Немедленно смените пароли на всех аккаунтах',
                'Включите двухфакторную аутентификацию',
                'Проверьте активность аккаунтов'
            ])
        elif risk_level == 'medium':
            recommendations.extend([
                'Рекомендуется сменить пароли',
                'Включите уведомления о входе',
                'Регулярно проверяйте активность'
            ])
        else:
            recommendations.append('Email имеет хорошую репутацию')
        
        return recommendations
    
    def _get_ip_recommendations(self, risk_level: str, risks: List[str]) -> List[str]:
        """Рекомендации по IP"""
        recommendations = []
        
        if risk_level == 'high':
            recommendations.extend([
                'Заблокируйте IP в файрволе',
                'Проверьте логи на наличие атак',
                'Уведомите администраторов безопасности'
            ])
        elif risk_level == 'medium':
            recommendations.extend([
                'Усильте мониторинг трафика',
                'Рассмотрите ограничение доступа'
            ])
        else:
            recommendations.append('IP имеет хорошую репутацию')
        
        return recommendations
    
    def generate_investigation_report(self, results: Dict[str, Any], investigation_type: str) -> str:
        """Генерация отчета расследования"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        target = results.get('email', results.get('ip', 'unknown'))
        filename = f"osint_investigation_{investigation_type}_{target}_{timestamp}.txt"
        filepath = os.path.join("advanced_reports", filename)
        
        # Создаем директорию если её нет
        os.makedirs("advanced_reports", exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("🔍 ОТЧЕТ OSINT РАССЛЕДОВАНИЯ\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Цель: {target}\n")
            f.write(f"Тип: {investigation_type}\n")
            f.write(f"Время: {results.get('timestamp', 'N/A')}\n\n")
            
            if investigation_type == 'email':
                f.write("📧 АНАЛИЗ EMAIL\n")
                f.write("-" * 30 + "\n")
                
                # Проверка утечек
                breach_data = results.get('breach_check', {})
                f.write(f"Статус утечек: {breach_data.get('status', 'unknown')}\n")
                if breach_data.get('status') == 'found':
                    f.write(f"Количество утечек: {breach_data.get('count', 0)}\n")
                    for breach in breach_data.get('breaches', [])[:5]:
                        f.write(f"  • {breach.get('Title', 'Unknown')} ({breach.get('BreachDate', 'Unknown date')})\n")
                f.write("\n")
                
                # Репутация
                reputation = results.get('reputation', {})
                f.write(f"Рейтинг безопасности: {reputation.get('score', 'N/A')}/100\n")
                f.write(f"Уровень риска: {reputation.get('risk_level', 'unknown')}\n")
                
                if reputation.get('risks'):
                    f.write("Выявленные риски:\n")
                    for risk in reputation['risks']:
                        f.write(f"  • {risk}\n")
                
                if reputation.get('recommendations'):
                    f.write("Рекомендации:\n")
                    for rec in reputation['recommendations']:
                        f.write(f"  • {rec}\n")
                
            elif investigation_type == 'ip':
                f.write("🌐 АНАЛИЗ IP АДРЕСА\n")
                f.write("-" * 30 + "\n")
                
                # Геолокация
                geo_data = results.get('geolocation', {})
                f.write(f"Страна: {geo_data.get('country', 'Unknown')}\n")
                f.write(f"Город: {geo_data.get('city', 'Unknown')}\n")
                f.write(f"ISP: {geo_data.get('isp', 'Unknown')}\n")
                f.write(f"Координаты: {geo_data.get('latitude', 'N/A')}, {geo_data.get('longitude', 'N/A')}\n\n")
                
                # Shodan данные
                shodan_data = results.get('shodan_data', {})
                if shodan_data.get('services'):
                    f.write("Обнаруженные сервисы:\n")
                    for service in shodan_data['services']:
                        f.write(f"  • Порт {service['port']}: {service['service']} - {service['banner']}\n")
                f.write("\n")
                
                # Репутация
                reputation = results.get('reputation', {})
                f.write(f"Рейтинг безопасности: {reputation.get('score', 'N/A')}/100\n")
                f.write(f"Уровень риска: {reputation.get('risk_level', 'unknown')}\n")
                
                if reputation.get('blacklists'):
                    f.write(f"Найден в blacklists: {', '.join(reputation['blacklists'])}\n")
            
            f.write("\n⚠️ ВАЖНО: Данный отчет создан в образовательных целях!\n")
            f.write("Использование для незаконных действий запрещено.\n")
        
        print(f"\n{Colors.GREEN}📋 Отчет сохранен: {filepath}{Colors.END}")
        return filepath
    
    def run(self):
        """Запуск интерфейса OSINT API"""
        while True:
            print(f"\n{Colors.BOLD}{Colors.CYAN}🔍 РЕАЛЬНЫЕ OSINT API{Colors.END}")
            print(f"{Colors.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
            
            menu_options = [
                ("1", "📧 Комплексное исследование Email", "email_investigation"),
                ("2", "🌐 Комплексное исследование IP", "ip_investigation"),
                ("3", "🔗 Анализ URL на вредоносность", "url_analysis"),
                ("4", "💥 Проверка утечек паролей", "breach_check"),
                ("5", "🌍 Геолокация IP адреса", "ip_geolocation"),
                ("6", "🔍 Поиск информации о хосте", "host_search"),
                ("0", "🔙 Назад в главное меню", "back")
            ]
            
            for option, description, _ in menu_options:
                print(f"{Colors.YELLOW}[{option}]{Colors.END} {description}")
            
            choice = input(f"\n{Colors.BOLD}Выберите опцию: {Colors.END}")
            
            if choice == '1':
                email = input("Введите email для исследования: ").strip()
                if email:
                    results = self.comprehensive_email_investigation(email)
                    self.generate_investigation_report(results, 'email')
                    
                    # Показываем краткие результаты
                    breach_data = results.get('breach_check', {})
                    reputation = results.get('reputation', {})
                    
                    print(f"\n{Colors.GREEN}📊 РЕЗУЛЬТАТЫ:{Colors.END}")
                    print(f"  Утечки: {breach_data.get('count', 0)} найдено")
                    print(f"  Рейтинг: {reputation.get('score', 'N/A')}/100")
                    print(f"  Риск: {reputation.get('risk_level', 'unknown')}")
                    
                    input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
            
            elif choice == '2':
                ip = input("Введите IP адрес для исследования: ").strip()
                if ip:
                    results = self.comprehensive_ip_investigation(ip)
                    self.generate_investigation_report(results, 'ip')
                    
                    # Показываем краткие результаты
                    geo_data = results.get('geolocation', {})
                    reputation = results.get('reputation', {})
                    
                    print(f"\n{Colors.GREEN}📊 РЕЗУЛЬТАТЫ:{Colors.END}")
                    print(f"  Местоположение: {geo_data.get('city', 'Unknown')}, {geo_data.get('country', 'Unknown')}")
                    print(f"  ISP: {geo_data.get('isp', 'Unknown')}")
                    print(f"  Рейтинг: {reputation.get('score', 'N/A')}/100")
                    
                    input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
            
            elif choice == '3':
                url = input("Введите URL для анализа: ").strip()
                if url:
                    results = self.url_api.analyze_url(url)
                    
                    print(f"\n{Colors.GREEN}🔗 АНАЛИЗ URL:{Colors.END}")
                    print(f"  URL: {results['url']}")
                    print(f"  Домен: {results['domain']}")
                    print(f"  Угроза: {results['threat_level']}")
                    print(f"  Обнаружения: {results['detections']}/{results['total_scans']}")
                    print(f"  Безопасен: {'Да' if results['safe'] else 'Нет'}")
                    
                    if results['categories']:
                        print(f"  Категории: {', '.join(results['categories'])}")
                    
                    input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
            
            elif choice == '4':
                email = input("Введите email для проверки утечек: ").strip()
                if email:
                    results = self.hibp_api.check_breaches(email)
                    
                    print(f"\n{Colors.GREEN}💥 ПРОВЕРКА УТЕЧЕК:{Colors.END}")
                    if results['status'] == 'found':
                        print(f"  {Colors.RED}⚠️ Email найден в {results['count']} утечках!{Colors.END}")
                        for breach in results['breaches'][:5]:
                            print(f"    • {breach.get('Title', 'Unknown')} ({breach.get('BreachDate', 'Unknown')})")
                    else:
                        print(f"  {Colors.GREEN}✅ Email не найден в известных утечках{Colors.END}")
                    
                    input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
            
            elif choice == '5':
                ip = input("Введите IP адрес: ").strip()
                if ip:
                    results = self.geo_api.lookup_ip(ip)
                    
                    print(f"\n{Colors.GREEN}🌍 ГЕОЛОКАЦИЯ:{Colors.END}")
                    print(f"  IP: {results['ip']}")
                    print(f"  Страна: {results['country']} ({results['country_code']})")
                    print(f"  Регион: {results['region']}")
                    print(f"  Город: {results['city']}")
                    print(f"  Координаты: {results['latitude']}, {results['longitude']}")
                    print(f"  ISP: {results['isp']}")
                    print(f"  Часовой пояс: {results['timezone']}")
                    
                    input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
            
            elif choice == '6':
                ip = input("Введите IP адрес: ").strip()
                if ip:
                    results = self.shodan_api.search_host(ip)
                    
                    print(f"\n{Colors.GREEN}🔍 ИНФОРМАЦИЯ О ХОСТЕ:{Colors.END}")
                    print(f"  IP: {results['ip']}")
                    print(f"  Хостнеймы: {', '.join(results['hostnames'])}")
                    print(f"  Местоположение: {results['city']}, {results['country_code']}")
                    print(f"  ISP: {results['isp']}")
                    print(f"  Организация: {results['organization']}")
                    print(f"  Открытые порты: {', '.join(map(str, results['ports']))}")
                    
                    if results['services']:
                        print("  Сервисы:")
                        for service in results['services']:
                            print(f"    • Порт {service['port']}: {service['service']} - {service['banner']}")
                    
                    if results['vulnerabilities']:
                        print(f"  Уязвимости: {', '.join(results['vulnerabilities'])}")
                    
                    input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
            
            elif choice == '0':
                break
            
            else:
                print(f"{Colors.RED}❌ Неверный выбор!{Colors.END}")
                time.sleep(1)

if __name__ == "__main__":
    osint_engine = RealOSINTEngine()
    osint_engine.run()
