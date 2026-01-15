"""
Main Window - Ventana principal del PS2 Launcher
Diseño minimalista - Blanco y Negro
"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
from pathlib import Path
import sys
import os

# Agregar el path del proyecto
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.rom_scanner import ROMScanner
from core.game_info import GameInfo
from core.emulator import EmulatorManager, ControllerConfig
from core.gamepad_detector import GamepadDetector, get_controller_type_display_name
from core.logger import get_logger, PS2LauncherLogger


# Paleta de colores - Blanco y Negro
COLORS = {
    'bg_dark': '#0a0a0a',
    'bg_medium': '#141414',
    'bg_light': '#1e1e1e',
    'bg_hover': '#2a2a2a',
    'text_primary': '#ffffff',
    'text_secondary': '#b0b0b0',
    'text_muted': '#666666',
    'accent': '#ffffff',
    'accent_hover': '#cccccc',
    'success': '#90EE90',
    'error': '#ff6b6b',
    'border': '#2a2a2a',
}


class PS2Launcher(ctk.CTk):
    """Ventana principal del PS2 Launcher"""
    
    def __init__(self):
        super().__init__()
        
        # Inicializar logger
        self.logger = get_logger()
        self.logger.log_system_info()
        
        # Configuración de la ventana
        self.title("PS2 Launcher")
        self.geometry("1000x600")
        self.minsize(900, 500)
        self.configure(fg_color=COLORS['bg_dark'])
        
        # Tema
        ctk.set_appearance_mode("dark")
        
        # Inicializar componentes
        self.base_path = Path(__file__).parent.parent.parent
        self.game_info = GameInfo()
        self.emulator = EmulatorManager(logger=self.logger)
        self.controller_config = ControllerConfig()
        
        # Cargar ruta de ROMs guardada o usar por defecto
        saved_roms_path = self.emulator.settings.get('roms_path')
        if saved_roms_path and Path(saved_roms_path).exists():
            self.roms_path = Path(saved_roms_path)
        else:
            self.roms_path = self.base_path / "roms"
        self.scanner = ROMScanner(str(self.roms_path))
        
        # Inicializar detector de gamepads
        self.gamepad_detector = GamepadDetector(logger=self.logger)
        self.gamepad_detector.initialize()
        
        # Lista de juegos
        self.games = []
        self.selected_game = None
        
        # Crear interfaz
        self._create_ui()
        
        # Cargar juegos
        self._load_games()
        
        # Verificar estado del emulador
        self._check_emulator()
        
        # Detectar gamepads
        self._detect_gamepads()
        
        # Iniciar monitoreo de gamepads
        self.gamepad_detector.start_monitoring(
            on_connected=self._on_gamepad_connected,
            on_disconnected=self._on_gamepad_disconnected
        )
        
        # Manejar cierre
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        
        self.logger.info("Launcher iniciado correctamente")
        
    def _on_close(self):
        self.logger.info("Cerrando launcher...")
        self.gamepad_detector.cleanup()
        self.destroy()
        
    def _create_ui(self):
        """Crea la interfaz de usuario"""
        # Container principal
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        self._create_header()
        
        # Contenido principal
        self.content = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.content.pack(fill="both", expand=True, pady=(20, 0))
        
        # Columna izquierda - Lista de juegos
        self._create_games_list()
        
        # Columna derecha - Detalles
        self._create_details_panel()
        
        # Footer
        self._create_footer()
        
    def _create_header(self):
        header = ctk.CTkFrame(self.main_container, fg_color="transparent", height=40)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        title = ctk.CTkLabel(
            header, 
            text="PS2 LAUNCHER",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COLORS['text_primary']
        )
        title.pack(side="left")
        
        btn_frame = ctk.CTkFrame(header, fg_color="transparent")
        btn_frame.pack(side="right")
        
        self.logs_btn = ctk.CTkButton(
            btn_frame,
            text="Logs",
            font=ctk.CTkFont(size=11),
            width=50,
            height=28,
            fg_color="transparent",
            hover_color=COLORS['bg_hover'],
            text_color=COLORS['text_secondary'],
            border_width=1,
            border_color=COLORS['border'],
            corner_radius=4,
            command=self._open_logs_window
        )
        self.logs_btn.pack(side="left", padx=4)
        
        self.settings_btn = ctk.CTkButton(
            btn_frame,
            text="Config",
            font=ctk.CTkFont(size=11),
            width=60,
            height=28,
            fg_color="transparent",
            hover_color=COLORS['bg_hover'],
            text_color=COLORS['text_secondary'],
            border_width=1,
            border_color=COLORS['border'],
            corner_radius=4,
            command=self._open_settings
        )
        self.settings_btn.pack(side="left", padx=4)
        
    def _create_games_list(self):
        left_container = ctk.CTkFrame(
            self.content, 
            fg_color=COLORS['bg_medium'],
            corner_radius=8,
            border_width=1,
            border_color=COLORS['border']
        )
        left_container.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        list_header = ctk.CTkFrame(left_container, fg_color="transparent", height=40)
        list_header.pack(fill="x", padx=16, pady=(16, 8))
        list_header.pack_propagate(False)
        
        list_title = ctk.CTkLabel(
            list_header,
            text="BIBLIOTECA",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=COLORS['text_muted']
        )
        list_title.pack(side="left")
        
        self.games_count = ctk.CTkLabel(
            list_header,
            text="0 juegos",
            font=ctk.CTkFont(size=10),
            text_color=COLORS['text_muted']
        )
        self.games_count.pack(side="right")
        
        self.games_scroll = ctk.CTkScrollableFrame(
            left_container, 
            fg_color="transparent",
            scrollbar_button_color=COLORS['bg_light'],
            scrollbar_button_hover_color=COLORS['bg_hover']
        )
        self.games_scroll.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        
    def _create_details_panel(self):
        self.right_container = ctk.CTkFrame(
            self.content,
            fg_color=COLORS['bg_medium'],
            corner_radius=8,
            border_width=1,
            border_color=COLORS['border'],
            width=340
        )
        self.right_container.pack(side="right", fill="y")
        self.right_container.pack_propagate(False)
        
        self.details_container = ctk.CTkFrame(self.right_container, fg_color="transparent")
        self.details_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Placeholder inicial
        self._show_placeholder()
        
    def _show_placeholder(self):
        for widget in self.details_container.winfo_children():
            widget.destroy()
        
        placeholder = ctk.CTkLabel(
            self.details_container,
            text="Selecciona un juego\nde la biblioteca",
            font=ctk.CTkFont(size=13),
            text_color=COLORS['text_muted'],
            justify="center"
        )
        placeholder.pack(expand=True)
        
    def _create_footer(self):
        footer = ctk.CTkFrame(self.main_container, fg_color="transparent", height=28)
        footer.pack(fill="x", pady=(16, 0))
        footer.pack_propagate(False)
        
        self.emulator_status = ctk.CTkLabel(
            footer,
            text="PCSX2: --",
            font=ctk.CTkFont(size=10),
            text_color=COLORS['text_muted']
        )
        self.emulator_status.pack(side="left")
        
        sep = ctk.CTkLabel(footer, text="|", text_color=COLORS['text_muted'], font=ctk.CTkFont(size=10))
        sep.pack(side="left", padx=10)
        
        self.gamepad_status = ctk.CTkLabel(
            footer,
            text="Mando: --",
            font=ctk.CTkFont(size=10),
            text_color=COLORS['text_muted']
        )
        self.gamepad_status.pack(side="left")
        
    def _load_games(self):
        self.logger.info(f"Escaneando ROMs en: {self.roms_path}")
        
        for widget in self.games_scroll.winfo_children():
            widget.destroy()
            
        try:
            self.games = self.scanner.scan()
            self.games_count.configure(text=f"{len(self.games)} juegos")
            self.logger.info(f"Encontrados {len(self.games)} juegos")
        except Exception as e:
            self.logger.error(f"Error escaneando ROMs: {e}")
            self.games = []
        
        if not self.games:
            no_games = ctk.CTkLabel(
                self.games_scroll,
                text=f"No hay juegos\n\nAgrega .iso a:\n{self.roms_path}",
                font=ctk.CTkFont(size=11),
                text_color=COLORS['text_muted'],
                justify="center"
            )
            no_games.pack(expand=True, pady=40)
            return
            
        for game in self.games:
            self._create_game_item(game)
            
    def _create_game_item(self, game: dict):
        item = ctk.CTkFrame(
            self.games_scroll,
            fg_color="transparent",
            height=55,
            corner_radius=4
        )
        item.pack(fill="x", pady=1, padx=4)
        item.pack_propagate(False)
        
        def on_enter(e):
            if self.selected_game != game:
                item.configure(fg_color=COLORS['bg_light'])
        
        def on_leave(e):
            if self.selected_game != game:
                item.configure(fg_color="transparent")
        
        item.bind("<Enter>", on_enter)
        item.bind("<Leave>", on_leave)
        item.bind("<Button-1>", lambda e: self._select_game(game))
        item.bind("<Double-Button-1>", lambda e: self._launch_game())
        
        content = ctk.CTkFrame(item, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=12, pady=8)
        content.bind("<Button-1>", lambda e: self._select_game(game))
        
        display_name = self.game_info.get_game_name(game['id'], game['name'])
        name_label = ctk.CTkLabel(
            content,
            text=display_name,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=COLORS['text_primary'],
            anchor="w"
        )
        name_label.pack(fill="x")
        name_label.bind("<Button-1>", lambda e: self._select_game(game))
        
        region = self.game_info.get_region(game['id'])
        info_text = f"{game['id']}  |  {region}  |  {game['size_formatted']}"
        info_label = ctk.CTkLabel(
            content,
            text=info_text,
            font=ctk.CTkFont(size=10),
            text_color=COLORS['text_muted'],
            anchor="w"
        )
        info_label.pack(fill="x")
        info_label.bind("<Button-1>", lambda e: self._select_game(game))
        
        game['_item'] = item
        
    def _select_game(self, game: dict):
        if self.selected_game and '_item' in self.selected_game:
            self.selected_game['_item'].configure(fg_color="transparent")
            
        self.selected_game = game
        if '_item' in game:
            game['_item'].configure(fg_color=COLORS['bg_hover'])
            
        self._show_game_details(game)
        self.logger.debug(f"Juego seleccionado: {game['name']}")
        
    def _show_game_details(self, game: dict):
        for widget in self.details_container.winfo_children():
            widget.destroy()
            
        # Nombre del juego
        display_name = self.game_info.get_game_name(game['id'], game['name'])
        name = ctk.CTkLabel(
            self.details_container,
            text=display_name,
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLORS['text_primary'],
            wraplength=290,
            justify="left",
            anchor="w"
        )
        name.pack(fill="x", pady=(0, 16))
        
        # Info
        info_frame = ctk.CTkFrame(self.details_container, fg_color="transparent")
        info_frame.pack(fill="x")
        
        info_items = [
            ("ID", game['id']),
            ("Region", self.game_info.get_region(game['id'])),
            ("Tamano", game['size_formatted']),
        ]
        
        db_info = self.game_info.get_game_info(game['id'])
        if db_info:
            if 'developer' in db_info:
                info_items.append(("Desarrollador", db_info['developer']))
            if 'year' in db_info:
                info_items.append(("Ano", str(db_info['year'])))
        
        for label, value in info_items:
            row = ctk.CTkFrame(info_frame, fg_color="transparent")
            row.pack(fill="x", pady=2)
            
            lbl = ctk.CTkLabel(
                row,
                text=label,
                font=ctk.CTkFont(size=10),
                text_color=COLORS['text_muted'],
                width=90,
                anchor="w"
            )
            lbl.pack(side="left")
            
            val = ctk.CTkLabel(
                row,
                text=value,
                font=ctk.CTkFont(size=11),
                text_color=COLORS['text_secondary'],
                anchor="w"
            )
            val.pack(side="left", fill="x", expand=True)
            
        # Mando
        if self.gamepad_detector.active_gamepad:
            gp = self.gamepad_detector.active_gamepad
            
            controller_frame = ctk.CTkFrame(
                self.details_container,
                fg_color=COLORS['bg_light'],
                corner_radius=4
            )
            controller_frame.pack(fill="x", pady=(14, 0))
            
            controller_info = ctk.CTkFrame(controller_frame, fg_color="transparent")
            controller_info.pack(fill="x", padx=12, pady=10)
            
            controller_title = ctk.CTkLabel(
                controller_info,
                text=get_controller_type_display_name(gp.controller_type),
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=COLORS['text_primary'],
                anchor="w"
            )
            controller_title.pack(fill="x")
            
            controller_status = ctk.CTkLabel(
                controller_info,
                text="Configurado como mando PS2",
                font=ctk.CTkFont(size=9),
                text_color=COLORS['success'],
                anchor="w"
            )
            controller_status.pack(fill="x")
        
        # BOTON JUGAR (al final, sin spacer)
        play_btn = ctk.CTkButton(
            self.details_container,
            text="JUGAR",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=46,
            fg_color=COLORS['text_primary'],
            hover_color=COLORS['accent_hover'],
            text_color=COLORS['bg_dark'],
            corner_radius=8,
            border_width=2,
            border_color=COLORS['accent'],
            command=self._launch_game
        )
        play_btn.pack(fill="x", pady=(20, 0), side="bottom")
        
    def _launch_game(self):
        if not self.selected_game:
            messagebox.showwarning("Aviso", "Selecciona un juego primero")
            return
            
        game = self.selected_game
        self.logger.info(f"Lanzando juego: {game['name']}")
            
        if not self.emulator.is_configured():
            self.logger.error("PCSX2 no configurado")
            messagebox.showerror("Error", "PCSX2 no esta configurado.\nVe a Config para establecer la ruta.")
            return
            
        config = self.game_info.get_optimal_config(game['id'])
        
        try:
            success = self.emulator.launch_game(game['path'], config)
            if success:
                self.logger.info("Juego lanzado exitosamente")
            else:
                self.logger.error("Error al lanzar el juego")
                messagebox.showerror("Error", "No se pudo iniciar el juego")
        except Exception as e:
            self.logger.exception(f"Excepcion lanzando juego: {e}")
            messagebox.showerror("Error", f"Error: {e}")
            
    def _detect_gamepads(self):
        try:
            gamepads = self.gamepad_detector.scan()
            self._update_gamepad_status(gamepads)
            # Aplicar configuración automática si hay un mando conectado
            if gamepads and self.gamepad_detector.active_gamepad:
                if self.gamepad_detector.apply_pcsx2_config():
                    self.logger.info("Configuración de mando aplicada automáticamente a PCSX2")
        except Exception as e:
            self.logger.error(f"Error detectando gamepads: {e}")
            
    def _update_gamepad_status(self, gamepads=None):
        if gamepads is None:
            gamepads = self.gamepad_detector.gamepads
            
        if gamepads:
            active = self.gamepad_detector.active_gamepad
            if active:
                type_name = get_controller_type_display_name(active.controller_type)
                self.gamepad_status.configure(
                    text=f"Mando: {type_name}",
                    text_color=COLORS['success']
                )
        else:
            self.gamepad_status.configure(
                text="Mando: No detectado",
                text_color=COLORS['text_muted']
            )
            
    def _on_gamepad_connected(self, gamepad):
        self.logger.info(f"Gamepad conectado: {gamepad.name}")
        # Aplicar configuración automática a PCSX2
        if self.gamepad_detector.apply_pcsx2_config():
            self.logger.info("Configuración de mando aplicada automáticamente a PCSX2")
        self.after(0, lambda: self._update_gamepad_status())
        
    def _on_gamepad_disconnected(self):
        self.logger.warning("Gamepad desconectado")
        self.after(0, lambda: self._update_gamepad_status())
        
    def _check_emulator(self):
        if self.emulator.is_configured():
            self.emulator_status.configure(
                text="PCSX2: Listo",
                text_color=COLORS['success']
            )
        elif self.emulator.detect_pcsx2():
            self.emulator_status.configure(
                text="PCSX2: Detectado",
                text_color=COLORS['success']
            )
        else:
            self.emulator_status.configure(
                text="PCSX2: No detectado",
                text_color=COLORS['error']
            )
            
    def _open_settings(self):
        settings_window = SettingsWindow(self, self.emulator, self.roms_path, self.logger)
        settings_window.grab_set()
        
    def _open_logs_window(self):
        logs_window = LogsWindow(self, self.logger)
        logs_window.grab_set()


class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, parent, emulator: EmulatorManager, roms_path: Path, logger):
        super().__init__(parent)
        
        self.emulator = emulator
        self.roms_path = roms_path
        self.logger = logger
        
        self.title("Configuracion")
        self.geometry("500x320")
        self.resizable(False, False)
        self.configure(fg_color=COLORS['bg_dark'])
        
        self._create_ui()
        
    def _create_ui(self):
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=28, pady=28)
        
        title = ctk.CTkLabel(
            container,
            text="CONFIGURACION",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=COLORS['text_muted']
        )
        title.pack(anchor="w", pady=(0, 20))
        
        pcsx2_label = ctk.CTkLabel(
            container,
            text="Ruta de PCSX2",
            font=ctk.CTkFont(size=11),
            text_color=COLORS['text_secondary']
        )
        pcsx2_label.pack(anchor="w", pady=(0, 4))
        
        path_frame = ctk.CTkFrame(container, fg_color="transparent")
        path_frame.pack(fill="x", pady=(0, 14))
        
        pcsx2_path = str(self.emulator.pcsx2_path) if self.emulator.pcsx2_path else "No configurado"
        self.pcsx2_entry = ctk.CTkEntry(
            path_frame,
            font=ctk.CTkFont(size=11),
            fg_color=COLORS['bg_medium'],
            border_color=COLORS['border'],
            text_color=COLORS['text_primary'],
            height=34
        )
        self.pcsx2_entry.insert(0, pcsx2_path)
        self.pcsx2_entry.pack(side="left", fill="x", expand=True, padx=(0, 6))
        
        browse_btn = ctk.CTkButton(
            path_frame,
            text="...",
            width=36,
            height=34,
            fg_color=COLORS['bg_light'],
            hover_color=COLORS['bg_hover'],
            text_color=COLORS['text_primary'],
            command=self._browse_pcsx2
        )
        browse_btn.pack(side="right")
        
        roms_label = ctk.CTkLabel(
            container,
            text="Carpeta de ROMs",
            font=ctk.CTkFont(size=11),
            text_color=COLORS['text_secondary']
        )
        roms_label.pack(anchor="w", pady=(0, 4))
        
        roms_frame = ctk.CTkFrame(container, fg_color="transparent")
        roms_frame.pack(fill="x", pady=(0, 20))
        
        self.roms_entry = ctk.CTkEntry(
            roms_frame,
            font=ctk.CTkFont(size=11),
            fg_color=COLORS['bg_medium'],
            border_color=COLORS['border'],
            text_color=COLORS['text_primary'],
            height=34
        )
        self.roms_entry.insert(0, str(self.roms_path))
        self.roms_entry.pack(side="left", fill="x", expand=True, padx=(0, 6))
        
        browse_roms_btn = ctk.CTkButton(
            roms_frame,
            text="...",
            width=36,
            height=34,
            fg_color=COLORS['bg_light'],
            hover_color=COLORS['bg_hover'],
            text_color=COLORS['text_primary'],
            command=self._browse_roms
        )
        browse_roms_btn.pack(side="right")
        
        btn_frame = ctk.CTkFrame(container, fg_color="transparent")
        btn_frame.pack(fill="x")
        
        detect_btn = ctk.CTkButton(
            btn_frame,
            text="Auto-detectar",
            height=36,
            fg_color="transparent",
            hover_color=COLORS['bg_hover'],
            text_color=COLORS['text_secondary'],
            border_width=1,
            border_color=COLORS['border'],
            command=self._auto_detect
        )
        detect_btn.pack(side="left", fill="x", expand=True, padx=(0, 6))
        
        save_btn = ctk.CTkButton(
            btn_frame,
            text="Guardar",
            height=36,
            fg_color=COLORS['text_primary'],
            hover_color=COLORS['accent_hover'],
            text_color=COLORS['bg_dark'],
            corner_radius=8,
            command=self._save
        )
        save_btn.pack(side="right", fill="x", expand=True)
        
    def _browse_pcsx2(self):
        path = filedialog.askopenfilename(
            title="Seleccionar PCSX2",
            filetypes=[("Ejecutable", "*.exe")]
        )
        if path:
            self.pcsx2_entry.delete(0, "end")
            self.pcsx2_entry.insert(0, path)
    
    def _browse_roms(self):
        path = filedialog.askdirectory(
            title="Seleccionar carpeta de ROMs"
        )
        if path:
            self.roms_entry.delete(0, "end")
            self.roms_entry.insert(0, path)
            
    def _auto_detect(self):
        if self.emulator.detect_pcsx2():
            self.pcsx2_entry.delete(0, "end")
            self.pcsx2_entry.insert(0, str(self.emulator.pcsx2_path))
            messagebox.showinfo("Exito", "PCSX2 detectado")
        else:
            messagebox.showwarning("Aviso", "No se encontro PCSX2")
            
    def _save(self):
        # Guardar ruta de PCSX2
        pcsx2_path = self.pcsx2_entry.get()
        if pcsx2_path and pcsx2_path != "No configurado":
            if not self.emulator.set_pcsx2_path(pcsx2_path):
                messagebox.showerror("Error", "Ruta de PCSX2 invalida")
                return
        
        # Guardar ruta de ROMs
        roms_path = self.roms_entry.get()
        if roms_path:
            new_roms_path = Path(roms_path)
            if new_roms_path.exists() and new_roms_path.is_dir():
                # Actualizar la ruta en el launcher principal
                self.master.roms_path = new_roms_path
                self.master.scanner = ROMScanner(str(new_roms_path))
                # Guardar en settings
                self.emulator.settings['roms_path'] = str(new_roms_path)
                self.emulator.save_settings()
                # Recargar juegos
                self.master._load_games()
                self.logger.info(f"Carpeta de ROMs actualizada: {new_roms_path}")
            else:
                messagebox.showerror("Error", "La carpeta de ROMs no existe")
                return
        
        self.master._check_emulator()
        self.destroy()


class LogsWindow(ctk.CTkToplevel):
    def __init__(self, parent, logger: PS2LauncherLogger):
        super().__init__(parent)
        
        self.logger = logger
        
        self.title("Logs")
        self.geometry("600x400")
        self.configure(fg_color=COLORS['bg_dark'])
        
        self._create_ui()
        self._load_logs()
        
        self.logger.add_callback(self._on_new_log)
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        
    def _on_close(self):
        self.logger.remove_callback(self._on_new_log)
        self.destroy()
        
    def _create_ui(self):
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=16, pady=16)
        
        header = ctk.CTkFrame(container, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10))
        
        title = ctk.CTkLabel(
            header,
            text="LOGS",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=COLORS['text_muted']
        )
        title.pack(side="left")
        
        clear_btn = ctk.CTkButton(
            header,
            text="Limpiar",
            width=60,
            height=26,
            fg_color="transparent",
            hover_color=COLORS['bg_hover'],
            text_color=COLORS['text_secondary'],
            border_width=1,
            border_color=COLORS['border'],
            font=ctk.CTkFont(size=10),
            command=self._clear
        )
        clear_btn.pack(side="right")
        
        self.logs_text = ctk.CTkTextbox(
            container,
            font=ctk.CTkFont(family="Consolas", size=10),
            fg_color=COLORS['bg_medium'],
            text_color=COLORS['text_secondary'],
            border_width=1,
            border_color=COLORS['border'],
            wrap="word"
        )
        self.logs_text.pack(fill="both", expand=True)
        
    def _load_logs(self):
        self.logs_text.configure(state="normal")
        self.logs_text.delete("1.0", "end")
        
        logs = self.logger.get_recent_logs(100)
        for line in logs:
            self.logs_text.insert("end", line)
            
        self.logs_text.configure(state="disabled")
        self.logs_text.see("end")
        
    def _on_new_log(self, level, timestamp, message):
        line = f"{timestamp} | {level:8} | {message}\n"
        self.logs_text.configure(state="normal")
        self.logs_text.insert("end", line)
        self.logs_text.configure(state="disabled")
        self.logs_text.see("end")
        
    def _clear(self):
        self.logs_text.configure(state="normal")
        self.logs_text.delete("1.0", "end")
        self.logs_text.configure(state="disabled")


if __name__ == "__main__":
    app = PS2Launcher()
    app.mainloop()
