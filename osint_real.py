#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛰️  osint_real — РЕАЛЬНОЕ ядро OSINT-функций (без симуляции)

Каждая функция здесь либо выполняет настоящий сетевой/вычислительный запрос,
либо честно сообщает, что для работы нужен API-ключ. Здесь НЕТ random.choice
и НЕТ выдуманных данных, выдаваемых за настоящие.

Бесплатно и без ключей:
    dns_records, reverse_dns, whois_info, ip_geolocation, ssl_info,
    http_headers, email_validate, http_status

Требуют ключ (берётся из config.py или переменной окружения):
    hibp_breaches   -> HIBP_API_KEY
    shodan_host     -> SHODAN_API_KEY

⚠️ Только для образовательных целей, своих систем и разрешённого OSINT.
"""

from __future__ import annotations

import os
import re
import socket
import ssl
from datetime import datetime
from typing import Dict, List, Optional

import requests

# Конфиг не обязателен: при отсутствии файла используем пустые значения.
try:
    import config as _cfg
except Exception:  # noqa: BLE001
    _cfg = None

DEFAULT_TIMEOUT = 10.0
_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
       "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

EMAIL_RE = re.compile(r'^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$')


def _get_key(name: str) -> str:
    """Ключ из переменной окружения (приоритет) или из config.py."""
    val = os.environ.get(name)
    if val:
        return val.strip()
    if _cfg is not None:
        return str(getattr(_cfg, name, "") or "").strip()
    return ""


# ---------------------------------------------------------------------------
# DNS
# ---------------------------------------------------------------------------

def dns_records(domain: str,
                types=("A", "AAAA", "MX", "NS", "TXT", "CNAME")) -> Dict:
    """Реальные DNS-записи домена. Требует dnspython."""
    out: Dict[str, object] = {"domain": domain, "records": {}, "error": None}
    try:
        import dns.resolver
    except ImportError:
        out["error"] = "dnspython не установлен (pip install dnspython)"
        return out

    resolver = dns.resolver.Resolver()
    resolver.lifetime = DEFAULT_TIMEOUT
    for rtype in types:
        try:
            answers = resolver.resolve(domain, rtype)
            out["records"][rtype] = [r.to_text() for r in answers]
        except Exception:  # NXDOMAIN/NoAnswer/Timeout — запись просто отсутствует
            out["records"][rtype] = []
    if not any(out["records"].values()):
        out["error"] = "нет записей или домен не существует"
    return out


def reverse_dns(ip: str) -> Dict:
    """Обратный DNS (PTR): IP -> имя хоста."""
    out = {"ip": ip, "hostname": None, "error": None}
    try:
        out["hostname"] = socket.gethostbyaddr(ip)[0]
    except Exception as exc:  # noqa: BLE001
        out["error"] = f"{type(exc).__name__}: {exc}"
    return out


# ---------------------------------------------------------------------------
# WHOIS
# ---------------------------------------------------------------------------

def whois_info(domain: str) -> Dict:
    """Реальный WHOIS-запрос. Требует python-whois (порт 43 наружу)."""
    out: Dict[str, object] = {"domain": domain, "error": None}
    try:
        import whois
    except ImportError:
        out["error"] = "python-whois не установлен (pip install python-whois)"
        return out
    try:
        w = whois.whois(domain)
    except Exception as exc:  # noqa: BLE001
        out["error"] = f"{type(exc).__name__}: {exc}"
        return out

    def _first(v):
        return v[0] if isinstance(v, (list, tuple)) and v else v

    def _str(v):
        v = _first(v)
        return v.isoformat() if isinstance(v, datetime) else (str(v) if v else None)

    out.update({
        "registrar": _str(w.registrar),
        "creation_date": _str(w.creation_date),
        "expiration_date": _str(w.expiration_date),
        "updated_date": _str(w.updated_date),
        "name_servers": sorted({str(n).lower() for n in (w.name_servers or [])}),
        "emails": sorted({str(e).lower() for e in
                          (w.emails if isinstance(w.emails, (list, tuple))
                           else [w.emails] if w.emails else [])}),
        "country": _str(w.country),
        "org": _str(getattr(w, "org", None)),
    })
    return out


# ---------------------------------------------------------------------------
# IP-геолокация (несколько бесплатных провайдеров, без ключа)
# ---------------------------------------------------------------------------

def ip_geolocation(ip: str, timeout: float = DEFAULT_TIMEOUT) -> Dict:
    """
    Реальная геолокация IP через бесплатные провайдеры (по очереди, до успеха):
    ip-api.com -> ipwho.is -> ipinfo.io. Ключ не требуется.
    """
    out: Dict[str, object] = {"ip": ip, "source": None, "error": None}
    headers = {"User-Agent": _UA}

    # 1) ip-api.com
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}",
                         params={"fields": "status,message,country,regionName,"
                                 "city,lat,lon,isp,org,as,query"},
                         timeout=timeout, headers=headers)
        d = r.json()
        if d.get("status") == "success":
            out.update({"source": "ip-api.com", "country": d.get("country"),
                        "region": d.get("regionName"), "city": d.get("city"),
                        "lat": d.get("lat"), "lon": d.get("lon"),
                        "isp": d.get("isp"), "org": d.get("org"),
                        "asn": d.get("as")})
            return out
    except Exception:  # noqa: BLE001
        pass

    # 2) ipwho.is
    try:
        r = requests.get(f"https://ipwho.is/{ip}", timeout=timeout, headers=headers)
        d = r.json()
        if d.get("success"):
            conn = d.get("connection", {}) or {}
            out.update({"source": "ipwho.is", "country": d.get("country"),
                        "region": d.get("region"), "city": d.get("city"),
                        "lat": d.get("latitude"), "lon": d.get("longitude"),
                        "isp": conn.get("isp"), "org": conn.get("org"),
                        "asn": f"AS{conn.get('asn')}" if conn.get("asn") else None})
            return out
    except Exception:  # noqa: BLE001
        pass

    # 3) ipinfo.io (ключ опционален, повышает лимит)
    try:
        params = {}
        key = _get_key("IPINFO_API_KEY")
        if key:
            params["token"] = key
        r = requests.get(f"https://ipinfo.io/{ip}/json", params=params,
                         timeout=timeout, headers=headers)
        d = r.json()
        if d.get("ip"):
            loc = (d.get("loc") or ",").split(",")
            out.update({"source": "ipinfo.io", "country": d.get("country"),
                        "region": d.get("region"), "city": d.get("city"),
                        "lat": loc[0] or None, "lon": loc[1] if len(loc) > 1 else None,
                        "isp": d.get("org"), "org": d.get("org"), "asn": None})
            return out
    except Exception:  # noqa: BLE001
        pass

    out["error"] = "все бесплатные провайдеры недоступны"
    return out


# ---------------------------------------------------------------------------
# SSL / TLS
# ---------------------------------------------------------------------------

def ssl_info(host: str, port: int = 443, timeout: float = DEFAULT_TIMEOUT) -> Dict:
    """Реальные данные TLS-сертификата хоста."""
    out: Dict[str, object] = {"host": host, "port": port, "error": None}
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((host, port), timeout=timeout) as sock:
            with ctx.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()
                out["tls_version"] = ssock.version()
        subject = dict(x[0] for x in cert.get("subject", []))
        issuer = dict(x[0] for x in cert.get("issuer", []))
        out.update({
            "subject_cn": subject.get("commonName"),
            "issuer_org": issuer.get("organizationName"),
            "issuer_cn": issuer.get("commonName"),
            "not_before": cert.get("notBefore"),
            "not_after": cert.get("notAfter"),
            "san": [v for k, v in cert.get("subjectAltName", []) if k == "DNS"],
        })
    except Exception as exc:  # noqa: BLE001
        out["error"] = f"{type(exc).__name__}: {exc}"
    return out


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------

def http_headers(url: str, timeout: float = DEFAULT_TIMEOUT) -> Dict:
    """Реальные HTTP-заголовки + наивное определение технологий."""
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    out: Dict[str, object] = {"url": url, "error": None}
    try:
        r = requests.get(url, timeout=timeout, headers={"User-Agent": _UA},
                         allow_redirects=True)
        out["status_code"] = r.status_code
        out["final_url"] = r.url
        out["headers"] = dict(r.headers)
        tech = []
        h = {k.lower(): v for k, v in r.headers.items()}
        if "server" in h:
            tech.append(f"Server: {h['server']}")
        if "x-powered-by" in h:
            tech.append(f"X-Powered-By: {h['x-powered-by']}")
        if "cf-ray" in h or "cloudflare" in h.get("server", "").lower():
            tech.append("Cloudflare")
        out["technologies"] = tech
    except Exception as exc:  # noqa: BLE001
        out["error"] = f"{type(exc).__name__}: {exc}"
    return out


def http_status(url: str, timeout: float = DEFAULT_TIMEOUT) -> Dict:
    """Только код ответа и редиректы (лёгкая проверка доступности)."""
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    out: Dict[str, object] = {"url": url, "error": None}
    try:
        r = requests.head(url, timeout=timeout, headers={"User-Agent": _UA},
                         allow_redirects=True)
        out["status_code"] = r.status_code
        out["final_url"] = r.url
    except Exception as exc:  # noqa: BLE001
        out["error"] = f"{type(exc).__name__}: {exc}"
    return out


# ---------------------------------------------------------------------------
# Email
# ---------------------------------------------------------------------------

def email_validate(email: str, timeout: float = DEFAULT_TIMEOUT) -> Dict:
    """
    Валидация email: формат (offline) + реальная проверка MX-записей домена
    (домен действительно может принимать почту). SMTP-проба НЕ выполняется.
    """
    out: Dict[str, object] = {"email": email, "valid_format": False,
                              "domain": None, "has_mx": False, "mx": [],
                              "error": None}
    if not EMAIL_RE.match(email or ""):
        out["error"] = "неверный формат email"
        return out
    out["valid_format"] = True
    domain = email.split("@", 1)[1]
    out["domain"] = domain
    try:
        import dns.resolver
        answers = dns.resolver.resolve(domain, "MX", lifetime=timeout)
        out["mx"] = sorted(str(r.exchange).rstrip(".") for r in answers)
        out["has_mx"] = bool(out["mx"])
    except ImportError:
        out["error"] = "dnspython не установлен — MX не проверен"
    except Exception:  # noqa: BLE001
        out["has_mx"] = False
    return out


# ---------------------------------------------------------------------------
# HaveIBeenPwned (требует ключ)
# ---------------------------------------------------------------------------

def hibp_breaches(email: str, timeout: float = DEFAULT_TIMEOUT) -> Dict:
    """
    РЕАЛЬНАЯ проверка утечек через HaveIBeenPwned API v3.
    Требует ключ HIBP_API_KEY (config.py или переменная окружения).
    Без ключа честно возвращает needs_key=True, НЕ выдумывая результат.
    """
    out: Dict[str, object] = {"email": email, "needs_key": False,
                              "breached": None, "breaches": [], "error": None}
    if not EMAIL_RE.match(email or ""):
        out["error"] = "неверный формат email"
        return out
    key = _get_key("HIBP_API_KEY")
    if not key:
        out["needs_key"] = True
        out["error"] = ("нужен ключ HIBP_API_KEY — получить на "
                        "https://haveibeenpwned.com/API/Key")
        return out
    try:
        r = requests.get(
            f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}",
            params={"truncateResponse": "false"},
            headers={"hibp-api-key": key, "User-Agent": "OSINT-Toolkit"},
            timeout=timeout)
        if r.status_code == 404:
            out["breached"] = False  # утечек не найдено — это валидный ответ
        elif r.status_code == 200:
            out["breached"] = True
            out["breaches"] = [
                {"name": b.get("Name"), "domain": b.get("Domain"),
                 "date": b.get("BreachDate"),
                 "data": b.get("DataClasses", [])}
                for b in r.json()]
        elif r.status_code == 401:
            out["error"] = "ключ HIBP недействителен (401)"
        elif r.status_code == 429:
            out["error"] = "превышен лимит запросов HIBP (429)"
        else:
            out["error"] = f"HIBP вернул статус {r.status_code}"
    except Exception as exc:  # noqa: BLE001
        out["error"] = f"{type(exc).__name__}: {exc}"
    return out


# ---------------------------------------------------------------------------
# Shodan (требует ключ)
# ---------------------------------------------------------------------------

def shodan_host(ip: str, timeout: float = DEFAULT_TIMEOUT) -> Dict:
    """РЕАЛЬНЫЙ запрос к Shodan по IP. Требует SHODAN_API_KEY."""
    out: Dict[str, object] = {"ip": ip, "needs_key": False, "error": None}
    key = _get_key("SHODAN_API_KEY")
    if not key:
        out["needs_key"] = True
        out["error"] = "нужен ключ SHODAN_API_KEY — получить на https://shodan.io"
        return out
    try:
        r = requests.get(f"https://api.shodan.io/shodan/host/{ip}",
                         params={"key": key}, timeout=timeout)
        if r.status_code == 200:
            d = r.json()
            out.update({"org": d.get("org"), "os": d.get("os"),
                        "country": d.get("country_name"),
                        "ports": d.get("ports", []),
                        "hostnames": d.get("hostnames", [])})
        elif r.status_code == 401:
            out["error"] = "ключ Shodan недействителен (401)"
        elif r.status_code == 404:
            out["error"] = "по этому IP нет данных в Shodan (404)"
        else:
            out["error"] = f"Shodan вернул статус {r.status_code}"
    except Exception as exc:  # noqa: BLE001
        out["error"] = f"{type(exc).__name__}: {exc}"
    return out


# Карта возможностей: что бесплатно, что требует ключ.
CAPABILITIES = {
    "dns_records":    {"real": True,  "needs_key": None},
    "reverse_dns":    {"real": True,  "needs_key": None},
    "whois_info":     {"real": True,  "needs_key": None},
    "ip_geolocation": {"real": True,  "needs_key": None},
    "ssl_info":       {"real": True,  "needs_key": None},
    "http_headers":   {"real": True,  "needs_key": None},
    "http_status":    {"real": True,  "needs_key": None},
    "email_validate": {"real": True,  "needs_key": None},
    "hibp_breaches":  {"real": True,  "needs_key": "HIBP_API_KEY"},
    "shodan_host":    {"real": True,  "needs_key": "SHODAN_API_KEY"},
}


if __name__ == "__main__":
    import json
    import sys
    if len(sys.argv) < 3:
        print("Использование: python osint_real.py <функция> <аргумент>")
        print("Функции:", ", ".join(CAPABILITIES))
        sys.exit(1)
    func = globals().get(sys.argv[1])
    if not callable(func):
        print(f"Неизвестная функция: {sys.argv[1]}")
        sys.exit(1)
    print(json.dumps(func(sys.argv[2]), ensure_ascii=False, indent=2))
