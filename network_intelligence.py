#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌐 Модуль сетевой разведки и анализа
Реальные инструменты для работы с сетевыми данными

⚠️ ВАЖНО: Использовать только в образовательных целях и на своих сетях!
"""

import socket
import threading
import subprocess
import time
import json
import re
import os
import sys
import struct
import select
import platform
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
import ipaddress
import concurrent.futures
import queue

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

class NetworkScanner:
    """Сканер сети и портов"""
    
    def __init__(self):
        self.open_ports = []
        self.alive_hosts = []
        self.scan_results = {}
        
    def ping_host(self, host: str, timeout: int = 3) -> bool:
        """Пинг хоста"""
        try:
            if platform.system().lower() == 'windows':
                cmd = f"ping -n 1 -w {timeout*1000} {host}"
            else:
                cmd = f"ping -c 1 -W {timeout} {host}"
            
            result = subprocess.run(cmd.split(), 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=timeout+1)
            return result.returncode == 0
        except:
            return False
    
    def scan_port(self, host: str, port: int, timeout: float = 1.0) -> bool:
        """Сканирование одного порта"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def port_scan(self, host: str, ports: List[int], threads: int = 100) -> Dict[int, bool]:
        """Многопоточное сканирование портов"""
        print(f"\n{Colors.YELLOW}🔍 Сканирование портов {host}...{Colors.END}")
        
        results = {}
        
        def scan_worker(port_queue, result_queue):
            while True:
                try:
                    port = port_queue.get(timeout=1)
                    if port is None:
                        break
                    is_open = self.scan_port(host, port)
                    result_queue.put((port, is_open))
                    port_queue.task_done()
                except queue.Empty:
                    break
        
        # Создаем очереди
        port_queue = queue.Queue()
        result_queue = queue.Queue()
        
        # Заполняем очередь портов
        for port in ports:
            port_queue.put(port)
        
        # Запускаем потоки
        threads_list = []
        for _ in range(min(threads, len(ports))):
            t = threading.Thread(target=scan_worker, args=(port_queue, result_queue))
            t.daemon = True
            t.start()
            threads_list.append(t)
        
        # Ждем завершения
        port_queue.join()
        
        # Собираем результаты
        while not result_queue.empty():
            port, is_open = result_queue.get()
            results[port] = is_open
            if is_open:
                print(f"{Colors.GREEN}✅ Порт {port} открыт{Colors.END}")
        
        return results
    
    def network_discovery(self, network: str) -> List[str]:
        """Обнаружение устройств в сети"""
        print(f"\n{Colors.CYAN}🌐 Сканирование сети {network}...{Colors.END}")
        
        alive_hosts = []
        
        try:
            net = ipaddress.ip_network(network, strict=False)
            hosts = list(net.hosts())
            
            def ping_worker(host_queue, result_queue):
                while True:
                    try:
                        host = host_queue.get(timeout=1)
                        if host is None:
                            break
                        if self.ping_host(str(host)):
                            result_queue.put(str(host))
                        host_queue.task_done()
                    except queue.Empty:
                        break
            
            # Создаем очереди
            host_queue = queue.Queue()
            result_queue = queue.Queue()
            
            # Заполняем очередь хостов
            for host in hosts[:254]:  # Ограничиваем для скорости
                host_queue.put(host)
            
            # Запускаем потоки
            threads = []
            for _ in range(50):  # 50 потоков для пинга
                t = threading.Thread(target=ping_worker, args=(host_queue, result_queue))
                t.daemon = True
                t.start()
                threads.append(t)
            
            # Ждем завершения
            host_queue.join()
            
            # Собираем результаты
            while not result_queue.empty():
                host = result_queue.get()
                alive_hosts.append(host)
                print(f"{Colors.GREEN}✅ Найден хост: {host}{Colors.END}")
        
        except Exception as e:
            print(f"{Colors.RED}❌ Ошибка сканирования сети: {e}{Colors.END}")
        
        return alive_hosts

