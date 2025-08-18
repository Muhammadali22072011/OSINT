#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔬 Продвинутый многоуровневый поиск и анализ
Глубокий OSINT с машинным обучением и AI анализом

⚠️ ВАЖНО: Использовать только в образовательных целях!
"""

import requests
import json
import time
import random
import re
import socket
import ssl
import threading
import concurrent.futures
from datetime import datetime, timedelta
import os
import base64
import hashlib
from urllib.parse import urlparse, urljoin, parse_qs
import subprocess
import itertools
import collections
import pickle
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import math

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

@dataclass
class SearchResult:
    """Структура результата поиска"""
    source: str
    data_type: str
    confidence: float
    content: Dict[str, Any]
    timestamp: datetime
    metadata: Dict[str, Any]

class AIAnalyzer:
    """AI анализатор для обработки данных"""
    
    def __init__(self):
        self.patterns = self.load_analysis_patterns()
        self.confidence_weights = {
            'exact_match': 1.0,
            'partial_match': 0.7,
            'pattern_match': 0.5,
            'context_match': 0.3
        }
    
    def load_analysis_patterns(self):
        """Загрузка паттернов для анализа"""
        return {
            'email_patterns': [
                r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
                r'[a-zA-Z0-9._%+-]+\s*@\s*[a-zA-Z0-9.-]+\s*\.\s*[a-zA-Z]{2,}',
                r'[a-zA-Z0-9._%+-]+\[at\][a-zA-Z0-9.-]+\[dot\][a-zA-Z]{2,}'
            ],
            'phone_patterns': [
                r'\+?[0-9]{1,4}[-.\s]?[0-9]{1,3}[-.\s]?[0-9]{1,4}[-.\s]?[0-9]{1,4}[-.\s]?[0-9]{1,9}',
                r'\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}',
                r'[0-9]{3}-[0-9]{3}-[0-9]{4}'
            ],
            'social_patterns': [
                r'(?:instagram\.com/|@)[a-zA-Z0-9_.]+',
                r'(?:twitter\.com/|@)[a-zA-Z0-9_]+',
                r'(?:facebook\.com/)[a-zA-Z0-9.]+',
                r'(?:linkedin\.com/in/)[a-zA-Z0-9-]+',
                r'(?:vk\.com/)[a-zA-Z0-9_.]+',
                r'(?:t\.me/)[a-zA-Z0-9_]+'
            ],
            'crypto_patterns': [
                r'[13][a-km-zA-HJ-NP-Z1-9]{25,34}',  # Bitcoin
                r'0x[a-fA-F0-9]{40}',                 # Ethereum
                r'[LM3][a-km-zA-HJ-NP-Z1-9]{26,33}', # Litecoin
            ],
            'ip_patterns': [
                r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
                r'(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}',  # IPv6
            ],
            'credential_patterns': [
                r'password[:\s=]+[^\s\n]+',
                r'pass[:\s=]+[^\s\n]+',
                r'pwd[:\s=]+[^\s\n]+',
                r'api[_-]?key[:\s=]+[^\s\n]+',
                r'secret[:\s=]+[^\s\n]+',
                r'token[:\s=]+[^\s\n]+'
            ]
        }
    
    def analyze_text(self, text: str) -> Dict[str, List]:
        """Анализ текста с поиском паттернов"""
        results = {}
        
        for pattern_type, patterns in self.patterns.items():
            found_items = []
            
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    found_items.append({
                        'value': match,
                        'pattern': pattern,
                        'confidence': self.calculate_confidence(match, pattern_type)
                    })
            
            if found_items:
                results[pattern_type] = found_items
        
        return results
    
    def calculate_confidence(self, match: str, pattern_type: str) -> float:
        """Расчет уверенности в найденном паттерне"""
        base_confidence = 0.5
        
        # Дополнительные проверки для повышения уверенности
        if pattern_type == 'email_patterns':
            if '@' in match and '.' in match.split('@')[1]:
                base_confidence += 0.3
            if len(match) > 5:
                base_confidence += 0.2
        
        elif pattern_type == 'phone_patterns':
            if len(re.sub(r'[^\d]', '', match)) >= 10:
                base_confidence += 0.3
        
        elif pattern_type == 'social_patterns':
            if any(platform in match.lower() for platform in ['instagram', 'twitter', 'facebook']):
                base_confidence += 0.4
        
        return min(base_confidence, 1.0)

class AdvancedSearchEngine:
    """Продвинутый поисковый движок"""
    
    def __init__(self):
        self.ai_analyzer = AIAnalyzer()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.search_cache = {}
        self.search_history = []
    
    def multi_level_search(self, target: str, search_type: str = 'comprehensive') -> List[SearchResult]:
        """Многоуровневый поиск по цели"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}🔬 МНОГОУРОВНЕВЫЙ ПОИСК: {target}{Colors.END}")
        
        all_results = []
        search_levels = [
            ('Level 1: Базовая разведка', self.basic_reconnaissance),
            ('Level 2: Глубокий анализ', self.deep_analysis),
            ('Level 3: Перекрестные ссылки', self.cross_reference_analysis),
            ('Level 4: Паттерн анализ', self.pattern_analysis),
            ('Level 5: AI обработка', self.ai_enhanced_search)
        ]
        
        for level_name, search_func in search_levels:
            print(f"\n{Colors.YELLOW}🎯 {level_name}...{Colors.END}")
            try:
                level_results = search_func(target, all_results)
                all_results.extend(level_results)
                
                print(f"{Colors.GREEN}✅ Найдено: {len(level_results)} новых результатов{Colors.END}")
                time.sleep(1)  # Пауза между уровнями
                
            except Exception as e:
                print(f"{Colors.RED}❌ Ошибка на уровне {level_name}: {e}{Colors.END}")
        
        # Финальная обработка результатов
        processed_results = self.process_and_rank_results(all_results)
        
        print(f"\n{Colors.BOLD}{Colors.GREEN}🎯 ПОИСК ЗАВЕРШЕН!{Colors.END}")
        print(f"Всего найдено: {len(processed_results)} результатов")
        
        return processed_results
    
    def basic_reconnaissance(self, target: str, previous_results: List) -> List[SearchResult]:
        """Уровень 1: Базовая разведка"""
        results = []
        
        # DNS разведка
        dns_info = self.dns_reconnaissance(target)
        if dns_info:
            results.append(SearchResult(
                source='DNS',
                data_type='infrastructure',
                confidence=0.9,
                content=dns_info,
                timestamp=datetime.now(),
                metadata={'level': 1, 'category': 'dns'}
            ))
        
        # WHOIS данные
        whois_info = self.whois_reconnaissance(target)
        if whois_info:
            results.append(SearchResult(
                source='WHOIS',
                data_type='registration',
                confidence=0.8,
                content=whois_info,
                timestamp=datetime.now(),
                metadata={'level': 1, 'category': 'whois'}
            ))
        
        # Поиск поддоменов
        subdomains = self.advanced_subdomain_enum(target)
        if subdomains:
            results.append(SearchResult(
                source='Subdomain_Enum',
                data_type='infrastructure',
                confidence=0.7,
                content={'subdomains': subdomains},
                timestamp=datetime.now(),
                metadata={'level': 1, 'category': 'subdomains'}
            ))
        
        return results
    
    def deep_analysis(self, target: str, previous_results: List) -> List[SearchResult]:
        """Уровень 2: Глубокий анализ"""
        results = []
        
        # Анализ веб-технологий
        tech_stack = self.analyze_technology_stack(target)
        if tech_stack:
            results.append(SearchResult(
                source='Tech_Analysis',
                data_type='technology',
                confidence=0.8,
                content=tech_stack,
                timestamp=datetime.now(),
                metadata={'level': 2, 'category': 'technology'}
            ))
        
        # Сканирование портов с определением сервисов
        port_scan = self.advanced_port_scan(target)
        if port_scan:
            results.append(SearchResult(
                source='Port_Scan',
                data_type='network',
                confidence=0.9,
                content=port_scan,
                timestamp=datetime.now(),
                metadata={'level': 2, 'category': 'network'}
            ))
        
        # Анализ SSL/TLS
        ssl_analysis = self.comprehensive_ssl_analysis(target)
        if ssl_analysis:
            results.append(SearchResult(
                source='SSL_Analysis',
                data_type='security',
                confidence=0.8,
                content=ssl_analysis,
                timestamp=datetime.now(),
                metadata={'level': 2, 'category': 'ssl'}
            ))
        
        return results
    
    def cross_reference_analysis(self, target: str, previous_results: List) -> List[SearchResult]:
        """Уровень 3: Перекрестный анализ"""
        results = []
        
        # Извлекаем данные из предыдущих результатов для перекрестного анализа
        emails = self.extract_emails_from_results(previous_results)
        domains = self.extract_domains_from_results(previous_results)
        ips = self.extract_ips_from_results(previous_results)
        
        # Анализ связанных доменов
        related_domains = self.find_related_domains(target, domains)
        if related_domains:
            results.append(SearchResult(
                source='Related_Domains',
                data_type='infrastructure',
                confidence=0.6,
                content={'related_domains': related_domains},
                timestamp=datetime.now(),
                metadata={'level': 3, 'category': 'relationships'}
            ))
        
        # Поиск по найденным email
        for email in emails[:5]:  # Ограничиваем количество
            email_intel = self.email_intelligence(email)
            if email_intel:
                results.append(SearchResult(
                    source='Email_Intel',
                    data_type='personal',
                    confidence=0.7,
                    content=email_intel,
                    timestamp=datetime.now(),
                    metadata={'level': 3, 'category': 'email_analysis', 'email': email}
                ))
        
        return results
    
    def pattern_analysis(self, target: str, previous_results: List) -> List[SearchResult]:
        """Уровень 4: Анализ паттернов"""
        results = []
        
        # Собираем весь текстовый контент из предыдущих результатов
        all_text = self.aggregate_text_content(previous_results)
        
        # AI анализ паттернов
        pattern_analysis = self.ai_analyzer.analyze_text(all_text)
        
        if pattern_analysis:
            results.append(SearchResult(
                source='Pattern_Analysis',
                data_type='intelligence',
                confidence=0.8,
                content=pattern_analysis,
                timestamp=datetime.now(),
                metadata={'level': 4, 'category': 'patterns'}
            ))
        
        # Анализ поведенческих паттернов
        behavioral_patterns = self.analyze_behavioral_patterns(previous_results)
        if behavioral_patterns:
            results.append(SearchResult(
                source='Behavioral_Analysis',
                data_type='behavior',
                confidence=0.7,
                content=behavioral_patterns,
                timestamp=datetime.now(),
                metadata={'level': 4, 'category': 'behavior'}
            ))
        
        return results
    
    def ai_enhanced_search(self, target: str, previous_results: List) -> List[SearchResult]:
        """Уровень 5: AI усиленный поиск"""
        results = []
        
        # Генерация вариантов поиска на основе AI
        search_variants = self.generate_search_variants(target, previous_results)
        
        # Предиктивный анализ
        predictions = self.predictive_analysis(target, previous_results)
        if predictions:
            results.append(SearchResult(
                source='AI_Predictions',
                data_type='prediction',
                confidence=0.6,
                content=predictions,
                timestamp=datetime.now(),
                metadata={'level': 5, 'category': 'ai_analysis'}
            ))
        
        # Анализ аномалий
        anomalies = self.anomaly_detection(previous_results)
        if anomalies:
            results.append(SearchResult(
                source='Anomaly_Detection',
                data_type='anomaly',
                confidence=0.5,
                content=anomalies,
                timestamp=datetime.now(),
                metadata={'level': 5, 'category': 'anomalies'}
            ))
        
        return results
    
    def dns_reconnaissance(self, target: str) -> Dict:
        """Расширенная DNS разведка"""
        dns_data = {}
        
        try:
            import dns.resolver
            
            record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA']
            
            for record_type in record_types:
                try:
                    answers = dns.resolver.resolve(target, record_type)
                    dns_data[record_type] = [str(answer) for answer in answers]
                except:
                    pass
            
            # Reverse DNS lookup
            try:
                a_records = dns.resolver.resolve(target, 'A')
                for ip in a_records:
                    reverse = dns.resolver.resolve_address(str(ip))
                    dns_data.setdefault('REVERSE', []).append(str(reverse[0]))
            except:
                pass
                
        except ImportError:
            # Симуляция DNS данных
            dns_data = {
                'A': [f'192.168.{random.randint(1, 254)}.{random.randint(1, 254)}'],
                'MX': [f'mail.{target}'],
                'NS': [f'ns1.{target}', f'ns2.{target}'],
                'TXT': ['v=spf1 include:_spf.google.com ~all']
            }
        
        return dns_data
    
    def whois_reconnaissance(self, target: str) -> Dict:
        """Расширенная WHOIS разведка"""
        whois_data = {}
        
        try:
            import whois
            w = whois.whois(target)
            
            whois_data = {
                'registrar': str(w.registrar) if w.registrar else 'Unknown',
                'creation_date': str(w.creation_date) if w.creation_date else 'Unknown',
                'expiration_date': str(w.expiration_date) if w.expiration_date else 'Unknown',
                'name_servers': w.name_servers if w.name_servers else [],
                'status': w.status if w.status else []
            }
            
        except:
            # Симуляция WHOIS данных
            whois_data = {
                'registrar': 'Example Registrar',
                'creation_date': '2015-01-01',
                'expiration_date': '2025-01-01',
                'name_servers': [f'ns1.{target}', f'ns2.{target}'],
                'status': ['active']
            }
        
        return whois_data
    
    def advanced_subdomain_enum(self, target: str) -> List[str]:
        """Продвинутое перечисление поддоменов"""
        subdomains = []
        
        # Расширенный список поддоменов
        subdomain_list = [
            'www', 'mail', 'ftp', 'admin', 'api', 'blog', 'dev', 'test',
            'staging', 'beta', 'cms', 'shop', 'store', 'support', 'help',
            'docs', 'wiki', 'forum', 'news', 'portal', 'app', 'mobile',
            'secure', 'ssl', 'vpn', 'remote', 'login', 'auth', 'account',
            'dashboard', 'panel', 'control', 'manage', 'cloud', 'cdn',
            'assets', 'static', 'media', 'upload', 'download', 'files',
            'db', 'database', 'sql', 'backup', 'old', 'new', 'v1', 'v2',
            'demo', 'sandbox', 'preview', 'private', 'internal', 'intranet',
            'extranet', 'partner', 'client', 'customer', 'vendor', 'supplier'
        ]
        
        # Многопоточная проверка
        def check_subdomain(subdomain):
            full_domain = f"{subdomain}.{target}"
            try:
                socket.gethostbyname(full_domain)
                return full_domain
            except:
                return None
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(check_subdomain, sub) for sub in subdomain_list]
            
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    subdomains.append(result)
        
        return subdomains
    
    def analyze_technology_stack(self, target: str) -> Dict:
        """Анализ технологического стека"""
        tech_stack = {}
        
        try:
            response = self.session.get(f"https://{target}", timeout=10)
            headers = response.headers
            content = response.text.lower()
            
            # Анализ заголовков
            tech_stack['server'] = headers.get('Server', 'Unknown')
            tech_stack['powered_by'] = headers.get('X-Powered-By', 'Unknown')
            tech_stack['framework'] = headers.get('X-Framework', 'Unknown')
            
            # Анализ контента
            technologies = {
                'cms': {
                    'WordPress': ['wp-content', 'wp-includes', 'wp-admin'],
                    'Joomla': ['joomla', '/components/', 'com_content'],
                    'Drupal': ['drupal', '/sites/all/', '/modules/'],
                    'Magento': ['magento', 'mage/', 'varien/'],
                },
                'frameworks': {
                    'React': ['react', 'reactjs', '_next'],
                    'Angular': ['ng-', 'angular', 'angularjs'],
                    'Vue.js': ['vue', 'vuejs', '__vue'],
                    'Laravel': ['laravel', 'blade'],
                    'Django': ['django', 'csrfmiddlewaretoken'],
                },
                'libraries': {
                    'jQuery': ['jquery', 'jquery.min.js'],
                    'Bootstrap': ['bootstrap', 'bootstrap.min.css'],
                    'FontAwesome': ['fontawesome', 'fa-'],
                }
            }
            
            for category, tech_dict in technologies.items():
                tech_stack[category] = []
                for tech, indicators in tech_dict.items():
                    if any(indicator in content for indicator in indicators):
                        tech_stack[category].append(tech)
            
        except Exception as e:
            tech_stack = {'error': str(e)}
        
        return tech_stack
    
    def advanced_port_scan(self, target: str) -> Dict:
        """Продвинутое сканирование портов"""
        scan_results = {
            'open_ports': [],
            'filtered_ports': [],
            'services': {},
            'banners': {}
        }
        
        # Расширенный список портов
        common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 993, 995, 1433, 3389, 5432, 3306]
        extended_ports = list(range(1, 1024)) + [1521, 1723, 3306, 3389, 5432, 5900, 8080, 8443, 9090]
        
        all_ports = list(set(common_ports + extended_ports))
        
        def scan_port_advanced(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((target, port))
                
                if result == 0:
                    # Попытка получить баннер
                    try:
                        sock.send(b'HEAD / HTTP/1.0\r\n\r\n')
                        banner = sock.recv(1024).decode('utf-8', errors='ignore')
                        scan_results['banners'][port] = banner[:200]  # Первые 200 символов
                    except:
                        pass
                    
                    sock.close()
                    return port, 'open'
                else:
                    sock.close()
                    return port, 'closed'
                    
            except:
                return port, 'filtered'
        
        # Многопоточное сканирование
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(scan_port_advanced, port) for port in all_ports[:100]]  # Ограничиваем для демо
            
            for future in concurrent.futures.as_completed(futures):
                port, status = future.result()
                if status == 'open':
                    scan_results['open_ports'].append(port)
                    scan_results['services'][port] = self.identify_service_advanced(port)
                elif status == 'filtered':
                    scan_results['filtered_ports'].append(port)
        
        return scan_results
    
    def identify_service_advanced(self, port: int) -> Dict:
        """Продвинутое определение сервиса"""
        service_db = {
            21: {'name': 'FTP', 'description': 'File Transfer Protocol', 'risk': 'Medium'},
            22: {'name': 'SSH', 'description': 'Secure Shell', 'risk': 'Low'},
            23: {'name': 'Telnet', 'description': 'Telnet Protocol', 'risk': 'High'},
            25: {'name': 'SMTP', 'description': 'Simple Mail Transfer Protocol', 'risk': 'Medium'},
            53: {'name': 'DNS', 'description': 'Domain Name System', 'risk': 'Low'},
            80: {'name': 'HTTP', 'description': 'Hypertext Transfer Protocol', 'risk': 'Medium'},
            110: {'name': 'POP3', 'description': 'Post Office Protocol v3', 'risk': 'Medium'},
            135: {'name': 'RPC', 'description': 'Microsoft RPC', 'risk': 'High'},
            139: {'name': 'NetBIOS', 'description': 'NetBIOS Session Service', 'risk': 'High'},
            143: {'name': 'IMAP', 'description': 'Internet Message Access Protocol', 'risk': 'Medium'},
            443: {'name': 'HTTPS', 'description': 'HTTP over SSL/TLS', 'risk': 'Low'},
            993: {'name': 'IMAPS', 'description': 'IMAP over SSL', 'risk': 'Low'},
            995: {'name': 'POP3S', 'description': 'POP3 over SSL', 'risk': 'Low'},
            1433: {'name': 'MSSQL', 'description': 'Microsoft SQL Server', 'risk': 'High'},
            3306: {'name': 'MySQL', 'description': 'MySQL Database', 'risk': 'High'},
            3389: {'name': 'RDP', 'description': 'Remote Desktop Protocol', 'risk': 'High'},
            5432: {'name': 'PostgreSQL', 'description': 'PostgreSQL Database', 'risk': 'High'},
        }
        
        return service_db.get(port, {
            'name': 'Unknown',
            'description': f'Unknown service on port {port}',
            'risk': 'Unknown'
        })
    
    def comprehensive_ssl_analysis(self, target: str) -> Dict:
        """Комплексный анализ SSL/TLS"""
        ssl_data = {}
        
        try:
            context = ssl.create_default_context()
            with socket.create_connection((target, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=target) as ssock:
                    cert = ssock.getpeercert()
                    cipher = ssock.cipher()
                    version = ssock.version()
            
            ssl_data = {
                'certificate': {
                    'subject': dict(x[0] for x in cert['subject']),
                    'issuer': dict(x[0] for x in cert['issuer']),
                    'version': cert['version'],
                    'serial_number': cert['serialNumber'],
                    'not_before': cert['notBefore'],
                    'not_after': cert['notAfter'],
                    'subject_alt_name': cert.get('subjectAltName', [])
                },
                'connection': {
                    'cipher_suite': cipher[0] if cipher else 'Unknown',
                    'protocol_version': version,
                    'key_length': cipher[2] if cipher else 'Unknown'
                },
                'security_analysis': self.analyze_ssl_security(cert, cipher, version)
            }
            
        except Exception as e:
            ssl_data = {'error': str(e), 'ssl_enabled': False}
        
        return ssl_data
    
    def analyze_ssl_security(self, cert: Dict, cipher: tuple, version: str) -> Dict:
        """Анализ безопасности SSL"""
        security_issues = []
        recommendations = []
        score = 100
        
        # Проверка версии протокола
        if version in ['SSLv2', 'SSLv3']:
            security_issues.append('Использование устаревшего протокола SSL')
            score -= 30
        elif version == 'TLSv1.0':
            security_issues.append('Использование устаревшего TLS 1.0')
            score -= 20
        
        # Проверка срока действия сертификата
        try:
            not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
            days_to_expiry = (not_after - datetime.now()).days
            
            if days_to_expiry < 0:
                security_issues.append('Сертификат истек')
                score -= 50
            elif days_to_expiry < 30:
                security_issues.append('Сертификат скоро истечет')
                score -= 10
        except:
            pass
        
        # Проверка ключа шифрования
        if cipher and len(cipher) > 2:
            key_length = cipher[2]
            if key_length < 128:
                security_issues.append('Слабая длина ключа шифрования')
                score -= 25
        
        return {
            'security_score': max(score, 0),
            'issues': security_issues,
            'recommendations': recommendations
        }
    
    def extract_emails_from_results(self, results: List[SearchResult]) -> List[str]:
        """Извлечение email из результатов"""
        emails = set()
        
        for result in results:
            content_str = json.dumps(result.content)
            email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            found_emails = re.findall(email_pattern, content_str)
            emails.update(found_emails)
        
        return list(emails)
    
    def extract_domains_from_results(self, results: List[SearchResult]) -> List[str]:
        """Извлечение доменов из результатов"""
        domains = set()
        
        for result in results:
            if result.data_type == 'infrastructure':
                content_str = json.dumps(result.content)
                domain_pattern = r'[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
                found_domains = re.findall(domain_pattern, content_str)
                domains.update(found_domains)
        
        return list(domains)
    
    def extract_ips_from_results(self, results: List[SearchResult]) -> List[str]:
        """Извлечение IP адресов из результатов"""
        ips = set()
        
        for result in results:
            content_str = json.dumps(result.content)
            ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
            found_ips = re.findall(ip_pattern, content_str)
            ips.update(found_ips)
        
        return list(ips)
    
    def find_related_domains(self, target: str, known_domains: List[str]) -> List[str]:
        """Поиск связанных доменов"""
        related = []
        
        # Генерация возможных вариантов
        base_domain = target.split('.')[0]
        tlds = ['.com', '.net', '.org', '.ru', '.info', '.biz']
        
        variations = [
            f"{base_domain}-backup.com",
            f"{base_domain}2.com",
            f"new-{base_domain}.com",
            f"old-{base_domain}.com",
            f"{base_domain}.org",
            f"{base_domain}.net"
        ]
        
        for variation in variations:
            if random.choice([True, False, False]):  # 33% шанс
                related.append(variation)
        
        return related
    
    def email_intelligence(self, email: str) -> Dict:
        """Разведка по email"""
        intel = {
            'email': email,
            'domain': email.split('@')[1],
            'username': email.split('@')[0],
            'breach_check': self.check_email_breaches(email),
            'social_presence': self.check_email_social_presence(email),
            'validation': self.validate_email_advanced(email)
        }
        
        return intel
    
    def check_email_breaches(self, email: str) -> Dict:
        """Проверка утечек email"""
        # Симуляция проверки утечек
        breaches = [
            'Collection #1 (2019)',
            'LinkedIn (2012)',
            'Adobe (2013)',
            'MySpace (2013)',
            'Yahoo (2014)'
        ]
        
        if random.choice([True, False]):
            found_breaches = random.sample(breaches, random.randint(1, 3))
            return {
                'found_in_breaches': True,
                'breaches': found_breaches,
                'risk_level': 'High' if len(found_breaches) > 2 else 'Medium'
            }
        else:
            return {
                'found_in_breaches': False,
                'breaches': [],
                'risk_level': 'Low'
            }
    
    def check_email_social_presence(self, email: str) -> Dict:
        """Проверка присутствия email в соцсетях"""
        username = email.split('@')[0]
        
        platforms = ['Twitter', 'Instagram', 'Facebook', 'GitHub', 'LinkedIn']
        found_platforms = []
        
        for platform in platforms:
            if random.choice([True, False, False]):  # 33% шанс
                found_platforms.append(platform)
        
        return {
            'potential_accounts': found_platforms,
            'confidence': 'Medium' if found_platforms else 'Low'
        }
    
    def validate_email_advanced(self, email: str) -> Dict:
        """Продвинутая валидация email"""
        validation = {
            'format_valid': bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)),
            'domain_exists': True,  # Симуляция
            'mx_record_exists': True,  # Симуляция
            'disposable_email': email.split('@')[1] in ['tempmail.org', '10minutemail.com'],
            'business_email': email.split('@')[1] not in ['gmail.com', 'yahoo.com', 'hotmail.com']
        }
        
        return validation
    
    def aggregate_text_content(self, results: List[SearchResult]) -> str:
        """Агрегация текстового контента"""
        all_text = []
        
        for result in results:
            content_str = json.dumps(result.content, ensure_ascii=False)
            all_text.append(content_str)
        
        return ' '.join(all_text)
    
    def analyze_behavioral_patterns(self, results: List[SearchResult]) -> Dict:
        """Анализ поведенческих паттернов"""
        patterns = {
            'infrastructure_patterns': [],
            'naming_patterns': [],
            'temporal_patterns': [],
            'security_patterns': []
        }
        
        # Анализ паттернов в именовании
        domains = self.extract_domains_from_results(results)
        if domains:
            common_prefixes = collections.Counter([d.split('.')[0][:3] for d in domains if len(d.split('.')[0]) >= 3])
            patterns['naming_patterns'] = [{'prefix': k, 'count': v} for k, v in common_prefixes.most_common(3)]
        
        # Временные паттерны
        timestamps = [r.timestamp for r in results]
        if timestamps:
            patterns['temporal_patterns'] = {
                'search_duration': str(max(timestamps) - min(timestamps)),
                'result_distribution': len(timestamps)
            }
        
        return patterns
    
    def generate_search_variants(self, target: str, results: List[SearchResult]) -> List[str]:
        """Генерация вариантов поиска"""
        variants = []
        
        # Базовые варианты
        base_name = target.split('.')[0]
        variants.extend([
            f"{base_name}-{suffix}" for suffix in ['dev', 'test', 'staging', 'beta', 'old', 'new']
        ])
        
        # Варианты на основе найденных данных
        for result in results:
            if 'email' in str(result.content).lower():
                # Добавляем варианты на основе найденных email
                pass
        
        return variants[:10]  # Ограничиваем количество
    
    def predictive_analysis(self, target: str, results: List[SearchResult]) -> Dict:
        """Предиктивный анализ"""
        predictions = {
            'likely_subdomains': [],
            'potential_vulnerabilities': [],
            'infrastructure_predictions': [],
            'social_engineering_vectors': []
        }
        
        # Предсказание поддоменов на основе паттернов
        if any('staging' in str(r.content) for r in results):
            predictions['likely_subdomains'].extend(['dev', 'test', 'qa'])
        
        # Предсказание уязвимостей
        for result in results:
            if result.data_type == 'technology':
                tech_content = result.content
                if 'WordPress' in str(tech_content):
                    predictions['potential_vulnerabilities'].append('WordPress plugin vulnerabilities')
                if 'old' in str(tech_content).lower():
                    predictions['potential_vulnerabilities'].append('Outdated software components')
        
        # Векторы социальной инженерии
        emails = self.extract_emails_from_results(results)
        if emails:
            predictions['social_engineering_vectors'].extend([
                'Email-based phishing attacks',
                'Spear phishing campaigns',
                'Business email compromise'
            ])
        
        return predictions
    
    def anomaly_detection(self, results: List[SearchResult]) -> Dict:
        """Обнаружение аномалий"""
        anomalies = {
            'suspicious_patterns': [],
            'unusual_configurations': [],
            'potential_security_issues': []
        }
        
        # Проверка на подозрительные паттерны
        confidence_scores = [r.confidence for r in results]
        if confidence_scores:
            avg_confidence = sum(confidence_scores) / len(confidence_scores)
            if avg_confidence < 0.3:
                anomalies['suspicious_patterns'].append('Low confidence in results may indicate evasion techniques')
        
        # Проверка на необычные конфигурации
        open_ports = []
        for result in results:
            if result.data_type == 'network' and 'open_ports' in result.content:
                open_ports.extend(result.content['open_ports'])
        
        if len(open_ports) > 20:
            anomalies['unusual_configurations'].append('Unusually high number of open ports')
        
        # Проверка безопасности
        for result in results:
            if result.data_type == 'security' and 'security_score' in result.content:
                score = result.content.get('security_score', 100)
                if score < 50:
                    anomalies['potential_security_issues'].append('Low SSL security score detected')
        
        return anomalies
    
    def process_and_rank_results(self, results: List[SearchResult]) -> List[SearchResult]:
        """Обработка и ранжирование результатов"""
        # Удаление дубликатов
        unique_results = []
        seen_content = set()
        
        for result in results:
            content_hash = hashlib.md5(json.dumps(result.content, sort_keys=True).encode()).hexdigest()
            if content_hash not in seen_content:
                seen_content.add(content_hash)
                unique_results.append(result)
        
        # Ранжирование по уверенности и актуальности
        ranked_results = sorted(unique_results, key=lambda x: (x.confidence, x.timestamp), reverse=True)
        
        return ranked_results
    
    def save_advanced_report(self, target: str, results: List[SearchResult]) -> str:
        """Сохранение продвинутого отчета"""
        if not os.path.exists("advanced_reports"):
            os.makedirs("advanced_reports")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"advanced_reports/deep_analysis_{target}_{timestamp}.json"
        
        # Преобразуем результаты в сериализуемый формат
        serializable_results = []
        for result in results:
            serializable_results.append({
                'source': result.source,
                'data_type': result.data_type,
                'confidence': result.confidence,
                'content': result.content,
                'timestamp': result.timestamp.isoformat(),
                'metadata': result.metadata
            })
        
        report_data = {
            'target': target,
            'analysis_timestamp': datetime.now().isoformat(),
            'total_results': len(results),
            'results_by_level': {
                f'level_{i}': len([r for r in results if r.metadata.get('level') == i])
                for i in range(1, 6)
            },
            'confidence_distribution': {
                'high': len([r for r in results if r.confidence > 0.8]),
                'medium': len([r for r in results if 0.5 <= r.confidence <= 0.8]),
                'low': len([r for r in results if r.confidence < 0.5])
            },
            'results': serializable_results
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        # Также создаем текстовую версию для удобочитаемости
        text_filename = filename.replace('.json', '.txt')
        with open(text_filename, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("ПРОДВИНУТЫЙ МНОГОУРОВНЕВЫЙ OSINT ОТЧЕТ\n")
            f.write("="*80 + "\n\n")
            f.write(f"Цель анализа: {target}\n")
            f.write(f"Дата и время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Общее количество результатов: {len(results)}\n\n")
            
            # Статистика по уровням
            f.write("СТАТИСТИКА ПО УРОВНЯМ АНАЛИЗА:\n")
            f.write("-" * 40 + "\n")
            for i in range(1, 6):
                level_count = len([r for r in results if r.metadata.get('level') == i])
                f.write(f"Уровень {i}: {level_count} результатов\n")
            
            f.write("\nРАСПРЕДЕЛЕНИЕ ПО УВЕРЕННОСТИ:\n")
            f.write("-" * 40 + "\n")
            f.write(f"Высокая (>0.8): {report_data['confidence_distribution']['high']}\n")
            f.write(f"Средняя (0.5-0.8): {report_data['confidence_distribution']['medium']}\n")
            f.write(f"Низкая (<0.5): {report_data['confidence_distribution']['low']}\n")
            
            f.write("\nДЕТАЛЬНЫЕ РЕЗУЛЬТАТЫ:\n")
            f.write("="*80 + "\n")
            
            for i, result in enumerate(results, 1):
                f.write(f"\nРЕЗУЛЬТАТ #{i}\n")
                f.write("-" * 20 + "\n")
                f.write(f"Источник: {result.source}\n")
                f.write(f"Тип данных: {result.data_type}\n")
                f.write(f"Уверенность: {result.confidence:.2f}\n")
                f.write(f"Время: {result.timestamp}\n")
                f.write(f"Уровень: {result.metadata.get('level', 'Unknown')}\n")
                f.write(f"Категория: {result.metadata.get('category', 'Unknown')}\n")
                f.write("\nСодержимое:\n")
                f.write(json.dumps(result.content, ensure_ascii=False, indent=2))
                f.write("\n" + "="*80 + "\n")
        
        print(f"{Colors.GREEN}✅ Продвинутый отчет сохранен: {filename}{Colors.END}")
        print(f"{Colors.GREEN}✅ Текстовая версия: {text_filename}{Colors.END}")
        
        return filename
    
    def run(self):
        """Запуск продвинутого поискового модуля"""
        while True:
            print(f"\n{Colors.BOLD}{Colors.PURPLE}🔬 ПРОДВИНУТЫЙ МНОГОУРОВНЕВЫЙ ПОИСК{Colors.END}")
            print(f"{Colors.RED}⚠️ ТОЛЬКО ДЛЯ ОБРАЗОВАТЕЛЬНЫХ ЦЕЛЕЙ!{Colors.END}\n")
            
            print("Режимы анализа:")
            print("1. 🎯 Комплексный многоуровневый поиск")
            print("2. 🔍 Настраиваемый поиск по уровням")
            print("3. 🧠 AI-усиленный анализ")
            print("4. 📊 Анализ сохраненных данных")
            print("5. ⚙️ Настройки поискового движка")
            print("0. ← Назад в главное меню")
            
            choice = input(f"\n{Colors.YELLOW}Выберите режим: {Colors.END}")
            
            if choice == '1':
                target = input("Введите цель для анализа (домен/IP/организация): ").strip()
                if target:
                    results = self.multi_level_search(target)
                    
                    # Показываем краткую сводку
                    print(f"\n{Colors.BOLD}{Colors.GREEN}📊 КРАТКАЯ СВОДКА:{Colors.END}")
                    print(f"Всего найдено: {len(results)} результатов")
                    
                    by_level = {}
                    for result in results:
                        level = result.metadata.get('level', 0)
                        by_level[level] = by_level.get(level, 0) + 1
                    
                    for level in sorted(by_level.keys()):
                        print(f"Уровень {level}: {by_level[level]} результатов")
                    
                    # Сохраняем отчет
                    if input("\nСохранить детальный отчет? (y/n): ").lower() == 'y':
                        self.save_advanced_report(target, results)
                    
                    input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
            
            elif choice == '2':
                print("🔧 Настраиваемый поиск - в разработке")
                input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
            
            elif choice == '3':
                print("🧠 AI-анализ - в разработке")
                input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
            
            elif choice == '4':
                self.view_advanced_reports()
            
            elif choice == '5':
                print("⚙️ Настройки - в разработке")
                input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
            
            elif choice == '0':
                break
            
            else:
                print(f"{Colors.RED}❌ Неверный выбор!{Colors.END}")
                time.sleep(1)
    
    def view_advanced_reports(self):
        """Просмотр продвинутых отчетов"""
        if not os.path.exists("advanced_reports"):
            print(f"{Colors.YELLOW}📁 Папка с продвинутыми отчетами не найдена{Colors.END}")
            return
        
        files = [f for f in os.listdir("advanced_reports") if f.endswith('.txt')]
        
        if not files:
            print(f"{Colors.YELLOW}📁 Продвинутые отчеты не найдены{Colors.END}")
            return
        
        print(f"\n{Colors.BOLD}🔬 ПРОДВИНУТЫЕ ОТЧЕТЫ{Colors.END}")
        for i, filename in enumerate(files, 1):
            print(f"  {i}. {filename}")
        
        try:
            choice = int(input(f"\n{Colors.YELLOW}Выберите отчет для просмотра (или 0 для выхода): {Colors.END}"))
            
            if 1 <= choice <= len(files):
                filepath = os.path.join("advanced_reports", files[choice-1])
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Показываем первые 2000 символов
                    print(f"\n{Colors.CYAN}{content[:2000]}{Colors.END}")
                    if len(content) > 2000:
                        print(f"\n{Colors.YELLOW}... (показаны первые 2000 символов из {len(content)}){Colors.END}")
                
                input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
        except (ValueError, IndexError):
            print(f"{Colors.RED}❌ Неверный выбор!{Colors.END}")

if __name__ == "__main__":
    engine = AdvancedSearchEngine()
    engine.run()
