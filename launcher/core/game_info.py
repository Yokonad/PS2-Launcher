"""
Game Info - Base de datos de juegos y configuraciones óptimas
"""
from typing import Dict, Optional
import json
from pathlib import Path


# Base de datos de juegos conocidos con configuraciones óptimas
GAMES_DATABASE = {
    # ==================== CRASH BANDICOOT SERIES ====================
    # Crash of the Titans - Todas las regiones
    "SLUS_216.64": {
        "name": "Crash of the Titans",
        "region": "NTSC-U",
        "developer": "Radical Entertainment",
        "year": 2007,
        "genre": "Action/Adventure",
        "config": {
            "renderer": "Vulkan",
            "internal_resolution": 3,  # 3x Native
            "anisotropic_filtering": 16,
            "texture_filtering": 2,  # Bilinear
            "vsync": True,
            "frame_limit": 60,
            "ee_cycle_rate": 0,
            "ee_cycle_skip": 0,
            "vu_cycle_stealing": 0,
            "mtvu": True,
            "game_fixes": ["VuAddSubHack"],
            "speedhacks": True
        }
    },
    "SLES_548.39": {
        "name": "Crash of the Titans",
        "region": "PAL",
        "developer": "Radical Entertainment",
        "year": 2007,
        "genre": "Action/Adventure",
        "config": {
            "renderer": "Vulkan",
            "internal_resolution": 3,
            "anisotropic_filtering": 16,
            "texture_filtering": 2,
            "vsync": True,
            "frame_limit": 50,  # PAL = 50Hz
            "ee_cycle_rate": 0,
            "ee_cycle_skip": 0,
            "vu_cycle_stealing": 0,
            "mtvu": True,
            "game_fixes": ["VuAddSubHack"],
            "speedhacks": True
        }
    },
    "SLES_548.40": {
        "name": "Crash of the Titans",
        "region": "PAL",
        "developer": "Radical Entertainment",
        "year": 2007,
        "genre": "Action/Adventure",
        "config": {
            "renderer": "Vulkan",
            "internal_resolution": 3,
            "anisotropic_filtering": 16,
            "texture_filtering": 2,
            "vsync": True,
            "frame_limit": 50,
            "ee_cycle_rate": 0,
            "ee_cycle_skip": 0,
            "vu_cycle_stealing": 0,
            "mtvu": True,
            "game_fixes": ["VuAddSubHack"],
            "speedhacks": True
        }
    },
    "SLES_548.41": {
        "name": "Crash of the Titans",
        "region": "PAL",
        "developer": "Radical Entertainment",
        "year": 2007,
        "genre": "Action/Adventure",
        "config": {
            "renderer": "Vulkan",
            "internal_resolution": 3,
            "anisotropic_filtering": 16,
            "texture_filtering": 2,
            "vsync": True,
            "frame_limit": 50,
            "ee_cycle_rate": 0,
            "ee_cycle_skip": 0,
            "vu_cycle_stealing": 0,
            "mtvu": True,
            "game_fixes": ["VuAddSubHack"],
            "speedhacks": True
        }
    },
    
    # ==================== GOD OF WAR SERIES ====================
    "SCUS_971.99": {
        "name": "God of War",
        "region": "NTSC-U",
        "developer": "Santa Monica Studio",
        "year": 2005,
        "genre": "Action/Adventure",
        "config": {
            "renderer": "Vulkan",
            "internal_resolution": 3,
            "anisotropic_filtering": 16,
            "texture_filtering": 2,
            "vsync": True,
            "frame_limit": 60,
            "ee_cycle_rate": 0,
            "ee_cycle_skip": 0,
            "vu_cycle_stealing": 0,
            "mtvu": True,
            "game_fixes": [],
            "speedhacks": True
        }
    },
    "SCUS_973.99": {
        "name": "God of War II",
        "region": "NTSC-U",
        "developer": "Santa Monica Studio",
        "year": 2007,
        "genre": "Action/Adventure",
        "config": {
            "renderer": "Vulkan",
            "internal_resolution": 3,
            "anisotropic_filtering": 16,
            "texture_filtering": 2,
            "vsync": True,
            "frame_limit": 60,
            "ee_cycle_rate": 0,
            "ee_cycle_skip": 0,
            "vu_cycle_stealing": 0,
            "mtvu": True,
            "game_fixes": [],
            "speedhacks": True
        }
    },
    
    # ==================== KINGDOM HEARTS ====================
    "SLUS_210.05": {
        "name": "Kingdom Hearts",
        "region": "NTSC-U",
        "developer": "Square Enix",
        "year": 2002,
        "genre": "Action RPG",
        "config": {
            "renderer": "Vulkan",
            "internal_resolution": 3,
            "anisotropic_filtering": 16,
            "texture_filtering": 2,
            "vsync": True,
            "frame_limit": 60,
            "ee_cycle_rate": 0,
            "ee_cycle_skip": 0,
            "vu_cycle_stealing": 0,
            "mtvu": True,
            "game_fixes": [],
            "speedhacks": True
        }
    },
    
    # ==================== FINAL FANTASY ====================
    "SLUS_203.12": {
        "name": "Final Fantasy X",
        "region": "NTSC-U",
        "developer": "Square Enix",
        "year": 2001,
        "genre": "RPG",
        "config": {
            "renderer": "Vulkan",
            "internal_resolution": 3,
            "anisotropic_filtering": 16,
            "texture_filtering": 2,
            "vsync": True,
            "frame_limit": 60,
            "ee_cycle_rate": 0,
            "ee_cycle_skip": 0,
            "vu_cycle_stealing": 0,
            "mtvu": True,
            "game_fixes": [],
            "speedhacks": True
        }
    },
    
    # ==================== SHADOW OF THE COLOSSUS ====================
    "SCUS_974.72": {
        "name": "Shadow of the Colossus",
        "region": "NTSC-U",
        "developer": "Team Ico",
        "year": 2005,
        "genre": "Action/Adventure",
        "config": {
            "renderer": "Vulkan",
            "internal_resolution": 2,  # Menor para estabilidad
            "anisotropic_filtering": 8,
            "texture_filtering": 2,
            "vsync": True,
            "frame_limit": 30,  # El juego corre a 30fps
            "ee_cycle_rate": -1,  # Underclock para bugs
            "ee_cycle_skip": 0,
            "vu_cycle_stealing": 0,
            "mtvu": False,  # Puede causar bugs
            "game_fixes": ["EETimingHack"],
            "speedhacks": True
        }
    },
    
    # ==================== RACHET & CLANK ====================
    "SCUS_971.99": {
        "name": "Ratchet & Clank",
        "region": "NTSC-U",
        "developer": "Insomniac Games",
        "year": 2002,
        "genre": "Platformer",
        "config": {
            "renderer": "Vulkan",
            "internal_resolution": 3,
            "anisotropic_filtering": 16,
            "texture_filtering": 2,
            "vsync": True,
            "frame_limit": 60,
            "ee_cycle_rate": 0,
            "ee_cycle_skip": 0,
            "vu_cycle_stealing": 0,
            "mtvu": True,
            "game_fixes": [],
            "speedhacks": True
        }
    },
}

