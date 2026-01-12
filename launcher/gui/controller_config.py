"""
Controller Config - Configuración de mandos
"""
import customtkinter as ctk
from typing import Dict, Callable
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from core.emulator import ControllerConfig


class ControllerConfigWindow(ctk.CTkToplevel):
    """Ventana de configuración de mandos"""
    
    def __init__(self, parent, controller_config: ControllerConfig):
        super().__init__(parent)
        
        self.controller_config = controller_config
        self.waiting_for_key = None
        self.button_widgets = {}
        
        self.title("🎮 Configuración de Mandos")
        self.geometry("700x600")
        self.resizable(False, False)
        
        # Bind para capturar teclas
        self.bind("<Key>", self._on_key_press)
        
        self._create_ui()
        
    def _create_ui(self):
        """Crea la interfaz"""
        # Título
        header = ctk.CTkFrame(self, height=60, fg_color=("#1a1a2e", "#1a1a2e"))
        header.pack(fill="x")
        header.pack_propagate(False)
        
        title = ctk.CTkLabel(header, text="🎮 Configuración de Control",
                            font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=15)
        
        # Instrucciones
        info = ctk.CTkLabel(self, 
                           text="Haz clic en un botón y presiona la tecla que deseas asignar",
                           font=ctk.CTkFont(size=12),
                           text_color="#888")
        info.pack(pady=10)
        
        # Contenedor principal
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Frame izquierdo - D-Pad y Analógicos
        left_frame = ctk.CTkFrame(main_container, fg_color=("#16213e", "#16213e"),
                                  corner_radius=15)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Frame derecho - Botones de acción
        right_frame = ctk.CTkFrame(main_container, fg_color=("#16213e", "#16213e"),
                                   corner_radius=15)
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # === D-PAD ===
        self._create_section(left_frame, "D-Pad", [
            ('up', 'D-Pad ↑'),
            ('down', 'D-Pad ↓'),
            ('left', 'D-Pad ←'),
            ('right', 'D-Pad →'),
        ])
        
        # === STICK IZQUIERDO ===
        self._create_section(left_frame, "Stick Izquierdo", [
            ('left_analog_up', 'Stick ↑'),
            ('left_analog_down', 'Stick ↓'),
            ('left_analog_left', 'Stick ←'),
            ('left_analog_right', 'Stick →'),
        ])
        
        # === BOTONES DE ACCIÓN ===
        self._create_section(right_frame, "Botones", [
            ('cross', '✕ Cross'),
            ('circle', '○ Circle'),
            ('square', '□ Square'),
            ('triangle', '△ Triangle'),
        ])
        
        # === TRIGGERS Y BUMPERS ===
        self._create_section(right_frame, "Triggers", [
            ('l1', 'L1'),
            ('l2', 'L2'),
            ('r1', 'R1'),
            ('r2', 'R2'),
        ])
        
        # === OTROS ===
        other_frame = ctk.CTkFrame(self, fg_color=("#16213e", "#16213e"),
                                   corner_radius=15, height=80)
        other_frame.pack(fill="x", padx=20, pady=10)
        
        other_inner = ctk.CTkFrame(other_frame, fg_color="transparent")
        other_inner.pack(fill="x", padx=15, pady=10)
        
        buttons_row = [
            ('start', 'START'),
            ('select', 'SELECT'),
            ('l3', 'L3'),
            ('r3', 'R3'),
        ]
        
        for button_id, label in buttons_row:
            self._create_button_mapping(other_inner, button_id, label, horizontal=True)
            
        # Botones de acción
        action_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_frame.pack(fill="x", padx=20, pady=15)
        
        # Resetear
        reset_btn = ctk.CTkButton(
            action_frame, text="🔄 Restaurar Por Defecto",
            fg_color="#e74c3c",
            hover_color="#c0392b",
            command=self._reset_to_default
        )
        reset_btn.pack(side="left", padx=5)
        
        # Guardar
        save_btn = ctk.CTkButton(
            action_frame, text="💾 Guardar Cambios",
            fg_color="#00b894",
            hover_color="#00a884",
            command=self._save_and_close
        )
        save_btn.pack(side="right", padx=5)
        
    def _create_section(self, parent, title: str, buttons: list):
        """Crea una sección de botones"""
        section = ctk.CTkFrame(parent, fg_color="transparent")
        section.pack(fill="x", padx=15, pady=10)
        
        # Título de sección
        title_label = ctk.CTkLabel(section, text=title,
                                   font=ctk.CTkFont(size=14, weight="bold"),
                                   text_color="#00d4ff")
        title_label.pack(anchor="w", pady=(5, 10))
        
        # Botones
        for button_id, label in buttons:
            self._create_button_mapping(section, button_id, label)
            
    def _create_button_mapping(self, parent, button_id: str, label: str, horizontal: bool = False):
        """Crea un mapeo de botón"""
        if horizontal:
            frame = ctk.CTkFrame(parent, fg_color="transparent")
            frame.pack(side="left", padx=10, pady=5)
        else:
            frame = ctk.CTkFrame(parent, fg_color="transparent")
            frame.pack(fill="x", pady=3)
        
        # Label del botón
        if horizontal:
            lbl = ctk.CTkLabel(frame, text=label, font=ctk.CTkFont(size=11),
                              width=50, anchor="center")
            lbl.pack()
        else:
            lbl = ctk.CTkLabel(frame, text=label, font=ctk.CTkFont(size=12),
                              width=100, anchor="w")
            lbl.pack(side="left")
        
        # Botón de tecla asignada
        current_key = self.controller_config.get_mapping(button_id)
        btn = ctk.CTkButton(
            frame,
            text=current_key,
            width=80 if not horizontal else 60,
            height=30,
            fg_color=("#2d3436", "#2d3436"),
            hover_color=("#636e72", "#636e72"),
            command=lambda bid=button_id: self._start_key_capture(bid)
        )
        
        if horizontal:
            btn.pack(pady=5)
        else:
            btn.pack(side="right")
        
        self.button_widgets[button_id] = btn
        
    def _start_key_capture(self, button_id: str):
        """Inicia la captura de tecla para un botón"""
        # Resetear el botón anterior si existe
        if self.waiting_for_key and self.waiting_for_key in self.button_widgets:
            prev_key = self.controller_config.get_mapping(self.waiting_for_key)
            self.button_widgets[self.waiting_for_key].configure(
                text=prev_key,
                fg_color=("#2d3436", "#2d3436")
            )
        
        self.waiting_for_key = button_id
        self.button_widgets[button_id].configure(
            text="...",
            fg_color=("#e74c3c", "#e74c3c")
        )
        self.focus_set()
        
    def _on_key_press(self, event):
        """Maneja la presión de teclas"""
        if not self.waiting_for_key:
            return
            
        # Obtener nombre de la tecla
        key_name = event.keysym
        
        # Ignorar algunas teclas especiales
        if key_name in ['Escape']:
            # Cancelar
            prev_key = self.controller_config.get_mapping(self.waiting_for_key)
            self.button_widgets[self.waiting_for_key].configure(
                text=prev_key,
                fg_color=("#2d3436", "#2d3436")
            )
            self.waiting_for_key = None
            return
            
        # Asignar la tecla
        self.controller_config.set_mapping(self.waiting_for_key, key_name)
        
        # Actualizar UI
        self.button_widgets[self.waiting_for_key].configure(
            text=key_name,
            fg_color=("#00b894", "#00b894")
        )
        
        # Después de un momento, volver al color normal
        self.after(500, lambda bid=self.waiting_for_key: 
                  self.button_widgets[bid].configure(fg_color=("#2d3436", "#2d3436")))
        
        self.waiting_for_key = None
        
    def _reset_to_default(self):
        """Restaura los controles por defecto"""
        self.controller_config.reset_to_default()
        
        # Actualizar todos los botones
        for button_id, btn in self.button_widgets.items():
            key = self.controller_config.get_mapping(button_id)
            btn.configure(text=key)
            
    def _save_and_close(self):
        """Guarda y cierra"""
        self.controller_config.save_config()
        self.destroy()


if __name__ == "__main__":
    # Test
    root = ctk.CTk()
    root.withdraw()
    
    config = ControllerConfig()
    window = ControllerConfigWindow(root, config)
    window.mainloop()
