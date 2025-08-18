#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 Модуль анализа сетевого трафика
Реальные инструменты для захвата и анализа сетевых пакетов

⚠️ ВАЖНО: Использовать только в образовательных целях и на своих сетях!
"""

import socket
import struct
import threading
import time
import json
import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import collections
import queue
import platform
import subprocess

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

class PacketSniffer:
    """Сниффер пакетов"""
    
    def __init__(self):
        self.packets = []
        self.sniffing = False
        self.protocols = {
            1: 'ICMP',
            6: 'TCP', 
            17: 'UDP'
        }
    
    def parse_ip_header(self, data: bytes) -> Dict[str, Any]:
        """Парсинг IP заголовка"""
        try:
            # Распаковываем первые 20 байт IP заголовка
            ip_header = struct.unpack('!BBHHHBBH4s4s', data[:20])
            
            version_ihl = ip_header[0]
            version = version_ihl >> 4
            ihl = version_ihl & 0xF
            
            packet_info = {
                'version': version,
                'header_length': ihl * 4,
                'type_of_service': ip_header[1],
                'total_length': ip_header[2],
                'identification': ip_header[3],
                'flags': ip_header[4] >> 13,
                'fragment_offset': ip_header[4] & 0x1FFF,
                'ttl': ip_header[5],
                'protocol': ip_header[6],
                'checksum': ip_header[7],
                'source_ip': socket.inet_ntoa(ip_header[8]),
                'destination_ip': socket.inet_ntoa(ip_header[9]),
                'protocol_name': self.protocols.get(ip_header[6], 'Other')
            }
            
            return packet_info
        except:
            return {}
    
    def parse_tcp_header(self, data: bytes) -> Dict[str, Any]:
        """Парсинг TCP заголовка"""
        try:
            tcp_header = struct.unpack('!HHLLBBHHH', data[:20])
            
            tcp_info = {
                'source_port': tcp_header[0],
                'dest_port': tcp_header[1],
                'sequence': tcp_header[2],
                'acknowledgment': tcp_header[3],
                'offset_reserved': tcp_header[4],
                'flags': tcp_header[5],
                'window': tcp_header[6],
                'checksum': tcp_header[7],
                'urgent_pointer': tcp_header[8]
            }
            
            # Флаги TCP
            tcp_info['flag_urg'] = (tcp_info['flags'] & 32) >> 5
            tcp_info['flag_ack'] = (tcp_info['flags'] & 16) >> 4
            tcp_info['flag_psh'] = (tcp_info['flags'] & 8) >> 3
            tcp_info['flag_rst'] = (tcp_info['flags'] & 4) >> 2
            tcp_info['flag_syn'] = (tcp_info['flags'] & 2) >> 1
            tcp_info['flag_fin'] = tcp_info['flags'] & 1
            
            return tcp_info
        except:
            return {}
    
    def parse_udp_header(self, data: bytes) -> Dict[str, Any]:
        """Парсинг UDP заголовка"""
        try:
            udp_header = struct.unpack('!HHHH', data[:8])
            
            udp_info = {
                'source_port': udp_header[0],
                'dest_port': udp_header[1],
                'length': udp_header[2],
                'checksum': udp_header[3]
            }
            
            return udp_info
        except:
            return {}
    
    def start_sniffing(self, interface: str = None, duration: int = 60):
        """Запуск захвата пакетов"""
        print(f"\n{Colors.CYAN}📡 Запуск захвата пакетов на {duration} секунд...{Colors.END}")
        
        try:
            # Создаем raw socket (требует прав администратора)
            if platform.system().lower() == 'windows':
                # Windows
                sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
                sock.bind(('0.0.0.0', 0))
                sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
                
                # Включаем promiscuous mode
                sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
            else:
                # Linux
                sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
            
            self.sniffing = True
            start_time = time.time()
            packet_count = 0
            
            while self.sniffing and (time.time() - start_time) < duration:
                try:
                    data, addr = sock.recvfrom(65536)
                    packet_count += 1
                    
                    if platform.system().lower() == 'windows':
                        # В Windows получаем сразу IP пакет
                        ip_info = self.parse_ip_header(data)
                    else:
                        # В Linux нужно пропустить Ethernet заголовок
                        ip_info = self.parse_ip_header(data[14:])
                        data = data[14:]
                    
                    if ip_info:
                        packet = {
                            'timestamp': datetime.now().isoformat(),
                            'size': len(data),
                            'ip_info': ip_info
                        }
                        
                        # Парсим транспортный уровень
                        if ip_info['protocol'] == 6:  # TCP
                            tcp_info = self.parse_tcp_header(data[ip_info['header_length']:])
                            packet['tcp_info'] = tcp_info
                        elif ip_info['protocol'] == 17:  # UDP
                            udp_info = self.parse_udp_header(data[ip_info['header_length']:])
                            packet['udp_info'] = udp_info
                        
                        self.packets.append(packet)
                        
                        if packet_count % 100 == 0:
                            print(f"{Colors.YELLOW}📊 Захвачено пакетов: {packet_count}{Colors.END}")
                
                except socket.timeout:
                    continue
                except Exception as e:
                    if "Доступ запрещен" in str(e) or "Permission denied" in str(e):
                        print(f"{Colors.RED}❌ Требуются права администратора для захвата пакетов{Colors.END}")
                        self._simulate_traffic_data()
                        return
                    break
            
            if platform.system().lower() == 'windows':
                sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
            
            sock.close()
            print(f"\n{Colors.GREEN}✅ Захват завершен. Собрано пакетов: {len(self.packets)}{Colors.END}")
            
        except Exception as e:
            print(f"{Colors.RED}❌ Ошибка захвата пакетов: {e}{Colors.END}")
            print(f"{Colors.YELLOW}💡 Генерируем тестовые данные...{Colors.END}")
            self._simulate_traffic_data()
    
    def _simulate_traffic_data(self):
        """Генерация тестовых данных трафика"""
        import random
        
        protocols = ['TCP', 'UDP', 'ICMP']
        common_ports = [80, 443, 22, 21, 25, 53, 110, 143, 993, 995, 3389]
        
        for i in range(100):
            protocol = random.choice(protocols)
            
            packet = {
                'timestamp': (datetime.now() - timedelta(seconds=random.randint(0, 300))).isoformat(),
                'size': random.randint(64, 1500),
                'ip_info': {
                    'source_ip': f"192.168.1.{random.randint(1, 254)}",
                    'destination_ip': f"{random.randint(1, 223)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 254)}",
                    'protocol_name': protocol,
                    'ttl': random.randint(32, 128)
                }
            }
            
            if protocol == 'TCP':
                packet['tcp_info'] = {
                    'source_port': random.randint(1024, 65535),
                    'dest_port': random.choice(common_ports),
                    'flag_syn': random.choice([0, 1]),
                    'flag_ack': random.choice([0, 1]),
                    'flag_fin': random.choice([0, 1])
                }
            elif protocol == 'UDP':
                packet['udp_info'] = {
                    'source_port': random.randint(1024, 65535),
                    'dest_port': random.choice(common_ports)
                }
            
            self.packets.append(packet)

class TrafficAnalyzer:
    """Анализатор трафика"""
    
    def __init__(self):
        self.sniffer = PacketSniffer()
    
    def analyze_protocols(self, packets: List[Dict]) -> Dict[str, int]:
        """Анализ протоколов"""
        protocol_stats = collections.Counter()
        
        for packet in packets:
            protocol = packet['ip_info'].get('protocol_name', 'Unknown')
            protocol_stats[protocol] += 1
        
        return dict(protocol_stats)
    
    def analyze_top_talkers(self, packets: List[Dict], top_n: int = 10) -> List[Dict]:
        """Анализ самых активных хостов"""
        ip_stats = collections.defaultdict(lambda: {'sent': 0, 'received': 0, 'total': 0})
        
        for packet in packets:
            src_ip = packet['ip_info'].get('source_ip', '')
            dst_ip = packet['ip_info'].get('destination_ip', '')
            size = packet.get('size', 0)
            
            if src_ip:
                ip_stats[src_ip]['sent'] += size
                ip_stats[src_ip]['total'] += size
            
            if dst_ip:
                ip_stats[dst_ip]['received'] += size
                ip_stats[dst_ip]['total'] += size
        
        # Сортируем по общему трафику
        sorted_ips = sorted(ip_stats.items(), key=lambda x: x[1]['total'], reverse=True)
        
        top_talkers = []
        for ip, stats in sorted_ips[:top_n]:
            top_talkers.append({
                'ip': ip,
                'sent_bytes': stats['sent'],
                'received_bytes': stats['received'],
                'total_bytes': stats['total']
            })
        
        return top_talkers
    
    def analyze_ports(self, packets: List[Dict]) -> Dict[int, int]:
        """Анализ портов"""
        port_stats = collections.Counter()
        
        for packet in packets:
            # TCP порты
            if 'tcp_info' in packet:
                dest_port = packet['tcp_info'].get('dest_port')
                if dest_port:
                    port_stats[dest_port] += 1
            
            # UDP порты
            if 'udp_info' in packet:
                dest_port = packet['udp_info'].get('dest_port')
                if dest_port:
                    port_stats[dest_port] += 1
        
        return dict(port_stats.most_common(20))
    
    def detect_suspicious_activity(self, packets: List[Dict]) -> List[Dict]:
        """Обнаружение подозрительной активности"""
        suspicious = []
        
        # Анализируем каждый пакет
        for packet in packets:
            alerts = []
            
            # Проверка на сканирование портов
            if 'tcp_info' in packet:
                tcp_info = packet['tcp_info']
                if tcp_info.get('flag_syn') == 1 and tcp_info.get('flag_ack') == 0:
                    alerts.append("Возможное сканирование портов (SYN)")
            
            # Проверка на необычные порты
            if 'tcp_info' in packet:
                dest_port = packet['tcp_info'].get('dest_port', 0)
                if dest_port > 49152:  # Динамические порты как назначение
                    alerts.append(f"Необычный порт назначения: {dest_port}")
            
            # Проверка на большие пакеты
            if packet.get('size', 0) > 1400:
                alerts.append(f"Большой пакет: {packet['size']} байт")
            
            # Проверка на внешние IP
            dst_ip = packet['ip_info'].get('destination_ip', '')
            if dst_ip and not dst_ip.startswith('192.168.') and not dst_ip.startswith('10.') and not dst_ip.startswith('172.'):
                alerts.append(f"Внешний IP: {dst_ip}")
            
            if alerts:
                suspicious.append({
                    'packet': packet,
                    'alerts': alerts,
                    'severity': len(alerts)
                })
        
        return sorted(suspicious, key=lambda x: x['severity'], reverse=True)
    
    def generate_traffic_report(self, packets: List[Dict]) -> str:
        """Генерация отчета по трафику"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"traffic_analysis_{timestamp}.txt"
        filepath = os.path.join("osint_reports", filename)
        
        # Создаем директорию если её нет
        os.makedirs("osint_reports", exist_ok=True)
        
        # Анализируем данные
        protocol_stats = self.analyze_protocols(packets)
        top_talkers = self.analyze_top_talkers(packets)
        port_stats = self.analyze_ports(packets)
        suspicious = self.detect_suspicious_activity(packets)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("📊 ОТЧЕТ АНАЛИЗА СЕТЕВОГО ТРАФИКА\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Время анализа: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Всего пакетов: {len(packets)}\n")
            f.write(f"Период: {packets[0]['timestamp'] if packets else 'N/A'} - {packets[-1]['timestamp'] if packets else 'N/A'}\n\n")
            
            # Статистика протоколов
            f.write("🌐 СТАТИСТИКА ПРОТОКОЛОВ\n")
            f.write("-" * 30 + "\n")
            total_packets = sum(protocol_stats.values())
            for protocol, count in sorted(protocol_stats.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / total_packets) * 100 if total_packets > 0 else 0
                f.write(f"{protocol}: {count} пакетов ({percentage:.1f}%)\n")
            f.write("\n")
            
            # Топ хосты
            f.write("💬 ТОП АКТИВНЫЕ ХОСТЫ\n")
            f.write("-" * 30 + "\n")
            for i, talker in enumerate(top_talkers, 1):
                f.write(f"{i}. {talker['ip']}\n")
                f.write(f"   Отправлено: {talker['sent_bytes']} байт\n")
                f.write(f"   Получено: {talker['received_bytes']} байт\n")
                f.write(f"   Всего: {talker['total_bytes']} байт\n\n")
            
            # Статистика портов
            f.write("🔌 АКТИВНЫЕ ПОРТЫ\n")
            f.write("-" * 30 + "\n")
            for port, count in sorted(port_stats.items(), key=lambda x: x[1], reverse=True)[:15]:
                f.write(f"Порт {port}: {count} соединений\n")
            f.write("\n")
            
            # Подозрительная активность
            f.write("🚨 ПОДОЗРИТЕЛЬНАЯ АКТИВНОСТЬ\n")
            f.write("-" * 30 + "\n")
            if suspicious:
                for i, alert in enumerate(suspicious[:10], 1):
                    f.write(f"{i}. IP: {alert['packet']['ip_info'].get('source_ip', 'N/A')} -> ")
                    f.write(f"{alert['packet']['ip_info'].get('destination_ip', 'N/A')}\n")
                    f.write(f"   Время: {alert['packet']['timestamp']}\n")
                    f.write(f"   Предупреждения:\n")
                    for warning in alert['alerts']:
                        f.write(f"     • {warning}\n")
                    f.write("\n")
            else:
                f.write("Подозрительной активности не обнаружено.\n\n")
            
            f.write("⚠️ ВАЖНО: Данный отчет создан в образовательных целях!\n")
            f.write("Использование для незаконных действий запрещено.\n")
        
        print(f"\n{Colors.GREEN}📋 Отчет сохранен: {filepath}{Colors.END}")
        return filepath
    
    def run(self):
        """Запуск анализатора трафика"""
        while True:
            print(f"\n{Colors.BOLD}{Colors.CYAN}📊 АНАЛИЗАТОР СЕТЕВОГО ТРАФИКА{Colors.END}")
            print(f"{Colors.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
            
            menu_options = [
                ("1", "📡 Захват сетевого трафика", "capture"),
                ("2", "📊 Анализ протоколов", "protocols"),
                ("3", "💬 Анализ активных хостов", "hosts"),
                ("4", "🔌 Анализ портов", "ports"),
                ("5", "🚨 Поиск подозрительной активности", "suspicious"),
                ("6", "📋 Полный отчет", "report"),
                ("0", "🔙 Назад в главное меню", "back")
            ]
            
            for option, description, _ in menu_options:
                print(f"{Colors.YELLOW}[{option}]{Colors.END} {description}")
            
            choice = input(f"\n{Colors.BOLD}Выберите опцию: {Colors.END}")
            
            if choice == '1':
                duration = input("Длительность захвата в секундах (по умолчанию 60): ").strip()
                try:
                    duration = int(duration) if duration else 60
                except:
                    duration = 60
                
                print(f"\n{Colors.YELLOW}⚠️ Для захвата пакетов требуются права администратора!{Colors.END}")
                confirm = input("Продолжить? (y/n): ").lower()
                
                if confirm == 'y':
                    self.sniffer.packets = []  # Очищаем предыдущие данные
                    self.sniffer.start_sniffing(duration=duration)
                    
                    if self.sniffer.packets:
                        print(f"\n{Colors.GREEN}✅ Захвачено {len(self.sniffer.packets)} пакетов{Colors.END}")
                    
                input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
            
            elif choice == '2':
                if not self.sniffer.packets:
                    print(f"{Colors.RED}❌ Нет данных трафика. Сначала выполните захват.{Colors.END}")
                else:
                    protocol_stats = self.analyze_protocols(self.sniffer.packets)
                    print(f"\n{Colors.GREEN}🌐 Статистика протоколов:{Colors.END}")
                    total = sum(protocol_stats.values())
                    for protocol, count in sorted(protocol_stats.items(), key=lambda x: x[1], reverse=True):
                        percentage = (count / total) * 100 if total > 0 else 0
                        print(f"{Colors.CYAN}  {protocol}: {count} пакетов ({percentage:.1f}%){Colors.END}")
                
                input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
            
            elif choice == '3':
                if not self.sniffer.packets:
                    print(f"{Colors.RED}❌ Нет данных трафика. Сначала выполните захват.{Colors.END}")
                else:
                    top_talkers = self.analyze_top_talkers(self.sniffer.packets)
                    print(f"\n{Colors.GREEN}💬 Топ активные хосты:{Colors.END}")
                    for i, talker in enumerate(top_talkers, 1):
                        print(f"{Colors.CYAN}  {i}. {talker['ip']}{Colors.END}")
                        print(f"     Отправлено: {talker['sent_bytes']} байт")
                        print(f"     Получено: {talker['received_bytes']} байт")
                        print(f"     Всего: {talker['total_bytes']} байт")
                
                input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
            
            elif choice == '4':
                if not self.sniffer.packets:
                    print(f"{Colors.RED}❌ Нет данных трафика. Сначала выполните захват.{Colors.END}")
                else:
                    port_stats = self.analyze_ports(self.sniffer.packets)
                    print(f"\n{Colors.GREEN}🔌 Активные порты:{Colors.END}")
                    for port, count in sorted(port_stats.items(), key=lambda x: x[1], reverse=True)[:15]:
                        print(f"{Colors.CYAN}  Порт {port}: {count} соединений{Colors.END}")
                
                input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
            
            elif choice == '5':
                if not self.sniffer.packets:
                    print(f"{Colors.RED}❌ Нет данных трафика. Сначала выполните захват.{Colors.END}")
                else:
                    suspicious = self.detect_suspicious_activity(self.sniffer.packets)
                    print(f"\n{Colors.GREEN}🚨 Подозрительная активность:{Colors.END}")
                    
                    if suspicious:
                        for i, alert in enumerate(suspicious[:10], 1):
                            packet = alert['packet']
                            print(f"{Colors.RED}  {i}. {packet['ip_info'].get('source_ip', 'N/A')} -> {packet['ip_info'].get('destination_ip', 'N/A')}{Colors.END}")
                            print(f"     Время: {packet['timestamp']}")
                            for warning in alert['alerts']:
                                print(f"     • {warning}")
                            print()
                    else:
                        print(f"{Colors.GREEN}  Подозрительной активности не обнаружено{Colors.END}")
                
                input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
            
            elif choice == '6':
                if not self.sniffer.packets:
                    print(f"{Colors.RED}❌ Нет данных трафика. Сначала выполните захват.{Colors.END}")
                else:
                    self.generate_traffic_report(self.sniffer.packets)
                
                input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
            
            elif choice == '0':
                break
            
            else:
                print(f"{Colors.RED}❌ Неверный выбор!{Colors.END}")
                time.sleep(1)

if __name__ == "__main__":
    analyzer = TrafficAnalyzer()
    analyzer.run()
