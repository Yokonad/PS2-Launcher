"""
Logger - Sistema de registro de errores y eventos
"""
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional
import traceback


class PS2LauncherLogger:
    """Sistema de logging para el PS2 Launcher"""
    
    def __init__(self, log_dir: str = None, name: str = "PS2Launcher"):
        self.name = name
        self.base_path = Path(__file__).parent.parent.parent
        self.log_dir = Path(log_dir) if log_dir else self.base_path / "logs"
        self.log_file = None
        self.logger = None
        self._callbacks = []
        
        self._setup_logger()
        
    def _setup_logger(self):
        """Configura el logger"""
        # Crear directorio de logs
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Nombre del archivo con fecha
        date_str = datetime.now().strftime("%Y-%m-%d")
        self.log_file = self.log_dir / f"ps2launcher_{date_str}.log"
        
        # Configurar logger
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.DEBUG)
        
        # Limpiar handlers existentes
        self.logger.handlers.clear()
        
        # Handler para archivo
        file_handler = logging.FileHandler(
            self.log_file, 
            encoding='utf-8',
            mode='a'
        )
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)
        self.logger.addHandler(file_handler)
        
        # Handler para consola
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            '%(levelname)s: %(message)s'
        )
        console_handler.setFormatter(console_format)
        self.logger.addHandler(console_handler)
        
        # Log inicial
        self.info("=" * 60)
        self.info(f"PS2 Launcher iniciado - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.info("=" * 60)
        
    def add_callback(self, callback):
        """Agrega un callback para recibir logs en tiempo real"""
        self._callbacks.append(callback)
        
    def remove_callback(self, callback):
        """Remueve un callback"""
        if callback in self._callbacks:
            self._callbacks.remove(callback)
            
    def _notify_callbacks(self, level: str, message: str):
        """Notifica a los callbacks"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        for callback in self._callbacks:
            try:
                callback(level, timestamp, message)
            except:
                pass
    
    def debug(self, message: str):
        """Log de debug"""
        self.logger.debug(message)
        self._notify_callbacks("DEBUG", message)
        
    def info(self, message: str):
        """Log de información"""
        self.logger.info(message)
        self._notify_callbacks("INFO", message)
        
    def warning(self, message: str):
        """Log de advertencia"""
        self.logger.warning(message)
        self._notify_callbacks("WARNING", message)
        
    def error(self, message: str, exc_info: bool = False):
        """Log de error"""
        self.logger.error(message, exc_info=exc_info)
        self._notify_callbacks("ERROR", message)
        
    def critical(self, message: str, exc_info: bool = True):
        """Log crítico"""
        self.logger.critical(message, exc_info=exc_info)
        self._notify_callbacks("CRITICAL", message)
        
    def exception(self, message: str):
        """Log de excepción con traceback"""
        self.logger.exception(message)
        tb = traceback.format_exc()
        self._notify_callbacks("ERROR", f"{message}\n{tb}")
        
    def log_system_info(self):
        """Registra información del sistema"""
        import platform
        
        self.info(f"Sistema: {platform.system()} {platform.release()}")
        self.info(f"Python: {platform.python_version()}")
        self.info(f"Arquitectura: {platform.machine()}")
        
    def get_recent_logs(self, count: int = 100) -> list:
        """Obtiene los últimos logs"""
        logs = []
        try:
            if self.log_file.exists():
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    logs = lines[-count:] if len(lines) > count else lines
        except Exception:
            pass
        return logs
    
    def get_log_file_path(self) -> Path:
        """Obtiene la ruta del archivo de log"""
        return self.log_file
    
    def clear_old_logs(self, days: int = 7):
        """Elimina logs antiguos"""
        try:
            cutoff = datetime.now().timestamp() - (days * 24 * 60 * 60)
            for log_file in self.log_dir.glob("ps2launcher_*.log"):
                if log_file.stat().st_mtime < cutoff:
                    log_file.unlink()
                    self.info(f"Log antiguo eliminado: {log_file.name}")
        except Exception as e:
            self.error(f"Error limpiando logs antiguos: {e}")


# Logger global
_logger: Optional[PS2LauncherLogger] = None


def get_logger() -> PS2LauncherLogger:
    """Obtiene el logger global"""
    global _logger
    if _logger is None:
        _logger = PS2LauncherLogger()
    return _logger


def setup_logger(log_dir: str = None) -> PS2LauncherLogger:
    """Configura y retorna el logger global"""
    global _logger
    _logger = PS2LauncherLogger(log_dir)
    return _logger


if __name__ == "__main__":
    # Test
    logger = get_logger()
    logger.log_system_info()
    logger.info("Test de información")
    logger.warning("Test de advertencia")
    logger.error("Test de error")
    
    try:
        raise ValueError("Error de prueba")
    except:
        logger.exception("Excepción capturada")
        
    print(f"\nLogs guardados en: {logger.get_log_file_path()}")
