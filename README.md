<p align="center">
  <h1 align="center">🎮 PS2 Launcher</h1>
  <p align="center">
    <strong>Un launcher minimalista para PlayStation 2</strong>
  </p>
  <p align="center">
    Interfaz moderna • Detección automática de mandos • Integración con PCSX2
  </p>
</p>

---

## ✨ Características

- 🎨 **Interfaz minimalista** — Diseño limpio en blanco y negro
- 🎮 **Detección automática de mandos** — DualSense, DualShock, Xbox, Switch Pro
- ⚡ **Integración con PCSX2** — Lanza juegos directamente
- 📋 **Sistema de logs** — Seguimiento de eventos y errores
- 🔧 **Configuración simple** — Auto-detecta PCSX2 instalado

---

## 🚀 Instalación

### Requisitos previos

| Requisito | Descripción |
|-----------|-------------|
| **Python** | 3.10 o superior ([descargar](https://python.org)) |
| **PCSX2** | Versión 2.0+ ([descargar](https://pcsx2.net/downloads)) |
| **BIOS PS2** | Requerida por PCSX2 |

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/Yokonad/PS2-Launcher.git
cd PS2-Launcher

# 2. Instalar dependencias
install.bat

# 3. Iniciar el launcher
ps2.bat
```

---

## 🎯 Uso

1. **Agrega tus juegos** — Coloca archivos `.iso` en la carpeta `roms/`
2. **Ejecuta el launcher** — Doble clic en `ps2.bat` o `ps2.exe`
3. **Selecciona un juego** — Haz clic en el juego de la biblioteca
4. **¡Juega!** — Presiona el botón **JUGAR**

---

## 🎮 Mandos Soportados

| Mando | Detección |
|-------|-----------|
| PlayStation 5 DualSense | ✅ Automática |
| PlayStation 4 DualShock | ✅ Automática |
| Xbox Series X\|S | ✅ Automática |
| Xbox One / 360 | ✅ Automática |
| Nintendo Switch Pro | ✅ Automática |

> Los mandos se configuran automáticamente al conectarlos. No requiere configuración manual.

---

## ⚙️ Configuración de BIOS

PCSX2 requiere la BIOS de PS2 para funcionar:

1. Abre **PCSX2** → **Settings** → **BIOS**
2. Haz clic en **"Abrir carpeta de BIOS"**
3. Copia los archivos de BIOS a esa carpeta
4. Haz clic en **"Actualizar lista"**
5. Selecciona: **Europe v02.20 (04/02/2006)**
6. Haz clic en **Aplicar**

---

## 📁 Estructura del Proyecto

```
PS2-Launcher/
├── 📄 install.bat       # Instalador de dependencias
├── 📄 ps2.bat           # Iniciar launcher
├── 📄 ps2.exe           # Ejecutable compilado
├── 📁 launcher/         # Código fuente
│   ├── main.py          # Punto de entrada
│   ├── core/            # Lógica del launcher
│   └── gui/             # Interfaz gráfica
├── 📁 roms/             # Tus juegos (.iso)
├── 📁 logs/             # Registros del sistema
└── 📁 config/           # Configuración guardada
```

---

## 🔧 Configuración de Video Recomendada

Para la mejor calidad visual, configura en **PCSX2 → Settings → Graphics**:

| Opción | Valor Recomendado |
|--------|-------------------|
| Renderer | Vulkan |
| Internal Resolution | 4x Native (1440p) |
| Anisotropic Filtering | 16x |
| MTVU | ✅ Activado |
| Instant VU1 | ✅ Activado |

---

## 🐛 Solución de Problemas

| Problema | Solución |
|----------|----------|
| PCSX2 no detectado | Ve a **Config** y selecciona la ruta manualmente |
| No inicia el juego | Configura la BIOS en PCSX2 primero |
| Mando no funciona | Conéctalo antes de iniciar el juego |

---

## 📝 Licencia

Este proyecto es de código abierto. Siéntete libre de usarlo y modificarlo.

---

<p align="center">
  Hecho con ❤️ por <a href="https://github.com/Yokonad">Yokonad</a>
</p>
