"""
PS2 Launcher - Punto de entrada principal
==========================================
Ejecuta este archivo para iniciar el launcher.

Requisitos:
- Python 3.8+
- customtkinter

Instalación:
    pip install customtkinter

Uso:
    python main.py
"""
import sys
from pathlib import Path

# Configurar paths
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))

def check_dependencies():
    """Verifica que las dependencias estén instaladas"""
    missing = []
    
    try:
        import customtkinter
    except ImportError:
        missing.append("customtkinter")
    
    if missing:
        print("=" * 50)
        print("DEPENDENCIAS FALTANTES")
        print("=" * 50)
        print("\nPor favor, instala las siguientes dependencias:\n")
        print(f"    pip install {' '.join(missing)}")
        print("\n" + "=" * 50)
        return False
    
    return True


def main():
    """Función principal"""
    print("🎮 PS2 Launcher - Iniciando...")
    
    # Verificar dependencias
    if not check_dependencies():
        input("\nPresiona Enter para salir...")
        sys.exit(1)
    
    # Importar y ejecutar la aplicación
    try:
        from gui.main_window import PS2Launcher
        
        print("📀 Cargando interfaz...")
        app = PS2Launcher()
        app.mainloop()
        
    except Exception as e:
        print(f"\n❌ Error al iniciar: {e}")
        import traceback
        traceback.print_exc()
        input("\nPresiona Enter para salir...")
        sys.exit(1)


if __name__ == "__main__":
    main()
