#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тесты для osint_real.

Проверяют логику без зависимости от внешних API:
  - валидацию email (формат)
  - честную обработку отсутствия API-ключей (без выдуманных данных)
  - карту возможностей CAPABILITIES

Запуск:  python -m pytest test_osint_real.py -v
   или:  python test_osint_real.py
"""

import os

import osint_real as o


# --- Формат email --------------------------------------------------------

def test_email_format_rejects_garbage():
    r = o.email_validate("not-an-email")
    assert r["valid_format"] is False
    assert r["error"] == "неверный формат email"


def test_email_format_accepts_valid():
    # Не делаем сетевой MX-запрос — проверяем только разбор формата/домена.
    r = o.email_validate("john.doe+tag@sub.example.com")
    assert r["valid_format"] is True
    assert r["domain"] == "sub.example.com"


# --- Честность при отсутствии ключей -------------------------------------

def test_hibp_without_key_is_honest():
    os.environ.pop("HIBP_API_KEY", None)
    r = o.hibp_breaches("user@example.com")
    assert r["needs_key"] is True
    assert r["breached"] is None          # НЕ выдумывает результат
    assert r["breaches"] == []
    assert "HIBP_API_KEY" in r["error"]


def test_hibp_rejects_bad_email_before_network():
    r = o.hibp_breaches("garbage")
    assert r["error"] == "неверный формат email"


def test_shodan_without_key_is_honest():
    os.environ.pop("SHODAN_API_KEY", None)
    r = o.shodan_host("8.8.8.8")
    assert r["needs_key"] is True
    assert "SHODAN_API_KEY" in r["error"]


# --- Чтение ключей -------------------------------------------------------

def test_env_key_overrides(monkeypatch=None):
    os.environ["HIBP_API_KEY"] = "test-key-123"
    try:
        assert o._get_key("HIBP_API_KEY") == "test-key-123"
    finally:
        os.environ.pop("HIBP_API_KEY", None)


# --- Карта возможностей --------------------------------------------------

def test_capabilities_map_is_consistent():
    for name, meta in o.CAPABILITIES.items():
        assert callable(getattr(o, name)), name
        assert meta["real"] is True, name
        # needs_key либо None, либо имя реально читаемого ключа
        if meta["needs_key"]:
            assert isinstance(meta["needs_key"], str)


def test_free_functions_need_no_key():
    free = ["dns_records", "reverse_dns", "whois_info", "ip_geolocation",
            "ssl_info", "http_headers", "http_status", "email_validate"]
    for name in free:
        assert o.CAPABILITIES[name]["needs_key"] is None, name


if __name__ == "__main__":
    import sys

    failures = 0
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for test in tests:
        try:
            test()
            print(f"  PASS  {test.__name__}")
        except AssertionError as exc:
            failures += 1
            print(f"  FAIL  {test.__name__}: {exc}")
        except Exception as exc:  # noqa: BLE001
            failures += 1
            print(f"  ERROR {test.__name__}: {type(exc).__name__}: {exc}")
    print(f"\n{len(tests) - failures}/{len(tests)} тестов прошло")
    sys.exit(1 if failures else 0)
