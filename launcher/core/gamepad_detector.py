"""
Gamepad Detector - Detecta y mapea mandos conectados
"""
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import threading
import time

# Intentar importar pygame para detección de gamepads
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False


class ControllerType(Enum):
    """Tipos de mandos soportados"""
    UNKNOWN = "unknown"
    PS5_DUALSENSE = "ps5_dualsense"
    PS4_DUALSHOCK = "ps4_dualshock"
    XBOX_SERIES = "xbox_series"
    XBOX_ONE = "xbox_one"
    XBOX_360 = "xbox_360"
    NINTENDO_SWITCH_PRO = "switch_pro"
    GENERIC = "generic"


@dataclass
class GamepadInfo:
    """Información de un gamepad detectado"""
    id: int
    name: str
    controller_type: ControllerType
    num_axes: int
    num_buttons: int
    num_hats: int
    guid: str = ""


# Mapeo de nombres de controladores a tipos
CONTROLLER_NAME_PATTERNS = {
    ControllerType.PS5_DUALSENSE: [
        "dualsense", "ps5", "playstation 5", "wireless controller"
    ],
    ControllerType.PS4_DUALSHOCK: [
        "dualshock", "ps4", "playstation 4", "sony interactive"
    ],
    ControllerType.XBOX_SERIES: [
        "xbox series", "xbox wireless controller"
    ],
    ControllerType.XBOX_ONE: [
        "xbox one", "microsoft xbox one"
    ],
    ControllerType.XBOX_360: [
        "xbox 360", "xinput"
    ],
    ControllerType.NINTENDO_SWITCH_PRO: [
        "switch pro", "nintendo", "pro controller"
    ],
}


# Mapeo de botones de cada tipo de mando al mando de PS2
# Formato: {button_index: ps2_button_name}
PS2_BUTTON_MAPPINGS = {
    ControllerType.PS5_DUALSENSE: {
        # Botones
        0: 'cross',      # X
        1: 'circle',     # O
        2: 'square',     # □
        3: 'triangle',   # △
        4: 'select',     # Share/Create
        5: 'start',      # Options
        6: 'l3',         # L3
        7: 'r3',         # R3
        8: 'l1',         # L1
        9: 'r1',         # R1
        10: 'up',        # D-Pad Up
        11: 'down',      # D-Pad Down
        12: 'left',      # D-Pad Left
        13: 'right',     # D-Pad Right
        # Axes
        'axis_0': 'left_x',      # Stick Izq X
        'axis_1': 'left_y',      # Stick Izq Y
        'axis_2': 'right_x',     # Stick Der X
        'axis_3': 'right_y',     # Stick Der Y
        'axis_4': 'l2',          # L2
        'axis_5': 'r2',          # R2
    },
    ControllerType.PS4_DUALSHOCK: {
        0: 'cross',
        1: 'circle',
        2: 'square',
        3: 'triangle',
        4: 'select',
        5: 'start',
        6: 'l3',
        7: 'r3',
        8: 'l1',
        9: 'r1',
        10: 'up',
        11: 'down',
        12: 'left',
        13: 'right',
        'axis_0': 'left_x',
        'axis_1': 'left_y',
        'axis_2': 'right_x',
        'axis_3': 'right_y',
        'axis_4': 'l2',
        'axis_5': 'r2',
    },
    ControllerType.XBOX_SERIES: {
        0: 'cross',      # A -> X
        1: 'circle',     # B -> O
        2: 'square',     # X -> □
        3: 'triangle',   # Y -> △
        4: 'l1',         # LB
        5: 'r1',         # RB
        6: 'select',     # View/Back
        7: 'start',      # Menu/Start
        8: 'l3',
        9: 'r3',
        'axis_0': 'left_x',
        'axis_1': 'left_y',
        'axis_2': 'right_x',
        'axis_3': 'right_y',
        'axis_4': 'l2',
        'axis_5': 'r2',
    },
    ControllerType.XBOX_ONE: {
        0: 'cross',
        1: 'circle',
        2: 'square',
        3: 'triangle',
        4: 'l1',
        5: 'r1',
        6: 'select',
        7: 'start',
        8: 'l3',
        9: 'r3',
        'axis_0': 'left_x',
        'axis_1': 'left_y',
        'axis_2': 'right_x',
        'axis_3': 'right_y',
        'axis_4': 'l2',
        'axis_5': 'r2',
    },
    ControllerType.XBOX_360: {
        0: 'cross',
        1: 'circle',
        2: 'square',
        3: 'triangle',
        4: 'l1',
        5: 'r1',
        6: 'select',
        7: 'start',
        8: 'l3',
        9: 'r3',
        'axis_0': 'left_x',
        'axis_1': 'left_y',
        'axis_2': 'l2',
        'axis_3': 'right_x',
        'axis_4': 'right_y',
        'axis_5': 'r2',
    },
}

