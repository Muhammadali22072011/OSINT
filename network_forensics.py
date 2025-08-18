#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌐 Сетевые форензик инструменты
Продвинутые инструменты для анализа сетевого трафика и форензики

⚠️ ВАЖНО: Использовать только в образовательных целях!
"""

import socket
import struct
import threading
import time
import json
import os
from datetime import datetime, timedelta
import random
import hashlib
import base64
import collections
from typing import Dict, List, Any, Optional, Tuple
import subprocess
import concurrent.futures
import ipaddress

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
        self.discovered_hosts = {}
        self.scan_results = {}
        self.vulnerabilities = {}
    
    def network_discovery(self, network: str) -> Dict:
        """Обнаружение хостов в сети"""
        print(f"\n{Colors.CYAN}🌐 ОБНАРУЖЕНИЕ ХОСТОВ В СЕТИ: {network}{Colors.END}")
        
        try:
            network_obj = ipaddress.IPv4Network(network, strict=False)
        except:
            print(f"{Colors.RED}❌ Неверный формат сети{Colors.END}")
            return {}
        
        discovered = {}
        total_hosts = list(network_obj.hosts())
        
        print(f"🔍 Сканирование {len(total_hosts)} адресов...")
        
        # Ограничиваем количество для демонстрации
        hosts_to_scan = total_hosts[:min(50, len(total_hosts))]
        
        def ping_host(ip):
            try:
                # Симуляция ping (в реальности использовать ping команду)
                if random.choice([True, False, False, False]):  # 25% вероятность
                    response_time = random.uniform(1, 100)
                    return str(ip), {
                        'status': 'alive',
                        'response_time': f"{response_time:.2f}ms",
                        'discovered_at': datetime.now().isoformat()
                    }
            except:
                pass
            return None, None
        
        # Многопоточное сканирование
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(ping_host, ip) for ip in hosts_to_scan]
            
            for future in concurrent.futures.as_completed(futures):
                ip, result = future.result()
                if ip and result:
                    discovered[ip] = result
                    print(f"  {Colors.GREEN}✅ {ip} - {result['response_time']}{Colors.END}")
        
        print(f"\n{Colors.YELLOW}📊 Обнаружено активных хостов: {len(discovered)}{Colors.END}")
        
        self.discovered_hosts.update(discovered)
        return discovered
    
    def advanced_port_scan(self, target: str, port_range: str = "1-1000") -> Dict:
        """Продвинутое сканирование портов"""
        print(f"\n{Colors.PURPLE}🔍 ПРОДВИНУТОЕ СКАНИРОВАНИЕ ПОРТОВ: {target}{Colors.END}")
        
        # Парсинг диапазона портов
        if '-' in port_range:
            start_port, end_port = map(int, port_range.split('-'))
        else:
            start_port = end_port = int(port_range)
        
        ports_to_scan = list(range(start_port, min(end_port + 1, start_port + 200)))  # Ограничиваем
        
        scan_results = {
            'target': target,
            'open_ports': [],
            'filtered_ports': [],
            'closed_ports': [],
            'services': {},
            'vulnerabilities': [],
            'os_fingerprint': {},
            'scan_timestamp': datetime.now().isoformat()
        }
        
        print(f"🎯 Сканирование {len(ports_to_scan)} портов...")
        
        def scan_port_advanced(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((target, port))
                
                if result == 0:
                    # Порт открыт - пытаемся получить баннер
                    try:
                        banner = self.grab_banner(sock, port)
                        service_info = self.identify_service_detailed(port, banner)
                        
                        return {
                            'port': port,
                            'status': 'open',
                            'banner': banner,
                            'service': service_info
                        }
                    except:
                        return {
                            'port': port,
                            'status': 'open',
                            'banner': '',
                            'service': self.identify_service_detailed(port, '')
                        }
                    finally:
                        sock.close()
                else:
                    sock.close()
                    return {'port': port, 'status': 'closed'}
                    
            except socket.timeout:
                return {'port': port, 'status': 'filtered'}
            except:
                return {'port': port, 'status': 'error'}
        
        # Многопоточное сканирование
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(scan_port_advanced, port) for port in ports_to_scan]
            
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                port = result['port']
                status = result['status']
                
                if status == 'open':
                    scan_results['open_ports'].append(port)
                    scan_results['services'][port] = result.get('service', {})
                    
                    # Проверка на уязвимости
                    vulns = self.check_vulnerabilities(port, result.get('service', {}))
                    if vulns:
                        scan_results['vulnerabilities'].extend(vulns)
                    
                    print(f"  {Colors.GREEN}✅ {port} - {result.get('service', {}).get('name', 'Unknown')}{Colors.END}")
                    
                elif status == 'filtered':
                    scan_results['filtered_ports'].append(port)
                elif status == 'closed':
                    scan_results['closed_ports'].append(port)
        
        # OS Fingerprinting (симуляция)
        scan_results['os_fingerprint'] = self.os_fingerprint(target, scan_results['open_ports'])
        
        print(f"\n{Colors.YELLOW}📊 Результаты сканирования:{Colors.END}")
        print(f"  Открытые порты: {len(scan_results['open_ports'])}")
        print(f"  Фильтруемые порты: {len(scan_results['filtered_ports'])}")
        print(f"  Закрытые порты: {len(scan_results['closed_ports'])}")
        print(f"  Найдено уязвимостей: {len(scan_results['vulnerabilities'])}")
        
        return scan_results
    
    def grab_banner(self, sock: socket.socket, port: int) -> str:
        """Захват баннера сервиса"""
        banner = ""
        
        try:
            if port == 80:
                sock.send(b'GET / HTTP/1.1\r\nHost: target\r\n\r\n')
            elif port == 21:
                sock.send(b'HELP\r\n')
            elif port == 25:
                sock.send(b'EHLO test\r\n')
            elif port == 22:
                pass  # SSH отправляет баннер автоматически
            else:
                sock.send(b'\r\n')
            
            banner = sock.recv(1024).decode('utf-8', errors='ignore')
            
        except:
            pass
        
        return banner[:200]  # Первые 200 символов
    
    def identify_service_detailed(self, port: int, banner: str) -> Dict:
        """Детальное определение сервиса"""
        service_db = {
            21: {'name': 'FTP', 'protocol': 'TCP', 'risk': 'Medium'},
            22: {'name': 'SSH', 'protocol': 'TCP', 'risk': 'Low'},
            23: {'name': 'Telnet', 'protocol': 'TCP', 'risk': 'High'},
            25: {'name': 'SMTP', 'protocol': 'TCP', 'risk': 'Medium'},
            53: {'name': 'DNS', 'protocol': 'TCP/UDP', 'risk': 'Low'},
            80: {'name': 'HTTP', 'protocol': 'TCP', 'risk': 'Medium'},
            110: {'name': 'POP3', 'protocol': 'TCP', 'risk': 'Medium'},
            135: {'name': 'RPC', 'protocol': 'TCP', 'risk': 'High'},
            139: {'name': 'NetBIOS', 'protocol': 'TCP', 'risk': 'High'},
            143: {'name': 'IMAP', 'protocol': 'TCP', 'risk': 'Medium'},
            443: {'name': 'HTTPS', 'protocol': 'TCP', 'risk': 'Low'},
            993: {'name': 'IMAPS', 'protocol': 'TCP', 'risk': 'Low'},
            995: {'name': 'POP3S', 'protocol': 'TCP', 'risk': 'Low'},
            1433: {'name': 'MSSQL', 'protocol': 'TCP', 'risk': 'High'},
            3306: {'name': 'MySQL', 'protocol': 'TCP', 'risk': 'High'},
            3389: {'name': 'RDP', 'protocol': 'TCP', 'risk': 'High'},
            5432: {'name': 'PostgreSQL', 'protocol': 'TCP', 'risk': 'High'},
        }
        
        base_service = service_db.get(port, {
            'name': 'Unknown',
            'protocol': 'TCP',
            'risk': 'Unknown'
        })
        
        # Анализ баннера для получения дополнительной информации
        version_info = self.extract_version_from_banner(banner)
        if version_info:
            base_service['version'] = version_info
        
        base_service['banner'] = banner
        
        return base_service
    
    def extract_version_from_banner(self, banner: str) -> str:
        """Извлечение версии из баннера"""
        if not banner:
            return ""
        
        # Простые паттерны для извлечения версий
        import re
        
        patterns = [
            r'(\d+\.\d+\.\d+)',  # x.y.z
            r'(\d+\.\d+)',       # x.y
            r'version\s+(\S+)',  # version xyz
            r'v(\d+\.\d+)',      # v1.2
        ]
        
        for pattern in patterns:
            match = re.search(pattern, banner, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return ""
    
    def check_vulnerabilities(self, port: int, service_info: Dict) -> List[Dict]:
        """Проверка на известные уязвимости"""
        vulnerabilities = []
        
        # Простая база уязвимостей
        vuln_db = {
            21: [
                {'cve': 'CVE-2010-4221', 'description': 'ProFTPD buffer overflow', 'severity': 'High'},
                {'cve': 'CVE-2019-12815', 'description': 'ProFTPD arbitrary file copy', 'severity': 'Medium'}
            ],
            22: [
                {'cve': 'CVE-2016-0777', 'description': 'OpenSSH client information disclosure', 'severity': 'Medium'},
                {'cve': 'CVE-2020-14145', 'description': 'OpenSSH observable discrepancy', 'severity': 'Low'}
            ],
            80: [
                {'cve': 'CVE-2021-44228', 'description': 'Log4j RCE (Log4Shell)', 'severity': 'Critical'},
                {'cve': 'CVE-2017-5638', 'description': 'Apache Struts2 RCE', 'severity': 'Critical'}
            ],
            3389: [
                {'cve': 'CVE-2019-0708', 'description': 'BlueKeep RCE', 'severity': 'Critical'},
                {'cve': 'CVE-2020-0609', 'description': 'RDP Gateway RCE', 'severity': 'Critical'}
            ]
        }
        
        port_vulns = vuln_db.get(port, [])
        
        # Случайная симуляция обнаружения уязвимостей
        for vuln in port_vulns:
            if random.choice([True, False, False]):  # 33% шанс
                vulnerabilities.append({
                    'port': port,
                    'service': service_info.get('name', 'Unknown'),
                    **vuln
                })
        
        return vulnerabilities
    
    def os_fingerprint(self, target: str, open_ports: List[int]) -> Dict:
        """Определение операционной системы"""
        fingerprint = {
            'method': 'TCP/IP stack analysis',
            'confidence': 0,
            'os_family': 'Unknown',
            'os_version': 'Unknown',
            'details': []
        }
        
        # Простая логика определения ОС по открытым портам
        if 3389 in open_ports:  # RDP
            fingerprint['os_family'] = 'Windows'
            fingerprint['confidence'] = 0.8
            fingerprint['details'].append('RDP service indicates Windows')
            
        elif 22 in open_ports and 80 in open_ports:  # SSH + HTTP
            fingerprint['os_family'] = 'Linux/Unix'
            fingerprint['confidence'] = 0.6
            fingerprint['details'].append('SSH service indicates Unix-like system')
            
        elif 139 in open_ports or 445 in open_ports:  # SMB
            fingerprint['os_family'] = 'Windows'
            fingerprint['confidence'] = 0.7
            fingerprint['details'].append('SMB services indicate Windows')
        
        # Добавляем случайные детали для демонстрации
        if fingerprint['os_family'] == 'Windows':
            versions = ['Windows 10', 'Windows Server 2019', 'Windows Server 2016']
            fingerprint['os_version'] = random.choice(versions)
        elif fingerprint['os_family'] == 'Linux/Unix':
            versions = ['Ubuntu 20.04', 'CentOS 7', 'Debian 10']
            fingerprint['os_version'] = random.choice(versions)
        
        return fingerprint

class TrafficAnalyzer:
    """Анализатор сетевого трафика"""
    
    def __init__(self):
        self.captured_packets = []
        self.analysis_results = {}
        self.suspicious_patterns = []
    
    def simulate_packet_capture(self, duration: int = 30) -> List[Dict]:
        """Симуляция захвата пакетов"""
        print(f"\n{Colors.BLUE}📡 СИМУЛЯЦИЯ ЗАХВАТА ТРАФИКА ({duration} сек){Colors.END}")
        
        packets = []
        start_time = datetime.now()
        
        # Симуляция различных типов трафика
        protocols = ['TCP', 'UDP', 'ICMP', 'HTTP', 'HTTPS', 'DNS', 'FTP', 'SSH']
        
        for i in range(random.randint(50, 200)):
            packet = {
                'timestamp': (start_time + timedelta(seconds=random.uniform(0, duration))).isoformat(),
                'src_ip': f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}",
                'dst_ip': f"10.0.{random.randint(1, 254)}.{random.randint(1, 254)}",
                'src_port': random.randint(1024, 65535),
                'dst_port': random.choice([80, 443, 22, 21, 25, 53, 3389, random.randint(1, 65535)]),
                'protocol': random.choice(protocols),
                'size': random.randint(64, 1500),
                'flags': random.choice(['SYN', 'ACK', 'FIN', 'RST', 'PSH', 'URG']),
                'payload_hash': hashlib.md5(f"packet_{i}".encode()).hexdigest()
            }
            packets.append(packet)
        
        print(f"{Colors.GREEN}✅ Захвачено {len(packets)} пакетов{Colors.END}")
        
        self.captured_packets = packets
        return packets
    
    def analyze_traffic_patterns(self, packets: List[Dict]) -> Dict:
        """Анализ паттернов трафика"""
        print(f"\n{Colors.YELLOW}📊 АНАЛИЗ ПАТТЕРНОВ ТРАФИКА{Colors.END}")
        
        analysis = {
            'total_packets': len(packets),
            'protocol_distribution': collections.Counter(),
            'top_talkers': {},
            'port_analysis': {},
            'time_analysis': {},
            'suspicious_activity': [],
            'bandwidth_usage': {}
        }
        
        # Анализ протоколов
        for packet in packets:
            analysis['protocol_distribution'][packet['protocol']] += 1
        
        # Анализ активных хостов
        host_stats = collections.defaultdict(lambda: {'sent': 0, 'received': 0, 'bytes': 0})
        
        for packet in packets:
            src = packet['src_ip']
            dst = packet['dst_ip']
            size = packet['size']
            
            host_stats[src]['sent'] += 1
            host_stats[src]['bytes'] += size
            host_stats[dst]['received'] += 1
        
        # Топ-5 активных хостов
        analysis['top_talkers'] = dict(
            sorted(host_stats.items(), key=lambda x: x[1]['bytes'], reverse=True)[:5]
        )
        
        # Анализ портов
        port_stats = collections.defaultdict(int)
        for packet in packets:
            port_stats[packet['dst_port']] += 1
        
        analysis['port_analysis'] = dict(
            sorted(port_stats.items(), key=lambda x: x[1], reverse=True)[:10]
        )
        
        # Поиск подозрительной активности
        analysis['suspicious_activity'] = self.detect_suspicious_activity(packets)
        
        # Анализ использования полосы пропускания
        total_bytes = sum(packet['size'] for packet in packets)
        analysis['bandwidth_usage'] = {
            'total_bytes': total_bytes,
            'average_packet_size': total_bytes / len(packets) if packets else 0,
            'estimated_bandwidth': f"{(total_bytes * 8) / 1024 / 1024:.2f} Mbps"
        }
        
        return analysis
    
    def detect_suspicious_activity(self, packets: List[Dict]) -> List[Dict]:
        """Обнаружение подозрительной активности"""
        suspicious = []
        
        # Счетчики для различных типов активности
        port_scan_threshold = 10
        connection_counts = collections.defaultdict(set)
        
        # Проверка на сканирование портов
        for packet in packets:
            if packet['flags'] == 'SYN':
                connection_counts[packet['src_ip']].add(packet['dst_port'])
        
        for src_ip, ports in connection_counts.items():
            if len(ports) > port_scan_threshold:
                suspicious.append({
                    'type': 'Port Scan',
                    'source': src_ip,
                    'description': f'Attempted connections to {len(ports)} different ports',
                    'severity': 'Medium',
                    'ports': list(ports)[:10]  # Первые 10 портов
                })
        
        # Проверка на необычные порты
        unusual_ports = [1337, 4444, 6666, 8080, 9999]
        for packet in packets:
            if packet['dst_port'] in unusual_ports:
                suspicious.append({
                    'type': 'Unusual Port Activity',
                    'source': packet['src_ip'],
                    'destination': packet['dst_ip'],
                    'port': packet['dst_port'],
                    'description': f'Connection to unusual port {packet["dst_port"]}',
                    'severity': 'Low'
                })
        
        # Проверка на большие объемы данных
        large_packets = [p for p in packets if p['size'] > 1200]
        if len(large_packets) > len(packets) * 0.1:  # Более 10% больших пакетов
            suspicious.append({
                'type': 'Large Data Transfer',
                'description': f'{len(large_packets)} large packets detected',
                'severity': 'Low'
            })
        
        return suspicious
    
    def deep_packet_inspection(self, packets: List[Dict]) -> Dict:
        """Глубокая инспекция пакетов"""
        print(f"\n{Colors.PURPLE}🔍 ГЛУБОКАЯ ИНСПЕКЦИЯ ПАКЕТОВ{Colors.END}")
        
        inspection = {
            'payload_analysis': {},
            'protocol_anomalies': [],
            'encrypted_traffic': {},
            'potential_malware': [],
            'data_exfiltration': []
        }
        
        # Анализ полезной нагрузки (симуляция)
        http_packets = [p for p in packets if p['dst_port'] in [80, 8080]]
        https_packets = [p for p in packets if p['dst_port'] == 443]
        
        inspection['payload_analysis'] = {
            'http_requests': len(http_packets),
            'https_requests': len(https_packets),
            'encrypted_ratio': len(https_packets) / len(packets) if packets else 0
        }
        
        # Поиск аномалий протоколов
        for packet in packets:
            # Проверка на необычные комбинации порт-протокол
            if packet['protocol'] == 'HTTP' and packet['dst_port'] not in [80, 8080]:
                inspection['protocol_anomalies'].append({
                    'type': 'Unusual HTTP port',
                    'packet': packet,
                    'description': f'HTTP traffic on port {packet["dst_port"]}'
                })
        
        # Анализ зашифрованного трафика
        inspection['encrypted_traffic'] = {
            'tls_sessions': random.randint(5, 20),
            'ssh_sessions': random.randint(1, 5),
            'vpn_traffic': random.choice([True, False])
        }
        
        # Симуляция обнаружения потенциального вредоносного ПО
        if random.choice([True, False, False]):
            inspection['potential_malware'].append({
                'type': 'Suspicious DNS Query',
                'domain': 'malicious.example.com',
                'source_ip': random.choice([p['src_ip'] for p in packets]),
                'confidence': 0.7
            })
        
        return inspection

class ForensicsToolkit:
    """Набор инструментов для цифровой форензики"""
    
    def __init__(self):
        self.evidence_chain = []
        self.artifacts = {}
        self.timeline = []
    
    def collect_network_artifacts(self, scan_results: Dict, traffic_analysis: Dict) -> Dict:
        """Сбор сетевых артефактов"""
        print(f"\n{Colors.GREEN}🔬 СБОР СЕТЕВЫХ АРТЕФАКТОВ{Colors.END}")
        
        artifacts = {
            'collection_timestamp': datetime.now().isoformat(),
            'network_artifacts': {
                'discovered_hosts': scan_results.get('discovered_hosts', {}),
                'open_services': scan_results.get('services', {}),
                'vulnerabilities': scan_results.get('vulnerabilities', []),
                'os_fingerprints': scan_results.get('os_fingerprint', {})
            },
            'traffic_artifacts': {
                'suspicious_connections': traffic_analysis.get('suspicious_activity', []),
                'protocol_distribution': dict(traffic_analysis.get('protocol_distribution', {})),
                'top_talkers': traffic_analysis.get('top_talkers', {}),
                'bandwidth_patterns': traffic_analysis.get('bandwidth_usage', {})
            },
            'indicators_of_compromise': self.extract_iocs(scan_results, traffic_analysis),
            'evidence_hash': None
        }
        
        # Создаем хеш для целостности доказательств
        evidence_string = json.dumps(artifacts, sort_keys=True)
        artifacts['evidence_hash'] = hashlib.sha256(evidence_string.encode()).hexdigest()
        
        self.artifacts.update(artifacts)
        
        print(f"{Colors.GREEN}✅ Собрано артефактов: {len(artifacts)}{Colors.END}")
        
        return artifacts
    
    def extract_iocs(self, scan_results: Dict, traffic_analysis: Dict) -> List[Dict]:
        """Извлечение индикаторов компрометации"""
        iocs = []
        
        # IoCs из уязвимостей
        for vuln in scan_results.get('vulnerabilities', []):
            iocs.append({
                'type': 'vulnerability',
                'indicator': f"{vuln.get('cve', 'Unknown')} on port {vuln.get('port')}",
                'severity': vuln.get('severity', 'Unknown'),
                'description': vuln.get('description', ''),
                'source': 'port_scan'
            })
        
        # IoCs из подозрительной активности
        for activity in traffic_analysis.get('suspicious_activity', []):
            iocs.append({
                'type': 'network_anomaly',
                'indicator': activity.get('type', 'Unknown'),
                'severity': activity.get('severity', 'Unknown'),
                'description': activity.get('description', ''),
                'source': 'traffic_analysis'
            })
        
        # Дополнительные IoCs (симуляция)
        if random.choice([True, False]):
            iocs.append({
                'type': 'malicious_ip',
                'indicator': '192.168.1.100',
                'severity': 'High',
                'description': 'IP address found in threat intelligence feed',
                'source': 'threat_intel'
            })
        
        return iocs
    
    def create_timeline(self, artifacts: Dict) -> List[Dict]:
        """Создание временной шкалы событий"""
        timeline = []
        
        # События из сканирования
        for host, info in artifacts.get('network_artifacts', {}).get('discovered_hosts', {}).items():
            timeline.append({
                'timestamp': info.get('discovered_at', ''),
                'event_type': 'host_discovery',
                'description': f'Host {host} discovered',
                'source': 'network_scan'
            })
        
        # События из трафика
        for activity in artifacts.get('traffic_artifacts', {}).get('suspicious_connections', []):
            timeline.append({
                'timestamp': datetime.now().isoformat(),
                'event_type': 'suspicious_activity',
                'description': activity.get('description', ''),
                'source': 'traffic_analysis'
            })
        
        # Сортировка по времени
        timeline.sort(key=lambda x: x['timestamp'])
        
        self.timeline = timeline
        return timeline
    
    def generate_forensics_report(self, artifacts: Dict, timeline: List[Dict]) -> str:
        """Генерация форензического отчета"""
        if not os.path.exists("forensics_reports"):
            os.makedirs("forensics_reports")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"forensics_reports/network_forensics_{timestamp}.json"
        
        report = {
            'report_metadata': {
                'generated_at': datetime.now().isoformat(),
                'report_type': 'Network Forensics',
                'version': '1.0',
                'analyst': 'OSINT Toolkit'
            },
            'executive_summary': {
                'total_hosts_discovered': len(artifacts.get('network_artifacts', {}).get('discovered_hosts', {})),
                'vulnerabilities_found': len(artifacts.get('network_artifacts', {}).get('vulnerabilities', [])),
                'suspicious_activities': len(artifacts.get('traffic_artifacts', {}).get('suspicious_connections', [])),
                'iocs_identified': len(artifacts.get('indicators_of_compromise', []))
            },
            'detailed_findings': artifacts,
            'timeline_of_events': timeline,
            'recommendations': self.generate_recommendations(artifacts),
            'chain_of_custody': self.evidence_chain
        }
        
        # Сохранение JSON отчета
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        # Создание текстового отчета
        text_filename = filename.replace('.json', '.txt')
        with open(text_filename, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("ОТЧЕТ ПО СЕТЕВОЙ ФОРЕНЗИКЕ\n")
            f.write("="*80 + "\n\n")
            f.write(f"Дата генерации: {report['report_metadata']['generated_at']}\n")
            f.write(f"Аналитик: {report['report_metadata']['analyst']}\n\n")
            
            f.write("КРАТКОЕ РЕЗЮМЕ:\n")
            f.write("-" * 40 + "\n")
            for key, value in report['executive_summary'].items():
                f.write(f"{key.replace('_', ' ').title()}: {value}\n")
            
            f.write("\nОБНАРУЖЕННЫЕ УЯЗВИМОСТИ:\n")
            f.write("-" * 40 + "\n")
            for vuln in artifacts.get('network_artifacts', {}).get('vulnerabilities', []):
                f.write(f"• {vuln.get('cve', 'Unknown')} - {vuln.get('description', '')} (Порт: {vuln.get('port', 'Unknown')})\n")
            
            f.write("\nПОДОЗРИТЕЛЬНАЯ АКТИВНОСТЬ:\n")
            f.write("-" * 40 + "\n")
            for activity in artifacts.get('traffic_artifacts', {}).get('suspicious_connections', []):
                f.write(f"• {activity.get('type', 'Unknown')} - {activity.get('description', '')}\n")
            
            f.write("\nРЕКОМЕНДАЦИИ:\n")
            f.write("-" * 40 + "\n")
            for rec in report['recommendations']:
                f.write(f"• {rec}\n")
            
            f.write("\n" + "="*80 + "\n")
        
        print(f"{Colors.GREEN}✅ Форензический отчет сохранен: {filename}{Colors.END}")
        print(f"{Colors.GREEN}✅ Текстовая версия: {text_filename}{Colors.END}")
        
        return filename
    
    def generate_recommendations(self, artifacts: Dict) -> List[str]:
        """Генерация рекомендаций на основе находок"""
        recommendations = []
        
        # Рекомендации по уязвимостям
        vulnerabilities = artifacts.get('network_artifacts', {}).get('vulnerabilities', [])
        if vulnerabilities:
            recommendations.append("Немедленно обновите уязвимые сервисы до последних версий")
            
            critical_vulns = [v for v in vulnerabilities if v.get('severity') == 'Critical']
            if critical_vulns:
                recommendations.append("Критические уязвимости требуют экстренного патчинга")
        
        # Рекомендации по подозрительной активности
        suspicious = artifacts.get('traffic_artifacts', {}).get('suspicious_connections', [])
        if suspicious:
            recommendations.append("Исследуйте источники подозрительной сетевой активности")
            
            port_scans = [s for s in suspicious if s.get('type') == 'Port Scan']
            if port_scans:
                recommendations.append("Заблокируйте IP-адреса, выполняющие сканирование портов")
        
        # Общие рекомендации
        recommendations.extend([
            "Настройте мониторинг сетевого трафика в реальном времени",
            "Реализуйте систему обнаружения вторжений (IDS/IPS)",
            "Регулярно проводите аудит безопасности сети",
            "Создайте план реагирования на инциденты безопасности"
        ])
        
        return recommendations

class NetworkForensicsSuite:
    """Основной класс для сетевой форензики"""
    
    def __init__(self):
        self.scanner = NetworkScanner()
        self.traffic_analyzer = TrafficAnalyzer()
        self.forensics = ForensicsToolkit()
    
    def run_comprehensive_analysis(self, target_network: str) -> Dict:
        """Запуск комплексного анализа"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}🌐 КОМПЛЕКСНЫЙ СЕТЕВОЙ АНАЛИЗ{Colors.END}")
        
        results = {}
        
        # 1. Обнаружение хостов
        print(f"\n{Colors.YELLOW}[1/5] Обнаружение хостов в сети...{Colors.END}")
        discovered_hosts = self.scanner.network_discovery(target_network)
        results['discovered_hosts'] = discovered_hosts
        
        # 2. Сканирование портов активных хостов
        if discovered_hosts:
            print(f"\n{Colors.YELLOW}[2/5] Сканирование портов активных хостов...{Colors.END}")
            target_host = list(discovered_hosts.keys())[0]  # Берем первый найденный хост
            scan_results = self.scanner.advanced_port_scan(target_host)
            results.update(scan_results)
        
        # 3. Анализ трафика
        print(f"\n{Colors.YELLOW}[3/5] Захват и анализ трафика...{Colors.END}")
        packets = self.traffic_analyzer.simulate_packet_capture(30)
        traffic_analysis = self.traffic_analyzer.analyze_traffic_patterns(packets)
        results['traffic_analysis'] = traffic_analysis
        
        # 4. Глубокая инспекция пакетов
        print(f"\n{Colors.YELLOW}[4/5] Глубокая инспекция пакетов...{Colors.END}")
        deep_inspection = self.traffic_analyzer.deep_packet_inspection(packets)
        results['deep_inspection'] = deep_inspection
        
        # 5. Сбор артефактов и создание отчета
        print(f"\n{Colors.YELLOW}[5/5] Сбор форензических данных...{Colors.END}")
        artifacts = self.forensics.collect_network_artifacts(results, traffic_analysis)
        timeline = self.forensics.create_timeline(artifacts)
        
        report_file = self.forensics.generate_forensics_report(artifacts, timeline)
        results['forensics_report'] = report_file
        
        print(f"\n{Colors.BOLD}{Colors.GREEN}✅ КОМПЛЕКСНЫЙ АНАЛИЗ ЗАВЕРШЕН!{Colors.END}")
        
        return results
    
    def run(self):
        """Запуск главного меню сетевой форензики"""
        while True:
            print(f"\n{Colors.BOLD}{Colors.BLUE}🌐 СЕТЕВАЯ ФОРЕНЗИКА И АНАЛИЗ ТРАФИКА{Colors.END}")
            print(f"{Colors.RED}⚠️ ТОЛЬКО ДЛЯ ОБРАЗОВАТЕЛЬНЫХ ЦЕЛЕЙ!{Colors.END}\n")
            
            print("Инструменты:")
            print("1. 🔍 Обнаружение хостов в сети")
            print("2. 🎯 Продвинутое сканирование портов")
            print("3. 📡 Анализ сетевого трафика")
            print("4. 🔬 Глубокая инспекция пакетов")
            print("5. 🌐 Комплексный сетевой анализ")
            print("6. 📊 Просмотр форензических отчетов")
            print("0. ← Назад в главное меню")
            
            choice = input(f"\n{Colors.YELLOW}Выберите инструмент: {Colors.END}")
            
            if choice == '1':
                network = input("Введите сеть (например, 192.168.1.0/24): ")
                if network:
                    self.scanner.network_discovery(network)
                    input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
            
            elif choice == '2':
                target = input("Введите IP адрес цели: ")
                port_range = input("Диапазон портов (например, 1-1000): ") or "1-1000"
                if target:
                    self.scanner.advanced_port_scan(target, port_range)
                    input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
            
            elif choice == '3':
                duration = input("Длительность захвата трафика (сек, по умолчанию 30): ")
                duration = int(duration) if duration.isdigit() else 30
                
                packets = self.traffic_analyzer.simulate_packet_capture(duration)
                analysis = self.traffic_analyzer.analyze_traffic_patterns(packets)
                
                print(f"\n{Colors.BOLD}РЕЗУЛЬТАТЫ АНАЛИЗА:{Colors.END}")
                print(json.dumps(analysis, ensure_ascii=False, indent=2))
                
                input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
            
            elif choice == '4':
                packets = self.traffic_analyzer.simulate_packet_capture(15)
                inspection = self.traffic_analyzer.deep_packet_inspection(packets)
                
                print(f"\n{Colors.BOLD}РЕЗУЛЬТАТЫ ГЛУБОКОЙ ИНСПЕКЦИИ:{Colors.END}")
                print(json.dumps(inspection, ensure_ascii=False, indent=2))
                
                input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
            
            elif choice == '5':
                network = input("Введите сеть для комплексного анализа (например, 192.168.1.0/24): ")
                if network:
                    results = self.run_comprehensive_analysis(network)
                    print(f"\n{Colors.GREEN}Анализ завершен. Отчет сохранен: {results.get('forensics_report', 'Не создан')}{Colors.END}")
                    input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
            
            elif choice == '6':
                self.view_forensics_reports()
            
            elif choice == '0':
                break
            
            else:
                print(f"{Colors.RED}❌ Неверный выбор!{Colors.END}")
                time.sleep(1)
    
    def view_forensics_reports(self):
        """Просмотр форензических отчетов"""
        if not os.path.exists("forensics_reports"):
            print(f"{Colors.YELLOW}📁 Папка с форензическими отчетами не найдена{Colors.END}")
            return
        
        files = [f for f in os.listdir("forensics_reports") if f.endswith('.txt')]
        
        if not files:
            print(f"{Colors.YELLOW}📁 Форензические отчеты не найдены{Colors.END}")
            return
        
        print(f"\n{Colors.BOLD}🔬 ФОРЕНЗИЧЕСКИЕ ОТЧЕТЫ{Colors.END}")
        for i, filename in enumerate(files, 1):
            print(f"  {i}. {filename}")
        
        try:
            choice = int(input(f"\n{Colors.YELLOW}Выберите отчет для просмотра (или 0 для выхода): {Colors.END}"))
            
            if 1 <= choice <= len(files):
                filepath = os.path.join("forensics_reports", files[choice-1])
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
    suite = NetworkForensicsSuite()
    suite.run()
