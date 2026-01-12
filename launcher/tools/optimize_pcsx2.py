"""
PCSX2 Optimizer - Aplica configuraciones óptimas de gráficos
"""
import os
import sys
from pathlib import Path
import subprocess


def get_pcsx2_settings_path():
    """Encuentra la carpeta de configuración de PCSX2"""
    possible_paths = [
        Path(os.environ.get('APPDATA', '')) / "PCSX2" / "inis",
        Path(os.environ.get('LOCALAPPDATA', '')) / "PCSX2" / "inis", 
        Path.home() / "Documents" / "PCSX2" / "inis",
    ]
    
    for path in possible_paths:
        if path.exists():
            return path
    return None


def print_optimization_guide():
    """Imprime guía de optimización para PCSX2"""
    
    guide = """
╔══════════════════════════════════════════════════════════════════╗
║         🎮 GUÍA DE OPTIMIZACIÓN PCSX2 - CRASH OF THE TITANS       ║
╠══════════════════════════════════════════════════════════════════╣

Para la MEJOR CALIDAD VISUAL y RENDIMIENTO, configura esto en PCSX2:

════════════════════════════════════════════════════════════════════
  📺 CONFIGURACIÓN DE GRÁFICOS (Settings → Graphics)
════════════════════════════════════════════════════════════════════

  TAB: Rendering
  ─────────────────
  • Renderer:           Vulkan (mejor rendimiento) o Direct3D 12
  • Internal Resolution: 4x Native (~1440p) o 6x Native (4K)
                        *Si el juego va lento, baja a 3x Native

  TAB: Texture Replacement  
  ─────────────────
  • Anisotropic Filtering: 16x
  • Texture Filtering:     Bilinear (PS2)

  TAB: Rendering (Opciones adicionales)
  ─────────────────
  • FXAA:                  ✓ Activado (suaviza bordes)
  • Shader Texture Filtering Accuracy: Minimum (más rápido)

════════════════════════════════════════════════════════════════════
  ⚡ SPEEDHACKS (Settings → Emulation Settings → Speedhacks)
════════════════════════════════════════════════════════════════════

  • EE Cyclerate:          0 (Default)
  • EE Cycle Skipping:     0 (Disabled)
  • MTVU (Multi-Threaded): ✓ Activado (¡MUY IMPORTANTE!)
  • Instant VU1:           ✓ Activado

════════════════════════════════════════════════════════════════════
  🎮 CONFIGURACIÓN DEL MANDO PS5 DUALSENSE
════════════════════════════════════════════════════════════════════

  1. Ve a: Settings → Controllers → Controller Port 1
  
  2. Haz clic en "Automatic Mapping"
     → Selecciona "DualSense Wireless Controller"
  
  3. Verifica el mapeo:
     ┌─────────────────┬─────────────────┐
     │   DUALSENSE     │      PS2        │
     ├─────────────────┼─────────────────┤
     │   ✕ (Cross)     │   ✕ (Cross)     │
     │   ○ (Circle)    │   ○ (Circle)    │
     │   □ (Square)    │   □ (Square)    │
     │   △ (Triangle)  │   △ (Triangle)  │
     │   L1/R1         │   L1/R1         │
     │   L2/R2         │   L2/R2         │
     │   L3/R3         │   L3/R3         │
     │   Left Stick    │   Left Stick    │
     │   Right Stick   │   Right Stick   │
     │   D-Pad         │   D-Pad         │
     │   Options       │   Start         │
     │   Create        │   Select        │
     │   PS Button     │   (No usado)    │
     │   Touchpad      │   (No usado)    │
     └─────────────────┴─────────────────┘
  
  4. Ajusta "Dead Zone" de los sticks:
     → Left Stick Dead Zone: 10-15%
     → Right Stick Dead Zone: 10-15%
     (Esto evita drift y movimientos no deseados)

════════════════════════════════════════════════════════════════════
  🔧 CONFIGURACIÓN ESPECÍFICA PARA CRASH OF THE TITANS
════════════════════════════════════════════════════════════════════

  • El juego es PAL (50fps). Para forzar 60fps:
    Settings → Emulation Settings → GS → Frame Rate: 60
    (Puede acelerar el juego un poco)
  
  • Si hay glitches visuales:
    Settings → Graphics → Rendering → 
    Hardware Fixes → Half Pixel Offset: Special (Texture)

════════════════════════════════════════════════════════════════════
  ✅ RESUMEN DE CONFIGURACIÓN ÓPTIMA
════════════════════════════════════════════════════════════════════

  | Configuración          | Valor Recomendado        |
  |------------------------|--------------------------|
  | Renderer               | Vulkan                   |
  | Internal Resolution    | 4x Native (1440p)        |
  | Anisotropic Filtering  | 16x                      |
  | FXAA                   | Activado                 |
  | MTVU                   | Activado                 |
  | Instant VU1            | Activado                 |
  | Controller             | DualSense (Auto-mapped)  |
  | Dead Zone              | 10-15%                   |

╚══════════════════════════════════════════════════════════════════╝

¡Después de aplicar estos ajustes, el juego se verá increíble! 🎮✨
"""
    print(guide)
    return guide


def open_pcsx2_settings():
    """Abre PCSX2 directamente en configuración"""
    pcsx2_paths = [
        Path("C:/Program Files/PCSX2/pcsx2-qt.exe"),
        Path("C:/Program Files (x86)/PCSX2/pcsx2-qt.exe"),
    ]
    
    for path in pcsx2_paths:
        if path.exists():
            print(f"\n🚀 Abriendo PCSX2...")
            subprocess.Popen([str(path)])
            print("   → Ve a Settings → Graphics para configurar\n")
            return True
    
    print("❌ PCSX2 no encontrado")
    return False


if __name__ == "__main__":
    print_optimization_guide()
    
    response = input("\n¿Quieres abrir PCSX2 ahora para configurar? (s/n): ")
    if response.lower() in ['s', 'si', 'yes', 'y']:
        open_pcsx2_settings()
