#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚙️ Конфигурационный файл для OSINT Toolkit
Настройки API ключей и прочих параметров

⚠️ ВАЖНО: Не делитесь этим файлом! Добавьте его в .gitignore
"""

# =============================================================================
# API КЛЮЧИ ДЛЯ OSINT СЕРВИСОВ
# =============================================================================

# Have I Been Pwned API
# Получить ключ: https://haveibeenpwned.com/API/Key
HIBP_API_KEY = ""

# Shodan API
# Получить ключ: https://www.shodan.io/
SHODAN_API_KEY = ""

# VirusTotal API
# Получить ключ: https://www.virustotal.com/gui/join-us
VIRUSTOTAL_API_KEY = ""

# Hunter.io API (поиск email)
# Получить ключ: https://hunter.io/api
HUNTER_API_KEY = ""

# IPinfo.io API
# Получить ключ: https://ipinfo.io/signup
IPINFO_API_KEY = ""

# Censys API
# Получить ключи: https://censys.io/
CENSYS_API_ID = ""
CENSYS_API_SECRET = ""

# =============================================================================
# НАСТРОЙКИ ПРОКСИ
# =============================================================================

# Использовать прокси (True/False)
USE_PROXY = False

# Настройки прокси
PROXIES = {
    'http': 'http://proxy:port',
    'https': 'https://proxy:port'
}

# Tor прокси (если используется)
TOR_PROXY = {
    'http': 'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050'
}

# =============================================================================
# НАСТРОЙКИ RATE LIMITING
# =============================================================================

# Задержки между запросами (в секундах)
API_DELAYS = {
    'default': 1.0,
    'shodan': 1.0,
    'virustotal': 15.0,  # Бесплатный план - 4 запроса в минуту
    'hunter': 10.0,
    'hibp': 1.5
}

# Максимальное количество ретраев
MAX_RETRIES = 3

# Таймаут запросов (в секундах)
REQUEST_TIMEOUT = 30

# =============================================================================
# НАСТРОЙКИ БЕЗОПАСНОСТИ
# =============================================================================

# Логировать все действия (True/False)
ENABLE_LOGGING = True

# Показывать предупреждения об этике
SHOW_ETHICS_WARNING = True

# Максимальное количество целей для массового сканирования
MAX_BULK_TARGETS = 100

# Отключить опасные функции (True = безопасный режим)
SAFE_MODE = True

# =============================================================================
# НАСТРОЙКИ ОТЧЕТОВ
# =============================================================================

# Автоматически сохранять отчеты
AUTO_SAVE_REPORTS = True

# Формат отчетов по умолчанию
DEFAULT_REPORT_FORMAT = "txt"  # txt, json, html

# Включать метаданные в отчеты
INCLUDE_METADATA = True

# Директории для сохранения
REPORT_DIRECTORIES = {
    'osint': 'osint_reports',
    'social': 'reports', 
    'emails': 'generated_emails',
    'network': 'network_reports',
    'advanced': 'advanced_reports',
    'stego': 'steganography_results'
}

# =============================================================================
# НАСТРОЙКИ ПОЛЬЗОВАТЕЛЬСКОГО ИНТЕРФЕЙСА
# =============================================================================

# Показывать цветной вывод
COLORED_OUTPUT = True

# Показывать progress bars
SHOW_PROGRESS = True

# Автоочистка экрана при смене меню
AUTO_CLEAR_SCREEN = True

# Размер страницы для пагинации результатов
PAGE_SIZE = 20

# =============================================================================
# НАСТРОЙКИ СЕТИ
# =============================================================================

# User-Agent для HTTP запросов
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# Дополнительные заголовки
DEFAULT_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

# Настройки SSL
VERIFY_SSL = True

# =============================================================================
# НАСТРОЙКИ РАЗРАБОТЧИКА
# =============================================================================

# Режим отладки
DEBUG_MODE = False

# Подробное логирование API запросов
VERBOSE_API_LOGGING = False

# Сохранять raw ответы API
SAVE_RAW_RESPONSES = False

# =============================================================================
# ФУНКЦИИ ДЛЯ РАБОТЫ С КОНФИГУРАЦИЕЙ
# =============================================================================

def get_api_key(service: str) -> str:
    """Получить API ключ для сервиса"""
    keys = {
        'hibp': HIBP_API_KEY,
        'shodan': SHODAN_API_KEY,
        'virustotal': VIRUSTOTAL_API_KEY,
        'hunter': HUNTER_API_KEY,
        'ipinfo': IPINFO_API_KEY,
        'censys_id': CENSYS_API_ID,
        'censys_secret': CENSYS_API_SECRET
    }
    return keys.get(service, "")

def get_api_delay(service: str) -> float:
    """Получить задержку для API сервиса"""
    return API_DELAYS.get(service, API_DELAYS['default'])

def get_headers(additional_headers: dict = None) -> dict:
    """Получить HTTP заголовки"""
    headers = DEFAULT_HEADERS.copy()
    headers['User-Agent'] = USER_AGENT
    
    if additional_headers:
        headers.update(additional_headers)
    
    return headers

def get_proxies() -> dict:
    """Получить настройки прокси"""
    if USE_PROXY:
        return PROXIES
    return {}

def create_directories():
    """Создать необходимые директории"""
    import os
    
    for name, path in REPORT_DIRECTORIES.items():
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"📁 Создана директория: {path}")

# =============================================================================
# ВАЛИДАЦИЯ КОНФИГУРАЦИИ
# =============================================================================

def validate_config():
    """Проверка корректности конфигурации"""
    warnings = []
    
    # Проверяем API ключи
    if not HIBP_API_KEY:
        warnings.append("⚠️ HIBP_API_KEY не установлен - ограниченная функциональность")
    
    if not SHODAN_API_KEY:
        warnings.append("⚠️ SHODAN_API_KEY не установлен - будет использована симуляция")
    
    if not VIRUSTOTAL_API_KEY:
        warnings.append("⚠️ VIRUSTOTAL_API_KEY не установлен - ограниченная функциональность")
    
    # Проверяем настройки прокси
    if USE_PROXY and not PROXIES.get('http'):
        warnings.append("⚠️ Включены прокси, но адреса не указаны")
    
    # Проверяем rate limiting
    if API_DELAYS['virustotal'] < 15:
        warnings.append("⚠️ Слишком маленькая задержка для VirusTotal - может привести к блокировке")
    
    return warnings

def print_config_status():
    """Вывод статуса конфигурации"""
    print("\n🔧 СТАТУС КОНФИГУРАЦИИ:")
    print("=" * 30)
    
    # API ключи
    apis = [
        ('HIBP', HIBP_API_KEY),
        ('Shodan', SHODAN_API_KEY), 
        ('VirusTotal', VIRUSTOTAL_API_KEY),
        ('Hunter.io', HUNTER_API_KEY),
        ('IPinfo', IPINFO_API_KEY)
    ]
    
    for name, key in apis:
        status = "✅ Настроен" if key else "❌ Не настроен"
        print(f"  {name}: {status}")
    
    # Прокси
    proxy_status = "✅ Включен" if USE_PROXY else "❌ Отключен"
    print(f"  Прокси: {proxy_status}")
    
    # Безопасность
    safe_status = "✅ Включен" if SAFE_MODE else "⚠️ Отключен"
    print(f"  Безопасный режим: {safe_status}")
    
    # Предупреждения
    warnings = validate_config()
    if warnings:
        print("\n⚠️ ПРЕДУПРЕЖДЕНИЯ:")
        for warning in warnings:
            print(f"  {warning}")

if __name__ == "__main__":
    print_config_status()
