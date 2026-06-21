#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔎 Реальный поиск имени пользователя по публичным платформам
Настоящие HTTP-запросы (без симуляции) для проверки существования аккаунта.

В отличие от social_analyzer.analyze_username (который использует random.choice
и time.sleep вместо реальных запросов), этот модуль действительно обращается
к платформам и определяет наличие профиля по HTTP-статусу и сигнатурам страниц.

⚠️ ВАЖНО: Использовать только для проверки собственного цифрового следа,
в образовательных целях и в рамках разрешённого OSINT-исследования.
"""

import concurrent.futures
import re
from datetime import datetime
from typing import Dict, List, Optional

import requests


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


# Допустимый формат большинства платформ: буквы, цифры, точка, дефис,
# подчёркивание. Длина 1..40 — сознательно мягкая, чтобы не отсекать ники.
USERNAME_RE = re.compile(r'^[A-Za-z0-9._-]{1,40}$')


# Описание платформ. Для каждой:
#   url           — шаблон URL профиля ({} -> username)
#   absence       — сигнатуры в теле ответа, означающие "профиль не найден"
#                   (проверяются, когда статус 200, т.к. часть сайтов отдаёт
#                   200 даже для несуществующих страниц)
#   not_found     — набор HTTP-статусов, однозначно означающих отсутствие
PLATFORMS: Dict[str, Dict] = {
    "GitHub": {
        "url": "https://github.com/{}",
        "absence": ["Not Found", "page not found"],
        "not_found": {404},
    },
    "Reddit": {
        "url": "https://www.reddit.com/user/{}/about.json",
        "absence": ['"error": 404', "nobody on Reddit goes by that name"],
        "not_found": {404},
    },
    "Telegram": {
        "url": "https://t.me/{}",
        "absence": ["If you have <strong>Telegram</strong>, you can contact"],
        "not_found": {404},
    },
    "TikTok": {
        "url": "https://www.tiktok.com/@{}",
        "absence": ["Couldn't find this account", "page not available"],
        "not_found": {404},
    },
    "GitLab": {
        "url": "https://gitlab.com/{}",
        "absence": ["The page could not be found", "404"],
        "not_found": {404},
    },
    "Pinterest": {
        "url": "https://www.pinterest.com/{}/",
        "absence": ["Sorry! We couldn", "User not found"],
        "not_found": {404},
    },
    "Steam": {
        "url": "https://steamcommunity.com/id/{}",
        "absence": ["The specified profile could not be found"],
        "not_found": {404},
    },
    "Twitch": {
        "url": "https://m.twitch.tv/{}",
        "absence": ["Sorry. Unless you", "content is unavailable"],
        "not_found": {404},
    },
    "Replit": {
        "url": "https://replit.com/@{}",
        "absence": ["404", "not found"],
        "not_found": {404},
    },
    "Dev.to": {
        "url": "https://dev.to/{}",
        "absence": ["This page could not be found"],
        "not_found": {404},
    },
}


DEFAULT_HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/120.0 Safari/537.36'
    ),
    'Accept-Language': 'en-US,en;q=0.9',
}


def is_valid_username(username: str) -> bool:
    """Проверка допустимости имени пользователя."""
    return bool(username) and bool(USERNAME_RE.match(username))


def classify_response(status_code: int, body: str, platform: Dict) -> str:
    """
    Классифицировать ответ платформы.

    Возвращает один из статусов:
      "found"     — профиль существует
      "not_found" — профиль отсутствует
      "unknown"   — невозможно определить (блокировка, капча, иной код)

    Логика вынесена в отдельную функцию, чтобы её можно было покрыть тестами
    без реальной сети.
    """
    if status_code in platform.get("not_found", set()):
        return "not_found"

    if status_code in (403, 429):
        # Платформа отдала блокировку/лимит — однозначно судить нельзя.
        return "unknown"

    if 200 <= status_code < 300:
        lowered = body.lower()
        for marker in platform.get("absence", []):
            if marker.lower() in lowered:
                return "not_found"
        return "found"

    if 300 <= status_code < 400:
        # Редирект (например, на страницу логина) — неоднозначно.
        return "unknown"

    return "unknown"


class UsernameChecker:
    """Реальная проверка username по набору публичных платформ."""

    def __init__(self, timeout: float = 10.0, max_workers: int = 10):
        self.timeout = timeout
        self.max_workers = max_workers
        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)

    def _check_one(self, name: str, platform: Dict, username: str) -> Dict:
        """Проверить один сайт. Сетевые ошибки не пробрасываются наружу."""
        url = platform["url"].format(username)
        result = {"platform": name, "url": url, "status": "unknown",
                  "http_code": None, "error": None}
        try:
            resp = self.session.get(
                url, timeout=self.timeout, allow_redirects=True
            )
            result["http_code"] = resp.status_code
            # Берём ограниченный фрагмент тела — этого достаточно для сигнатур
            # и экономит память на больших страницах.
            body = resp.text[:20000] if resp.text else ""
            result["status"] = classify_response(resp.status_code, body, platform)
        except requests.exceptions.Timeout:
            result["error"] = "timeout"
        except requests.exceptions.RequestException as exc:
            result["error"] = type(exc).__name__
        return result

    def check(self, username: str) -> List[Dict]:
        """
        Проверить username на всех платформах параллельно.
        Возвращает список результатов по каждой платформе.
        """
        if not is_valid_username(username):
            raise ValueError(
                f"Недопустимое имя пользователя: {username!r}. "
                "Разрешены буквы, цифры, '.', '_', '-' (1..40 символов)."
            )

        results: List[Dict] = []
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.max_workers
        ) as executor:
            futures = {
                executor.submit(self._check_one, name, platform, username): name
                for name, platform in PLATFORMS.items()
            }
            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())

        results.sort(key=lambda r: r["platform"].lower())
        return results

    def check_and_print(self, username: str) -> List[Dict]:
        """Проверить и красиво вывести результаты в терминал."""
        print(f"\n{Colors.YELLOW}🔎 Реальная проверка username: "
              f"{Colors.BOLD}{username}{Colors.END}")
        print(f"{Colors.CYAN}{'━' * 60}{Colors.END}")

        try:
            results = self.check(username)
        except ValueError as exc:
            print(f"{Colors.RED}❌ {exc}{Colors.END}")
            return []

        found = [r for r in results if r["status"] == "found"]

        for r in results:
            if r["status"] == "found":
                mark = f"{Colors.GREEN}✅ НАЙДЕН{Colors.END}"
            elif r["status"] == "not_found":
                mark = f"{Colors.RED}— нет{Colors.END}"
            else:
                detail = r["error"] or f"HTTP {r['http_code']}"
                mark = f"{Colors.YELLOW}? неясно ({detail}){Colors.END}"
            print(f"  {r['platform']:<12} {mark}")
            if r["status"] == "found":
                print(f"               {Colors.BLUE}{r['url']}{Colors.END}")

        print(f"{Colors.CYAN}{'━' * 60}{Colors.END}")
        print(f"{Colors.BOLD}Итог: найдено {len(found)} из "
              f"{len(results)} платформ{Colors.END}")
        print(f"{Colors.WHITE}Проверено: "
              f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}")
        return results


def main(argv: Optional[List[str]] = None) -> int:
    """Точка входа для запуска из командной строки."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Реальная проверка username по публичным платформам"
    )
    parser.add_argument("username", help="Имя пользователя для проверки")
    parser.add_argument("--timeout", type=float, default=10.0,
                        help="Таймаут запроса в секундах (по умолчанию 10)")
    parser.add_argument("--workers", type=int, default=10,
                        help="Число параллельных потоков (по умолчанию 10)")
    args = parser.parse_args(argv)

    checker = UsernameChecker(timeout=args.timeout, max_workers=args.workers)
    results = checker.check_and_print(args.username)
    return 0 if results else 1


if __name__ == "__main__":
    raise SystemExit(main())
