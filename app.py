# -*- coding: utf-8 -*-
"""Web dashboard for the Auto-Income Agent.

Serves the generated landing page and provides a UI to trigger the
scanner and the AI web-builder.  Does not modify the existing core/
or modules/ scripts — it reuses the same Groq prompt directly.
"""
import os
import subprocess

from flask import Flask, send_from_directory, request, jsonify

app = Flask(__name__)

OUTPUT_DIR = "output_site"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "index.html")

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Auto-Income Agent — Dashboard</title>
<style>
  :root { --bg:#0f172a; --card:#1e293b; --accent:#6366f1; --text:#e2e8f0; --muted:#94a3b8; --ok:#22c55e; --err:#ef4444; }
  * { box-sizing:border-box; margin:0; padding:0; }
  body { font-family:system-ui,-apple-system,sans-serif; background:var(--bg); color:var(--text); min-height:100vh; display:flex; align-items:center; justify-content:center; padding:2rem; }
  .container { max-width:640px; width:100%; }
  .card { background:var(--card); border-radius:16px; padding:2.5rem; box-shadow:0 8px 32px rgba(0,0,0,.3); }
  h1 { font-size:1.75rem; margin-bottom:.5rem; }
  .subtitle { color:var(--muted); margin-bottom:2rem; line-height:1.5; }
  .status { display:flex; align-items:center; gap:.5rem; margin-bottom:1.5rem; font-size:.95rem; }
  .dot { width:10px; height:10px; border-radius:50%; }
  .dot.ok { background:var(--ok); } .dot.err { background:var(--err); }
  label { display:block; font-size:.85rem; color:var(--muted); margin-bottom:.4rem; }
  input[type=text] { width:100%; padding:.75rem 1rem; border-radius:8px; border:1px solid #334155; background:#0f172a; color:var(--text); font-size:1rem; margin-bottom:1rem; }
  button { width:100%; padding:.85rem 1.5rem; border-radius:8px; border:none; font-size:1rem; font-weight:600; cursor:pointer; transition:opacity .2s; }
  button:disabled { opacity:.5; cursor:not-allowed; }
  .btn-primary { background:var(--accent); color:#fff; margin-bottom:.75rem; }
  .btn-secondary { background:#334155; color:var(--text); }
  .btn-view { background:var(--ok); color:#fff; text-decoration:none; display:block; text-align:center; margin-top:1rem; }
  #result { margin-top:1.5rem; padding:1rem; border-radius:8px; font-size:.9rem; display:none; }
  #result.ok { background:rgba(34,197,94,.1); color:var(--ok); border:1px solid rgba(34,197,94,.3); }
  #result.err { background:rgba(239,68,68,.1); color:var(--err); border:1px solid rgba(239,68,68,.3); }
  .steps { margin-top:1.5rem; font-size:.85rem; color:var(--muted); line-height:1.8; }
  .steps code { background:#0f172a; padding:.15rem .4rem; border-radius:4px; color:var(--accent); }
</style>
</head>
<body>
  <div class="container">
    <div class="card">
      <h1>🤖 Auto-Income Agent</h1>
      <p class="subtitle">Generación automatizada de sitios web con IA (Qwen / LLaMA 3.3 vía Groq).</p>

      <div class="status">
        <span class="dot {{ 'ok' if groq_configured else 'err' }}"></span>
        Groq API: {{ 'configurada ✓' if groq_configured else 'NO configurada — añade GROQ_API_KEY' }}
      </div>

      <div class="status">
        <span class="dot {{ 'ok' if site_exists else 'err' }}"></span>
        Sitio generado: {{ 'sí — <a href="/site" style="color:var(--accent)">ver sitio</a>'|safe if site_exists else 'no todavía' }}
      </div>

      <label for="niche">Nicho / tema del sitio a generar</label>
      <input type="text" id="niche" placeholder="Ej: Accesorios ecológicos para mascotas" value="Accesorios ecológicos para mascotas">

      <button class="btn-primary" id="generate-btn" onclick="generate()">🏗️ Generar Landing Page con IA</button>
      <button class="btn-secondary" id="scan-btn" onclick="runScan()">🔎 Escanear oportunidades</button>

      <div id="result"></div>

      <div class="steps">
        <strong>Cómo funciona:</strong><br>
        1. El <strong>Scanner</strong> busca nichos rentables.<br>
        2. Introduces un nicho y pulsas <strong>Generar</strong>.<br>
        3. La IA (Groq) crea una landing page completa en <code>output_site/index.html</code>.<br>
        4. Pulsa <strong>Ver sitio</strong> para ver el resultado.
      </div>
    </div>
  </div>
<script>
async function generate() {
  const btn = document.getElementById('generate-btn');
  const niche = document.getElementById('niche').value.trim();
  const result = document.getElementById('result');
  btn.disabled = true; btn.textContent = '⏳ Generando…';
  result.style.display = 'none';
  try {
    const res = await fetch('/generate', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({niche}) });
    const data = await res.json();
    if (res.ok) {
      result.className = 'ok'; result.textContent = '✅ ' + data.message;
      result.style.display = 'block';
      setTimeout(() => location.reload(), 1500);
    } else {
      result.className = 'err'; result.textContent = '❌ ' + data.error;
      result.style.display = 'block';
    }
  } catch(e) { result.className = 'err'; result.textContent = '❌ Error de conexión'; result.style.display = 'block'; }
  finally { btn.disabled = false; btn.textContent = '🏗️ Generar Landing Page con IA'; }
}
async function runScan() {
  const btn = document.getElementById('scan-btn');
  const result = document.getElementById('result');
  btn.disabled = true; btn.textContent = '⏳ Escaneando…';
  result.style.display = 'none';
  try {
    const res = await fetch('/scan');
    const data = await res.json();
    result.className = 'ok'; result.textContent = '🔎 ' + data.output;
    result.style.display = 'block';
  } catch(e) { result.className = 'err'; result.textContent = '❌ Error'; result.style.display = 'block'; }
  finally { btn.disabled = false; btn.textContent = '🔎 Escanear oportunidades'; }
}
</script>
</body>
</html>"""


@app.route("/")
def dashboard():
    groq_configured = bool(os.environ.get("GROQ_API_KEY"))
    site_exists = os.path.exists(OUTPUT_FILE)
    from flask import render_template_string
    return render_template_string(DASHBOARD_HTML, groq_configured=groq_configured, site_exists=site_exists)


@app.route("/health")
def health():
    return "ok", 200


@app.route("/site")
def serve_site():
    if os.path.exists(OUTPUT_FILE):
        return send_from_directory(OUTPUT_DIR, "index.html")
    return "No site generated yet. Use the dashboard to generate one.", 404


@app.route("/scan")
def scan():
    """Run the scanner script and capture its output."""
    try:
        result = subprocess.run(
            ["python", "core/scanner.py"],
            capture_output=True, text=True, timeout=30,
        )
        output = result.stdout.strip() or result.stderr.strip() or "Scan complete"
        return jsonify({"output": output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/generate", methods=["POST"])
def generate():
    """Generate a landing page using Groq (same prompt as modules/web_builder.py)."""
    from groq import Groq

    niche = request.json.get("niche", "Sitio Web Genérico")
    groq_key = os.environ.get("GROQ_API_KEY")

    if not groq_key:
        return jsonify({"error": "GROQ_API_KEY no configurada. Añádela en los secrets."}), 500

    try:
        client = Groq(api_key=groq_key)
        prompt = f"""
        Actúa como un desarrollador web experto. Crea una Landing Page completa en un ÚNICO archivo HTML
        (con CSS moderno incrustado en <style> y JS básico en <script>) para el siguiente nicho: {niche}.

        Requisitos:
        - Diseño limpio, moderno y responsive (móvil y escritorio).
        - Secciones: Header atractivo, Beneficios, Características, Testimonios falsos (placeholder), Footer.
        - Incluye un botón de llamada a la acción (CTA) claro.
        - NO uses enlaces externos a CSS o JS, todo debe estar inline.
        - El código debe ser SOLO HTML, sin explicaciones de texto antes o después.
        - Optimizado para SEO básico.
        """
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=4096,
        )
        html_content = completion.choices[0].message.content
        html_content = html_content.replace("```html", "").replace("```", "")

        os.makedirs(OUTPUT_DIR, exist_ok=True)
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(html_content)

        return jsonify({"message": f"Sitio generado para '{niche}' en output_site/index.html"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
