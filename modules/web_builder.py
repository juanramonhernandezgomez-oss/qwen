# -*- coding: utf-8 -*-
import os
import json
from groq import Groq
from github import Github, Auth

def main():
    print("🏗️ Iniciando generador de código...")
    
    # Obtener variables de entorno
    groq_api_key = os.environ.get("GROQ_API_KEY")
    github_token = os.environ.get("GITHUB_TOKEN")
    issue_number = os.environ.get("ISSUE_NUMBER")
    repo_name = os.environ.get("GITHUB_REPOSITORY")
    
    if not all([groq_api_key, github_token, issue_number, repo_name]):
        print("❌ Faltan variables de entorno críticas.")
        return

    try:
        # 1. Conectar con GitHub y obtener el Issue aprobado
        auth = Auth.Token(github_token)
        gh = Github(auth=auth)
        repo = gh.get_repo(repo_name)
        issue = repo.get_issue(number=int(issue_number))
        
        # Verificar si el comentario de aprobación existe (seguridad extra)
        comments = issue.get_comments()
        approved = False
        niche_topic = "Sitio Web Genérico"
        
        for comment in comments:
            if "/approve" in comment.body.lower():
                approved = True
                # Intentar extraer el tema del cuerpo del issue
                if "Nicho:" in issue.body:
                    niche_topic = issue.body.split("Nicho:")[1].split("\n")[0].strip()
                break
        
        if not approved:
            print("⚠️ El issue no tiene la aprobación '/approve'. Cancelando.")
            return

        print(f"✅ Aprobación detectada. Generando web para: {niche_topic}")

        # 2. Llamar a Groq (Llama 3.3) para generar el HTML
        client = Groq(api_key=groq_api_key)
        
        prompt = f"""
        Actúa como un desarrollador web experto. Crea una Landing Page completa en un ÚNICO archivo HTML 
        (con CSS moderno incrustado en <style> y JS básico en <script>) para el siguiente nicho: {niche_topic}.
        
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
            max_tokens=4096
        )
        
        html_content = completion.choices[0].message.content
        
        # Limpiar posibles marcas de markdown si la IA las añade
        html_content = html_content.replace("```html", "").replace("```", "")

        # 3. Guardar el archivo localmente en la carpeta output_site
        output_dir = "output_site"
        os.makedirs(output_dir, exist_ok=True)
        
        file_path = os.path.join(output_dir, "index.html")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)
            
        print(f"✅ Archivo generado en {file_path}")
        
        # 4. Comentar en el Issue que la web está lista
        issue.create_comment(f"✅ **Web generada con éxito!**\n\nEl código ha sido creado y está listo para deploy. Revisa la carpeta `output_site`.")

    except Exception as e:
        print(f"❌ Error crítico: {str(e)}")
        # Opcional: Crear un issue de error o comentar en el actual
        raise e

if __name__ == "__main__":
    main()
