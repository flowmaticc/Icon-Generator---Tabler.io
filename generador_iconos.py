import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, colorchooser
import os
import requests
import cairosvg
from PIL import Image, ImageTk
import io
import threading
import webbrowser
import json
import re

# ===== CONFIGURACIÓN =====
# ===== IDIOMAS =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICONS_DIR = os.path.join(BASE_DIR, "icons")
CONFIG_FILE = os.path.join(BASE_DIR, "generator_config.json")
LANGUAGE_DIR = os.path.join(BASE_DIR, "language")
os.makedirs(ICONS_DIR, exist_ok=True)
os.makedirs(LANGUAGE_DIR, exist_ok=True)

def discover_languages():
    """Detecta automáticamente todos los JSON de la carpeta language."""
    languages = {}
    if not os.path.isdir(LANGUAGE_DIR):
        return languages
    for filename in sorted(os.listdir(LANGUAGE_DIR)):
        if filename.lower().endswith(".json"):
            try:
                with open(os.path.join(LANGUAGE_DIR, filename), "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, dict):
                    languages[os.path.splitext(filename)[0]] = data
            except (OSError, json.JSONDecodeError):
                pass
    return languages

# Colores
BG = "#1e1e1e"
FG = "#d4d4d4"
ACCENT = "#caff33"
SURFACE = "#2d2d2d"
BORDER = "#3d3d3d"

class IconGeneratorApp:
    def __init__(self, root):
        self.root = root

        # ===== CARGAR IDIOMAS Y CONFIGURACIÓN =====
        self.languages = discover_languages()

        if not self.languages:
            raise RuntimeError(
                f"No se encontraron archivos JSON de idioma en: {LANGUAGE_DIR}"
            )

        self.config = self.load_config()

        saved_language = self.config.get("language", "es")
        if saved_language in self.languages:
            self.current_language = saved_language
        elif "es" in self.languages:
            self.current_language = "es"
        else:
            self.current_language = next(iter(self.languages))

        self.language_data = self.languages[self.current_language]

        root.title(self.t("app.title"))
        root.geometry("1400x850")
        root.configure(bg=BG)

        # ===== ICONOS BASE (PROTEGIDOS) =====
        self.base_icons = [
            "pencil", "list", "settings", "chart-bar", "books",
            "plus", "edit", "trash", "search", "chevron-right",
            "download", "folder", "file"
        ]
        
        # ===== ICONOS DISPONIBLES =====
        if "icon_names" in self.config and self.config["icon_names"]:
            self.icon_names = self.config["icon_names"]
        else:
            base_icons = self.base_icons.copy()
            otros_iconos = [
                "home", "user", "bell", "heart", "star", "mail", 
                "calendar", "clock", "map-pin", "phone", "camera", 
                "video", "music", "book", "briefcase", "shield", 
                "lock", "unlock", "eye", "eye-off", "message"
            ]
            self.icon_names = base_icons + otros_iconos
        
        # ===== LISTA COMPLETA DE ICONOS TABLER =====
        self.tabler_icons_complete = [
            "pencil", "pencil-off", "pencil-plus", "pencil-minus", "pencil-filled",
            "list", "list-check", "list-numbers", "list-tree",
            "settings", "settings-2", "settings-cog", "settings-automation",
            "chart-bar", "chart-bar-off", "chart-pie", "chart-line",
            "books", "book", "book-2", "book-off", "book-plus",
            "plus", "minus", "x", "check", "search", "search-off",
            "zoom-in", "zoom-out", "chevron-right", "chevron-left",
            "chevron-up", "chevron-down", "download", "upload",
            "folder", "folder-plus", "folder-minus", "folder-off",
            "file", "file-plus", "file-minus", "file-off",
            "home", "home-2", "home-off", "house",
            "user", "users", "user-plus", "user-minus", "user-check",
            "bell", "bell-off", "bell-plus", "bell-ringing",
            "heart", "heart-off", "heart-plus", "heart-minus", "heart-filled",
            "star", "star-off", "star-half", "star-filled",
            "mail", "mail-off", "mail-plus", "mail-minus",
            "calendar", "calendar-off", "calendar-plus", "calendar-event",
            "clock", "clock-off", "clock-plus", "alarm",
            "map-pin", "map", "map-off", "location",
            "phone", "phone-off", "phone-call", "phone-plus",
            "camera", "camera-off", "camera-plus", "video",
            "video-off", "music", "music-off", "headphones",
            "briefcase", "briefcase-off", "shield", "shield-off",
            "lock", "lock-off", "lock-open", "lock-plus",
            "unlock", "eye", "eye-off", "eye-plus",
            "message", "message-off", "message-plus", "message-2",
            "send", "plane", "plane-off", "paperclip",
            "tag", "tag-off", "tags", "share", "share-off",
            "link", "link-off", "external-link", "arrow-right",
            "arrow-left", "arrow-up", "arrow-down", "arrow-bar-right",
            "brand-github", "brand-git", "brand-instagram", "brand-twitter",
            "brand-facebook", "brand-youtube", "brand-linkedin", "brand-twitch",
            "brand-discord", "brand-slack", "brand-figma", "brand-sketch",
            "brand-photoshop", "brand-illustrator", "brand-adobe",
            "brand-apple", "brand-android", "brand-windows", "brand-linux",
            "brand-chrome", "brand-firefox", "brand-edge",
            "moon", "sun", "cloud", "cloud-off", "cloud-rain",
            "snowflake", "wind", "droplet", "fire",
            "lightbulb", "bulb", "trash", "trash-off",
            "archive", "archive-off", "box", "box-off",
            "cube", "cube-off", "package", "package-off",
            "gift", "gift-off", "award", "award-off",
            "trophy", "trophy-off", "medal", "medal-off",
            "currency-dollar", "currency-euro", "currency-pound", "currency-yen",
            "percent", "discount", "discount-off"
        ]
        
        # ===== COLORES =====
        if "custom_colors" in self.config and self.config["custom_colors"]:
            self.color_options = self.config["custom_colors"]
        else:
            self.color_options = {
                "accent": "#caff33",
                "muted": "#898983",
                "text": "#f4f4ef",
                "red": "#ff4444",
                "green": "#4caf50",
                "blue": "#2196f3",
                "orange": "#ff9800",
                "purple": "#9c27b0",
                "pink": "#e91e63",
                "teal": "#009688",
                "yellow": "#ffeb3b",
                "cyan": "#00bcd4",
                "white": "#ffffff",
                "black": "#000000"
            }
        
        # ===== COLORES DE FONDO =====
        self.bg_options = {
            "black": "#000000",
            "white": "#ffffff",
            "dark_gray": "#1a1a1a",
            "light_gray": "#e0e0e0",
            "surface": "#2d2d2d",
        }
        for name, hex_color in self.color_options.items():
            self.bg_options[f"color:{name}"] = hex_color
        
        # ===== TAMAÑOS =====
        self.size_options = [12, 14, 16, 18, 20, 22, 24, 28, 32, 36, 40, 48, 56, 64, 72, 80, 96, 128]
        
        # ===== STROKES =====
        self.stroke_options = [1, 2, 3, 4, 5]
        
        # ===== VARIABLES =====
        self.preview_icon = tk.StringVar(value=self.config.get("preview_icon", "pencil"))
        self.preview_size = tk.IntVar(value=self.config.get("preview_size", 48))
        self.preview_color = tk.StringVar(value=self.config.get("preview_color", "#caff33"))
        self.preview_stroke = tk.IntVar(value=self.config.get("preview_stroke", 2))
        self.preview_bg_color = tk.StringVar(value=self.config.get("preview_bg", "#1a1a1a"))
        self.search_text = tk.StringVar()
        
        # ===== CACHÉ =====
        self.icon_cache = {}
        self.icon_thumbnails = {}
        self.icons_loaded = False
        
        # ===== VARS =====
        self.size_vars = {}
        self.color_vars = {}
        self.stroke_vars = {}
        self.icon_check_vars = {}

        # Selección persistente de iconos.
        # En un primer arranque se seleccionan todos los iconos por defecto.
        config_selected_icons = self.config.get("selected_icons")
        self.has_saved_icon_selection = isinstance(config_selected_icons, list)
        if self.has_saved_icon_selection:
            self.selected_icon_names = {icon for icon in config_selected_icons if icon in self.icon_names}
        else:
            self.selected_icon_names = set(self.icon_names)

        # Estado del placeholder del buscador.
        self.search_placeholder = self.t("search.placeholder")
        self.search_placeholder_active = True
        
        # ===== UI =====
        self.setup_ui()
        
        # ===== DESCARGAR ICONOS Y LUEGO ACTUALIZAR PANEL =====
        self.root.after(100, self.download_all_icons)
        
        # ===== GUARDAR CONFIGURACIÓN AL CERRAR =====
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def t(self, key, **kwargs):
        """Obtiene una traducción usando claves anidadas, por ejemplo 'app.title'."""
        def get_nested(data, dotted_key):
            value = data
            for part in dotted_key.split("."):
                if not isinstance(value, dict) or part not in value:
                    return None
                value = value[part]
            return value

        value = get_nested(self.language_data, key)

        # Si falta en el idioma actual, utilizar español como fallback.
        if value is None and "es" in self.languages:
            value = get_nested(self.languages["es"], key)

        if value is None:
            value = key

        if not isinstance(value, str):
            return value

        if kwargs:
            try:
                return value.format(**kwargs)
            except (KeyError, IndexError, ValueError):
                pass

        return value

    def language_name(self, code):
        return self.languages.get(code, {}).get("_language_name", code)

    def change_language(self, language_code):
        if language_code not in self.languages:
            return
        self.current_language = language_code
        self.language_data = self.languages[language_code]
        self.config["language"] = language_code
        self.save_config()
        self.rebuild_ui()

    def rebuild_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.size_vars = {}
        self.color_vars = {}
        self.stroke_vars = {}
        self.icon_check_vars = {}
        self.icon_buttons = {}
        self.icon_frames = {}
        self.search_placeholder = self.t("search.placeholder")
        self.search_placeholder_active = True
        self.setup_ui()
        self.root.after(50, self.create_icon_buttons)
        self.root.after(100, self.update_preview)
        self.root.after(150, self.update_gen_info)

    def load_config(self):
        """Cargar configuración desde archivo JSON"""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_config(self):
        """Guardar configuración a archivo JSON"""
        config = {
            "language": self.current_language,
            "icon_names": self.icon_names,
            "custom_colors": self.color_options,
            "preview_icon": self.preview_icon.get(),
            "preview_size": self.preview_size.get(),
            "preview_color": self.preview_color.get(),
            "preview_stroke": self.preview_stroke.get(),
            "preview_bg": self.preview_bg_color.get(),
        }
        
        try:
            config["selected_icons"] = [icon for icon in self.icon_names if icon in self.selected_icon_names]
        except:
            config["selected_icons"] = list(self.icon_names)
        
        try:
            if hasattr(self, 'size_vars'):
                config["selected_sizes"] = [s for s, var in self.size_vars.items() if var.get()]
        except:
            pass
        
        try:
            if hasattr(self, 'color_vars'):
                config["selected_colors"] = [name for name, var in self.color_vars.items() if var.get()]
        except:
            pass
        
        try:
            if hasattr(self, 'stroke_vars'):
                config["selected_strokes"] = [s for s, var in self.stroke_vars.items() if var.get()]
        except:
            pass
        
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except:
            pass
    
    def on_closing(self):
        """Guardar configuración y cerrar"""
        self.save_config()
        self.root.destroy()
    
    def setup_ui(self):
        """Crear interfaz completa"""
        
        # ===== PANEL PRINCIPAL =====
        main_frame = tk.Frame(self.root, bg=BG)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ===== PANEL IZQUIERDO =====
        left_panel = tk.Frame(main_frame, bg=SURFACE, relief=tk.FLAT, bd=1, width=520)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 5))
        left_panel.pack_propagate(False)
        
        # --- Previsualización ---
        preview_frame = tk.LabelFrame(left_panel, text=self.t("ui.preview"), bg=SURFACE, fg=FG, font=("Consolas", 10))
        preview_frame.pack(fill=tk.X, padx=8, pady=8)
        
        self.preview_canvas = tk.Canvas(preview_frame, bg="#1a1a1a", height=160, relief=tk.FLAT, bd=1)
        self.preview_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.preview_canvas.bind('<Configure>', lambda e: self.update_preview())
        
        # --- Controles ---
        controls = tk.Frame(left_panel, bg=SURFACE)
        controls.pack(fill=tk.X, padx=8, pady=5)
        
        # Tamaño
        tk.Label(controls, text=self.t("ui.size"), bg=SURFACE, fg=FG, font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=2)
        scale = tk.Scale(controls, from_=12, to=128, orient=tk.HORIZONTAL, 
                         variable=self.preview_size, bg=SURFACE, fg=FG, 
                         highlightthickness=0, length=180,
                         command=lambda x: self.update_all_previews())
        scale.grid(row=0, column=1, padx=5, pady=2)
        tk.Label(controls, textvariable=self.preview_size, bg=SURFACE, fg=ACCENT, font=("Consolas", 10)).grid(row=0, column=2, padx=5)
        
        # Color del icono
        tk.Label(controls, text=self.t("ui.color"), bg=SURFACE, fg=FG, font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=2)
        self.color_combo = ttk.Combobox(controls, values=[self.color_label(name) for name in self.color_options], state="readonly", width=14)
        self.color_combo.set(self.color_label("accent"))
        self.color_combo.grid(row=1, column=1, padx=5, pady=2)
        self.color_combo.bind('<<ComboboxSelected>>', self.on_color_change)
        
        self.color_indicator = tk.Canvas(controls, width=20, height=20, bg=SURFACE, highlightthickness=1, highlightbackground=BORDER)
        self.color_indicator.grid(row=1, column=2, padx=5, pady=2)
        self.color_indicator.create_rectangle(2, 2, 18, 18, fill="#caff33", outline="")
        
        # Color de fondo
        tk.Label(controls, text=self.t("ui.background"), bg=SURFACE, fg=FG, font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=2)
        self.bg_combo = ttk.Combobox(controls, values=[self.background_label(name) for name in self.bg_options], state="readonly", width=14)
        self.bg_combo.set(self.background_label("dark_gray"))
        self.bg_combo.grid(row=2, column=1, padx=5, pady=2)
        self.bg_combo.bind('<<ComboboxSelected>>', self.on_bg_change)
        
        self.bg_indicator = tk.Canvas(controls, width=20, height=20, bg=SURFACE, highlightthickness=1, highlightbackground=BORDER)
        self.bg_indicator.grid(row=2, column=2, padx=5, pady=2)
        self.bg_indicator.create_rectangle(2, 2, 18, 18, fill="#1a1a1a", outline="")
        
        # Stroke
        tk.Label(controls, text=self.t("ui.stroke"), bg=SURFACE, fg=FG, font=("Arial", 10)).grid(row=3, column=0, sticky="w", pady=2)
        stroke_scale = tk.Scale(controls, from_=1, to=5, orient=tk.HORIZONTAL, 
                                variable=self.preview_stroke, bg=SURFACE, fg=FG,
                                highlightthickness=0, length=180,
                                command=lambda x: self.update_all_previews())
        stroke_scale.grid(row=3, column=1, padx=5, pady=2)
        tk.Label(controls, textvariable=self.preview_stroke, bg=SURFACE, fg=ACCENT, font=("Consolas", 10)).grid(row=3, column=2, padx=5)
        
        # --- Buscador ---
        search_frame = tk.Frame(left_panel, bg=SURFACE)
        search_frame.pack(fill=tk.X, padx=8, pady=5)
        
        tk.Label(search_frame, text=self.t("ui.search"), bg=SURFACE, fg=FG, font=("Arial", 10)).pack(side=tk.LEFT)
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_text, 
                                     bg="#ffffff", fg="#000000", insertbackground="#000000",
                                     relief=tk.SUNKEN, font=("Arial", 10))
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.search_entry.bind('<KeyRelease>', lambda e: self.filter_icons())
        
        self.search_entry.insert(0, self.search_placeholder)
        self.search_entry.config(fg="#888888")
        self.search_entry.bind('<FocusIn>', self.on_search_focus_in)
        self.search_entry.bind('<FocusOut>', self.on_search_focus_out)
        
        tk.Button(search_frame, text=self.t("buttons.tabler_list"), bg=SURFACE, fg=ACCENT, relief=tk.FLAT,
                  command=self.open_tabler_selector).pack(side=tk.RIGHT, padx=2)
        
        # --- Botones de gestión ---
        icon_manage_frame = tk.Frame(left_panel, bg=SURFACE)
        icon_manage_frame.pack(fill=tk.X, padx=8, pady=5)
        
        tk.Button(icon_manage_frame, text=self.t("buttons.add_icon"), bg=SURFACE, fg=ACCENT, relief=tk.FLAT,
                  command=self.add_custom_icon).pack(side=tk.LEFT, padx=2)
        tk.Button(icon_manage_frame, text=self.t("buttons.change_variant"), bg=SURFACE, fg="#4caf50", relief=tk.FLAT,
                  command=self.change_icon_variant).pack(side=tk.LEFT, padx=2)
        tk.Button(icon_manage_frame, text=self.t("buttons.remove_icon"), bg=SURFACE, fg="#ff4444", relief=tk.FLAT,
                  command=self.remove_selected_icon).pack(side=tk.LEFT, padx=2)
        
        # --- Botones selección iconos ---
        icon_select_frame = tk.Frame(left_panel, bg=SURFACE)
        icon_select_frame.pack(fill=tk.X, padx=8, pady=2)
        
        tk.Button(icon_select_frame, text=self.t("buttons.select_all"), bg=SURFACE, fg=ACCENT, relief=tk.FLAT,
                  command=self.select_all_icons).pack(side=tk.LEFT, padx=2)
        tk.Button(icon_select_frame, text=self.t("buttons.deselect_all"), bg=SURFACE, fg="#ff4444", relief=tk.FLAT,
                  command=self.deselect_all_icons).pack(side=tk.LEFT, padx=2)
        
        # --- Lista de iconos ---
        icon_list_label = tk.Label(left_panel, text=self.t("ui.icons_count", count=len(self.icon_names)), bg=SURFACE, fg=FG, font=("Arial", 10, "bold"))
        icon_list_label.pack(anchor="w", padx=8, pady=(5, 2))
        
        self.icon_container = tk.Frame(left_panel, bg=SURFACE)
        self.icon_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.icon_scroll = tk.Canvas(
            self.icon_container,
            bg=SURFACE,
            highlightthickness=0,
            width=480
        )

        scrollbar = tk.Scrollbar(
            self.icon_container,
            orient=tk.VERTICAL,
            command=self.icon_scroll.yview
        )

        self.icon_scroll.configure(yscrollcommand=scrollbar.set)


        def on_icon_mousewheel(event):
            self.icon_scroll.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )


        def bind_icon_mousewheel(event):
            self.root.bind_all("<MouseWheel>", on_icon_mousewheel)


        def unbind_icon_mousewheel(event):
            self.root.unbind_all("<MouseWheel>")


        self.icon_container.bind("<Enter>", bind_icon_mousewheel)
        self.icon_container.bind("<Leave>", unbind_icon_mousewheel)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.icon_scroll.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.icon_inner = tk.Frame(self.icon_scroll, bg=SURFACE)
        self.icon_scroll.create_window((0, 0), window=self.icon_inner, anchor="nw")
        
        self.icon_inner.bind('<Configure>', lambda e: self.icon_scroll.configure(scrollregion=self.icon_scroll.bbox("all")))
        
        # ===== CREAR PANEL DE ICONOS =====
        self.icon_buttons = {}
        self.icon_frames = {}
        self.create_icon_buttons()
        
        # ===== PANEL DERECHO =====
        right_panel = tk.Frame(main_frame, bg=BG)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Selector de idioma
        language_bar = tk.Frame(right_panel, bg=BG)
        language_bar.pack(fill=tk.X, pady=(0, 8))

        tk.Label(language_bar, text=self.t("language.label"), bg=BG, fg=FG,
                 font=("Arial", 9)).pack(side=tk.RIGHT, padx=(0, 5))

        language_codes = list(self.languages.keys())
        language_combo = ttk.Combobox(
            language_bar,
            values=[self.language_name(code) for code in language_codes],
            state="readonly",
            width=14
        )
        if language_codes:
            language_combo.current(language_codes.index(self.current_language))
        language_combo.pack(side=tk.RIGHT)

        def on_language_selected(event):
            selected = language_combo.get()
            for code in language_codes:
                if self.language_name(code) == selected:
                    self.change_language(code)
                    break

        language_combo.bind("<<ComboboxSelected>>", on_language_selected)

        # Header
        header = tk.Label(right_panel, text=self.t("app.brand"), bg=BG, fg=ACCENT, font=("Consolas", 14))
        header.pack(anchor="w", pady=(0, 10))
        
        subheader = tk.Label(right_panel, text=self.t("app.subtitle"), bg=BG, fg=FG, font=("Arial", 18, "bold"))
        subheader.pack(anchor="w", pady=(0, 15))
        
        # ===== CONFIGURACIÓN =====
        config_frame = tk.LabelFrame(right_panel, text=self.t("sections.generation_config"), bg=SURFACE, fg=FG, font=("Arial", 10, "bold"))
        config_frame.pack(fill=tk.X, pady=5)
        
        # ---- Tamaños ----
        size_frame = tk.Frame(config_frame, bg=SURFACE)
        size_frame.pack(fill=tk.X, padx=10, pady=5)
        
        size_header = tk.Frame(size_frame, bg=SURFACE)
        size_header.pack(fill=tk.X)
        
        tk.Label(size_header, text=self.t("ui.sizes"), bg=SURFACE, fg=FG, font=("Arial", 10)).pack(side=tk.LEFT)
        tk.Button(size_header, text=self.t("buttons.all"), bg=SURFACE, fg=ACCENT, relief=tk.FLAT,
                  command=self.select_all_sizes).pack(side=tk.RIGHT, padx=2)
        tk.Button(size_header, text=self.t("buttons.none"), bg=SURFACE, fg="#ff4444", relief=tk.FLAT,
                  command=self.deselect_all_sizes).pack(side=tk.RIGHT, padx=2)
        
        size_grid = tk.Frame(size_frame, bg=SURFACE)
        size_grid.pack(fill=tk.X, pady=5)
        
        row, col = 0, 0
        default_sizes = self.config.get("selected_sizes", [16, 20, 24, 32, 48, 64])
        for size in self.size_options:
            var = tk.BooleanVar(value=(size in default_sizes))
            cb = tk.Checkbutton(size_grid, text=f"{size}px", variable=var, bg=SURFACE, fg=FG, 
                                selectcolor=SURFACE, activebackground=SURFACE, font=("Arial", 9))
            cb.grid(row=row, column=col, sticky="w", padx=3, pady=2)
            self.size_vars[size] = var
            col += 1
            if col > 7:
                col = 0
                row += 1
        
        # ---- Colores ----
        color_frame = tk.Frame(config_frame, bg=SURFACE)
        color_frame.pack(fill=tk.X, padx=10, pady=5)
        
        color_header = tk.Frame(color_frame, bg=SURFACE)
        color_header.pack(fill=tk.X)
        
        tk.Label(color_header, text=self.t("ui.colors"), bg=SURFACE, fg=FG, font=("Arial", 10)).pack(side=tk.LEFT)
        tk.Button(color_header, text=self.t("buttons.all"), bg=SURFACE, fg=ACCENT, relief=tk.FLAT,
                  command=self.select_all_colors).pack(side=tk.RIGHT, padx=2)
        tk.Button(color_header, text=self.t("buttons.none"), bg=SURFACE, fg="#ff4444", relief=tk.FLAT,
                  command=self.deselect_all_colors).pack(side=tk.RIGHT, padx=2)
        tk.Button(color_header, text=self.t("buttons.add"), bg=SURFACE, fg="#4caf50", relief=tk.FLAT,
                  command=self.add_color).pack(side=tk.RIGHT, padx=2)
        tk.Button(color_header, text=self.t("buttons.delete"), bg=SURFACE, fg="#ff4444", relief=tk.FLAT,
                  command=self.remove_selected_colors).pack(side=tk.RIGHT, padx=2)
        
        self.color_grid_frame = tk.Frame(color_frame, bg=SURFACE)
        self.color_grid_frame.pack(fill=tk.X, pady=5)
        
        self.color_vars = {}
        self.create_color_grid()
        
        # ---- Stroke ----
        stroke_frame = tk.Frame(config_frame, bg=SURFACE)
        stroke_frame.pack(fill=tk.X, padx=10, pady=5)
        
        stroke_header = tk.Frame(stroke_frame, bg=SURFACE)
        stroke_header.pack(fill=tk.X)
        
        tk.Label(stroke_header, text=self.t("ui.stroke"), bg=SURFACE, fg=FG, font=("Arial", 10)).pack(side=tk.LEFT)
        tk.Button(stroke_header, text=self.t("buttons.all"), bg=SURFACE, fg=ACCENT, relief=tk.FLAT,
                  command=self.select_all_strokes).pack(side=tk.RIGHT, padx=2)
        tk.Button(stroke_header, text=self.t("buttons.none"), bg=SURFACE, fg="#ff4444", relief=tk.FLAT,
                  command=self.deselect_all_strokes).pack(side=tk.RIGHT, padx=2)
        
        stroke_grid = tk.Frame(stroke_frame, bg=SURFACE)
        stroke_grid.pack(fill=tk.X, pady=5)
        
        row, col = 0, 0
        default_strokes = self.config.get("selected_strokes", [1, 2, 3])
        for stroke in self.stroke_options:
            var = tk.BooleanVar(value=(stroke in default_strokes))
            cb = tk.Checkbutton(stroke_grid, text=f"{stroke}px", variable=var, bg=SURFACE, fg=FG,
                                selectcolor=SURFACE, activebackground=SURFACE, font=("Arial", 9))
            cb.grid(row=row, column=col, sticky="w", padx=3, pady=2)
            self.stroke_vars[stroke] = var
            col += 1
        
        # ---- Opciones ----
        options_frame = tk.Frame(config_frame, bg=SURFACE)
        options_frame.pack(fill=tk.X, padx=10, pady=8)
        
        self.overwrite_var = tk.BooleanVar(value=False)
        cb_overwrite = tk.Checkbutton(options_frame, text=self.t("options.overwrite"), variable=self.overwrite_var,
                                      bg=SURFACE, fg=FG, selectcolor=SURFACE, activebackground=SURFACE, font=("Arial", 9))
        cb_overwrite.pack(side=tk.LEFT, padx=(0, 15))
        
        self.organize_var = tk.BooleanVar(value=True)
        cb_organize = tk.Checkbutton(options_frame, text=self.t("options.organize"), variable=self.organize_var,
                                     bg=SURFACE, fg=FG, selectcolor=SURFACE, activebackground=SURFACE, font=("Arial", 9))
        cb_organize.pack(side=tk.LEFT)
        
        # ===== BOTÓN GENERAR =====
        self.info_label = tk.Label(right_panel, text=self.t("status.loading_icons"), bg=BG, fg="#666", font=("Consolas", 10))
        self.info_label.pack(anchor="w", pady=(10, 5))
        
        self.generate_btn = tk.Button(right_panel, text=self.t("buttons.generate"), bg=ACCENT, fg="#111",
                                      font=("Arial", 12, "bold"), relief=tk.FLAT, padx=20, pady=10,
                                      command=self.start_generation)
        self.generate_btn.pack(fill=tk.X, pady=5)
        
        # ===== CONSOLA =====
        log_frame = tk.LabelFrame(right_panel, text=self.t("sections.console"), bg=SURFACE, fg=FG, font=("Arial", 10, "bold"))
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, bg="#1a1a1a", fg=FG, 
                                                   font=("Consolas", 9), relief=tk.FLAT, height=6)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Actualizar info
        self.update_gen_info()
    
    def on_search_focus_in(self, event):
        if self.search_placeholder_active:
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg="#000000")
            self.search_placeholder_active = False
            self.search_text.set("")
            self.filter_icons()

    def on_search_focus_out(self, event):
        if not self.search_entry.get().strip():
            self.search_placeholder_active = True
            self.search_entry.delete(0, tk.END)
            self.search_entry.insert(0, self.search_placeholder)
            self.search_entry.config(fg="#888888")
            self.search_text.set(self.search_placeholder)
    
    def update_all_previews(self):
        """Actualizar previsualización y todos los iconos del listado"""
        self.update_preview()
        for icon_name in self.icon_names:
            self.update_single_thumbnail(icon_name)
    
    def update_single_thumbnail(self, icon_name):
        """Actualizar la miniatura de un solo icono en el listado"""
        try:
            if icon_name not in self.icon_buttons:
                return
            
            size = 18
            color = self.preview_color.get()
            stroke = self.preview_stroke.get()
            
            svg_path = os.path.join(ICONS_DIR, f"{icon_name}.svg")
            if not os.path.exists(svg_path):
                # Si no existe el SVG, mostrar un placeholder
                if icon_name in self.icon_buttons:
                    self.icon_buttons[icon_name].config(image='', compound=tk.LEFT)
                return
            
            with open(svg_path, 'r') as f:
                svg = f.read()
            
            svg = svg.replace('currentColor', color)
            svg = svg.replace('stroke-width="2"', f'stroke-width="{stroke}"')
            svg = svg.replace('width="24"', f'width="{size}"')
            svg = svg.replace('height="24"', f'height="{size}"')
            
            png = cairosvg.svg2png(bytestring=svg.encode(), output_width=size, output_height=size)
            img = Image.open(io.BytesIO(png))
            photo = ImageTk.PhotoImage(img)
            
            self.icon_thumbnails[icon_name] = photo
            
            if icon_name in self.icon_buttons:
                self.icon_buttons[icon_name].config(image=photo, compound=tk.LEFT)
                
        except Exception as e:
            pass
    
    def color_label(self, name):
        # Los colores incluidos por defecto se traducen desde el JSON.
        # Los colores personalizados conservan el nombre que haya escrito el usuario.
        default_color_keys = {
            "accent", "muted", "text", "red", "green", "blue", "orange",
            "purple", "pink", "teal", "yellow", "cyan", "white", "black"
        }
        return self.t(f"colors.{name}") if name in default_color_keys else name

    def color_name_from_label(self, label):
        for name in self.color_options:
            if self.color_label(name) == label:
                return name
        return label

    def on_color_change(self, event):
        display_name = event.widget.get()
        color_name = self.color_name_from_label(display_name)
        if color_name in self.color_options:
            self.preview_color.set(self.color_options[color_name])
            self.color_indicator.delete("all")
            self.color_indicator.create_rectangle(2, 2, 18, 18, fill=self.color_options[color_name], outline="")
            self.update_all_previews()
    
    # ===== FUNCIONES DE SELECCIÓN =====
    
    def select_all_icons(self):
        self.selected_icon_names.update(self.icon_names)
        self.create_icon_buttons()
        self.update_gen_info()
    
    def deselect_all_icons(self):
        self.selected_icon_names.clear()
        self.create_icon_buttons()
        self.update_gen_info()
    
    def select_all_sizes(self):
        for var in self.size_vars.values():
            var.set(True)
        self.update_gen_info()
    
    def deselect_all_sizes(self):
        for var in self.size_vars.values():
            var.set(False)
        self.update_gen_info()
    
    def select_all_colors(self):
        for var in self.color_vars.values():
            var.set(True)
        self.update_gen_info()
    
    def deselect_all_colors(self):
        for var in self.color_vars.values():
            var.set(False)
        self.update_gen_info()
    
    def select_all_strokes(self):
        for var in self.stroke_vars.values():
            var.set(True)
        self.update_gen_info()
    
    def deselect_all_strokes(self):
        for var in self.stroke_vars.values():
            var.set(False)
        self.update_gen_info()
    
    # ===== FUNCIONES DE COLOR DE FONDO =====
    
    def background_label(self, name):
        if name.startswith("color:"):
            color_name = name.split(":", 1)[1]
            return self.t("background.color_prefix") + self.color_label(color_name)
        return self.t(f"background.{name}")

    def background_name_from_label(self, label):
        for name in self.bg_options:
            if self.background_label(name) == label:
                return name
        return label

    def on_bg_change(self, event):
        display_name = event.widget.get()
        bg_name = self.background_name_from_label(display_name)
        if bg_name in self.bg_options:
            self.preview_bg_color.set(self.bg_options[bg_name])
            self.bg_indicator.delete("all")
            self.bg_indicator.create_rectangle(2, 2, 18, 18, fill=self.bg_options[bg_name], outline="")
            self.preview_canvas.configure(bg=self.bg_options[bg_name])
            self.update_preview()
    
    # ===== FUNCIONES DE GESTIÓN DE ICONOS =====
    
    def get_icon_preview_char(self, icon_name):
        """Obtener un carácter o emoji representativo para el icono"""
        icon_map = {
            "pencil": "✏️", "settings": "⚙️", "search": "🔍", "home": "🏠",
            "user": "👤", "mail": "📧", "heart": "❤️", "star": "⭐",
            "calendar": "📅", "clock": "🕐", "phone": "📱", "camera": "📷",
            "music": "🎵", "book": "📖", "lock": "🔒", "unlock": "🔓",
            "eye": "👁️", "message": "💬", "folder": "📁", "file": "📄",
            "download": "⬇️", "upload": "⬆️", "plus": "➕", "minus": "➖",
            "check": "✅", "x": "❌", "trash": "🗑️", "tag": "🏷️",
            "share": "↗️", "link": "🔗", "cloud": "☁️", "moon": "🌙",
            "sun": "☀️", "fire": "🔥", "droplet": "💧", "gift": "🎁",
            "award": "🏆", "trophy": "🏆", "medal": "🥇", "cube": "📦",
            "list": "📋", "chart-bar": "📊", "books": "📚", "edit": "✏️",
            "chevron-right": "▶️", "briefcase": "💼", "shield": "🛡️"
        }
        
        for key, emoji in icon_map.items():
            if key in icon_name or icon_name in key:
                return emoji
        return "🔹"
    
    def open_tabler_selector(self):
        """Abrir selector de iconos de Tabler con previsualización en tiempo real"""
        dialog = tk.Toplevel(self.root)
        dialog.title(self.t("dialogs.tabler_title"))
        dialog.geometry("650x550")
        dialog.configure(bg=BG)
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text=self.t("dialogs.tabler_select"), bg=BG, fg=FG, font=("Arial", 12)).pack(pady=10)
        
        main_frame = tk.Frame(dialog, bg=BG)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=0)
        main_frame.grid_rowconfigure(0, weight=1)
        
        # --- Panel izquierdo: Lista ---
        list_frame = tk.Frame(main_frame, bg=SURFACE)
        list_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        # Buscador dentro del selector
        search_frame = tk.Frame(list_frame, bg=SURFACE)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(search_frame, text=self.t("ui.filter"), bg=SURFACE, fg=FG).pack(side=tk.LEFT)
        search_entry = tk.Entry(search_frame, bg="#ffffff", fg="#000000", insertbackground="#000000", width=20)
        search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Lista
        listbox_frame = tk.Frame(list_frame, bg=SURFACE)
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(listbox_frame, bg=SURFACE, fg=FG, selectbackground="#4a4a4a",
                             selectforeground=FG, font=("Consolas", 10), yscrollcommand=scrollbar.set)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        # Cargar lista
        for icon in sorted(self.tabler_icons_complete):
            emoji = self.get_icon_preview_char(icon)
            listbox.insert(tk.END, f"{emoji} {icon}")
        
        def filter_list(event):
            search = search_entry.get().strip().lower()
            listbox.delete(0, tk.END)
            for icon in sorted(self.tabler_icons_complete):
                if search in icon.lower():
                    emoji = self.get_icon_preview_char(icon)
                    listbox.insert(tk.END, f"{emoji} {icon}")
        
        search_entry.bind('<KeyRelease>', filter_list)
        
        # --- Panel derecho: Previsualización ---
        preview_frame = tk.LabelFrame(main_frame, text=self.t("ui.preview"), bg=SURFACE, fg=FG, font=("Arial", 10))
        preview_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        
        preview_canvas = tk.Canvas(preview_frame, bg="#1a1a1a", width=150, height=150, relief=tk.FLAT, bd=1)
        preview_canvas.pack(padx=15, pady=15)
        
        # Info del icono seleccionado
        info_frame = tk.Frame(preview_frame, bg=SURFACE)
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        info_label = tk.Label(info_frame, text=self.t("messages.select_icon"), bg=SURFACE, fg="#666", font=("Arial", 9))
        info_label.pack()
        
        def on_select(event):
            selection = listbox.curselection()
            if selection:
                full_text = listbox.get(selection[0])
                icon_name = full_text.split(' ', 1)[1] if ' ' in full_text else full_text
                self.preview_variant(preview_canvas, icon_name, size=64)
                info_label.config(text=f"📌 {icon_name}", fg=ACCENT)
        
        listbox.bind('<<ListboxSelect>>', on_select)
        
        # Preseleccionar el primero
        if listbox.size() > 0:
            listbox.selection_set(0)
            on_select(None)
        
        # --- Botones ---
        btn_frame = tk.Frame(dialog, bg=BG)
        btn_frame.pack(fill=tk.X, pady=10)
        
        def select_icon():
            selection = listbox.curselection()
            if not selection:
                messagebox.showerror(self.t("messages.error"), self.t("messages.select_icon"))
                return
            full_text = listbox.get(selection[0])
            icon_name = full_text.split(' ', 1)[1] if ' ' in full_text else full_text
            
            if icon_name in self.icon_names:
                messagebox.showinfo(self.t("messages.info"), self.t("messages.already_in_list", icon=icon_name))
                return
            
            self.icon_names.append(icon_name)
            self.selected_icon_names.add(icon_name)
            self.download_single_icon(icon_name)
            self.create_icon_buttons()
            self.preview_icon.set(icon_name)
            self.highlight_icon(icon_name)
            self.update_preview()
            self.log(self.t("logs.icon_added", icon=icon_name))
            dialog.destroy()
        
        tk.Button(btn_frame, text=self.t("buttons.add"), command=select_icon, bg=ACCENT, fg="#111", relief=tk.FLAT, padx=20).pack(side=tk.RIGHT, padx=5)
        tk.Button(btn_frame, text=self.t("buttons.view_tabler"), bg=SURFACE, fg=ACCENT, relief=tk.FLAT,
                  command=lambda: webbrowser.open("https://tabler.io/icons")).pack(side=tk.RIGHT, padx=5)
        tk.Button(btn_frame, text=self.t("buttons.cancel"), command=dialog.destroy, bg=SURFACE, fg=FG, relief=tk.FLAT, padx=20).pack(side=tk.RIGHT)
    
    def add_custom_icon(self):
        """Añadir un icono personalizado por nombre con búsqueda en tiempo real"""
        dialog = tk.Toplevel(self.root)
        dialog.title(self.t("dialogs.custom_title"))
        dialog.geometry("500x450")
        dialog.configure(bg=BG)
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text=self.t("dialogs.custom_select"), bg=BG, fg=FG, font=("Arial", 11)).pack(pady=10)
        
        search_frame = tk.Frame(dialog, bg=BG)
        search_frame.pack(fill=tk.X, padx=15, pady=5)
        
        tk.Label(search_frame, text=self.t("ui.search"), bg=BG, fg=FG).pack(side=tk.LEFT)
        search_entry = tk.Entry(search_frame, bg="#ffffff", fg="#000000", insertbackground="#000000", width=35)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        list_frame = tk.Frame(dialog, bg=SURFACE)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(list_frame, bg=SURFACE, fg=FG, selectbackground="#4a4a4a",
                             selectforeground=FG, font=("Consolas", 10), yscrollcommand=scrollbar.set)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        for icon in sorted(self.tabler_icons_complete):
            emoji = self.get_icon_preview_char(icon)
            listbox.insert(tk.END, f"{emoji} {icon}")
        
        def filter_list(event=None):
            search = search_entry.get().strip().lower()
            listbox.delete(0, tk.END)
            for icon in sorted(self.tabler_icons_complete):
                if search in icon.lower():
                    emoji = self.get_icon_preview_char(icon)
                    listbox.insert(tk.END, f"{emoji} {icon}")
        
        search_entry.bind('<KeyRelease>', filter_list)
        
        preview_frame = tk.LabelFrame(dialog, text=self.t("ui.preview"), bg=SURFACE, fg=FG, font=("Arial", 10))
        preview_frame.pack(fill=tk.X, padx=15, pady=5)
        
        preview_canvas = tk.Canvas(preview_frame, bg="#1a1a1a", height=60, relief=tk.FLAT, bd=1)
        preview_canvas.pack(fill=tk.X, padx=5, pady=5)
        
        def on_select(event):
            selection = listbox.curselection()
            if selection:
                full_text = listbox.get(selection[0])
                icon_name = full_text.split(' ', 1)[1] if ' ' in full_text else full_text
                self.preview_variant(preview_canvas, icon_name, size=40)
        
        listbox.bind('<<ListboxSelect>>', on_select)
        
        if listbox.size() > 0:
            listbox.selection_set(0)
            on_select(None)
        
        def confirm():
            selection = listbox.curselection()
            if not selection:
                messagebox.showerror(self.t("messages.error"), self.t("messages.select_icon"))
                return
            full_text = listbox.get(selection[0])
            icon_name = full_text.split(' ', 1)[1] if ' ' in full_text else full_text
            
            if icon_name in self.icon_names:
                messagebox.showerror(self.t("messages.error"), self.t("messages.icon_exists", icon=icon_name))
                return
            
            self.icon_names.append(icon_name)
            self.selected_icon_names.add(icon_name)
            self.download_single_icon(icon_name)
            self.create_icon_buttons()
            self.preview_icon.set(icon_name)
            self.highlight_icon(icon_name)
            self.update_preview()
            
            dialog.destroy()
            self.log(self.t("logs.icon_added", icon=icon_name))
        
        btn_frame = tk.Frame(dialog, bg=BG)
        btn_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(btn_frame, text=self.t("buttons.add"), command=confirm, bg=ACCENT, fg="#111", relief=tk.FLAT, padx=20).pack(side=tk.RIGHT, padx=5)
        tk.Button(btn_frame, text=self.t("buttons.cancel"), command=dialog.destroy, bg=SURFACE, fg=FG, relief=tk.FLAT, padx=20).pack(side=tk.RIGHT)
    
    def preview_variant(self, canvas, icon_name, size=48):
        """Mostrar previsualización de un icono en un canvas"""
        canvas.delete("all")
        color = self.preview_color.get()
        stroke = self.preview_stroke.get()
        
        try:
            svg_path = os.path.join(ICONS_DIR, f"{icon_name}.svg")
            if not os.path.exists(svg_path):
                self.download_single_icon(icon_name)
                if not os.path.exists(svg_path):
                    canvas.create_text(canvas.winfo_width()//2, canvas.winfo_height()//2, 
                                      text=self.t("messages.not_found"), fill="#ff4444", font=("Consolas", 10))
                    return
            
            with open(svg_path, 'r') as f:
                svg = f.read()
            
            svg = svg.replace('currentColor', color)
            svg = svg.replace('stroke-width="2"', f'stroke-width="{stroke}"')
            svg = svg.replace('width="24"', f'width="{size}"')
            svg = svg.replace('height="24"', f'height="{size}"')
            
            png = cairosvg.svg2png(bytestring=svg.encode(), output_width=size, output_height=size)
            img = Image.open(io.BytesIO(png))
            photo = ImageTk.PhotoImage(img)
            canvas.image = photo
            
            canvas_width = canvas.winfo_width()
            canvas_height = canvas.winfo_height()
            x = (canvas_width - size) // 2 if canvas_width > size else 0
            y = (canvas_height - size) // 2 if canvas_height > size else 0
            canvas.create_image(max(0, x), max(0, y), anchor="nw", image=photo)
            
        except Exception as e:
            canvas.create_text(canvas.winfo_width()//2, canvas.winfo_height()//2, 
                              text=self.t("messages.error"), fill="#ff4444", font=("Consolas", 9))
    
    def download_single_icon(self, icon_name):
        """Descargar un icono individual"""
        svg_path = os.path.join(ICONS_DIR, f"{icon_name}.svg")
        
        if os.path.exists(svg_path):
            self.generate_thumbnail(icon_name)
            return True
        
        try:
            url = f"https://cdn.jsdelivr.net/npm/@tabler/icons/icons/{icon_name}.svg"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                with open(svg_path, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                self.log(self.t("logs.icon_downloaded", icon=icon_name))
                self.generate_thumbnail(icon_name)
                return True
            else:
                self.log(self.t("logs.icon_http_error", icon=icon_name, status=response.status_code))
                return False
        except Exception as e:
            self.log(self.t("logs.download_error", icon=icon_name, error=e))
            return False
    
    def change_icon_variant(self):
        """Cambiar la variante de un icono seleccionado con previsualización"""
        current_icon = self.preview_icon.get()
        
        suffixes = ['', '-filled', '-off', '-plus', '-minus', '-check', '-x', '-2', '-3', '-4']
        base_name = current_icon
        for suf in suffixes:
            if suf and current_icon.endswith(suf):
                base_name = current_icon[:-len(suf)]
                break
        
        variants = []
        for suf in suffixes:
            candidate = base_name + suf
            if candidate != current_icon:
                variants.append(candidate)
        variants.insert(0, current_icon)
        variants = list(dict.fromkeys(variants))
        
        emoji = self.get_icon_preview_char(current_icon)
        dialog = tk.Toplevel(self.root)
        dialog.title(self.t("dialogs.change_variant_title", emoji=emoji, icon=current_icon))
        dialog.geometry("500x450")
        dialog.configure(bg=BG)
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text=self.t("dialogs.change_variant", icon=current_icon), bg=BG, fg=FG, font=("Arial", 11)).pack(pady=10)
        
        main_frame = tk.Frame(dialog, bg=BG)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        
        list_frame = tk.Frame(main_frame, bg=SURFACE)
        list_frame.grid(row=0, column=0, sticky="nsew", padx=(0,5))
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(list_frame, bg=SURFACE, fg=FG, selectbackground="#4a4a4a",
                             selectforeground=FG, font=("Consolas", 10), yscrollcommand=scrollbar.set)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        for v in variants:
            v_emoji = self.get_icon_preview_char(v)
            listbox.insert(tk.END, f"{v_emoji} {v}")
        listbox.selection_set(0)
        
        preview_frame = tk.LabelFrame(main_frame, text=self.t("ui.preview"), bg=SURFACE, fg=FG, font=("Arial", 10))
        preview_frame.grid(row=0, column=1, sticky="nsew", padx=(5,0))
        
        preview_canvas = tk.Canvas(preview_frame, bg="#1a1a1a", width=120, height=120, relief=tk.FLAT, bd=1)
        preview_canvas.pack(padx=10, pady=10)
        
        def on_select(event):
            selection = listbox.curselection()
            if selection:
                full_text = listbox.get(selection[0])
                variant = full_text.split(' ', 1)[1] if ' ' in full_text else full_text
                self.preview_variant(preview_canvas, variant)
        
        listbox.bind('<<ListboxSelect>>', on_select)
        self.preview_variant(preview_canvas, current_icon)
        
        btn_frame = tk.Frame(dialog, bg=BG)
        btn_frame.pack(fill=tk.X, pady=10)
        
        def confirm():
            selection = listbox.curselection()
            if not selection:
                return
            full_text = listbox.get(selection[0])
            new_icon = full_text.split(' ', 1)[1] if ' ' in full_text else full_text
            if new_icon == current_icon:
                dialog.destroy()
                return
            
            idx = self.icon_names.index(current_icon)
            self.icon_names[idx] = new_icon
            if current_icon in self.selected_icon_names:
                self.selected_icon_names.discard(current_icon)
                self.selected_icon_names.add(new_icon)
            
            self.download_single_icon(new_icon)
            self.create_icon_buttons()
            self.preview_icon.set(new_icon)
            self.highlight_icon(new_icon)
            self.update_preview()
            
            dialog.destroy()
            self.log(self.t("logs.icon_changed", old=current_icon, new=new_icon))
        
        tk.Button(btn_frame, text=self.t("buttons.change"), command=confirm, bg=ACCENT, fg="#111", relief=tk.FLAT, padx=20).pack(side=tk.RIGHT, padx=5)
        tk.Button(btn_frame, text=self.t("buttons.cancel"), command=dialog.destroy, bg=SURFACE, fg=FG, relief=tk.FLAT, padx=20).pack(side=tk.RIGHT)
    
    def remove_selected_icon(self):
        """Eliminar un icono seleccionado (protege los base)"""
        current_icon = self.preview_icon.get()
        
        if current_icon in self.base_icons:
            messagebox.showwarning(self.t("messages.warning"), 
                self.t("messages.base_icon_warning", icon=current_icon))
            return
        
        if messagebox.askyesno(self.t("messages.confirm"), self.t("messages.confirm_remove_icon", icon=current_icon)):
            self.icon_names.remove(current_icon)
            self.selected_icon_names.discard(current_icon)
            
            svg_path = os.path.join(ICONS_DIR, f"{current_icon}.svg")
            if os.path.exists(svg_path):
                os.remove(svg_path)
            
            self.create_icon_buttons()
            
            if self.icon_names:
                new_selection = self.icon_names[0] if self.icon_names else "pencil"
                self.preview_icon.set(new_selection)
                self.highlight_icon(new_selection)
                self.update_preview()
            
            self.log(self.t("logs.icon_removed", icon=current_icon))
            self.update_gen_info()
    
    # ===== FUNCIONES DE COLORES =====
    
    def create_color_grid(self):
        """Crear/actualizar grid de colores"""
        for widget in self.color_grid_frame.winfo_children():
            widget.destroy()
        
        row, col = 0, 0
        for name, hex_color in self.color_options.items():
            var = tk.BooleanVar(value=True)
            frame = tk.Frame(self.color_grid_frame, bg=SURFACE)
            frame.grid(row=row, column=col, sticky="w", padx=3, pady=2)
            
            cb = tk.Checkbutton(
                frame,
                variable=var,
                bg=SURFACE,
                fg=FG,
                selectcolor=SURFACE,
                activebackground=SURFACE,
                activeforeground=FG,
                highlightthickness=0,
                bd=0,
                relief=tk.FLAT,
                font=("Arial", 9),
                command=self.update_gen_info
            )
            cb.pack(side=tk.LEFT)
            
            indicator = tk.Canvas(frame, width=12, height=12, bg=SURFACE, highlightthickness=0)
            indicator.pack(side=tk.LEFT, padx=2)
            indicator.create_rectangle(0, 0, 12, 12, fill=hex_color, outline="")
            
            label = tk.Label(frame, text=self.color_label(name), bg=SURFACE, fg=hex_color, font=("Arial", 8))
            label.pack(side=tk.LEFT, padx=2)
            
            self.color_vars[name] = var
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        self.update_gen_info()
    
    def add_color(self):
        """Añadir un nuevo color"""
        color = colorchooser.askcolor(title=self.t("dialogs.choose_color"), color="#caff33")
        if color:
            hex_color = color[1]
            dialog = tk.Toplevel(self.root)
            dialog.title(self.t("dialogs.color_name_title"))
            dialog.geometry("300x100")
            dialog.configure(bg=BG)
            dialog.transient(self.root)
            dialog.grab_set()
            
            tk.Label(dialog, text=self.t("dialogs.color_name"), bg=BG, fg=FG).pack(pady=5)
            entry = tk.Entry(dialog, bg="#ffffff", fg="#000000", insertbackground="#000000")
            entry.pack(pady=5)
            entry.insert(0, self.t("color.default_name", number=len(self.color_options)+1))
            
            def confirm():
                new_name = entry.get().strip()
                if new_name:
                    self.color_options[new_name] = hex_color
                    self.create_color_grid()
                    self.color_combo['values'] = [self.color_label(name) for name in self.color_options]
                    self.bg_options[f"color:{new_name}"] = hex_color
                    self.bg_combo['values'] = [self.background_label(name) for name in self.bg_options]
                    dialog.destroy()
                    self.log(self.t("logs.color_added", name=new_name, color=hex_color))
            
            tk.Button(dialog, text=self.t("buttons.add"), command=confirm, bg=ACCENT, fg="#111", relief=tk.FLAT).pack(pady=5)
            entry.focus()
            dialog.wait_window()
    
    def remove_selected_colors(self):
        """Eliminar colores seleccionados"""
        to_remove = [name for name, var in self.color_vars.items() if var.get()]
        
        if not to_remove:
            messagebox.showinfo(self.t("messages.info"), self.t("messages.select_color_to_remove"))
            return
        
        if "accent" in to_remove:
            messagebox.showwarning(self.t("messages.warning"), self.t("messages.cannot_remove_accent"))
            to_remove.remove("accent")
        
        if not to_remove:
            return
        
        if messagebox.askyesno(self.t("messages.confirm"), self.t("messages.confirm_remove_colors", count=len(to_remove))):
            for name in to_remove:
                del self.color_options[name]
                bg_key = f"color:{name}"
                if bg_key in self.bg_options:
                    del self.bg_options[bg_key]
            
            self.create_color_grid()
            self.color_combo['values'] = [self.color_label(name) for name in self.color_options]
            self.bg_combo['values'] = [self.background_label(name) for name in self.bg_options]
            self.log(self.t("logs.colors_removed", count=len(to_remove)))
    
    # ===== FUNCIONES PRINCIPALES =====
    
    def create_icon_buttons(self):
        """Crear botones para iconos con checkboxes - base primero, línea separadora, luego resto"""
        # Limpiar todo
        for widget in self.icon_inner.winfo_children():
            widget.destroy()
        
        self.icon_buttons = {}
        self.icon_check_vars = {}
        self.icon_frames = {}

        # El placeholder no es una búsqueda real.
        raw_search = self.search_text.get().strip()
        search = "" if self.search_placeholder_active or raw_search == self.search_placeholder else raw_search.lower()

        # Mantener solo iconos válidos y evitar selecciones huérfanas.
        self.selected_icon_names.intersection_update(self.icon_names)
        
        # Si no hay iconos, mostrar mensaje
        if not self.icon_names:
            label = tk.Label(self.icon_inner, text=self.t("messages.no_icons"), 
                           bg=SURFACE, fg="#666", font=("Arial", 12))
            label.grid(row=0, column=0, columnspan=3, padx=20, pady=20)
            self.update_gen_info()
            return
        
        # Separar base y no-base
        base_icons = [icon for icon in self.icon_names if icon in self.base_icons]
        otros_icons = [icon for icon in self.icon_names if icon not in self.base_icons]
        
        # Filtrar por búsqueda
        if search:
            base_icons = [icon for icon in base_icons if search in icon.lower()]
            otros_icons = [icon for icon in otros_icons if search in icon.lower()]
        
        col_width = 140
        for i in range(3):
            self.icon_inner.grid_columnconfigure(i, weight=0, minsize=col_width)
        
        self.icon_inner.configure(width=col_width * 3 + 10)
        
        row, col = 0, 0
        found_base = False
        
        # Mostrar iconos base
        for icon in base_icons:
            found_base = True
            frame = tk.Frame(self.icon_inner, bg=SURFACE, width=col_width, height=30)
            frame.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
            frame.grid_propagate(False)
            self.icon_frames[icon] = frame
            
            var = tk.BooleanVar(value=(icon in self.selected_icon_names))
            cb = tk.Checkbutton(
                frame,
                variable=var,
                bg=SURFACE,
                fg=FG,
                selectcolor=SURFACE,
                activebackground=SURFACE,
                activeforeground=FG,
                highlightthickness=0,
                bd=0,
                relief=tk.FLAT,
                font=("Arial", 9),
                command=lambda i=icon, v=var: self.on_icon_check(i, v)
            )
            cb.pack(side=tk.LEFT, padx=(2, 0))
            self.icon_check_vars[icon] = var
            
            display_text = icon[:12] + ".." if len(icon) > 14 else icon
            btn = tk.Button(frame, text=display_text, 
                           bg="#2a2a2a" if icon != self.preview_icon.get() else "#4a4a4a", 
                           fg=ACCENT, relief=tk.FLAT, padx=2, pady=2, 
                           font=("Consolas", 9, "bold"),
                           command=lambda i=icon: self.select_icon(i))
            btn.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            # Si hay miniatura disponible, mostrarla
            if icon in self.icon_thumbnails and self.icon_thumbnails[icon]:
                btn.config(image=self.icon_thumbnails[icon], compound=tk.LEFT)
            else:
                # Mostrar un placeholder visual (un cuadrado pequeño)
                btn.config(compound=tk.LEFT)
            
            self.icon_buttons[icon] = btn
            
            col += 1
            if col >= 3:
                col = 0
                row += 1
        
        # Línea separadora si hay iconos base y otros iconos
        if found_base and otros_icons:
            if col != 0:
                row += 1
                col = 0
            
            sep_frame = tk.Frame(self.icon_inner, bg=SURFACE, height=5)
            sep_frame.grid(row=row, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
            
            line = tk.Frame(sep_frame, bg=BORDER, height=1)
            line.pack(fill=tk.X, padx=10, pady=2)
            
            sep_label = tk.Label(sep_frame, text=self.t("ui.additional_icons"), bg=SURFACE, fg="#666", font=("Arial", 8))
            sep_label.pack()
            
            row += 1
            col = 0
        
        # Mostrar otros iconos
        for icon in otros_icons:
            frame = tk.Frame(self.icon_inner, bg=SURFACE, width=col_width, height=30)
            frame.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
            frame.grid_propagate(False)
            self.icon_frames[icon] = frame
            
            var = tk.BooleanVar(value=(icon in self.selected_icon_names))
            cb = tk.Checkbutton(
                frame,
                variable=var,
                bg=SURFACE,
                fg=FG,
                selectcolor=SURFACE,
                activebackground=SURFACE,
                activeforeground=FG,
                highlightthickness=0,
                bd=0,
                relief=tk.FLAT,
                font=("Arial", 9),
                command=lambda i=icon, v=var: self.on_icon_check(i, v)
            )
            cb.pack(side=tk.LEFT, padx=(2, 0))
            self.icon_check_vars[icon] = var
            
            display_text = icon[:12] + ".." if len(icon) > 14 else icon
            btn = tk.Button(frame, text=display_text, 
                           bg="#2a2a2a" if icon != self.preview_icon.get() else "#4a4a4a", 
                           fg=FG, relief=tk.FLAT, padx=2, pady=2, 
                           font=("Consolas", 9),
                           command=lambda i=icon: self.select_icon(i))
            btn.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            if icon in self.icon_thumbnails and self.icon_thumbnails[icon]:
                btn.config(image=self.icon_thumbnails[icon], compound=tk.LEFT)
            else:
                btn.config(compound=tk.LEFT)
            
            self.icon_buttons[icon] = btn
            
            col += 1
            if col >= 3:
                col = 0
                row += 1
        
        self.icon_inner.update_idletasks()
        self.icon_scroll.configure(scrollregion=self.icon_scroll.bbox("all"))
        self.update_gen_info()
    
    def on_icon_check(self, icon_name, var):
        """Actualizar la selección persistente de un icono."""
        if var.get():
            self.selected_icon_names.add(icon_name)
        else:
            self.selected_icon_names.discard(icon_name)
        self.update_gen_info()

    def highlight_icon(self, icon_name):
        for name, btn in self.icon_buttons.items():
            btn.configure(bg="#2a2a2a" if name != icon_name else "#4a4a4a")
    
    def filter_icons(self):
        """Filtrar iconos sin tratar el placeholder como texto de búsqueda."""
        if self.search_entry.get().strip() == self.search_placeholder:
            self.search_placeholder_active = True
        else:
            self.search_placeholder_active = False
        self.create_icon_buttons()
    
    def select_icon(self, icon_name):
        self.preview_icon.set(icon_name)
        self.highlight_icon(icon_name)
        self.update_preview()
    
    def download_all_icons(self):
        """Descargar SVGs y generar miniaturas, luego actualizar panel"""
        self.log(self.t("logs.downloading"))
        
        for icon in self.icon_names:
            svg_path = os.path.join(ICONS_DIR, f"{icon}.svg")
            
            if not os.path.exists(svg_path):
                try:
                    url = f"https://cdn.jsdelivr.net/npm/@tabler/icons/icons/{icon}.svg"
                    response = requests.get(url, timeout=10)
                    if response.status_code == 200:
                        with open(svg_path, 'w', encoding='utf-8') as f:
                            f.write(response.text)
                        self.log(self.t("logs.icon_downloaded", icon=icon))
                    else:
                        self.log(self.t("logs.icon_http_error_short", icon=icon, status=response.status_code))
                except Exception as e:
                    self.log(self.t("logs.download_error_short", icon=icon, error=e))
            
            self.generate_thumbnail(icon)
        
        self.icons_loaded = True
        self.log(self.t("logs.icons_ready"))
        
        # ==== ACTUALIZAR PANEL DESPUÉS DE DESCARGAR ====
        self.root.after(50, self.create_icon_buttons)
        self.root.after(100, self.update_preview)
        self.root.after(150, self.update_gen_info)
    
    def generate_thumbnail(self, icon_name, size=18):
        """Generar miniatura para botones usando el color actual"""
        try:
            svg_path = os.path.join(ICONS_DIR, f"{icon_name}.svg")
            if not os.path.exists(svg_path):
                return
            
            with open(svg_path, 'r') as f:
                svg = f.read()
            
            color = self.preview_color.get()
            stroke = self.preview_stroke.get()
            
            svg = svg.replace('currentColor', color)
            svg = svg.replace('stroke-width="2"', f'stroke-width="{stroke}"')
            svg = svg.replace('width="24"', f'width="{size}"')
            svg = svg.replace('height="24"', f'height="{size}"')
            
            png = cairosvg.svg2png(bytestring=svg.encode(), output_width=size, output_height=size)
            img = Image.open(io.BytesIO(png))
            photo = ImageTk.PhotoImage(img)
            self.icon_thumbnails[icon_name] = photo
            
            if icon_name in self.icon_buttons:
                self.icon_buttons[icon_name].config(image=photo, compound=tk.LEFT)
                
        except Exception as e:
            pass
    
    def update_preview(self):
        """Actualizar previsualización"""
        self.preview_canvas.delete("all")
        
        if not self.icons_loaded:
            self.preview_canvas.create_text(
                self.preview_canvas.winfo_width()//2,
                self.preview_canvas.winfo_height()//2,
                text=self.t("status.loading_icons"), fill="#666", font=("Consolas", 12)
            )
            return
        
        icon_name = self.preview_icon.get()
        size = self.preview_size.get()
        color = self.preview_color.get()
        stroke = self.preview_stroke.get()
        bg_color = self.preview_bg_color.get()
        
        self.preview_canvas.configure(bg=bg_color)
        
        try:
            svg_path = os.path.join(ICONS_DIR, f"{icon_name}.svg")
            if not os.path.exists(svg_path):
                self.preview_canvas.create_text(
                    self.preview_canvas.winfo_width()//2,
                    self.preview_canvas.winfo_height()//2,
                    text=self.t("messages.icon_not_found", icon=icon_name), fill="#ff4444", font=("Consolas", 12)
                )
                return
            
            with open(svg_path, 'r') as f:
                svg = f.read()
            
            svg = svg.replace('currentColor', color)
            svg = svg.replace('stroke-width="2"', f'stroke-width="{stroke}"')
            svg = svg.replace('width="24"', f'width="{size}"')
            svg = svg.replace('height="24"', f'height="{size}"')
            
            png = cairosvg.svg2png(bytestring=svg.encode(), output_width=size, output_height=size)
            img = Image.open(io.BytesIO(png))
            photo = ImageTk.PhotoImage(img)
            
            self.preview_canvas.image = photo
            x = (self.preview_canvas.winfo_width() - size) // 2
            y = (self.preview_canvas.winfo_height() - size) // 2
            self.preview_canvas.create_image(max(0, x), max(0, y), anchor="nw", image=photo)
            
        except Exception as e:
            self.preview_canvas.create_text(
                self.preview_canvas.winfo_width()//2,
                self.preview_canvas.winfo_height()//2,
                text=self.t("messages.error_detail", error=e), fill="#ff4444", font=("Consolas", 10)
            )
    
    def update_gen_info(self):
        """Actualizar info de generación"""
        try:
            selected_icons = [icon for icon, var in self.icon_check_vars.items() if var.get()]
            selected_sizes = [s for s, var in self.size_vars.items() if var.get()]
            selected_colors = [name for name, var in self.color_vars.items() if var.get()]
            selected_strokes = [s for s, var in self.stroke_vars.items() if var.get()]
            
            total = len(selected_icons) * len(selected_sizes) * len(selected_colors) * len(selected_strokes)
            self.info_label.config(
                text=self.t("status.generation_summary",
                    icons=len(selected_icons), sizes=len(selected_sizes),
                    colors=len(selected_colors), strokes=len(selected_strokes),
                    total=total)
            )
        except:
            pass
    
    def log(self, message):
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def start_generation(self):
        """Iniciar generación"""
        selected_icons = [icon for icon, var in self.icon_check_vars.items() if var.get()]
        selected_sizes = [s for s, var in self.size_vars.items() if var.get()]
        selected_colors = [(name, hex) for name, hex in self.color_options.items() 
                          if self.color_vars[name].get()]
        selected_strokes = [s for s, var in self.stroke_vars.items() if var.get()]
        
        if not selected_icons or not selected_sizes or not selected_colors or not selected_strokes:
            messagebox.showerror(self.t("messages.error"), self.t("messages.select_requirements"))
            return
        
        self.generate_btn.config(state=tk.DISABLED, text=self.t("buttons.generating"))
        self.log(self.t("logs.generating"))
        self.log(self.t("logs.icons_count", count=len(selected_icons)))
        self.log(self.t("logs.sizes", values=", ".join(map(str, selected_sizes))))
        self.log(self.t("logs.colors", values=", ".join([name for name, _ in selected_colors])))
        self.log(self.t("logs.strokes", values=", ".join(map(str, selected_strokes))))
        self.log("-" * 40)
        
        thread = threading.Thread(
            target=self.generate_icons, 
            args=(selected_icons, selected_sizes, selected_colors, selected_strokes)
        )
        thread.daemon = True
        thread.start()
    
    def generate_icons(self, icons, sizes, colors, strokes):
        """Generar iconos en hilo"""
        count = 0
        errors = 0
        organize = self.organize_var.get()
        
        for icon in icons:
            svg_path = os.path.join(ICONS_DIR, f"{icon}.svg")
            if not os.path.exists(svg_path):
                self.log(f"⚠️ {icon}.svg no encontrado")
                continue
            
            with open(svg_path, 'r') as f:
                svg_content = f.read()
            
            for size in sizes:
                for color_name, color_hex in colors:
                    for stroke in strokes:
                        if organize:
                            size_dir = os.path.join(ICONS_DIR, f"size_{size}")
                            stroke_dir = os.path.join(size_dir, f"stroke_{stroke}")
                            os.makedirs(stroke_dir, exist_ok=True)
                            base_dir = stroke_dir
                        else:
                            base_dir = ICONS_DIR
                        
                        filename = f"{icon}_{size}px_{color_name}_stroke{stroke}.png"
                        filepath = os.path.join(base_dir, filename)
                        
                        if os.path.exists(filepath) and not self.overwrite_var.get():
                            continue
                        
                        try:
                            modified = svg_content
                            modified = modified.replace('currentColor', color_hex)
                            modified = modified.replace('stroke-width="2"', f'stroke-width="{stroke}"')
                            modified = modified.replace('width="24"', f'width="{size}"')
                            modified = modified.replace('height="24"', f'height="{size}"')
                            
                            cairosvg.svg2png(
                                bytestring=modified.encode(), 
                                write_to=filepath,
                                output_width=size, 
                                output_height=size
                            )
                            count += 1
                            
                            if count % 10 == 0:
                                self.log(self.t("logs.generated_progress", count=count))
                                
                        except Exception as e:
                            errors += 1
        
        self.log("-" * 40)
        self.log(self.t("logs.generated", count=count))
        if errors:
            self.log(self.t("logs.generation_errors", count=errors))
        self.generate_btn.config(state=tk.NORMAL, text=self.t("buttons.generate"))
        self.update_gen_info()


if __name__ == "__main__":
    root = tk.Tk()
    app = IconGeneratorApp(root)
    root.mainloop()