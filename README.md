<p align="center">
  <h1 align="center">PS2 Launcher</h1>
  <p align="center">
    <strong>Frontend para emulacion de PlayStation 2</strong>
  </p>
</p>

---

## **Descripcion**

PS2 Launcher es una interfaz grafica que permite gestionar y ejecutar juegos de PlayStation 2 mediante el emulador PCSX2. Incluye deteccion automatica de controladores y configuracion optimizada.

---

## **Caracteristicas**

- Interfaz con tema oscuro
- Deteccion automatica de controladores (DualSense, DualShock, Xbox, Switch Pro)
- Integracion nativa con PCSX2
- Sistema de registro de eventos (logging)
- Configuracion automatica del emulador

---

## **Requisitos del Sistema**

| Componente | Especificacion |
|------------|----------------|
| Sistema Operativo | Windows 10/11 |
| Python | 3.10 o superior |
| PCSX2 | Incluido en el repositorio |
| BIOS PS2 | Incluida en el repositorio |

---

## **Instalacion**

```bash
git clone https://github.com/Yokonad/PS2-Launcher.git
cd PS2-Launcher
install.bat
```

El script `install.bat` instalara las dependencias necesarias automaticamente.

---

## **Configuracion de BIOS**

El archivo de BIOS se encuentra en la carpeta `bios/` del repositorio.

### Procedimiento:

1. Descomprimir el archivo `bios.zip` ubicado en `bios/`
2. Ejecutar PCSX2
3. Acceder a **Settings** → **BIOS**
4. Seleccionar **"Abrir carpeta de BIOS"**
5. Copiar los archivos descomprimidos a dicha ubicacion
6. Hacer clic en **"Actualizar lista"**
7. Seleccionar **Europe v02.20 (04/02/2006)**
8. Aplicar cambios

Ruta predeterminada de BIOS: `C:\Users\[Usuario]\Documents\PCSX2\bios`

---

## **Uso**

1. Colocar archivos ISO en la carpeta `roms/`
2. Ejecutar `ps2.bat` o `ps2.exe`
3. Seleccionar el juego en la biblioteca
4. Presionar **JUGAR**

---

## **Descarga de Juegos**

Los archivos ISO de juegos de PS2 pueden descargarse desde:

**https://www.gamesgx.net/**

Una vez descargados, colocar los archivos `.iso` en la carpeta `roms/` del proyecto.

---

## **Controladores Compatibles**

| Dispositivo | Estado |
|-------------|--------|
| PlayStation 5 DualSense | Soportado |
| PlayStation 4 DualShock 4 | Soportado |
| Xbox Series X/S | Soportado |
| Xbox One / 360 | Soportado |
| Nintendo Switch Pro Controller | Soportado |

La configuracion de controladores se realiza automaticamente al detectar el dispositivo.

---

## **Estructura del Proyecto**

```
PS2-Launcher/
├── install.bat       # Script de instalacion
├── ps2.bat           # Ejecutar launcher
├── ps2.exe           # Binario compilado
├── bios/             # Archivos BIOS (descomprimir)
├── launcher/
│   ├── main.py       # Punto de entrada
│   ├── core/         # Modulos principales
│   └── gui/          # Interfaz grafica
├── roms/             # Directorio de ISOs
├── logs/             # Registros del sistema
└── config/           # Archivos de configuracion
```

---

## **Configuracion Grafica Recomendada**

Ajustes optimos en PCSX2 → Settings → Graphics:

| Parametro | Valor |
|-----------|-------|
| Renderer | Vulkan |
| Internal Resolution | 4x Native |
| Anisotropic Filtering | 16x |
| MTVU | Habilitado |
| Instant VU1 | Habilitado |

---

## **Solucion de Problemas**

| Incidencia | Solucion |
|------------|----------|
| PCSX2 no detectado | Configurar ruta manualmente en Settings |
| Error al iniciar juego | Verificar configuracion de BIOS |
| Controlador no responde | Conectar antes de iniciar el juego |

---

## **Licencia**

Proyecto de codigo abierto. Uso y modificacion permitidos.

---

<p align="center">
  Desarrollado por <a href="https://github.com/Yokonad">Yokonad</a>
</p>
