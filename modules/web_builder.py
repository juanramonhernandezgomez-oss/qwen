import os
import json
from groq import Groq
from github import Github, Auth

def get_issue_body():
    """Obtiene el cuerpo del issue que disparó el workflow"""
    issue_number = os.environ.get("ISSUE_NUMBER")
    token = os.environ.get("GITHUB_TOKEN")
    repo_name = os.environ.get("GITHUB_REPOSITORY")
    
    auth = Auth.Token(token)
    gh = Github(auth=auth)
    repo = gh.get_repo(repo_name)
    issue = repo.get_issue(number=int(issue_number))
    return issue.body, issue

def generate_html(niche_description):
    """Genera el HTML usando Groq"""
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    
    prompt = f"""
    Crea una Landing Page completa en un ÚNICO archivo HTML (con CSS y JS incrustados) 
    para el siguiente nicho de mercado: {niche_description}.
    
    Requisitos:
    - Diseño moderno, limpio y responsive (móvil y escritorio).
    - Sección Hero atractiva con título y botón de llamada a la acción.
    - Sección de beneficios o características.
    - Sección de testimonios falsos (placeholder).
    - Formulario de contacto simple (solo visual, no funcional).
    - Footer con enlaces legales ficticios.
    - Optimizado para SEO básico.
    - NO incluyas explicaciones ni markdown, solo el código HTML puro.
    """
    
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        max_tokens=4096
    )
    
    return response.choices[0].message.content

def main():
    print("🏗️ Iniciando generador de código...")
    
    try:
        # 1. Obtener detalles del issue
        issue_body, issue_obj = get_issue_body()
        print(f"📝 Leyendo issue: {issue_obj.title}")
        
        # 2. Generar HTML
        html_content = generate_html(issue_body)
        
        # 3. Guardar archivo
        os.makedirs("output_site", exist_ok=True)
        with open("output_site/index.html", "w", encoding="utf-8") as f:
            f.write(html_content)
            
        print("✅ Sitio generado en output_site/index.html")
        
        # 4. Comentar en el issue que terminó
        token = os.environ.get("GITHUB_TOKEN")
        repo_name = os.environ.get("GITHUB_REPOSITORY")
        auth = Auth.Token(token)
        gh = Github(auth=auth)
        repo = gh.get_repo(repo_name)
        
        issue_obj.create_comment("✅ Código generado correctamente. El deploy se iniciará automáticamente.")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise e

if __name__ == "__main__":
    main()
