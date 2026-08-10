#!/usr/bin/env python3
"""
Web Builder - Genera código completo usando Qwen 2.5 Coder vía Groq API
Crea landing pages funcionales listas para deploy
"""

import os
import json
from groq import Groq

def generate_website_code(niche):
    """
    Genera una web completa para el nicho especificado
    Returns: dict con HTML, CSS, JS
    """
    
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    
    # Prompt optimizado para Qwen 2.5 Coder
    prompt = f"""
Crea una landing page completa y funcional para: "{ niche }"

Requisitos:
1. Debe ser una herramienta web interactiva que los usuarios puedan usar directamente
2. Diseño moderno, responsive y profesional
3. Optimizada para SEO con meta tags apropiados
4. Incluye espacios para Google AdSense (comentados)
5. Incluye espacios para enlaces de afiliado Amazon (comentados)
6. Código limpio en un solo archivo HTML con CSS y JS embebidos

La página debe incluir:
- Header atractivo con título y subtítulo
- La herramienta principal funcional (JavaScript)
- Sección de explicación/beneficios
- Sección FAQ
- Footer con enlaces legales

Proporciona SOLO el código HTML completo, sin explicaciones adicionales.
El código debe ser válido y listo para production.
"""
    
    try:
        response = client.chat.completions.create(
            model="qwen-2.5-coder-32b",
            messages=[
                {"role": "system", "content": "Eres un desarrollador web experto. Generas código HTML/CSS/JS limpio, moderno y funcional."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=8000
        )
        
        html_code = response.choices[0].message.content
        
        # Limpiar el código si tiene markdown wrapping
        if "```html" in html_code:
            html_code = html_code.split("```html")[1].split("```")[0]
        elif "```" in html_code:
            html_code = html_code.split("```")[1].split("```")[0]
        
        return {
            "success": True,
            "html": html_code.strip(),
            "niche": niche
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "niche": niche
        }


def create_project_files(code_result, output_dir="projects"):
    """
    Crea los archivos del proyecto en el directorio especificado
    """
    
    if not code_result["success"]:
        print(f"❌ Error generando código: {code_result.get('error', 'Unknown')}")
        return False
    
    # Crear directorio si no existe
    os.makedirs(output_dir, exist_ok=True)
    
    # Nombre del archivo basado en el nicho
    niche_slug = code_result["niche"].lower().replace(" ", "-").replace("/", "-")[:50]
    filename = f"{niche_slug}.html"
    filepath = os.path.join(output_dir, filename)
    
    # Guardar HTML
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code_result["html"])
    
    # Crear index.html que redirige al proyecto (para GitHub Pages)
    index_path = os.path.join(output_dir, "index.html")
    redirect_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="0; url={filename}">
    <title>Redirecting...</title>
</head>
<body>
    <p>Redirigiendo a la herramienta... <a href="{filename}">Click aquí si no se redirige automáticamente</a></p>
</body>
</html>
"""
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(redirect_html)
    
    print(f"✅ Proyecto creado: {filepath}")
    print(f"✅ Index creado: {index_path}")
    
    return True


if __name__ == "__main__":
    # Obtener nicho desde variable de entorno (seteada por GitHub Actions)
    niche = os.environ.get("NICHE", "Calculadora online")
    
    print(f"🤖 Generando sitio para: { niche }")
    print("⏳ Usando Qwen 2.5 Coder via Groq API...")
    
    # Generar código
    code_result = generate_website_code(niche)
    
    if code_result["success"]:
        print("✅ Código generado exitosamente")
        
        # Crear archivos
        if create_project_files(code_result):
            print("🎉 Proyecto listo para deploy!")
        else:
            print("❌ Error creando archivos")
            exit(1)
    else:
        print(f"❌ Error: {code_result.get('error', 'Unknown error')}")
        exit(1)
