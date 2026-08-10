# Auto-Income Agent - Cloud-Based Architecture

Agente automático de generación de ingresos usando GitHub Actions + Qwen Online (sin coste local).

## 🏗️ Arquitectura

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Tu PC         │     │   GitHub         │     │   Qwen API      │
│   (Supervisor)  │────▶│   Actions        │────▶│   (Groq Free)   │
│                 │     │   (Worker)       │     │                 │
│ - Dashboard     │◀────│ - Genera código  │     │ - IA gratuita   │
│ - Aprueba       │     │ - Deploy auto    │     │ - Sin límite    │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

## ✅ Ventajas

- **Cero coste eléctrico** en tu PC (solo supervisas)
- **Cero instalación** de modelos pesados
- **GitHub Actions free**: 2000 minutos/mes gratis
- **Groq API free**: Qwen 2.5 Coder sin límites actuales
- **Deploy automático** a GitHub Pages/Vercel/Netlify (todos free)

## 📁 Estructura

auto-income-agent/
├── .github/workflows/
│   ├── opportunity-scan.yml    # Escanea oportunidades cada hora
│   ├── code-generator.yml      # Genera código con Qwen
│   └── deploy-site.yml         # Deploy automático
├── core/
│   ├── scanner.py              # Busca nichos (APIs free)
│   └── approver.py             # Sistema de aprobación
├── modules/
│   ├── web_builder.py          # Prompt para Qwen
│   ├── github_manager.py       # Crea repos/deploy
│   └── paypal_tracker.py       # Monitoriza ingresos
├── workflows/
│   └── templates/              # Prompts optimizados
├── templates/
│   └── landing_page.html       # Plantilla base
├── requirements.txt
├── .env.example
└── README.md

## 🚀 Setup en 5 minutos

### 1. Fork este repo a tu GitHub

### 2. Configura Secrets en GitHub
Ve a: Settings > Secrets and variables > Actions
Añade:
- GROQ_API_KEY: Obtén gratis en https://console.groq.com
- PAYPAL_CLIENT_ID: (opcional, para tracking)
- PAYPAL_SECRET: (opcional)

### 3. Activa GitHub Pages
Ve a: Settings > Pages
Source: GitHub Actions

### 4. Primera ejecución manual
Ve a: Actions > Opportunity Scan > Run workflow

### 5. Revisa y aprueba
El agente creará un Issue en GitHub con:
- Oportunidad detectada
- Nicho analizado
- Plan de acción
- Botón de aprobación (comentario en el Issue)

## 🔍 Cómo funciona

### Flujo completo:

1. **Escaneo automático** (cada hora vía GitHub Actions)
   - Busca tendencias en Google Trends API (free)
   - Analiza keywords en Reddit/Twitter APIs (free tiers)
   - Detecta nichos con baja competencia

2. **Generación de propuesta** (automático)
   - Crea Issue en GitHub con análisis completo
   - Incluye mockup del sitio web
   - Estimación de ingresos potenciales

3. **Tu aprobación** (manual, 1 click)
   - Revisas el Issue
   - Comentas: /approve o /reject
   - Opcional: añades comentarios

4. **Generación de código** (automático tras aprobación)
   - GitHub Actions llama a Groq API con Qwen 2.5 Coder
   - Genera HTML/CSS/JS completo
   - Crea branch en el repo

5. **Deploy automático** (automático)
   - Push a branch gh-pages
   - GitHub Pages publica en tu-usuario.github.io/proyecto
   - O deploy a Vercel/Netlify vía webhook

6. **Monetización** (semi-automático)
   - Inserta enlaces de afiliado (Amazon, etc.)
   - Añade Google AdSense (requiere aprobación manual)
   - Trackea clicks/ventas en dashboard

## 💰 Estrategias de Ingreso (Coste 0)

| Estrategia | Implementación | Tiempo hasta ingreso |
|------------|----------------|---------------------|
| Afiliados Amazon | Links en webs | 1-7 días |
| AdSense | Banner en landing | 2-14 días (aprobación) |
| Micro-SaaS | Herramientas JS simples | 1-30 días |
| Lead Generation | Forms a email | 1-7 días |
| Donaciones | BuyMeACoffee/Ko-fi | 1-30 días |

## 🛡️ Seguridad

- **Nunca** se almacenan credenciales en código
- **Nunca** se ejecuta código no aprobado
- **Siempre** logs públicos en GitHub Actions
- **Siempre** puedes cancelar cualquier workflow

## 📊 Dashboard de Control

Accede a: https://github.com/tu-usuario/auto-income-agent/issues

- Issues abiertos = Oportunidades pendientes
- Issues cerrados = Proyectos en producción
- Labels: opportunity, approved, rejected, deployed

## 🔧 Personalización

Edita .github/workflows/opportunity-scan.yml para:
- Cambiar frecuencia de escaneo
- Añadir nuevas fuentes de datos
- Modificar criterios de nicho

Edita workflows/templates/ para:
- Mejorar prompts para Qwen
- Añadir tipos de proyectos
- Personalizar estilo de webs

## ⚠️ Limitaciones Reales

- GitHub Actions: 2000 min/mes (≈ 66 min/día)
- Groq API: Rate limits (actualmente generous free tier)
- GitHub Pages: Sitios estáticos only (sin backend)
- APIs free: Rate limits en algunas fuentes

## 📈 Escalabilidad

Cuando tengas ingresos:
1. Upgrade a GitHub Pro ($4/mes) → más minutos
2. Dominio personalizado ($10/año) → más profesional
3. Vercel Pro ($20/mes) → funciones serverless
4. APIs de pago → mejores datos

## 🎯 Primer Proyecto Recomendado

**Nicho**: Calculadoras online para [tema trending]
- Ejemplo: Calculadora de propinas, conversor de unidades, etc.
- Tráfico: Búsquedas evergreen
- Monetización: AdSense + afiliados relacionados
- Tiempo desarrollo: < 1 hora con Qwen
- Coste: $0

---

**Próximo paso**: Ejecuta el primer workflow y revisa el Issue creado!
