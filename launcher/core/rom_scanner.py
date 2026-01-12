"""
ROM Scanner - Detecta y lee información de ROMs de PS2
"""
import os
from pathlib import Path
from typing import List, Dict, Optional
import struct


class ROMScanner:
    """Escanea carpetas en busca de ROMs de PS2"""
    
    SUPPORTED_EXTENSIONS = {'.iso', '.bin', '.cso', '.img'}
    
    def __init__(self, roms_path: str):
        self.roms_path = Path(roms_path)
        
    def scan(self) -> List[Dict]:
        """Escanea la carpeta de ROMs y retorna lista de juegos encontrados"""
        games = []
        
        if not self.roms_path.exists():
            return games
            
        for file_path in self.roms_path.iterdir():
            if file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS:
                game_info = self._extract_game_info(file_path)
                if game_info:
                    games.append(game_info)
                    
        return games
    
    def _extract_game_info(self, file_path: Path) -> Optional[Dict]:
        """Extrae información del juego desde el archivo ISO"""
        try:
            game_id = self._read_game_id(file_path)
            file_size = file_path.stat().st_size
            
            # Nombre limpio del archivo
            name = file_path.stem
            # Limpiar caracteres comunes en nombres de ROM
            name = name.replace('_', ' ').replace('.', ' ')
            
            return {
                'id': game_id or 'UNKNOWN',
                'name': name,
                'path': str(file_path),
                'size': file_size,
                'size_formatted': self._format_size(file_size),
                'extension': file_path.suffix.lower()
            }
        except Exception as e:
            print(f"Error leyendo {file_path}: {e}")
            return None
    
    def _read_game_id(self, file_path: Path) -> Optional[str]:
        """Lee el Game ID desde el ISO de PS2"""
        try:
            with open(file_path, 'rb') as f:
                # El system.cnf suele estar en el sector 12-16 del ISO
                # Buscamos el patrón BOOT2 que contiene el game ID
                f.seek(0)
                # Leer los primeros 2MB para buscar el ID
                data = f.read(2 * 1024 * 1024)
                
                # Buscar patrón de Game ID de PS2 (ej: SLUS_123.45)
                import re
                # Patrones comunes de Game ID de PS2
                patterns = [
                    rb'BOOT2\s*=\s*cdrom0:\\([A-Z]{4}_\d{3}\.\d{2})',
                    rb'([A-Z]{4}_\d{3}\.\d{2})',
                    rb'([A-Z]{4}-\d{5})'
                ]
                
                for pattern in patterns:
                    match = re.search(pattern, data)
                    if match:
                        game_id = match.group(1).decode('ascii', errors='ignore')
                        # Limpiar el ID
                        game_id = game_id.replace('\\', '').replace(';1', '')
                        return game_id
                        
        except Exception:
            pass
        return None
    
    def _format_size(self, size_bytes: int) -> str:
        """Formatea el tamaño en formato legible"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.2f} TB"


if __name__ == "__main__":
    # Test del scanner
    scanner = ROMScanner("../roms")
    games = scanner.scan()
    for game in games:
        print(f"Encontrado: {game['name']} ({game['id']}) - {game['size_formatted']}")
