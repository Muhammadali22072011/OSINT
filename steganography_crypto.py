#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔐 Модуль стеганографии и криптоанализа
Инструменты для скрытия/извлечения данных и анализа шифров

⚠️ ВАЖНО: Использовать только в образовательных целях!
"""

import os
import sys
import base64
import hashlib
import random
import string
import itertools
import collections
from datetime import datetime
import json
import binascii
import zlib
import struct
from typing import List, Dict, Any, Optional, Tuple
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

class SteganographyEngine:
    """Движок стеганографии"""
    
    def __init__(self):
        self.supported_formats = ['txt', 'png', 'jpg', 'bmp', 'wav']
        self.encoding_methods = [
            'lsb',           # Least Significant Bit
            'dct',           # Discrete Cosine Transform
            'metadata',      # Metadata hiding
            'frequency',     # Frequency domain
            'spatial'        # Spatial domain
        ]
    
    def hide_text_in_text(self, cover_text: str, secret_text: str, method: str = 'whitespace') -> str:
        """Скрытие текста в тексте"""
        print(f"\n{Colors.CYAN}📝 СКРЫТИЕ ТЕКСТА В ТЕКСТЕ{Colors.END}")
        print(f"Метод: {method}")
        
        if method == 'whitespace':
            return self.whitespace_steganography(cover_text, secret_text)
        elif method == 'unicode':
            return self.unicode_steganography(cover_text, secret_text)
        elif method == 'invisible_chars':
            return self.invisible_char_steganography(cover_text, secret_text)
        else:
            return self.simple_text_steganography(cover_text, secret_text)
    
    def whitespace_steganography(self, cover_text: str, secret_text: str) -> str:
        """Стеганография с использованием пробелов"""
        # Преобразуем секретный текст в двоичный код
        binary_secret = ''.join(format(ord(char), '08b') for char in secret_text)
        binary_secret += '1111111111111110'  # Маркер конца
        
        result = ""
        binary_index = 0
        
        words = cover_text.split(' ')
        
        for i, word in enumerate(words):
            result += word
            
            if i < len(words) - 1:  # Не последнее слово
                if binary_index < len(binary_secret):
                    if binary_secret[binary_index] == '0':
                        result += ' '  # Один пробел = 0
                    else:
                        result += '  '  # Два пробела = 1
                    binary_index += 1
                else:
                    result += ' '
        
        print(f"{Colors.GREEN}✅ Текст успешно скрыт методом пробелов{Colors.END}")
        return result
    
    def unicode_steganography(self, cover_text: str, secret_text: str) -> str:
        """Стеганография с использованием Unicode символов"""
        # Используем невидимые Unicode символы
        zero_width_space = '\u200B'  # 0
        zero_width_joiner = '\u200D'  # 1
        
        binary_secret = ''.join(format(ord(char), '08b') for char in secret_text)
        binary_secret += '1111111111111110'  # Маркер конца
        
        result = ""
        binary_index = 0
        
        for char in cover_text:
            result += char
            
            if binary_index < len(binary_secret):
                if binary_secret[binary_index] == '0':
                    result += zero_width_space
                else:
                    result += zero_width_joiner
                binary_index += 1
        
        print(f"{Colors.GREEN}✅ Текст скрыт с помощью Unicode символов{Colors.END}")
        return result
    
    def invisible_char_steganography(self, cover_text: str, secret_text: str) -> str:
        """Стеганография с невидимыми символами"""
        # Невидимые символы для кодирования
        invisible_chars = {
            '0': '\u2060',  # Word joiner
            '1': '\u2061',  # Function application
            '2': '\u2062',  # Invisible times
            '3': '\u2063'   # Invisible separator
        }
        
        # Кодируем секретный текст в base4
        binary_secret = ''.join(format(ord(char), '08b') for char in secret_text)
        
        # Преобразуем в base4
        base4_secret = ""
        for i in range(0, len(binary_secret), 2):
            if i + 1 < len(binary_secret):
                two_bits = binary_secret[i:i+2]
                base4_secret += str(int(two_bits, 2))
            else:
                base4_secret += str(int(binary_secret[i] + '0', 2))
        
        base4_secret += '3'  # Маркер конца
        
        result = ""
        secret_index = 0
        
        for char in cover_text:
            result += char
            
            if secret_index < len(base4_secret):
                digit = base4_secret[secret_index]
                result += invisible_chars[digit]
                secret_index += 1
        
        print(f"{Colors.GREEN}✅ Текст скрыт с помощью невидимых символов{Colors.END}")
        return result
    
    def simple_text_steganography(self, cover_text: str, secret_text: str) -> str:
        """Простая текстовая стеганография"""
        # Используем первые буквы слов
        words = cover_text.split()
        secret_chars = list(secret_text.lower())
        
        result_words = []
        secret_index = 0
        
        for word in words:
            if secret_index < len(secret_chars) and word:
                target_char = secret_chars[secret_index]
                
                # Пытаемся найти слово, начинающееся с нужной буквы
                if word[0].lower() == target_char:
                    result_words.append(word.upper())  # Выделяем нужные слова
                    secret_index += 1
                else:
                    result_words.append(word)
            else:
                result_words.append(word)
        
        print(f"{Colors.GREEN}✅ Секретный текст закодирован в первых буквах выделенных слов{Colors.END}")
        return ' '.join(result_words)
    
    def extract_text_from_text(self, stego_text: str, method: str = 'whitespace') -> str:
        """Извлечение скрытого текста"""
        print(f"\n{Colors.YELLOW}🔍 ИЗВЛЕЧЕНИЕ СКРЫТОГО ТЕКСТА{Colors.END}")
        print(f"Метод: {method}")
        
        try:
            if method == 'whitespace':
                return self.extract_whitespace_steganography(stego_text)
            elif method == 'unicode':
                return self.extract_unicode_steganography(stego_text)
            elif method == 'invisible_chars':
                return self.extract_invisible_char_steganography(stego_text)
            else:
                return self.extract_simple_text_steganography(stego_text)
        except Exception as e:
            print(f"{Colors.RED}❌ Ошибка извлечения: {e}{Colors.END}")
            return ""
    
    def extract_whitespace_steganography(self, stego_text: str) -> str:
        """Извлечение из пробелов"""
        binary_data = ""
        words = stego_text.split(' ')
        
        for i in range(len(words) - 1):
            # Проверяем количество пробелов между словами
            next_word_index = stego_text.find(words[i+1], stego_text.find(words[i]) + len(words[i]))
            spaces_between = next_word_index - (stego_text.find(words[i]) + len(words[i]))
            
            if spaces_between == 1:
                binary_data += '0'
            elif spaces_between == 2:
                binary_data += '1'
        
        # Ищем маркер конца
        end_marker = '1111111111111110'
        if end_marker in binary_data:
            binary_data = binary_data[:binary_data.find(end_marker)]
        
        # Преобразуем двоичные данные обратно в текст
        secret_text = ""
        for i in range(0, len(binary_data), 8):
            if i + 8 <= len(binary_data):
                byte = binary_data[i:i+8]
                secret_text += chr(int(byte, 2))
        
        return secret_text
    
    def extract_unicode_steganography(self, stego_text: str) -> str:
        """Извлечение из Unicode символов"""
        zero_width_space = '\u200B'  # 0
        zero_width_joiner = '\u200D'  # 1
        
        binary_data = ""
        
        for char in stego_text:
            if char == zero_width_space:
                binary_data += '0'
            elif char == zero_width_joiner:
                binary_data += '1'
        
        # Ищем маркер конца
        end_marker = '1111111111111110'
        if end_marker in binary_data:
            binary_data = binary_data[:binary_data.find(end_marker)]
        
        # Преобразуем в текст
        secret_text = ""
        for i in range(0, len(binary_data), 8):
            if i + 8 <= len(binary_data):
                byte = binary_data[i:i+8]
                secret_text += chr(int(byte, 2))
        
        return secret_text
    
    def extract_invisible_char_steganography(self, stego_text: str) -> str:
        """Извлечение из невидимых символов"""
        invisible_chars = {
            '\u2060': '0',  # Word joiner
            '\u2061': '1',  # Function application
            '\u2062': '2',  # Invisible times
            '\u2063': '3'   # Invisible separator
        }
        
        base4_data = ""
        
        for char in stego_text:
            if char in invisible_chars:
                base4_data += invisible_chars[char]
        
        # Ищем маркер конца
        if '3' in base4_data:
            base4_data = base4_data[:base4_data.find('3')]
        
        # Преобразуем base4 в двоичный
        binary_data = ""
        for digit in base4_data:
            binary_data += format(int(digit), '02b')
        
        # Преобразуем в текст
        secret_text = ""
        for i in range(0, len(binary_data), 8):
            if i + 8 <= len(binary_data):
                byte = binary_data[i:i+8]
                secret_text += chr(int(byte, 2))
        
        return secret_text
    
    def extract_simple_text_steganography(self, stego_text: str) -> str:
        """Извлечение простой стеганографии"""
        words = stego_text.split()
        secret_chars = []
        
        for word in words:
            if word.isupper() and word:
                secret_chars.append(word[0].lower())
        
        return ''.join(secret_chars)
    
    def analyze_file_for_steganography(self, filepath: str) -> Dict:
        """Анализ файла на наличие стеганографии"""
        print(f"\n{Colors.PURPLE}🔍 АНАЛИЗ ФАЙЛА НА СТЕГАНОГРАФИЮ{Colors.END}")
        print(f"Файл: {filepath}")
        
        if not os.path.exists(filepath):
            return {'error': 'Файл не найден'}
        
        analysis = {
            'file_info': self.get_file_info(filepath),
            'entropy_analysis': self.calculate_entropy(filepath),
            'metadata_analysis': self.analyze_metadata(filepath),
            'pattern_analysis': self.analyze_patterns(filepath),
            'suspicious_indicators': []
        }
        
        # Проверка на подозрительные индикаторы
        if analysis['entropy_analysis']['entropy'] > 7.5:
            analysis['suspicious_indicators'].append('Высокая энтропия - возможно сжатие или шифрование')
        
        if analysis['file_info']['size'] > 1024 * 1024:  # >1MB
            analysis['suspicious_indicators'].append('Большой размер файла')
        
        return analysis
    
    def get_file_info(self, filepath: str) -> Dict:
        """Получение информации о файле"""
        stat = os.stat(filepath)
        
        return {
            'size': stat.st_size,
            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
            'extension': os.path.splitext(filepath)[1].lower()
        }
    
    def calculate_entropy(self, filepath: str) -> Dict:
        """Расчет энтропии файла"""
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
            
            if not data:
                return {'entropy': 0, 'analysis': 'Файл пустой'}
            
            # Подсчет частоты байтов
            byte_counts = collections.Counter(data)
            
            # Расчет энтропии
            entropy = 0
            total_bytes = len(data)
            
            for count in byte_counts.values():
                probability = count / total_bytes
                entropy -= probability * math.log2(probability)
            
            analysis = ""
            if entropy < 1:
                analysis = "Очень низкая энтропия - данные сильно структурированы"
            elif entropy < 4:
                analysis = "Низкая энтропия - текстовые данные"
            elif entropy < 6:
                analysis = "Средняя энтропия - смешанные данные"
            elif entropy < 7.5:
                analysis = "Высокая энтропия - сжатые или зашифрованные данные"
            else:
                analysis = "Очень высокая энтропия - случайные или зашифрованные данные"
            
            return {
                'entropy': entropy,
                'analysis': analysis,
                'unique_bytes': len(byte_counts),
                'total_bytes': total_bytes
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def analyze_metadata(self, filepath: str) -> Dict:
        """Анализ метаданных файла"""
        metadata = {
            'basic_info': {},
            'suspicious_metadata': [],
            'hidden_data_indicators': []
        }
        
        try:
            # Базовая информация
            with open(filepath, 'rb') as f:
                header = f.read(512)  # Первые 512 байт
            
            # Проверка магических байтов
            magic_bytes = {
                b'\x89PNG': 'PNG Image',
                b'\xFF\xD8\xFF': 'JPEG Image',
                b'BM': 'BMP Image',
                b'RIFF': 'WAV/AVI File',
                b'%PDF': 'PDF Document',
                b'PK\x03\x04': 'ZIP Archive'
            }
            
            for magic, file_type in magic_bytes.items():
                if header.startswith(magic):
                    metadata['basic_info']['detected_type'] = file_type
                    break
            
            # Поиск подозрительных паттернов в заголовке
            if b'steganography' in header.lower():
                metadata['suspicious_metadata'].append('Найдено слово "steganography" в заголовке')
            
            if b'hidden' in header.lower():
                metadata['suspicious_metadata'].append('Найдено слово "hidden" в заголовке')
            
            # Анализ на скрытые данные в конце файла
            with open(filepath, 'rb') as f:
                f.seek(-512, 2)  # Последние 512 байт
                tail = f.read()
            
            # Проверка на дополнительные данные после основного содержимого
            if len(tail) > 0:
                text_content = tail.decode('utf-8', errors='ignore')
                if any(word in text_content.lower() for word in ['password', 'secret', 'hidden', 'key']):
                    metadata['hidden_data_indicators'].append('Подозрительный текст в конце файла')
            
        except Exception as e:
            metadata['error'] = str(e)
        
        return metadata
    
    def analyze_patterns(self, filepath: str) -> Dict:
        """Анализ паттернов в файле"""
        patterns = {
            'repeated_sequences': [],
            'unusual_patterns': [],
            'encoding_indicators': []
        }
        
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
            
            # Поиск повторяющихся последовательностей
            chunk_size = 16
            chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
            chunk_counts = collections.Counter(chunks)
            
            for chunk, count in chunk_counts.most_common(5):
                if count > 3:  # Если chunk повторяется более 3 раз
                    patterns['repeated_sequences'].append({
                        'chunk': chunk.hex(),
                        'count': count
                    })
            
            # Поиск Base64 паттернов
            text_data = data.decode('utf-8', errors='ignore')
            base64_pattern = r'[A-Za-z0-9+/]{20,}={0,2}'
            import re
            base64_matches = re.findall(base64_pattern, text_data)
            
            if base64_matches:
                patterns['encoding_indicators'].append(f'Найдено {len(base64_matches)} возможных Base64 строк')
            
            # Поиск hex паттернов
            hex_pattern = r'[0-9A-Fa-f]{32,}'
            hex_matches = re.findall(hex_pattern, text_data)
            
            if hex_matches:
                patterns['encoding_indicators'].append(f'Найдено {len(hex_matches)} возможных hex строк')
            
        except Exception as e:
            patterns['error'] = str(e)
        
        return patterns

class CryptoAnalyzer:
    """Анализатор шифров и криптографии"""
    
    def __init__(self):
        self.classic_ciphers = [
            'caesar', 'vigenere', 'playfair', 'hill', 'rail_fence',
            'substitution', 'atbash', 'rot13', 'base64', 'morse'
        ]
        
        # Частоты букв в русском языке
        self.russian_freq = {
            'о': 10.97, 'е': 8.45, 'а': 8.01, 'и': 7.35, 'н': 6.70,
            'т': 6.26, 'с': 5.47, 'р': 4.73, 'в': 4.54, 'л': 4.40,
            'к': 3.49, 'м': 3.21, 'д': 2.98, 'п': 2.81, 'у': 2.62,
            'я': 2.01, 'ы': 1.90, 'ь': 1.74, 'г': 1.70, 'з': 1.65,
            'б': 1.59, 'ч': 1.44, 'й': 1.21, 'х': 0.97, 'ж': 0.94,
            'ш': 0.73, 'ю': 0.64, 'ц': 0.48, 'щ': 0.36, 'э': 0.32,
            'ф': 0.26, 'ъ': 0.04
        }
        
        # Частоты букв в английском языке
        self.english_freq = {
            'e': 12.70, 't': 9.06, 'a': 8.17, 'o': 7.51, 'i': 6.97,
            'n': 6.75, 's': 6.33, 'h': 6.09, 'r': 5.99, 'd': 4.25,
            'l': 4.03, 'c': 2.78, 'u': 2.76, 'm': 2.41, 'w': 2.36,
            'f': 2.23, 'g': 2.02, 'y': 1.97, 'p': 1.93, 'b': 1.29,
            'v': 0.98, 'k': 0.77, 'j': 0.15, 'x': 0.15, 'q': 0.10,
            'z': 0.07
        }
    
    def analyze_text_for_cipher(self, text: str) -> Dict:
        """Анализ текста на тип шифра"""
        print(f"\n{Colors.BLUE}🔍 АНАЛИЗ ШИФРА{Colors.END}")
        
        analysis = {
            'text_stats': self.get_text_statistics(text),
            'frequency_analysis': self.frequency_analysis(text),
            'pattern_analysis': self.pattern_analysis(text),
            'cipher_detection': self.detect_cipher_type(text),
            'language_detection': self.detect_language(text)
        }
        
        return analysis
    
    def get_text_statistics(self, text: str) -> Dict:
        """Получение статистики текста"""
        stats = {
            'length': len(text),
            'unique_chars': len(set(text)),
            'alphabetic_ratio': sum(1 for c in text if c.isalpha()) / len(text) if text else 0,
            'digit_ratio': sum(1 for c in text if c.isdigit()) / len(text) if text else 0,
            'space_ratio': sum(1 for c in text if c.isspace()) / len(text) if text else 0,
            'uppercase_ratio': sum(1 for c in text if c.isupper()) / len(text) if text else 0
        }
        
        return stats
    
    def frequency_analysis(self, text: str) -> Dict:
        """Частотный анализ текста"""
        # Подсчет частот символов
        char_counts = collections.Counter(text.lower())
        total_chars = sum(char_counts.values())
        
        frequencies = {}
        for char, count in char_counts.items():
            if char.isalpha():
                frequencies[char] = (count / total_chars) * 100
        
        # Сортировка по частоте
        sorted_freq = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'character_frequencies': frequencies,
            'most_frequent': sorted_freq[:10],
            'total_alphabetic': sum(frequencies.values())
        }
    
    def pattern_analysis(self, text: str) -> Dict:
        """Анализ паттернов в тексте"""
        patterns = {
            'repeated_bigrams': {},
            'repeated_trigrams': {},
            'word_patterns': {},
            'spacing_patterns': []
        }
        
        # Анализ биграмм
        for i in range(len(text) - 1):
            bigram = text[i:i+2].lower()
            if bigram.isalpha():
                patterns['repeated_bigrams'][bigram] = patterns['repeated_bigrams'].get(bigram, 0) + 1
        
        # Анализ триграмм
        for i in range(len(text) - 2):
            trigram = text[i:i+3].lower()
            if trigram.isalpha():
                patterns['repeated_trigrams'][trigram] = patterns['repeated_trigrams'].get(trigram, 0) + 1
        
        # Сортировка по частоте
        patterns['repeated_bigrams'] = dict(sorted(patterns['repeated_bigrams'].items(), 
                                                 key=lambda x: x[1], reverse=True)[:10])
        patterns['repeated_trigrams'] = dict(sorted(patterns['repeated_trigrams'].items(), 
                                                   key=lambda x: x[1], reverse=True)[:10])
        
        # Анализ расстояний между повторениями
        distances = []
        for pattern in patterns['repeated_trigrams']:
            positions = []
            start = 0
            while True:
                pos = text.lower().find(pattern, start)
                if pos == -1:
                    break
                positions.append(pos)
                start = pos + 1
            
            if len(positions) > 1:
                for i in range(len(positions) - 1):
                    distances.append(positions[i+1] - positions[i])
        
        patterns['common_distances'] = collections.Counter(distances).most_common(5)
        
        return patterns
    
    def detect_cipher_type(self, text: str) -> Dict:
        """Определение типа шифра"""
        detection = {
            'possible_ciphers': [],
            'confidence_scores': {},
            'indicators': []
        }
        
        # Проверка на Caesar cipher
        if self.is_likely_caesar(text):
            detection['possible_ciphers'].append('Caesar Cipher')
            detection['confidence_scores']['caesar'] = 0.7
            detection['indicators'].append('Равномерное распределение символов')
        
        # Проверка на Base64
        if self.is_likely_base64(text):
            detection['possible_ciphers'].append('Base64 Encoding')
            detection['confidence_scores']['base64'] = 0.9
            detection['indicators'].append('Характерные для Base64 символы')
        
        # Проверка на Morse code
        if self.is_likely_morse(text):
            detection['possible_ciphers'].append('Morse Code')
            detection['confidence_scores']['morse'] = 0.8
            detection['indicators'].append('Точки и тире')
        
        # Проверка на простую замену
        if self.is_likely_substitution(text):
            detection['possible_ciphers'].append('Substitution Cipher')
            detection['confidence_scores']['substitution'] = 0.6
            detection['indicators'].append('Сохраненная структура языка')
        
        # Проверка на Vigenère
        if self.is_likely_vigenere(text):
            detection['possible_ciphers'].append('Vigenère Cipher')
            detection['confidence_scores']['vigenere'] = 0.5
            detection['indicators'].append('Повторяющиеся паттерны на разных расстояниях')
        
        return detection
    
    def is_likely_caesar(self, text: str) -> bool:
        """Проверка на шифр Цезаря"""
        # Простая проверка: если текст содержит только буквы и распределение относительно равномерное
        if not text.isalpha():
            return False
        
        char_counts = collections.Counter(text.lower())
        if len(char_counts) < 10:  # Слишком мало уникальных символов
            return False
        
        # Проверяем равномерность распределения
        counts = list(char_counts.values())
        avg_count = sum(counts) / len(counts)
        variance = sum((count - avg_count) ** 2 for count in counts) / len(counts)
        
        return variance < avg_count * 2  # Относительно равномерное распределение
    
    def is_likely_base64(self, text: str) -> bool:
        """Проверка на Base64"""
        import re
        
        # Base64 содержит только определенные символы
        base64_pattern = r'^[A-Za-z0-9+/]*={0,2}$'
        if not re.match(base64_pattern, text.strip()):
            return False
        
        # Длина должна быть кратна 4 (с учетом padding)
        clean_text = text.strip().rstrip('=')
        return len(text.strip()) % 4 == 0
    
    def is_likely_morse(self, text: str) -> bool:
        """Проверка на азбуку Морзе"""
        # Морзе содержит только точки, тире и пробелы
        morse_chars = set('.-/ ')
        return all(c in morse_chars for c in text)
    
    def is_likely_substitution(self, text: str) -> bool:
        """Проверка на простую замену"""
        # При простой замене сохраняется структура языка
        if not text.isalpha():
            return False
        
        # Проверяем наличие коротких и длинных слов
        words = text.split()
        if not words:
            return False
        
        word_lengths = [len(word) for word in words]
        return min(word_lengths) == 1 and max(word_lengths) > 5  # Есть короткие и длинные слова
    
    def is_likely_vigenere(self, text: str) -> bool:
        """Проверка на шифр Виженера"""
        if not text.isalpha():
            return False
        
        # Ищем повторяющиеся триграммы на разных расстояниях
        trigrams = {}
        for i in range(len(text) - 2):
            trigram = text[i:i+3].lower()
            if trigram in trigrams:
                trigrams[trigram].append(i)
            else:
                trigrams[trigram] = [i]
        
        # Проверяем расстояния между повторениями
        distances = []
        for positions in trigrams.values():
            if len(positions) > 1:
                for i in range(len(positions) - 1):
                    distances.append(positions[i+1] - positions[i])
        
        if not distances:
            return False
        
        # Ищем общие делители расстояний (возможная длина ключа)
        from math import gcd
        common_gcd = distances[0]
        for distance in distances[1:]:
            common_gcd = gcd(common_gcd, distance)
        
        return common_gcd > 1  # Есть общий делитель > 1
    
    def detect_language(self, text: str) -> Dict:
        """Определение языка текста"""
        if not text.isalpha():
            return {'language': 'unknown', 'confidence': 0}
        
        # Подсчитываем частоты букв
        char_counts = collections.Counter(text.lower())
        total_chars = sum(char_counts.values())
        
        text_freq = {}
        for char, count in char_counts.items():
            if char.isalpha():
                text_freq[char] = (count / total_chars) * 100
        
        # Сравниваем с эталонными частотами
        russian_score = self.calculate_frequency_score(text_freq, self.russian_freq)
        english_score = self.calculate_frequency_score(text_freq, self.english_freq)
        
        if russian_score < english_score:
            return {'language': 'russian', 'confidence': min(1.0, 1.0 / (russian_score + 0.1))}
        else:
            return {'language': 'english', 'confidence': min(1.0, 1.0 / (english_score + 0.1))}
    
    def calculate_frequency_score(self, text_freq: Dict, ref_freq: Dict) -> float:
        """Расчет оценки соответствия частот"""
        score = 0
        for char in ref_freq:
            text_freq_val = text_freq.get(char, 0)
            ref_freq_val = ref_freq[char]
            score += abs(text_freq_val - ref_freq_val)
        
        return score
    
    def brute_force_caesar(self, text: str) -> Dict:
        """Перебор ключей шифра Цезаря"""
        print(f"\n{Colors.YELLOW}🔓 БРУТФОРС ШИФРА ЦЕЗАРЯ{Colors.END}")
        
        results = {}
        
        for shift in range(26):
            decrypted = ""
            for char in text:
                if char.isalpha():
                    ascii_offset = 65 if char.isupper() else 97
                    decrypted += chr((ord(char) - ascii_offset - shift) % 26 + ascii_offset)
                else:
                    decrypted += char
            
            # Оценка качества расшифровки
            score = self.evaluate_text_quality(decrypted)
            results[shift] = {
                'text': decrypted,
                'score': score
            }
        
        # Сортируем по качеству
        sorted_results = sorted(results.items(), key=lambda x: x[1]['score'], reverse=True)
        
        print(f"{Colors.GREEN}✅ Найдено {len(results)} вариантов{Colors.END}")
        
        return {
            'all_results': results,
            'best_candidates': sorted_results[:5]
        }
    
    def evaluate_text_quality(self, text: str) -> float:
        """Оценка качества текста (похожести на натуральный язык)"""
        if not text:
            return 0
        
        score = 0
        
        # Частотный анализ
        char_counts = collections.Counter(text.lower())
        total_chars = sum(1 for c in text if c.isalpha())
        
        if total_chars == 0:
            return 0
        
        # Сравнение с эталонными частотами английского языка
        for char, expected_freq in self.english_freq.items():
            actual_count = char_counts.get(char, 0)
            actual_freq = (actual_count / total_chars) * 100
            score -= abs(actual_freq - expected_freq)
        
        # Бонус за наличие общих слов
        common_words = ['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use']
        
        text_lower = text.lower()
        for word in common_words:
            if word in text_lower:
                score += 10
        
        return score
    
    def analyze_vigenere_key_length(self, text: str) -> Dict:
        """Анализ длины ключа Виженера (индекс совпадений)"""
        print(f"\n{Colors.CYAN}🔑 АНАЛИЗ ДЛИНЫ КЛЮЧА ВИЖЕНЕРА{Colors.END}")
        
        # Удаляем пробелы и приводим к верхнему регистру
        clean_text = ''.join(c.upper() for c in text if c.isalpha())
        
        if len(clean_text) < 50:
            return {'error': 'Текст слишком короткий для анализа'}
        
        key_lengths = {}
        
        # Тестируем длины ключа от 1 до 20
        for key_length in range(1, 21):
            ic_sum = 0
            
            # Разделяем текст на подстроки по длине ключа
            for i in range(key_length):
                substring = clean_text[i::key_length]
                
                if len(substring) > 1:
                    ic = self.calculate_index_of_coincidence(substring)
                    ic_sum += ic
            
            average_ic = ic_sum / key_length
            key_lengths[key_length] = average_ic
        
        # Сортируем по индексу совпадений (больше = лучше)
        sorted_lengths = sorted(key_lengths.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'all_lengths': key_lengths,
            'most_likely': sorted_lengths[:5],
            'analysis': 'Длины ключей с высоким индексом совпадений более вероятны'
        }
    
    def calculate_index_of_coincidence(self, text: str) -> float:
        """Расчет индекса совпадений"""
        if len(text) < 2:
            return 0
        
        char_counts = collections.Counter(text)
        n = len(text)
        
        ic = 0
        for count in char_counts.values():
            ic += count * (count - 1)
        
        ic = ic / (n * (n - 1))
        return ic
    
    def decode_common_encodings(self, text: str) -> Dict:
        """Декодирование распространенных кодировок"""
        print(f"\n{Colors.GREEN}🔓 ДЕКОДИРОВАНИЕ РАСПРОСТРАНЕННЫХ ФОРМАТОВ{Colors.END}")
        
        results = {}
        
        # Base64
        try:
            decoded = base64.b64decode(text).decode('utf-8')
            results['base64'] = decoded
        except:
            results['base64'] = 'Ошибка декодирования'
        
        # Hex
        try:
            decoded = bytes.fromhex(text).decode('utf-8')
            results['hex'] = decoded
        except:
            results['hex'] = 'Ошибка декодирования'
        
        # URL encoding
        try:
            import urllib.parse
            decoded = urllib.parse.unquote(text)
            results['url'] = decoded
        except:
            results['url'] = 'Ошибка декодирования'
        
        # ROT13
        try:
            decoded = text.translate(str.maketrans(
                'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
                'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm'
            ))
            results['rot13'] = decoded
        except:
            results['rot13'] = 'Ошибка декодирования'
        
        # Atbash (простая замена A=Z, B=Y, etc.)
        try:
            decoded = ""
            for char in text:
                if char.isalpha():
                    if char.isupper():
                        decoded += chr(ord('Z') - (ord(char) - ord('A')))
                    else:
                        decoded += chr(ord('z') - (ord(char) - ord('a')))
                else:
                    decoded += char
            results['atbash'] = decoded
        except:
            results['atbash'] = 'Ошибка декодирования'
        
        return results

class SteganoCryptoSuite:
    """Основной класс для работы со стеганографией и криптоанализом"""
    
    def __init__(self):
        self.stego_engine = SteganographyEngine()
        self.crypto_analyzer = CryptoAnalyzer()
    
    def run(self):
        """Запуск главного меню"""
        while True:
            print(f"\n{Colors.BOLD}{Colors.PURPLE}🔐 СТЕГАНОГРАФИЯ И КРИПТОАНАЛИЗ{Colors.END}")
            print(f"{Colors.RED}⚠️ ТОЛЬКО ДЛЯ ОБРАЗОВАТЕЛЬНЫХ ЦЕЛЕЙ!{Colors.END}\n")
            
            print("Выберите категорию:")
            print("1. 📝 Текстовая стеганография")
            print("2. 🔍 Анализ файлов на стеганографию")
            print("3. 🔓 Анализ и взлом шифров")
            print("4. 🧮 Частотный анализ")
            print("5. 📊 Криптографические инструменты")
            print("6. 📁 Просмотр результатов")
            print("0. ← Назад в главное меню")
            
            choice = input(f"\n{Colors.YELLOW}Выберите опцию: {Colors.END}")
            
            if choice == '1':
                self.text_steganography_menu()
            elif choice == '2':
                self.file_analysis_menu()
            elif choice == '3':
                self.cipher_analysis_menu()
            elif choice == '4':
                self.frequency_analysis_menu()
            elif choice == '5':
                self.crypto_tools_menu()
            elif choice == '6':
                self.view_results()
            elif choice == '0':
                break
            else:
                print(f"{Colors.RED}❌ Неверный выбор!{Colors.END}")
    
    def text_steganography_menu(self):
        """Меню текстовой стеганографии"""
        while True:
            print(f"\n{Colors.CYAN}📝 ТЕКСТОВАЯ СТЕГАНОГРАФИЯ{Colors.END}")
            print("1. 📥 Скрыть текст в тексте")
            print("2. 📤 Извлечь скрытый текст")
            print("3. 🔍 Анализ текста на скрытые данные")
            print("0. ← Назад")
            
            choice = input(f"\n{Colors.YELLOW}Выберите действие: {Colors.END}")
            
            if choice == '1':
                self.hide_text_interface()
            elif choice == '2':
                self.extract_text_interface()
            elif choice == '3':
                self.analyze_text_interface()
            elif choice == '0':
                break
            else:
                print(f"{Colors.RED}❌ Неверный выбор!{Colors.END}")
    
    def hide_text_interface(self):
        """Интерфейс скрытия текста"""
        print(f"\n{Colors.GREEN}📥 СКРЫТИЕ ТЕКСТА{Colors.END}")
        
        print("Методы:")
        print("1. whitespace - Использование пробелов")
        print("2. unicode - Unicode символы")
        print("3. invisible_chars - Невидимые символы")
        print("4. simple - Простая стеганография")
        
        method = input("Выберите метод (1-4): ").strip()
        method_map = {'1': 'whitespace', '2': 'unicode', '3': 'invisible_chars', '4': 'simple'}
        method = method_map.get(method, 'whitespace')
        
        cover_text = input("\nВведите текст-контейнер: ")
        secret_text = input("Введите секретный текст: ")
        
        if cover_text and secret_text:
            result = self.stego_engine.hide_text_in_text(cover_text, secret_text, method)
            
            print(f"\n{Colors.BOLD}РЕЗУЛЬТАТ:{Colors.END}")
            print(result)
            
            # Сохранение результата
            if input("\nСохранить результат? (y/n): ").lower() == 'y':
                self.save_steganography_result(result, method, 'hide')
        
        input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
    
    def extract_text_interface(self):
        """Интерфейс извлечения текста"""
        print(f"\n{Colors.YELLOW}📤 ИЗВЛЕЧЕНИЕ ТЕКСТА{Colors.END}")
        
        print("Методы:")
        print("1. whitespace")
        print("2. unicode")
        print("3. invisible_chars")
        print("4. simple")
        
        method = input("Выберите метод (1-4): ").strip()
        method_map = {'1': 'whitespace', '2': 'unicode', '3': 'invisible_chars', '4': 'simple'}
        method = method_map.get(method, 'whitespace')
        
        stego_text = input("\nВведите текст со скрытыми данными: ")
        
        if stego_text:
            result = self.stego_engine.extract_text_from_text(stego_text, method)
            
            if result:
                print(f"\n{Colors.BOLD}ИЗВЛЕЧЕННЫЙ ТЕКСТ:{Colors.END}")
                print(f"{Colors.GREEN}{result}{Colors.END}")
            else:
                print(f"{Colors.RED}Скрытый текст не найден{Colors.END}")
        
        input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
    
    def analyze_text_interface(self):
        """Интерфейс анализа текста"""
        print(f"\n{Colors.PURPLE}🔍 АНАЛИЗ ТЕКСТА{Colors.END}")
        
        text = input("Введите текст для анализа: ")
        
        if text:
            # Проверяем на разные методы стеганографии
            methods = ['whitespace', 'unicode', 'invisible_chars', 'simple']
            
            print(f"\n{Colors.BOLD}РЕЗУЛЬТАТЫ АНАЛИЗА:{Colors.END}")
            
            for method in methods:
                print(f"\n--- Метод: {method} ---")
                try:
                    extracted = self.stego_engine.extract_text_from_text(text, method)
                    if extracted and extracted.strip():
                        print(f"{Colors.GREEN}✅ Найден скрытый текст: {extracted}{Colors.END}")
                    else:
                        print(f"{Colors.YELLOW}❌ Скрытый текст не найден{Colors.END}")
                except Exception as e:
                    print(f"{Colors.RED}❌ Ошибка анализа: {e}{Colors.END}")
        
        input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
    
    def file_analysis_menu(self):
        """Меню анализа файлов"""
        print(f"\n{Colors.BLUE}🔍 АНАЛИЗ ФАЙЛОВ{Colors.END}")
        
        filepath = input("Введите путь к файлу: ")
        
        if os.path.exists(filepath):
            analysis = self.stego_engine.analyze_file_for_steganography(filepath)
            
            print(f"\n{Colors.BOLD}РЕЗУЛЬТАТЫ АНАЛИЗА:{Colors.END}")
            print(json.dumps(analysis, ensure_ascii=False, indent=2))
            
            if input("\nСохранить отчет? (y/n): ").lower() == 'y':
                self.save_analysis_report(filepath, analysis)
        else:
            print(f"{Colors.RED}❌ Файл не найден{Colors.END}")
        
        input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
    
    def cipher_analysis_menu(self):
        """Меню анализа шифров"""
        while True:
            print(f"\n{Colors.RED}🔓 АНАЛИЗ И ВЗЛОМ ШИФРОВ{Colors.END}")
            print("1. 🔍 Анализ типа шифра")
            print("2. 🔓 Брутфорс шифра Цезаря")
            print("3. 🔑 Анализ длины ключа Виженера")
            print("4. 📊 Декодирование стандартных форматов")
            print("0. ← Назад")
            
            choice = input(f"\n{Colors.YELLOW}Выберите действие: {Colors.END}")
            
            if choice == '1':
                text = input("Введите зашифрованный текст: ")
                if text:
                    analysis = self.crypto_analyzer.analyze_text_for_cipher(text)
                    print(f"\n{Colors.BOLD}АНАЛИЗ ШИФРА:{Colors.END}")
                    print(json.dumps(analysis, ensure_ascii=False, indent=2))
            
            elif choice == '2':
                text = input("Введите текст для брутфорса: ")
                if text:
                    results = self.crypto_analyzer.brute_force_caesar(text)
                    print(f"\n{Colors.BOLD}ЛУЧШИЕ КАНДИДАТЫ:{Colors.END}")
                    for shift, data in results['best_candidates'][:3]:
                        print(f"Сдвиг {shift}: {data['text'][:100]}...")
            
            elif choice == '3':
                text = input("Введите текст для анализа Виженера: ")
                if text:
                    analysis = self.crypto_analyzer.analyze_vigenere_key_length(text)
                    print(f"\n{Colors.BOLD}АНАЛИЗ ДЛИНЫ КЛЮЧА:{Colors.END}")
                    print(json.dumps(analysis, ensure_ascii=False, indent=2))
            
            elif choice == '4':
                text = input("Введите закодированный текст: ")
                if text:
                    results = self.crypto_analyzer.decode_common_encodings(text)
                    print(f"\n{Colors.BOLD}РЕЗУЛЬТАТЫ ДЕКОДИРОВАНИЯ:{Colors.END}")
                    for encoding, result in results.items():
                        print(f"{encoding}: {result[:100]}...")
            
            elif choice == '0':
                break
            else:
                print(f"{Colors.RED}❌ Неверный выбор!{Colors.END}")
            
            if choice != '0':
                input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
    
    def frequency_analysis_menu(self):
        """Меню частотного анализа"""
        print(f"\n{Colors.CYAN}📊 ЧАСТОТНЫЙ АНАЛИЗ{Colors.END}")
        
        text = input("Введите текст для анализа: ")
        
        if text:
            freq_analysis = self.crypto_analyzer.frequency_analysis(text)
            lang_detection = self.crypto_analyzer.detect_language(text)
            
            print(f"\n{Colors.BOLD}ЧАСТОТНЫЙ АНАЛИЗ:{Colors.END}")
            print(f"Определенный язык: {lang_detection['language']} (уверенность: {lang_detection['confidence']:.2f})")
            
            print(f"\nСамые частые символы:")
            for char, freq in freq_analysis['most_frequent'][:10]:
                print(f"  '{char}': {freq:.2f}%")
        
        input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
    
    def crypto_tools_menu(self):
        """Меню криптографических инструментов"""
        print(f"\n{Colors.GREEN}🧮 КРИПТОГРАФИЧЕСКИЕ ИНСТРУМЕНТЫ{Colors.END}")
        print("🚧 В разработке...")
        input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
    
    def view_results(self):
        """Просмотр сохраненных результатов"""
        print(f"\n{Colors.PURPLE}📁 СОХРАНЕННЫЕ РЕЗУЛЬТАТЫ{Colors.END}")
        print("🚧 В разработке...")
        input(f"\n{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.END}")
    
    def save_steganography_result(self, result: str, method: str, operation: str):
        """Сохранение результата стеганографии"""
        if not os.path.exists("steganography_results"):
            os.makedirs("steganography_results")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"steganography_results/stego_{operation}_{method}_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("РЕЗУЛЬТАТ СТЕГАНОГРАФИИ\n")
            f.write("="*60 + "\n\n")
            f.write(f"Операция: {operation}\n")
            f.write(f"Метод: {method}\n")
            f.write(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("Результат:\n")
            f.write("-" * 40 + "\n")
            f.write(result)
            f.write("\n\n" + "="*60 + "\n")
        
        print(f"{Colors.GREEN}✅ Результат сохранен: {filename}{Colors.END}")
    
    def save_analysis_report(self, filepath: str, analysis: Dict):
        """Сохранение отчета анализа"""
        if not os.path.exists("analysis_reports"):
            os.makedirs("analysis_reports")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"analysis_reports/file_analysis_{timestamp}.json"
        
        report = {
            'analyzed_file': filepath,
            'analysis_date': datetime.now().isoformat(),
            'results': analysis
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"{Colors.GREEN}✅ Отчет сохранен: {filename}{Colors.END}")

if __name__ == "__main__":
    suite = SteganoCryptoSuite()
    suite.run()
