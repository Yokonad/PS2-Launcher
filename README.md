<p align="center">
  <h1 align="center">PS2 Launcher v2.0</h1>
  <p align="center">
    <strong>Frontend para emulacion de PlayStation 2</strong>
  </p>
</p>

---

## Novedades v2.0

- Configuracion automatica de mandos al conectar
- Selector de carpeta de ROMs personalizada
- Instalador mejorado con extraccion de BIOS
- Interfaz con botones mejorados

---

## Descripcion

PS2 Launcher es una interfaz grafica para gestionar y ejecutar juegos de PlayStation 2 mediante PCSX2. Detecta controladores automaticamente y los configura como DualShock2.

---

## Requisitos

| Componente | Especificacion |
|------------|----------------|
| Sistema Operativo | Windows 10/11 |
| Python | 3.10+ |
| PCSX2 | v2.0+ |

---

## Instalacion

```bash
git clone https://github.com/Yokonad/PS2-Launcher.git
cd PS2-Launcher
install.bat
```

El instalador:
- Verifica Python
- Instala dependencias (customtkinter, pygame-ce, pillow)
- Crea carpetas necesarias
- Extrae BIOS automaticamente

---

## Configuracion de BIOS

1. El instalador extrae `bios.rar` a la carpeta `bios/`
2. Ejecutar PCSX2
3. Settings > BIOS > Open BIOS Folder
4. Copiar archivos de `bios/` a esa carpeta
5. Seleccionar **Europe v02.20 (04/02/2006)**

---

## Uso

1. Ejecutar `ps2.bat` o `ps2.exe`
2. Config > Seleccionar carpeta de ROMs
3. Conectar mando (se configura automaticamente)
4. Seleccionar juego > JUGAR

---

## Controladores Soportados

| Dispositivo | Auto-Config |
|-------------|-------------|
| PlayStation 5 DualSense | Automatico |
| PlayStation 4 DualShock 4 | Automatico |
| Xbox Series X/S | Automatico |
| Xbox One / 360 | Automatico |
| Nintendo Switch Pro | Automatico |

---

## Estructura

```
PS2-Launcher/
├── install.bat       # Instalador
├── ps2.bat           # Ejecutar launcher
├── bios.rar          # BIOS (se extrae automaticamente)
├── launcher/         # Codigo fuente
├── roms/             # Juegos ISO
├── logs/             # Registros
└── config/           # Configuracion
```

---

## Solucion de Problemas

| Problema | Solucion |
|----------|----------|
| PCSX2 no detectado | Config > Seleccionar ruta |
| Mando no responde | Reconectar mando |
| Sin juegos | Config > Seleccionar carpeta ROMs |

---

<p align="center">
  v2.0 | Desarrollado por <a href="https://github.com/Yokonad">Yokonad</a>
</p>
