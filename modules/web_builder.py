import os
import json
from groq import Groq
from github import Github, Auth

def main():
    print("🏗️ Iniciando generador de código...")
    
    # Configurar clientes
    groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    auth = Auth.Token(os.environ.get("GITHUB_TOKEN"))
    gh = Github(auth=auth)
    
    repo_name = os.environ.get("GITHUB_REPOSITORY")
    issue_number = int(os.environ.get("ISSUE_NUMBER"))
    
    repo = gh.get_repo(repo_name)
    issue = repo.get_issue(number=issue_number)
    
    # Obtener detalles del issue aprobado
    niche = issue.title.replace("💡 Oportunidad Detectada: ", "")
    body = issue.body
    
    print(f"Generando web para: {niche}")
    
    # Prompt para Qwen/Llama
    prompt = f"""
    Crea una Landing Page completa en UN SOLO archivo HTML (con CSS y JS incrustados) 
    para el nicho: {niche}.
    Detalles: {body}
    
    Requisitos:
    - Diseño moderno y responsive
    - Secciones: Hero, Beneficios, Testimonios, FAQ, Footer
    - Botones de llamada a la acción claros
    - Optimizado para SEO básico
    - NO incluyas markdown, solo el código HTML puro
    """
    
    try:
        response = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=4000
        )
        
        html_code = response.choices[0].message.content
        
        # Limpiar si viene con markdown
        if "```html" in html_code:
            html_code = html_code.split("```html")[1].split("```")[0]
        elif "```" in html_code:
            html_code = html_code.split("```")[1].split("```")[0]
            
        # Guardar archivo
        os.makedirs("output_site", exist_ok=True)
        with open("output_site/index.html", "w", encoding="utf-8") as f:
            f.write(html_code)
            
        print("✅ Sitio generado exitosamente.")
        
        # Commit y Push automático a rama gh-pages
        os.system("git config --global user.name 'github-actions[bot]'")
        os.system("git config --global user.email 'github-actions[bot]@users.noreply.github.com'")
        os.system("git add output_site/")
        os.system("git commit -m 'Deploy: Web generada para " + niche + "' || echo 'No changes'")
        os.system("git push origin HEAD:gh-pages --force")
        
        # Comentar en el issue
        issue.create_comment("✅ **¡Web generada y desplegada!**\n\nPuedes verla aquí: https://" + repo.owner.login + ".github.io/" + repo.name + "/")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        issue.create_comment(f"❌ Error generando la web: {str(e)}")
        raise e

if __name__ == "__main__":
    main()
