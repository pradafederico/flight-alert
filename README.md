**Prioridad aerolíneas:** LATAM y Delta (código compartido para millas LATAM Pass)

---

## Configuración en 5 pasos

### 1. Fork / clonar este repositorio
```bash
git clone https://github.com/TU_USUARIO/flight-monitor
cd flight-monitor
```

### 2. Configurar contraseña de aplicación Gmail

> Gmail requiere una "contraseña de app" (no tu contraseña normal).

1. Ir a [myaccount.google.com/security](https://myaccount.google.com/security)
2. Activar **verificación en 2 pasos** (si no está activada)
3. Buscar **"Contraseñas de aplicaciones"** → crear una nueva → copiar la contraseña de 16 caracteres

### 3. Agregar secrets en GitHub

Ir a tu repositorio → **Settings → Secrets and variables → Actions → New repository secret**

| Secret | Valor |
|--------|-------|
| `GMAIL_USER` | tu_email@gmail.com |
| `GMAIL_PASS` | contraseña de app de 16 chars |
| `ALERT_EMAIL` | email donde recibir alertas (puede ser el mismo) |

### 4. Habilitar el workflow

En tu repositorio ir a **Actions → "Flight Price Monitor" → Enable workflow**

### 5. Ejecutar por primera vez

En **Actions → Flight Price Monitor → Run workflow** para verificar que funciona.

---

## ¿Cómo funciona?

```
Cada día a las 08:00 (Santiago)
       ↓
Abre Google Flights para cada ruta
       ↓
Extrae precio mínimo en USD
       ↓
Compara con precio del día anterior
       ↓
¿Bajó ≥5%? → Email de alerta inmediata
  No bajó  → Email de resumen diario
       ↓
Guarda historial en data/history.csv
```

---

## Emails que recibirás

**Alerta de bajada (cuando baja ≥5%):**
- Precio anterior vs nuevo con % de caída
- Botón directo a Google Flights para comprar

**Resumen diario (todos los días):**
- Tabla con todos los vuelos y precios actuales
- Comparación con el día anterior

---

## Ejecutar localmente (opcional)

```bash
pip install -r requirements.txt

export GMAIL_USER="tu@gmail.com"
export GMAIL_PASS="xxxx xxxx xxxx xxxx"
export ALERT_EMAIL="tu@gmail.com"

python monitor.py
```

---

## Archivos generados

| Archivo | Descripción |
|---------|-------------|
| `data/prices.json` | Últimos precios guardados |
| `data/history.csv` | Historial completo de precios |

---

## Personalización

Para cambiar el umbral de alerta (por defecto 5%), editar en `monitor.py`:
```python
ALERT_THRESHOLD = 0.05   # 5% → cambiar a 0.08 para 8%, etc.
```

Para agregar más vuelos, copiar un bloque de la lista `FLIGHTS` en `monitor.py`.
