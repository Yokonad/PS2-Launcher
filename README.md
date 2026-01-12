<p align="center">
  <h1 align="center">PS2 Launcher</h1>
  <p align="center">
    <strong>Un launcher minimalista para PlayStation 2</strong>
  </p>
  <p align="center">
    Interfaz moderna | Deteccion automatica de mandos | Integracion con PCSX2
  </p>
</p>

---

## **Caracteristicas**

- **Interfaz minimalista** — Diseno limpio en blanco y negro
- **Deteccion automatica de mandos** — DualSense, DualShock, Xbox, Switch Pro
- **Integracion con PCSX2** — Lanza juegos directamente
- **Sistema de logs** — Seguimiento de eventos y errores
- **Configuracion simple** — Auto-detecta PCSX2 instalado

---

## **Instalacion**

### Requisitos previos

| Requisito | Descripcion |
|-----------|-------------|
| **Python** | 3.10 o superior ([descargar](https://python.org)) |
| **PCSX2** | Version 2.0+ ([descargar](https://pcsx2.net/downloads)) |
| **BIOS PS2** | Requerida por PCSX2 (incluida en el repositorio) |

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

## **Configuracion de BIOS**

La BIOS esta incluida en la carpeta `bios/` del repositorio.

### Pasos para configurar:

1. **Descomprime** el archivo `bios.zip` que esta en la carpeta `bios/`
2. Abre **PCSX2**
3. Ve a **Settings** → **BIOS**
4. Haz clic en **"Abrir carpeta de BIOS"** o copia la ruta que aparece
5. **Copia los archivos descomprimidos** a esa carpeta
6. Haz clic en **"Actualizar lista"**
7. Selecciona: **Europe v02.20 (04/02/2006)**
8. Haz clic en **Aplicar**

> La ruta tipica de BIOS en PCSX2 es: `C:\Users\TuUsuario\Documents\PCSX2\bios`

---

## **Uso**

1. **Agrega tus juegos** — Coloca archivos `.iso` en la carpeta `roms/`
2. **Ejecuta el launcher** — Doble clic en `ps2.bat` o `ps2.exe`
3. **Selecciona un juego** — Haz clic en el juego de la biblioteca
4. **Juega** — Presiona el boton **JUGAR**

---

## **Mandos Soportados**

| Mando | Deteccion |
|-------|-----------|
| PlayStation 5 DualSense | Automatica |
| PlayStation 4 DualShock | Automatica |
| Xbox Series X/S | Automatica |
| Xbox One / 360 | Automatica |
| Nintendo Switch Pro | Automatica |

> Los mandos se configuran automaticamente al conectarlos. No requiere configuracion manual.

---

## **Estructura del Proyecto**

```
PS2-Launcher/
├── install.bat       # Instalador de dependencias
├── ps2.bat           # Iniciar launcher
├── ps2.exe           # Ejecutable compilado
├── bios/             # BIOS de PS2 (descomprimir)
├── launcher/         # Codigo fuente
│   ├── main.py       # Punto de entrada
│   ├── core/         # Logica del launcher
│   └── gui/          # Interfaz grafica
├── roms/             # Tus juegos (.iso)
├── logs/             # Registros del sistema
└── config/           # Configuracion guardada
```

---

## **Configuracion de Video Recomendada**

Para la mejor calidad visual, configura en **PCSX2 → Settings → Graphics**:

| Opcion | Valor Recomendado |
|--------|-------------------|
| Renderer | Vulkan |
| Internal Resolution | 4x Native (1440p) |
| Anisotropic Filtering | 16x |
| MTVU | Activado |
| Instant VU1 | Activado |

---

## **Solucion de Problemas**

| Problema | Solucion |
|----------|----------|
| PCSX2 no detectado | Ve a **Config** y selecciona la ruta manualmente |
| No inicia el juego | Configura la BIOS en PCSX2 primero |
| Mando no funciona | Conectalo antes de iniciar el juego |

---

## **Licencia**

Este proyecto es de codigo abierto. Sientete libre de usarlo y modificarlo.

---

<p align="center">
  Hecho por <a href="https://github.com/Yokonad">Yokonad</a>
</p>
