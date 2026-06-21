#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌐 Веб-версия OSINT Toolkit

Лёгкий Flask-интерфейс поверх РЕАЛЬНО работающих, защитных модулей проекта:
  • Username Checker  — настоящие HTTP-проверки наличия аккаунта (username_checker.py)
  • Криптоанализ      — брутфорс Цезаря и декодирование форматов (steganography_crypto.py)
  • Стеганография     — скрытие/извлечение текста в тексте (steganography_crypto.py)

Сознательно НЕ выносятся в веб симулированные / наступательные модули
(генератор фишинга, "поиск людей", сетевое сканирование чужих хостов).

⚠️ Только для образовательных целей и проверки собственного цифрового следа.

Запуск:  python webapp.py            # http://127.0.0.1:5000
         PORT=8080 python webapp.py
"""

import io
import os
from contextlib import redirect_stdout

from flask import Flask, jsonify, render_template_string, request

from username_checker import UsernameChecker
from steganography_crypto import CryptoAnalyzer, SteganographyEngine

app = Flask(__name__)

_checker = UsernameChecker(timeout=8.0)
_crypto = CryptoAnalyzer()
_stego = SteganographyEngine()

STEGO_METHODS = ("whitespace", "unicode", "invisible", "simple")


def _quiet(func, *args, **kwargs):
    """Вызвать функцию, подавив её цветной вывод в stdout сервера."""
    with redirect_stdout(io.StringIO()):
        return func(*args, **kwargs)


PAGE = r"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>OSINT Toolkit — Web</title>
<style>
  :root { --bg:#0d1117; --card:#161b22; --br:#30363d; --fg:#c9d1d9;
          --accent:#58a6ff; --green:#3fb950; --red:#f85149; --yellow:#d29922; }
  * { box-sizing: border-box; }
  body { margin:0; background:var(--bg); color:var(--fg);
         font-family: ui-monospace, "Cascadia Code", Menlo, Consolas, monospace; }
  header { padding:24px 16px; text-align:center; border-bottom:1px solid var(--br); }
  header h1 { margin:0 0 4px; font-size:22px; }
  header p { margin:0; color:var(--yellow); font-size:12px; }
  .wrap { max-width:860px; margin:0 auto; padding:16px; }
  .tabs { display:flex; gap:8px; flex-wrap:wrap; margin-bottom:16px; }
  .tab { background:var(--card); border:1px solid var(--br); color:var(--fg);
         padding:8px 14px; border-radius:8px; cursor:pointer; font:inherit; }
  .tab.active { border-color:var(--accent); color:var(--accent); }
  .panel { display:none; background:var(--card); border:1px solid var(--br);
           border-radius:12px; padding:16px; }
  .panel.active { display:block; }
  label { display:block; font-size:12px; margin:10px 0 4px; color:#8b949e; }
  input, textarea, select { width:100%; background:var(--bg); color:var(--fg);
         border:1px solid var(--br); border-radius:8px; padding:9px; font:inherit; }
  textarea { min-height:80px; resize:vertical; }
  button.go { margin-top:12px; background:var(--accent); color:#0d1117; border:none;
         padding:10px 16px; border-radius:8px; font:inherit; font-weight:bold; cursor:pointer; }
  button.go:disabled { opacity:.5; cursor:wait; }
  .out { margin-top:14px; white-space:pre-wrap; word-break:break-word; font-size:13px; }
  .row { display:flex; gap:8px; align-items:center; padding:4px 0;
         border-bottom:1px solid #21262d; }
  .row .name { width:120px; color:#8b949e; }
  .found { color:var(--green); } .nf { color:var(--red); } .unk { color:var(--yellow); }
  a { color:var(--accent); }
  .muted { color:#6e7681; font-size:11px; }
  .cand { padding:6px 8px; border:1px solid var(--br); border-radius:6px; margin:6px 0; }
  .cand b { color:var(--green); }
</style>
</head>
<body>
<header>
  <h1>🕵️ OSINT Toolkit — Web</h1>
  <p>⚠️ Только для образовательных целей и проверки собственного цифрового следа</p>
</header>
<div class="wrap">
  <div class="tabs">
    <button class="tab active" data-tab="user">🔎 Username</button>
    <button class="tab" data-tab="caesar">🔓 Цезарь</button>
    <button class="tab" data-tab="decode">🧬 Декодер</button>
    <button class="tab" data-tab="stego">🫥 Стеганография</button>
  </div>

  <!-- USERNAME -->
  <div class="panel active" id="user">
    <label>Имя пользователя</label>
    <input id="u-name" placeholder="например, torvalds" autocomplete="off">
    <button class="go" onclick="checkUser()">Проверить на 10 платформах</button>
    <div class="muted">Реальные HTTP-запросы. «неясно» = сайт заблокировал/ограничил ответ.</div>
    <div class="out" id="u-out"></div>
  </div>

  <!-- CAESAR -->
  <div class="panel" id="caesar">
    <label>Зашифрованный текст (шифр Цезаря)</label>
    <textarea id="c-text" placeholder="Wkh txlfn eurzq ira">Wkh txlfn eurzq ira</textarea>
    <button class="go" onclick="caesar()">Брутфорс (топ-5 вариантов)</button>
    <div class="out" id="c-out"></div>
  </div>

  <!-- DECODE -->
  <div class="panel" id="decode">
    <label>Строка для декодирования</label>
    <textarea id="d-text" placeholder="SGVsbG8gV29ybGQ=">SGVsbG8gV29ybGQ=</textarea>
    <button class="go" onclick="decode()">Декодировать (Base64/Hex/URL/ROT13/Atbash)</button>
    <div class="out" id="d-out"></div>
  </div>

  <!-- STEGO -->
  <div class="panel" id="stego">
    <label>Метод</label>
    <select id="s-method">
      <option value="unicode">unicode (zero-width, надёжный round-trip)</option>
    </select>
    <div class="muted">Носитель должен быть длиннее секрета (≈ символов носителя ≥ длина секрета × 8 + 16).
      Методы whitespace/invisible/simple доступны в CLI, но их декодеры в исходном модуле ненадёжны.</div>
    <label>Текст-носитель</label>
    <textarea id="s-cover">This is a perfectly ordinary and sufficiently long sentence that carries no obvious secret at all.</textarea>
    <label>Секрет (для скрытия)</label>
    <input id="s-secret" value="hi">
    <button class="go" onclick="hide()">Скрыть</button>
    <button class="go" onclick="extract()">Извлечь из «носителя» выше</button>
    <div class="out" id="s-out"></div>
  </div>
</div>

<script>
const $ = id => document.getElementById(id);
document.querySelectorAll('.tab').forEach(t => t.onclick = () => {
  document.querySelectorAll('.tab').forEach(x => x.classList.remove('active'));
  document.querySelectorAll('.panel').forEach(x => x.classList.remove('active'));
  t.classList.add('active'); $(t.dataset.tab).classList.add('active');
});
async function post(url, body) {
  const r = await fetch(url, {method:'POST', headers:{'Content-Type':'application/json'},
                             body: JSON.stringify(body)});
  return r.json();
}
function busy(btn, on){ btn.disabled = on; }

async function checkUser() {
  const btn = event.target, out = $('u-out');
  out.textContent = '⏳ Проверяю платформы...'; busy(btn, true);
  try {
    const d = await post('/api/username', {username: $('u-name').value.trim()});
    if (d.error) { out.textContent = '❌ ' + d.error; return; }
    out.innerHTML = d.results.map(r => {
      let cls = r.status==='found'?'found':(r.status==='not_found'?'nf':'unk');
      let tag = r.status==='found'?'✅ НАЙДЕН':(r.status==='not_found'?'— нет':'? неясно');
      let link = r.status==='found' ? ` <a href="${r.url}" target="_blank" rel="noopener">${r.url}</a>` : '';
      let extra = r.status==='unknown' ? ` <span class="muted">(${r.error||('HTTP '+r.http_code)})</span>` : '';
      return `<div class="row"><span class="name">${r.platform}</span><span class="${cls}">${tag}</span>${extra}${link}</div>`;
    }).join('') + `<div class="muted" style="margin-top:8px">Найдено ${d.found} из ${d.total}</div>`;
  } catch(e){ out.textContent = '❌ ' + e; } finally { busy(btn, false); }
}
async function caesar() {
  const btn = event.target, out = $('c-out'); busy(btn, true); out.textContent='⏳';
  const d = await post('/api/caesar', {text: $('c-text').value});
  out.innerHTML = d.candidates.map(c =>
     `<div class="cand">сдвиг <b>${c.shift}</b> · score ${c.score.toFixed(1)}<br>${c.text}</div>`).join('');
  busy(btn,false);
}
async function decode() {
  const btn = event.target, out = $('d-out'); busy(btn, true); out.textContent='⏳';
  const d = await post('/api/decode', {text: $('d-text').value});
  out.innerHTML = Object.entries(d.results).map(([k,v]) =>
     `<div class="row"><span class="name">${k}</span><span>${v}</span></div>`).join('');
  busy(btn,false);
}
async function hide() {
  const out = $('s-out'); out.textContent='⏳';
  const d = await post('/api/stego/hide',
     {cover:$('s-cover').value, secret:$('s-secret').value, method:$('s-method').value});
  if (d.error){ out.textContent='❌ '+d.error; return; }
  $('s-cover').value = d.stego;
  out.innerHTML = `<div class="found">✅ Секрет встроен (метод ${d.method}). Текст-носитель обновлён выше — нажмите «Извлечь», чтобы проверить.</div>`;
}
async function extract() {
  const out = $('s-out'); out.textContent='⏳';
  const d = await post('/api/stego/extract', {text:$('s-cover').value, method:$('s-method').value});
  if (d.error){ out.textContent='❌ '+d.error; return; }
  out.innerHTML = d.secret ? `<div class="found">🔓 Извлечено: ${d.secret}</div>`
                           : `<div class="nf">Ничего не извлечено (метод/носитель не совпадают).</div>`;
}
</script>
</body>
</html>"""


