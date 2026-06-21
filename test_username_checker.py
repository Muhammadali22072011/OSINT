#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тесты для username_checker.

Покрывают логику без обращения к сети:
  - валидация имени пользователя
  - классификация ответа платформы (classify_response)
  - корректность шаблонов URL

Запуск:  python -m pytest test_username_checker.py -v
   или:  python test_username_checker.py
"""

from username_checker import (
    PLATFORMS,
    UsernameChecker,
    classify_response,
    is_valid_username,
)


GITHUB = PLATFORMS["GitHub"]


# --- Валидация username --------------------------------------------------

def test_valid_usernames():
    for name in ["torvalds", "user_name", "a", "John.Doe-99", "x" * 40]:
        assert is_valid_username(name), name


def test_invalid_usernames():
    for name in ["", "with space", "пробел", "has/slash", "a@b", "x" * 41]:
        assert not is_valid_username(name), name


# --- classify_response: not found ----------------------------------------

def test_404_is_not_found():
    assert classify_response(404, "", GITHUB) == "not_found"


def test_200_with_absence_marker_is_not_found():
    body = "<html><title>Page not found</title></html>"
    assert classify_response(200, body, GITHUB) == "not_found"


def test_absence_marker_is_case_insensitive():
    body = "this PAGE NOT FOUND on github"
    assert classify_response(200, body, GITHUB) == "not_found"


# --- classify_response: found --------------------------------------------

def test_200_without_absence_marker_is_found():
    body = "<html><title>torvalds (Linus Torvalds)</title></html>"
    assert classify_response(200, body, GITHUB) == "found"


# --- classify_response: unknown ------------------------------------------

def test_403_is_unknown():
    assert classify_response(403, "", GITHUB) == "unknown"


def test_429_rate_limit_is_unknown():
    assert classify_response(429, "", GITHUB) == "unknown"


def test_redirect_is_unknown():
    assert classify_response(302, "", GITHUB) == "unknown"


def test_500_is_unknown():
    assert classify_response(500, "", GITHUB) == "unknown"


# --- Конфигурация платформ -----------------------------------------------

def test_all_platforms_have_required_fields():
    for name, cfg in PLATFORMS.items():
        assert "url" in cfg, name
        assert "{}" in cfg["url"], name
        assert isinstance(cfg.get("absence", []), list), name
        assert isinstance(cfg.get("not_found", set()), set), name


def test_url_template_formats_correctly():
    url = PLATFORMS["GitHub"]["url"].format("octocat")
    assert url == "https://github.com/octocat"


# --- check() отвергает мусорный ввод без сети ----------------------------

def test_check_rejects_invalid_username():
    checker = UsernameChecker()
    try:
        checker.check("bad name with spaces")
    except ValueError:
        return
    raise AssertionError("ожидалась ValueError для недопустимого username")


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