# Mapeo genérico (fallback)
PS2_BUTTON_MAPPINGS[ControllerType.GENERIC] = PS2_BUTTON_MAPPINGS[ControllerType.XBOX_360]
PS2_BUTTON_MAPPINGS[ControllerType.UNKNOWN] = PS2_BUTTON_MAPPINGS[ControllerType.XBOX_360]
PS2_BUTTON_MAPPINGS[ControllerType.NINTENDO_SWITCH_PRO] = {
    0: 'circle',     # A -> O (Nintendo invierte A/B)
    1: 'cross',      # B -> X
    2: 'triangle',   # X -> △
    3: 'square',     # Y -> □
    4: 'l1',
    5: 'r1',
    6: 'l2',
    7: 'r2',
    8: 'select',
    9: 'start',
    10: 'l3',
    11: 'r3',
    'axis_0': 'left_x',
    'axis_1': 'left_y',
    'axis_2': 'right_x',
    'axis_3': 'right_y',
}


class GamepadDetector:
    """Detecta y gestiona gamepads conectados"""
    
    def __init__(self, logger=None):
        self.logger = logger
        self.gamepads: List[GamepadInfo] = []
        self.active_gamepad: Optional[GamepadInfo] = None
        self._initialized = False
        self._monitor_thread = None
        self._stop_monitoring = False
        self._on_gamepad_connected = None
        self._on_gamepad_disconnected = None
        
    def initialize(self) -> bool:
        """Inicializa el sistema de detección de gamepads"""
        if not PYGAME_AVAILABLE:
            if self.logger:
                self.logger.warning("pygame no disponible - detección de mandos deshabilitada")
            return False
            
        try:
            pygame.init()
            pygame.joystick.init()
            self._initialized = True
            self._log_info("Sistema de gamepads inicializado")
            return True
        except Exception as e:
            self._log_error(f"Error inicializando pygame: {e}")
            return False
            
    def scan(self) -> List[GamepadInfo]:
        """Escanea gamepads conectados"""
        if not self._initialized:
            if not self.initialize():
                return []
                
        self.gamepads = []
        
        try:
            pygame.joystick.quit()
            pygame.joystick.init()
            
            count = pygame.joystick.get_count()
            self._log_info(f"Gamepads detectados: {count}")
            
            for i in range(count):
                try:
                    joy = pygame.joystick.Joystick(i)
                    joy.init()
                    
                    name = joy.get_name()
                    controller_type = self._identify_controller_type(name)
                    
                    # Obtener GUID si está disponible
                    guid = ""
                    try:
                        guid = joy.get_guid()
                    except:
                        pass
                    
                    gamepad = GamepadInfo(
                        id=i,
                        name=name,
                        controller_type=controller_type,
                        num_axes=joy.get_numaxes(),
                        num_buttons=joy.get_numbuttons(),
                        num_hats=joy.get_numhats(),
                        guid=guid
                    )
                    
                    self.gamepads.append(gamepad)
                    self._log_info(
                        f"Gamepad {i}: {name} "
                        f"(Tipo: {controller_type.value}, "
                        f"Botones: {gamepad.num_buttons}, "
                        f"Ejes: {gamepad.num_axes})"
                    )
                    
                except Exception as e:
                    self._log_error(f"Error inicializando gamepad {i}: {e}")
                    
        except Exception as e:
            self._log_error(f"Error escaneando gamepads: {e}")
            
        # Seleccionar el primer gamepad si no hay uno activo
        if self.gamepads and not self.active_gamepad:
            self.set_active_gamepad(0)
            
        return self.gamepads
    
    def _identify_controller_type(self, name: str) -> ControllerType:
        """Identifica el tipo de controlador por su nombre"""
        name_lower = name.lower()
        
        for controller_type, patterns in CONTROLLER_NAME_PATTERNS.items():
            for pattern in patterns:
                if pattern in name_lower:
                    return controller_type
                    
        return ControllerType.GENERIC
    
    def set_active_gamepad(self, gamepad_id: int) -> bool:
        """Establece el gamepad activo"""
        for gamepad in self.gamepads:
            if gamepad.id == gamepad_id:
                self.active_gamepad = gamepad
                self._log_info(f"Gamepad activo: {gamepad.name}")
                return True
        return False
    
    def get_button_mapping(self, gamepad: GamepadInfo = None) -> Dict:
        """Obtiene el mapeo de botones para el tipo de gamepad"""
        gamepad = gamepad or self.active_gamepad
        if not gamepad:
            return {}
            
        return PS2_BUTTON_MAPPINGS.get(
            gamepad.controller_type,
            PS2_BUTTON_MAPPINGS[ControllerType.GENERIC]
        )
    
    def get_ps2_button_name(self, button_index: int, gamepad: GamepadInfo = None) -> str:
        """Convierte un índice de botón al nombre del botón de PS2"""
        mapping = self.get_button_mapping(gamepad)
        return mapping.get(button_index, f"button_{button_index}")
    
    def start_monitoring(self, on_connected=None, on_disconnected=None):
        """Inicia el monitoreo de conexiones/desconexiones"""
        if self._monitor_thread and self._monitor_thread.is_alive():
            return
            
        self._on_gamepad_connected = on_connected
        self._on_gamepad_disconnected = on_disconnected
        self._stop_monitoring = False
        
        self._monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._monitor_thread.start()
        
    def stop_monitoring(self):
        """Detiene el monitoreo"""
        self._stop_monitoring = True
        if self._monitor_thread:
            self._monitor_thread.join(timeout=1)
            
    def _monitor_loop(self):
        """Loop de monitoreo de gamepads"""
        previous_count = len(self.gamepads)
        
        while not self._stop_monitoring:
            try:
                current_gamepads = self.scan()
                current_count = len(current_gamepads)
                
                if current_count > previous_count and self._on_gamepad_connected:
                    # Nuevo gamepad conectado
                    new_gamepad = current_gamepads[-1]
                    self._on_gamepad_connected(new_gamepad)
                elif current_count < previous_count and self._on_gamepad_disconnected:
                    # Gamepad desconectado
                    self._on_gamepad_disconnected()
                    
                previous_count = current_count
                
            except Exception as e:
                self._log_error(f"Error en monitoreo: {e}")
                
            time.sleep(2)  # Revisar cada 2 segundos
    
    def cleanup(self):
        """Limpia recursos"""
        self.stop_monitoring()
        if self._initialized and PYGAME_AVAILABLE:
            pygame.joystick.quit()
            
    def _log_info(self, message: str):
        """Log de información"""
        if self.logger:
            self.logger.info(message)
        else:
            print(f"[INFO] {message}")
            
    def _log_error(self, message: str):
        """Log de error"""
        if self.logger:
            self.logger.error(message)
        else:
            print(f"[ERROR] {message}")