@app.route("/")
def index():
    return render_template_string(PAGE)


@app.route("/api/username", methods=["POST"])
def api_username():
    username = (request.get_json(silent=True) or {}).get("username", "").strip()
    try:
        results = _checker.check(username)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    found = sum(1 for r in results if r["status"] == "found")
    return jsonify({"results": results, "found": found, "total": len(results)})


@app.route("/api/caesar", methods=["POST"])
def api_caesar():
    text = (request.get_json(silent=True) or {}).get("text", "")
    data = _quiet(_crypto.brute_force_caesar, text)
    candidates = [
        {"shift": shift, "text": info["text"], "score": info["score"]}
        for shift, info in data["best_candidates"]
    ]
    return jsonify({"candidates": candidates})


@app.route("/api/decode", methods=["POST"])
def api_decode():
    text = (request.get_json(silent=True) or {}).get("text", "")
    results = _quiet(_crypto.decode_common_encodings, text)
    return jsonify({"results": results})


@app.route("/api/stego/hide", methods=["POST"])
def api_stego_hide():
    body = request.get_json(silent=True) or {}
    method = body.get("method", "whitespace")
    if method not in STEGO_METHODS:
        return jsonify({"error": f"неизвестный метод: {method}"}), 400
    try:
        stego = _quiet(_stego.hide_text_in_text,
                       body.get("cover", ""), body.get("secret", ""), method)
    except Exception as exc:  # noqa: BLE001
        return jsonify({"error": f"{type(exc).__name__}: {exc}"}), 500
    return jsonify({"stego": stego, "method": method})


@app.route("/api/stego/extract", methods=["POST"])
def api_stego_extract():
    body = request.get_json(silent=True) or {}
    method = body.get("method", "whitespace")
    if method not in STEGO_METHODS:
        return jsonify({"error": f"неизвестный метод: {method}"}), 400
    try:
        secret = _quiet(_stego.extract_text_from_text, body.get("text", ""), method)
    except Exception as exc:  # noqa: BLE001
        return jsonify({"error": f"{type(exc).__name__}: {exc}"}), 500
    return jsonify({"secret": secret or ""})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    print(f"🌐 OSINT Toolkit web → http://127.0.0.1:{port}")
    app.run(host="127.0.0.1", port=port, debug=False)
