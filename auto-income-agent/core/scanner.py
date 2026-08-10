#!/usr/bin/env python3
"""
Scanner de Oportunidades - Busca nichos rentables usando APIs gratuitas
"""

import os
import json
from datetime import datetime
from groq import Groq

def scan_trending_niches():
    """
    Escanea tendencias y detecta nichos con potencial de ingresos
    Usa Google Trends (simulado) + análisis con Qwen
    """
    
    # Nichos predefinidos basados en patrones evergreen
    # En producción, esto se conectaría a APIs reales
    potential_niches = [
        {
            "category": "Herramientas Online",
            "ideas": [
                "Calculadora de propinas para restaurantes",
                "Conversor de unidades de cocina",
                "Generador de contraseñas seguras",
                "Contador de palabras para escritores"
            ]
        },
        {
            "category": "Salud y Bienestar",
            "ideas": [
                "Calculadora de IMC personalizada",
                "Tracker de agua diario",
                "Guía de estiramientos para oficina",
                "Recetario keto rápido"
            ]
        },
        {
            "category": "Finanzas Personales",
            "ideas": [
                "Calculadora de ahorro para jubilación",
                "Tracker de gastos diarios",
                "Comparador de tarjetas de crédito",
                "Planificador de presupuestos mensuales"
            ]
        },
        {
            "category": "Educación",
            "ideas": [
                "Flashcards para aprender idiomas",
                "Test de práctica para exámenes",
                "Generador de ejercicios de matemáticas",
                "Guía de estudio Pomodoro"
            ]
        }
    ]
    
    # Analizar cada nicho con Qwen para evaluar potencial
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    
    opportunities = []
    
    for category_data in potential_niches:
        category = category_data["category"]
        
        for idea in category_data["ideas"]:
            # Prompt para evaluar el nicho
            prompt = f"""
            Evalúa esta oportunidad de negocio online:
            
            Nicho: {idea}
            Categoría: {category}
            
            Proporciona un análisis breve en formato JSON con:
            - puntuacion_potencial (1-10)
            - competencia (baja/media/alta)
            - tiempo_desarrollo_horas (número)
            - estrategias_monetizacion (lista de 2-3 métodos)
            - trafico_mensual_estimado (número aproximado)
            - dificultad_seo (baja/media/alta)
            
            Solo responde con JSON válido, sin texto adicional.
            """
            
            try:
                response = client.chat.completions.create(
                    model="qwen-2.5-coder-32b",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=500
                )
                
                analysis = json.loads(response.choices[0].message.content)
                
                # Filtrar solo oportunidades con buen potencial
                if analysis.get("puntuacion_potencial", 0) >= 7:
                    opportunities.append({
                        "idea": idea,
                        "categoria": category,
                        "analisis": analysis,
                        "timestamp": datetime.now().isoformat()
                    })
                    
            except Exception as e:
                print(f"Error analizando {idea}: {e}")
                continue
    
    # Ordenar por puntuación
    opportunities.sort(key=lambda x: x["analisis"].get("puntuacion_potencial", 0), reverse=True)
    
    return opportunities[:3]  # Top 3 oportunidades


def generate_report(opportunities):
    """Genera un reporte en Markdown para crear el Issue"""
    
    if not opportunities:
        return "# ❌ No se encontraron oportunidades válidas\n\nInténtalo de nuevo más tarde."
    
    top = opportunities[0]
    analisis = top["analisis"]
    
    report = f"""# 🎯 Oportunidad detectada: {top['idea']}

## 📊 Análisis del Nicho

| Métrica | Valor |
|---------|-------|
| **Categoría** | {top['categoria']} |
| **Potencial** | ⭐ {analisis.get('puntuacion_potencial', 0)}/10 |
| **Competencia** | {analisis.get('competencia', 'N/A')} |
| **Tiempo desarrollo** | ~{analisis.get('tiempo_desarrollo_horas', 0)} horas |
| **Tráfico estimado** | {analisis.get('trafico_mensual_estimado', 0):,} visitas/mes |
| **Dificultad SEO** | {analisis.get('dificultad_seo', 'N/A')} |

## 💰 Estrategias de Monetización

"""
    
    for i, estrategia in enumerate(analisis.get('estrategias_monetizacion', []), 1):
        report += f"{i}. **{estrategia}**\n"
    
    report += f"""
## 🚀 Plan de Acción Recomendado

1. ✅ **Crear landing page** optimizada para SEO
2. ✅ **Implementar herramienta principal** ({top['idea']})
3. ✅ **Añadir enlaces de afiliado** relacionados
4. ✅ **Configurar Google AdSense** para display ads
5. ✅ **Promocionar en redes sociales** y foros

## 🛠️ Stack Técnico Sugerido

- **Frontend**: HTML5 + CSS3 + JavaScript vanilla
- **Hosting**: GitHub Pages (gratis)
- **Analytics**: Google Analytics (gratis)
- **Monetización**: AdSense + Amazon Associates

## ⏱️ Timeline Estimado

- **Desarrollo**: {analisis.get('tiempo_desarrollo_horas', 2)} horas (automatizado con IA)
- **Aprobación AdSense**: 2-14 días
- **Primeros ingresos**: 1-4 semanas

---

## 👤 Tu Decisión

¿Quieres proceder con esta oportunidad?

**Para APROBAR**: Comenta `/approve` en este issue
**Para RECHAZAR**: Comenta `/reject` o cierra el issue

_El código se generará automáticamente tras tu aprobación_
"""
    
    return report


if __name__ == "__main__":
    print("🔍 Escaneando oportunidades...")
    
    opportunities = scan_trending_niches()
    
    if opportunities:
        report = generate_report(opportunities)
        
        # Guardar reporte para el workflow
        with open("opportunity_report.md", "w") as f:
            f.write(report)
        
        print(f"✅ Reporte generado: {len(opportunities)} oportunidades encontradas")
        print(f"📄 Top oportunidad: {opportunities[0]['idea']}")
    else:
        with open("opportunity_report.md", "w") as f:
            f.write("# ❌ No se encontraron oportunidades\n\nReintentando en la próxima ejecución...")
        print("❌ No se encontraron oportunidades válidas")
