# 🚀 Setup Rápido - Auto-Income Agent

## Tiempo estimado: 5 minutos

### Paso 1: Obtén tu API Key de Groq (1 min)

1. Ve a https://console.groq.com
2. Regístrate gratis (no requiere tarjeta de crédito)
3. Ve a "API Keys" y crea una nueva key
4. Copia la key (empieza con `gsk_...`)

### Paso 2: Sube el código a GitHub (2 min)

```bash
# En tu terminal local
cd /workspace/auto-income-agent

# Inicializa git (si no lo está)
git init

# Crea un repo nuevo en GitHub (desde github.com)
# Luego añade el remote (reemplaza TU_USUARIO con tu username)
git remote add origin https://github.com/TU_USUARIO/auto-income-agent.git

# Sube todo
git add .
git commit -m "Initial commit: Auto-Income Agent setup"
git push -u origin main
```

### Paso 3: Configura Secrets en GitHub (1 min)

1. Ve a tu repo en GitHub
2. Click en **Settings** (pestaña superior)
3. Click en **Secrets and variables** > **Actions** (menú izquierdo)
4. Click en **New repository secret**
5. Añade:
   - Name: `GROQ_API_KEY`
   - Value: (la key que copiaste de Groq)
6. Click **Add secret**

### Paso 4: Activa GitHub Pages (1 min)

1. En tu repo, ve a **Settings** > **Pages**
2. En **Build and deployment**:
   - Source: `GitHub Actions`
3. GitHub guardará automáticamente

### Paso 5: Ejecuta el primer scan (30 seg)

1. Ve a la pestaña **Actions** en tu repo
2. Click en **"🔍 Opportunity Scan"** (workflow de la izquierda)
3. Click en **Run workflow** (botón verde)
4. Click **Run workflow** otra vez para confirmar

¡Listo! El agente empezará a escanear oportunidades.

---

## ¿Qué pasa ahora?

### El agente hará esto automáticamente:

1. ✅ Escanea nichos rentables (cada hora si usas el schedule)
2. ✅ Crea un Issue con el análisis completo
3. ⏳ **Espera tu aprobación** (comenta `/approve` en el Issue)
4. ✅ Genera el código de la web con Qwen 2.5 Coder
5. ✅ Hace deploy automático a GitHub Pages
6. ✅ Te da la URL del sitio live

### Tu único trabajo:

- Revisar Issues creados
- Comentar `/approve` o `/reject`
- ¡Listo!

---

## URLs importantes

- **Issues (tu dashboard)**: `https://github.com/TU_USUARIO/auto-income-agent/issues`
- **Sitios desplegados**: `https://TU_USUARIO.github.io/auto-income-agent/`
- **Logs de ejecución**: Pestaña **Actions** en GitHub

---

## Primeros ingresos

Una vez tengas sitios desplegados:

1. **Google AdSense**: Registra cada URL en https://adsense.google.com
2. **Amazon Associates**: Crea cuenta en https://affiliate-program.amazon.com
3. **Promociona**: Comparte en Reddit, Twitter, foros del nicho

**Timeline realista:**
- Día 1: Setup completado
- Día 2-3: Primer sitio generado y aprobado por AdSense
- Semana 2-4: Primeros clicks/ingresos
- Mes 2+: Escalar a más sitios

---

## Solución de problemas

### Error: "Rate limit exceeded"
- Groq tiene límites en free tier. Espera unos minutos y reintenta.

### Error: "No opportunities found"
- Es normal a veces. El scanner es conservador. Reintentará en la próxima hora.

### Workflow no se ejecuta
- Verifica que los Secrets estén bien configurados
- Revisa la pestaña Actions para ver logs de error

### Sitio no se despliega
- Verifica que GitHub Pages esté activado (Settings > Pages)
- Revisa el workflow "Deploy Site" en Actions

---

## ¿Necesitas ayuda?

Revisa el README.md para documentación completa.

**¡A generar ingresos! 💰**