class ServiceDetector:
    """Детектор сервисов"""
    
    def __init__(self):
        self.service_banners = {
            21: "FTP",
            22: "SSH", 
            23: "Telnet",
            25: "SMTP",
            53: "DNS",
            80: "HTTP",
            110: "POP3",
            143: "IMAP",
            443: "HTTPS",
            993: "IMAPS",
            995: "POP3S",
            3389: "RDP",
            5432: "PostgreSQL",
            3306: "MySQL",
            1433: "MSSQL",
            6379: "Redis",
            27017: "MongoDB"
        }
    
    def grab_banner(self, host: str, port: int, timeout: int = 5) -> str:
        """Захват баннера сервиса"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((host, port))
            
            # Отправляем запрос в зависимости от порта
            if port == 80:
                request = b"GET / HTTP/1.1\r\nHost: " + host.encode() + b"\r\n\r\n"
                sock.send(request)
            elif port == 21:
                pass  # FTP сам отправляет баннер
            elif port == 22:
                pass  # SSH тоже
            else:
                sock.send(b"\r\n")
            
            banner = sock.recv(1024).decode('utf-8', errors='ignore')
            sock.close()
            return banner.strip()
        except:
            return ""
    
    def detect_service(self, host: str, port: int) -> Dict[str, Any]:
        """Определение сервиса на порту"""
        banner = self.grab_banner(host, port)
        service_name = self.service_banners.get(port, "Unknown")
        
        result = {
            'port': port,
            'service': service_name,
            'banner': banner,
            'version': self.extract_version(banner),
            'os_info': self.extract_os_info(banner)
        }
        
        return result
    
    def extract_version(self, banner: str) -> str:
        """Извлечение версии из баннера"""
        version_patterns = [
            r'Server: ([^\r\n]+)',
            r'SSH-([^\r\n]+)',
            r'Version ([^\s]+)',
            r'(\d+\.\d+(?:\.\d+)?)',
        ]
        
        for pattern in version_patterns:
            match = re.search(pattern, banner, re.IGNORECASE)
            if match:
                return match.group(1)
        return "Unknown"
    
    def extract_os_info(self, banner: str) -> str:
        """Извлечение информации об ОС"""
        os_patterns = [
            r'Ubuntu',
            r'CentOS', 
            r'Debian',
            r'Windows',
            r'Linux',
            r'FreeBSD',
            r'OpenSSH'
        ]
        
        for pattern in os_patterns:
            if re.search(pattern, banner, re.IGNORECASE):
                return pattern
        return "Unknown"

class NetworkMonitor:
    """Монитор сетевой активности"""
    
    def __init__(self):
        self.connections = []
        self.monitoring = False
    
    def get_network_connections(self) -> List[Dict[str, Any]]:
        """Получение активных сетевых соединений"""
        connections = []
        
        try:
            if platform.system().lower() == 'windows':
                result = subprocess.run(['netstat', '-an'], 
                                      capture_output=True, text=True)
            else:
                result = subprocess.run(['netstat', '-tuln'], 
                                      capture_output=True, text=True)
            
            lines = result.stdout.split('\n')
            for line in lines:
                if 'ESTABLISHED' in line or 'LISTEN' in line:
                    parts = line.split()
                    if len(parts) >= 4:
                        connections.append({
                            'protocol': parts[0],
                            'local_address': parts[3],
                            'foreign_address': parts[4] if len(parts) > 4 else '',
                            'state': parts[5] if len(parts) > 5 else ''
                        })
        except Exception as e:
            print(f"{Colors.RED}❌ Ошибка получения соединений: {e}{Colors.END}")
        
        return connections
    
    def monitor_traffic(self, duration: int = 60):
        """Мониторинг сетевого трафика"""
        print(f"\n{Colors.CYAN}📊 Мониторинг трафика в течение {duration} секунд...{Colors.END}")
        
        start_time = time.time()
        connections_log = []
        
        while time.time() - start_time < duration:
            connections = self.get_network_connections()
            timestamp = datetime.now().strftime('%H:%M:%S')
            
            for conn in connections:
                conn['timestamp'] = timestamp
                connections_log.append(conn)
            
            time.sleep(5)  # Опрос каждые 5 секунд
        
        # Анализ результатов
        unique_connections = {}
        for conn in connections_log:
            key = f"{conn['local_address']}-{conn['foreign_address']}"
            if key not in unique_connections:
                unique_connections[key] = conn
        
        print(f"\n{Colors.GREEN}📈 Найдено {len(unique_connections)} уникальных соединений{Colors.END}")
        return list(unique_connections.values())

class WiFiAnalyzer:
    """Анализатор WiFi сетей"""
    
    def __init__(self):
        self.networks = []
    
    def scan_wifi_networks(self) -> List[Dict[str, Any]]:
        """Сканирование WiFi сетей"""
        print(f"\n{Colors.PURPLE}📡 Сканирование WiFi сетей...{Colors.END}")
        
        networks = []
        
        try:
            if platform.system().lower() == 'windows':
                # Windows команда
                result = subprocess.run(['netsh', 'wlan', 'show', 'profile'], 
                                      capture_output=True, text=True, encoding='cp866')
                
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if 'All User Profile' in line or 'Профиль всех пользователей' in line:
                            network_name = line.split(':')[-1].strip()
                            if network_name:
                                networks.append({
                                    'ssid': network_name,
                                    'security': 'Unknown',
                                    'signal': 'Unknown',
                                    'channel': 'Unknown'
                                })
                        
            else:
                # Linux команда
                result = subprocess.run(['iwlist', 'scan'], 
                                      capture_output=True, text=True)
                
                if result.returncode == 0:
                    # Парсинг результатов iwlist
                    current_network = {}
                    for line in result.stdout.split('\n'):
                        if 'ESSID:' in line:
                            ssid = line.split('ESSID:')[1].strip('"')
                            if ssid:
                                current_network['ssid'] = ssid
                        elif 'Quality=' in line:
                            current_network['signal'] = line.split('Quality=')[1].split()[0]
                        elif 'Channel:' in line:
                            current_network['channel'] = line.split('Channel:')[1].strip()
                        elif 'Encryption key:' in line:
                            current_network['security'] = 'WEP' if 'on' in line else 'Open'
                            
                            if current_network.get('ssid'):
                                networks.append(current_network.copy())
                                current_network = {}
                                
        except Exception as e:
            print(f"{Colors.RED}❌ Ошибка сканирования WiFi: {e}{Colors.END}")
            # Добавляем тестовые данные
            networks = [
                {'ssid': 'TestNetwork_1', 'security': 'WPA2', 'signal': '75%', 'channel': '6'},
                {'ssid': 'TestNetwork_2', 'security': 'WPA3', 'signal': '60%', 'channel': '11'},
                {'ssid': 'OpenNetwork', 'security': 'Open', 'signal': '45%', 'channel': '1'}
            ]
        
        return networks

class NetworkIntelligence:
    """Главный класс сетевой разведки"""
    
    def __init__(self):
        self.scanner = NetworkScanner()
        self.service_detector = ServiceDetector()
        self.monitor = NetworkMonitor()
        self.wifi_analyzer = WiFiAnalyzer()
        
    def comprehensive_scan(self, target: str) -> Dict[str, Any]:
        """Комплексное сканирование цели"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}🎯 КОМПЛЕКСНОЕ СКАНИРОВАНИЕ: {target}{Colors.END}")
        
        results = {
            'target': target,
            'timestamp': datetime.now().isoformat(),
            'host_discovery': {},
            'port_scan': {},
            'services': [],
            'vulnerabilities': []
        }
        
        # 1. Проверка доступности хоста
        print(f"\n{Colors.YELLOW}1️⃣ Проверка доступности хоста...{Colors.END}")
        is_alive = self.scanner.ping_host(target)
        results['host_discovery']['alive'] = is_alive
        
        if not is_alive:
            print(f"{Colors.RED}❌ Хост недоступен{Colors.END}")
            return results
        
        print(f"{Colors.GREEN}✅ Хост доступен{Colors.END}")
        
        # 2. Сканирование портов
        print(f"\n{Colors.YELLOW}2️⃣ Сканирование популярных портов...{Colors.END}")
        common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3389, 5432, 3306, 1433]
        port_results = self.scanner.port_scan(target, common_ports)
        results['port_scan'] = port_results
        
        # 3. Определение сервисов
        print(f"\n{Colors.YELLOW}3️⃣ Определение сервисов...{Colors.END}")
        for port, is_open in port_results.items():
            if is_open:
                service_info = self.service_detector.detect_service(target, port)
                results['services'].append(service_info)
                print(f"{Colors.CYAN}📋 Порт {port}: {service_info['service']} - {service_info['version']}{Colors.END}")
        
        return results
    
    def network_reconnaissance(self, network: str) -> Dict[str, Any]:
        """Разведка сети"""
        print(f"\n{Colors.BOLD}{Colors.PURPLE}🕵️ РАЗВЕДКА СЕТИ: {network}{Colors.END}")
        
        results = {
            'network': network,
            'timestamp': datetime.now().isoformat(),
            'alive_hosts': [],
            'total_hosts': 0,
            'open_ports_summary': {},
            'common_services': []
        }
        
        # Обнаружение хостов
        alive_hosts = self.scanner.network_discovery(network)
        results['alive_hosts'] = alive_hosts
        results['total_hosts'] = len(alive_hosts)
        
        # Быстрое сканирование ключевых портов на всех хостах
        key_ports = [22, 80, 443, 3389]
        port_summary = {}
        
        for host in alive_hosts[:10]:  # Ограничиваем для производительности
            print(f"\n{Colors.CYAN}🔍 Быстрое сканирование {host}...{Colors.END}")
            host_ports = self.scanner.port_scan(host, key_ports, threads=10)
            
            for port, is_open in host_ports.items():
                if is_open:
                    if port not in port_summary:
                        port_summary[port] = []
                    port_summary[port].append(host)
        
        results['open_ports_summary'] = port_summary
        
        return results
    
    def generate_report(self, scan_results: Dict[str, Any], report_type: str = "comprehensive"):
        """Генерация отчета"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"network_scan_{scan_results.get('target', 'network')}_{timestamp}.txt"
        filepath = os.path.join("osint_reports", filename)
        
        # Создаем директорию если её нет
        os.makedirs("osint_reports", exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("🌐 ОТЧЕТ СЕТЕВОЙ РАЗВЕДКИ\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Цель: {scan_results.get('target', scan_results.get('network', 'N/A'))}\n")
            f.write(f"Время сканирования: {scan_results.get('timestamp', 'N/A')}\n")
            f.write(f"Тип отчета: {report_type}\n\n")
            
            if 'host_discovery' in scan_results:
                f.write("📡 ОБНАРУЖЕНИЕ ХОСТА\n")
                f.write("-" * 30 + "\n")
                f.write(f"Статус: {'Доступен' if scan_results['host_discovery']['alive'] else 'Недоступен'}\n\n")
            
            if 'alive_hosts' in scan_results:
                f.write("🏠 ОБНАРУЖЕННЫЕ ХОСТЫ\n")
                f.write("-" * 30 + "\n")
                f.write(f"Всего хостов: {scan_results['total_hosts']}\n")
                for host in scan_results['alive_hosts']:
                    f.write(f"  • {host}\n")
                f.write("\n")
            
            if 'port_scan' in scan_results:
                f.write("🔍 СКАНИРОВАНИЕ ПОРТОВ\n")
                f.write("-" * 30 + "\n")
                open_ports = [port for port, is_open in scan_results['port_scan'].items() if is_open]
                f.write(f"Открытые порты: {', '.join(map(str, open_ports)) if open_ports else 'Нет'}\n\n")
            
            if 'services' in scan_results:
                f.write("🛠️ ОБНАРУЖЕННЫЕ СЕРВИСЫ\n")
                f.write("-" * 30 + "\n")
                for service in scan_results['services']:
                    f.write(f"Порт {service['port']}: {service['service']}\n")
                    f.write(f"  Версия: {service['version']}\n")
                    if service['banner']:
                        f.write(f"  Баннер: {service['banner'][:100]}...\n")
                    f.write("\n")
            
            if 'open_ports_summary' in scan_results:
                f.write("📊 СВОДКА ПО ПОРТАМ\n")
                f.write("-" * 30 + "\n")
                for port, hosts in scan_results['open_ports_summary'].items():
                    f.write(f"Порт {port}: {len(hosts)} хостов\n")
                    for host in hosts:
                        f.write(f"  • {host}\n")
                f.write("\n")
            
            f.write("⚠️ ВАЖНО: Данный отчет создан в образовательных целях!\n")
            f.write("Использование для незаконных действий запрещено.\n")
        
        print(f"\n{Colors.GREEN}📋 Отчет сохранен: {filepath}{Colors.END}")
        return filepath
    
    def run(self):
        """Запуск интерфейса сетевой разведки"""
        while True:
            print(f"\n{Colors.BOLD}{Colors.CYAN}🌐 СЕТЕВАЯ РАЗВЕДКА{Colors.END}")
            print(f"{Colors.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
            
            menu_options = [
                ("1", "🎯 Комплексное сканирование хоста", "comprehensive_scan"),
                ("2", "🌐 Разведка сети", "network_recon"),
                ("3", "🔍 Быстрое сканирование портов", "quick_port_scan"),
                ("4", "📡 Анализ WiFi сетей", "wifi_analysis"),
                ("5", "📊 Мониторинг сетевой активности", "traffic_monitor"),
                ("6", "🛠️ Определение сервисов", "service_detection"),
                ("0", "🔙 Назад в главное меню", "back")
            ]
            
            for option, description, _ in menu_options:
                print(f"{Colors.YELLOW}[{option}]{Colors.END} {description}")
            
            choice = input(f"\n{Colors.BOLD}Выберите опцию: {Colors.END}")
            
            if choice == '1':
                target = input("Введите IP адрес или домен для сканирования: ").strip()
                if target:
                    results = self.comprehensive_scan(target)
                    self.generate_report(results, "comprehensive")
                    input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
            
            elif choice == '2':
                network = input("Введите сеть (например, 192.168.1.0/24): ").strip()
                if network:
                    results = self.network_reconnaissance(network)
                    self.generate_report(results, "network_recon")
                    input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
            
            elif choice == '3':
                host = input("Введите IP адрес: ").strip()
                ports_input = input("Введите порты через запятую (или Enter для стандартных): ").strip()
                
                if ports_input:
                    try:
                        ports = [int(p.strip()) for p in ports_input.split(',')]
                    except:
                        print(f"{Colors.RED}❌ Неверный формат портов{Colors.END}")
                        continue
                else:
                    ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3389]
                
                if host:
                    results = self.scanner.port_scan(host, ports)
                    print(f"\n{Colors.GREEN}📊 Результаты сканирования:{Colors.END}")
                    for port, is_open in results.items():
                        status = "открыт" if is_open else "закрыт"
                        color = Colors.GREEN if is_open else Colors.RED
                        print(f"{color}  Порт {port}: {status}{Colors.END}")
                    
                    input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
            
            elif choice == '4':
                networks = self.wifi_analyzer.scan_wifi_networks()
                print(f"\n{Colors.GREEN}📡 Обнаруженные WiFi сети:{Colors.END}")
                for i, network in enumerate(networks, 1):
                    print(f"{Colors.CYAN}  {i}. {network['ssid']}{Colors.END}")
                    print(f"     Безопасность: {network['security']}")
                    print(f"     Сигнал: {network['signal']}")
                    print(f"     Канал: {network['channel']}")
                    print()
                
                input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
            
            elif choice == '5':
                duration = input("Длительность мониторинга в секундах (по умолчанию 60): ").strip()
                try:
                    duration = int(duration) if duration else 60
                except:
                    duration = 60
                
                connections = self.monitor.monitor_traffic(duration)
                print(f"\n{Colors.GREEN}📊 Активные соединения:{Colors.END}")
                for conn in connections[:20]:  # Показываем первые 20
                    print(f"{Colors.CYAN}  {conn['protocol']} {conn['local_address']} -> {conn['foreign_address']} [{conn['state']}]{Colors.END}")
                
                input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
            
            elif choice == '6':
                host = input("Введите IP адрес: ").strip()
                port = input("Введите порт: ").strip()
                
                try:
                    port = int(port)
                    service_info = self.service_detector.detect_service(host, port)
                    
                    print(f"\n{Colors.GREEN}🛠️ Информация о сервисе:{Colors.END}")
                    print(f"  Порт: {service_info['port']}")
                    print(f"  Сервис: {service_info['service']}")
                    print(f"  Версия: {service_info['version']}")
                    print(f"  ОС: {service_info['os_info']}")
                    if service_info['banner']:
                        print(f"  Баннер: {service_info['banner'][:200]}...")
                    
                except ValueError:
                    print(f"{Colors.RED}❌ Неверный номер порта{Colors.END}")
                
                input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
            
            elif choice == '0':
                break
            
            else:
                print(f"{Colors.RED}❌ Неверный выбор!{Colors.END}")
                time.sleep(1)

if __name__ == "__main__":
    network_intel = NetworkIntelligence()
    network_intel.run()