# Configuración por defecto para juegos no reconocidos
DEFAULT_CONFIG = {
    "renderer": "Vulkan",
    "internal_resolution": 2,  # 2x Native - seguro para la mayoría
    "anisotropic_filtering": 8,
    "texture_filtering": 2,
    "vsync": True,
    "frame_limit": 60,
    "ee_cycle_rate": 0,
    "ee_cycle_skip": 0,
    "vu_cycle_stealing": 0,
    "mtvu": True,
    "game_fixes": [],
    "speedhacks": True
}

# Nombres legibles para las configuraciones
CONFIG_DISPLAY_NAMES = {
    "renderer": {
        "OpenGL": "OpenGL",
        "Vulkan": "Vulkan",
        "Direct3D 11": "Direct3D 11",
        "Direct3D 12": "Direct3D 12"
    },
    "internal_resolution": {
        1: "Native (PS2)",
        2: "2x Native (720p)",
        3: "3x Native (1080p)",
        4: "4x Native (1440p)",
        5: "5x Native",
        6: "6x Native (4K)"
    },
    "anisotropic_filtering": {
        0: "Off",
        2: "2x",
        4: "4x",
        8: "8x",
        16: "16x"
    },
    "texture_filtering": {
        0: "Nearest",
        1: "Bilinear (Forced)",
        2: "Bilinear (PS2)",
        3: "Bilinear (Forced excluding Sprites)"
    }
}