def get_controller_type_display_name(controller_type: ControllerType) -> str:
    """Obtiene el nombre para mostrar del tipo de controlador"""
    display_names = {
        ControllerType.PS5_DUALSENSE: "DualSense (PS5)",
        ControllerType.PS4_DUALSHOCK: "DualShock 4 (PS4)",
        ControllerType.XBOX_SERIES: "Xbox Series X|S",
        ControllerType.XBOX_ONE: "Xbox One",
        ControllerType.XBOX_360: "Xbox 360",
        ControllerType.NINTENDO_SWITCH_PRO: "Switch Pro Controller",
        ControllerType.GENERIC: "Genérico",
        ControllerType.UNKNOWN: "Desconocido",
    }
    return display_names.get(controller_type, "Desconocido")


if __name__ == "__main__":
    # Test
    detector = GamepadDetector()
    gamepads = detector.scan()
    
    if gamepads:
        for gp in gamepads:
            print(f"\n=== {gp.name} ===")
            print(f"Tipo: {get_controller_type_display_name(gp.controller_type)}")
            print(f"Botones: {gp.num_buttons}")
            print(f"Ejes: {gp.num_axes}")
            print(f"Mapeo PS2: {detector.get_button_mapping(gp)}")
    else:
        print("No se detectaron gamepads")
        
    detector.cleanup()
