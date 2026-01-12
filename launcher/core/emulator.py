"""
Emulator - Integración con PCSX2
"""
import os
import subprocess
import json
from pathlib import Path
from typing import Dict, Optional
import configparser


class EmulatorManager:
    """Gestiona la integración con PCSX2"""
    
    PCSX2_DOWNLOAD_URL = "https://pcsx2.net/downloads"
    
    def __init__(self, config_path: str = None, logger=None):
        self.base_path = Path(__file__).parent.parent.parent
        self.config_path = Path(config_path) if config_path else self.base_path / "config"
        self.pcsx2_path = None
        self.pcsx2_config_dir = None
        self.settings = {}
        self.logger = logger
        self._load_settings()
        
    def _log(self, message: str, level: str = "info"):
        """Helper para logging"""
        if self.logger:
            getattr(self.logger, level)(message)
        else:
            print(f"[{level.upper()}] {message}")
        
    def _load_settings(self):
        """Carga la configuración guardada"""
        settings_file = self.config_path / "settings.json"
        if settings_file.exists():
            try:
                with open(settings_file, 'r') as f:
                    self.settings = json.load(f)
                    self.pcsx2_path = self.settings.get('pcsx2_path')
                    self.pcsx2_config_dir = self.settings.get('pcsx2_config_dir')
            except Exception:
                pass
                
    def save_settings(self):
        """Guarda la configuración"""
        self.config_path.mkdir(parents=True, exist_ok=True)
        settings_file = self.config_path / "settings.json"
        
        self.settings['pcsx2_path'] = str(self.pcsx2_path) if self.pcsx2_path else None
        self.settings['pcsx2_config_dir'] = str(self.pcsx2_config_dir) if self.pcsx2_config_dir else None
        
        with open(settings_file, 'w') as f:
            json.dump(self.settings, f, indent=2)
            
    def detect_pcsx2(self) -> Optional[Path]:
        """Detecta la instalación de PCSX2"""
        possible_paths = [
            # Portable en el proyecto
            self.base_path / "pcsx2" / "pcsx2-qt.exe",
            self.base_path / "pcsx2" / "pcsx2.exe",
            # Instalación típica
            Path("C:/Program Files/PCSX2/pcsx2-qt.exe"),
            Path("C:/Program Files/PCSX2/pcsx2.exe"),
            Path("C:/Program Files (x86)/PCSX2/pcsx2-qt.exe"),
            Path(os.environ.get('LOCALAPPDATA', '')) / "PCSX2" / "pcsx2-qt.exe",
        ]
        
        for path in possible_paths:
            if path.exists():
                self.pcsx2_path = path
                self._detect_pcsx2_config_dir()
                self.save_settings()
                self._log(f"PCSX2 detectado: {path}")
                return path
                
        return None
    
    def _detect_pcsx2_config_dir(self):
        """Detecta el directorio de configuración de PCSX2"""
        possible_dirs = [
            # PCSX2 2.0+ Qt
            Path(os.environ.get('APPDATA', '')) / "PCSX2",
            Path(os.environ.get('LOCALAPPDATA', '')) / "PCSX2",
            # Portable
            self.pcsx2_path.parent / "inis" if self.pcsx2_path else None,
            self.pcsx2_path.parent if self.pcsx2_path else None,
        ]
        
        for dir_path in possible_dirs:
            if dir_path and dir_path.exists():
                self.pcsx2_config_dir = dir_path
                self._log(f"Directorio config PCSX2: {dir_path}")
                return dir_path
                
        return None
    
    def set_pcsx2_path(self, path: str) -> bool:
        """Establece la ruta de PCSX2 manualmente"""
        path = Path(path)
        if path.exists() and path.suffix == '.exe':
            self.pcsx2_path = path
            self._detect_pcsx2_config_dir()
            self.save_settings()
            return True
        return False
    
    def is_configured(self) -> bool:
        """Verifica si PCSX2 está configurado"""
        return self.pcsx2_path is not None and Path(self.pcsx2_path).exists()
    
    def launch_game(self, rom_path: str, config: Dict = None) -> bool:
        """Lanza un juego con PCSX2"""
        if not self.is_configured():
            if not self.detect_pcsx2():
                self._log("PCSX2 no configurado", "error")
                return False
        
        rom_path = Path(rom_path)
        if not rom_path.exists():
            self._log(f"ROM no encontrada: {rom_path}", "error")
            return False
            
        try:
            pcsx2_exe = str(self.pcsx2_path)
            pcsx2_dir = str(Path(self.pcsx2_path).parent)  # Directorio donde está PCSX2
            rom_file = str(rom_path.resolve())  # Ruta absoluta completa
            
            self._log(f"PCSX2: {pcsx2_exe}")
            self._log(f"ROM: {rom_file}")
            
            # Usar shell=True en Windows para manejar espacios en rutas
            import platform
            if platform.system() == 'Windows':
                # Escapar rutas con comillas para manejar espacios
                cmd = f'"{pcsx2_exe}" "{rom_file}"'
                self._log(f"Comando: {cmd}")
                
                # Usar subprocess.Popen con shell para Windows
                process = subprocess.Popen(
                    cmd,
                    shell=True,
                    cwd=pcsx2_dir,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                self._log(f"Proceso iniciado con PID: {process.pid}")
            else:
                # Linux/Mac
                subprocess.Popen([pcsx2_exe, rom_file], cwd=str(self.pcsx2_path.parent))
            
            return True
            
        except FileNotFoundError as e:
            self._log(f"Archivo no encontrado: {e}", "error")
            return False
        except PermissionError as e:
            self._log(f"Error de permisos: {e}", "error")
            return False
        except Exception as e:
            self._log(f"Error lanzando PCSX2: {type(e).__name__}: {e}", "error")
            import traceback
            self._log(traceback.format_exc(), "error")
            return False
    
    def get_download_instructions(self) -> str:
        """Retorna instrucciones para descargar PCSX2"""
        return f"""
PCSX2 no está instalado o no se encontró.

Para instalar PCSX2:
1. Ve a: https://pcsx2.net/downloads
2. Descarga la última versión estable para Windows (PCSX2 2.0+)
3. Instálalo o extrae el archivo

Después de instalar, configura la ruta en el launcher.
"""

    def get_recommended_settings_text(self, config: Dict) -> str:
        """Genera texto con las configuraciones recomendadas"""
        from core.game_info import CONFIG_DISPLAY_NAMES
        
        lines = [
            "╔══════════════════════════════════════╗",
            "║   CONFIGURACIÓN RECOMENDADA          ║",
            "╠══════════════════════════════════════╣"
        ]
        
        settings_map = {
            'renderer': 'Renderer',
            'internal_resolution': 'Resolución',
            'anisotropic_filtering': 'Filtro AF',
            'frame_limit': 'FPS Límite',
            'mtvu': 'MTVU Hack',
            'speedhacks': 'SpeedHacks'
        }
        
        for key, label in settings_map.items():
            if key in config:
                value = config[key]
                if key in CONFIG_DISPLAY_NAMES and value in CONFIG_DISPLAY_NAMES[key]:
                    display_value = CONFIG_DISPLAY_NAMES[key][value]
                elif isinstance(value, bool):
                    display_value = "Activado" if value else "Desactivado"
                else:
                    display_value = str(value)
                lines.append(f"║  {label:15} │ {display_value:18} ║")
        
        lines.append("╚══════════════════════════════════════╝")
        
        return "\n".join(lines)


class ControllerConfig:
    """Gestiona la configuración de mandos"""
    
    # Mapeo por defecto del control de PS2 a teclado
    DEFAULT_KEYBOARD_MAP = {
        'up': 'W',
        'down': 'S',
        'left': 'A',
        'right': 'D',
        'cross': 'K',      # X
        'circle': 'L',     # O
        'square': 'J',     # □
        'triangle': 'I',   # △
        'l1': 'Q',
        'l2': 'E',
        'r1': 'U',
        'r2': 'O',
        'l3': 'Z',
        'r3': 'C',
        'start': 'Return',
        'select': 'BackSpace',
        'left_analog_up': 'Up',
        'left_analog_down': 'Down',
        'left_analog_left': 'Left',
        'left_analog_right': 'Right',
    }
    
    # Nombres amigables para los botones
    BUTTON_LABELS = {
        'up': 'D-Pad ↑',
        'down': 'D-Pad ↓',
        'left': 'D-Pad ←',
        'right': 'D-Pad →',
        'cross': '✕ (Cross)',
        'circle': '○ (Circle)',
        'square': '□ (Square)',
        'triangle': '△ (Triangle)',
        'l1': 'L1',
        'l2': 'L2',
        'r1': 'R1',
        'r2': 'R2',
        'l3': 'L3 (Stick)',
        'r3': 'R3 (Stick)',
        'start': 'START',
        'select': 'SELECT',
        'left_analog_up': 'Left Stick ↑',
        'left_analog_down': 'Left Stick ↓',
        'left_analog_left': 'Left Stick ←',
        'left_analog_right': 'Left Stick →',
    }
    
    def __init__(self, config_path: str = None):
        self.base_path = Path(__file__).parent.parent.parent
        self.config_path = Path(config_path) if config_path else self.base_path / "config"
        self.controller_map = self.DEFAULT_KEYBOARD_MAP.copy()
        self._load_config()
        
    def _load_config(self):
        """Carga la configuración de controles guardada"""
        config_file = self.config_path / "controller.json"
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    saved_map = json.load(f)
                    self.controller_map.update(saved_map)
            except Exception:
                pass
                
    def save_config(self):
        """Guarda la configuración de controles"""
        self.config_path.mkdir(parents=True, exist_ok=True)
        config_file = self.config_path / "controller.json"
        
        with open(config_file, 'w') as f:
            json.dump(self.controller_map, f, indent=2)
            
    def set_mapping(self, button: str, key: str):
        """Establece el mapeo de un botón"""
        if button in self.controller_map:
            self.controller_map[button] = key
            self.save_config()
            
    def get_mapping(self, button: str) -> str:
        """Obtiene el mapeo de un botón"""
        return self.controller_map.get(button, '')
    
    def get_all_mappings(self) -> Dict[str, str]:
        """Obtiene todos los mapeos"""
        return self.controller_map.copy()
    
    def reset_to_default(self):
        """Restaura los controles por defecto"""
        self.controller_map = self.DEFAULT_KEYBOARD_MAP.copy()
        self.save_config()


if __name__ == "__main__":
    # Test
    em = EmulatorManager()
    print(f"PCSX2 configurado: {em.is_configured()}")
    if not em.is_configured():
        print(em.get_download_instructions())