class GameInfo:
    """Gestiona información y configuraciones de juegos"""
    
    def __init__(self):
        self.database = GAMES_DATABASE
        self.custom_configs = {}
        self._load_custom_configs()
        
    def _load_custom_configs(self):
        """Carga configuraciones personalizadas guardadas"""
        config_path = Path(__file__).parent.parent.parent / "config" / "game_configs.json"
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    self.custom_configs = json.load(f)
            except:
                pass
                
    def save_custom_config(self, game_id: str, config: Dict):
        """Guarda una configuración personalizada para un juego"""
        config_path = Path(__file__).parent.parent.parent / "config"
        config_path.mkdir(parents=True, exist_ok=True)
        
        self.custom_configs[game_id] = config
        
        with open(config_path / "game_configs.json", 'w') as f:
            json.dump(self.custom_configs, f, indent=2)
        
    def get_game_info(self, game_id: str) -> Dict:
        """Obtiene info del juego por su ID"""
        # Normalizar ID (reemplazar - por _ y viceversa)
        normalized_id = game_id.replace('-', '_').replace('.', '.')
        
        if normalized_id in self.database:
            return self.database[normalized_id]
        
        # Intentar con variaciones del ID
        for db_id, info in self.database.items():
            if self._ids_match(game_id, db_id):
                return info
                
        return None
    
    def _ids_match(self, id1: str, id2: str) -> bool:
        """Compara dos Game IDs de forma flexible"""
        # Normalizar ambos IDs
        norm1 = id1.replace('-', '').replace('_', '').replace('.', '').upper()
        norm2 = id2.replace('-', '').replace('_', '').replace('.', '').upper()
        return norm1 == norm2
    
    def get_optimal_config(self, game_id: str) -> Dict:
        """Obtiene la configuración óptima para un juego"""
        # Primero revisar configuraciones personalizadas
        if game_id in self.custom_configs:
            return self.custom_configs[game_id]
            
        game_info = self.get_game_info(game_id)
        if game_info and 'config' in game_info:
            return game_info['config']
        return DEFAULT_CONFIG.copy()
    
    def get_game_name(self, game_id: str, fallback: str = None) -> str:
        """Obtiene el nombre del juego"""
        game_info = self.get_game_info(game_id)
        if game_info:
            return game_info.get('name', fallback or game_id)
        return fallback or game_id
    
    def get_region(self, game_id: str) -> str:
        """Obtiene la región del juego basada en el prefijo del ID"""
        prefix = game_id[:4].upper() if len(game_id) >= 4 else ""
        
        regions = {
            'SLUS': 'NTSC-U (USA)',
            'SCUS': 'NTSC-U (USA)',
            'SLPM': 'NTSC-J (Japan)',
            'SCPS': 'NTSC-J (Japan)',
            'SLES': 'PAL (Europe)',
            'SCES': 'PAL (Europe)',
            'SLKA': 'NTSC-K (Korea)',
        }
        
        return regions.get(prefix, 'Unknown')
    
    def get_config_display_value(self, key: str, value) -> str:
        """Obtiene el valor legible de una configuración"""
        if key in CONFIG_DISPLAY_NAMES and value in CONFIG_DISPLAY_NAMES[key]:
            return CONFIG_DISPLAY_NAMES[key][value]
        return str(value)


if __name__ == "__main__":
    # Test
    gi = GameInfo()
    print("=== SLES_548.41 ===")
    print(gi.get_game_info("SLES_548.41"))
    print("\n=== Config ===")
    print(gi.get_optimal_config("SLES_548.41"))
