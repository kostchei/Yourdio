#!/usr/bin/env python3
"""
Yourdio GUI - Retro Lo-Fi Music Generator

Classic Winamp-inspired graphical interface for generating algorithmic music.

This module provides a desktop GUI application with two main features:
1. Theme Generator: Create 6-hour MIDI compositions (12 x 30-minute chapters)
2. Event Soundscapes: Generate short loopable event music for games

Features:
- Visual theme parameter editing
- YAML theme import/export
- Real-time generation status
- Retro dark/green aesthetic
- Cross-platform compatibility (Windows, macOS, Linux)

Author: Yourdio Contributors
License: MIT
"""

__version__ = "1.0.2"
__author__ = "Yourdio Contributors"
__license__ = "MIT"

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import yaml
from pathlib import Path
from typing import Dict, Any

from yourdio import generate_full_composition
from event_generator import EventSoundscapeGenerator
from theme_loader import ThemeLoader


class RetroStyle:
    """Retro Winamp-inspired color scheme and styling"""

    # Classic Winamp colors
    BG_DARK = "#000000"
    BG_MEDIUM = "#0a0a0a"
    BG_LIGHT = "#1a1a1a"

    ACCENT_GREEN = "#00ff00"
    ACCENT_CYAN = "#00ffff"
    ACCENT_ORANGE = "#ff8800"
    ACCENT_BLUE = "#0088ff"

    TEXT_BRIGHT = "#00ff00"
    TEXT_NORMAL = "#88ff88"
    TEXT_DIM = "#448844"

    BORDER = "#004400"
    BUTTON_BG = "#003300"
    BUTTON_ACTIVE = "#005500"

    LCD_BG = "#0a1a0a"
    LCD_TEXT = "#00ff00"

    @classmethod
    def configure_styles(cls, root):
        """Configure ttk styles for retro look"""
        style = ttk.Style(root)

        # Configure notebook (tabs)
        style.configure("Retro.TNotebook", background=cls.BG_DARK, borderwidth=0)
        style.configure(
            "Retro.TNotebook.Tab",
            background=cls.BG_LIGHT,
            foreground="#006400",  # Dark green
            padding=[20, 8],
            borderwidth=2,
            relief="raised",
            font=("Courier", 10, "bold"),
        )
        style.map(
            "Retro.TNotebook.Tab",
            background=[("selected", cls.BG_MEDIUM)],
            foreground=[("selected", "#006400")],
            relief=[("selected", "sunken")],
        )


class YourdioGUI:
    """Main GUI application"""

    def __init__(self, root):
        self.root = root
        self.root.title("YOURDIO - Retro Lo-Fi Generator")
        self.root.geometry("900x700")
        self.root.configure(bg=RetroStyle.BG_DARK)
        self.root.resizable(True, True)

        # Apply retro styling
        RetroStyle.configure_styles(root)

        # Current theme data
        self.current_theme = ThemeLoader.DEFAULT_THEME.copy()
        self.theme_file_path = None

        # Build UI
        self.build_ui()

    def build_ui(self):
        """Build the main interface"""
        # Header
        self.build_header()

        # Main tabbed interface
        self.build_tabs()

        # Footer with status
        self.build_footer()

    def build_header(self):
        """Build header with title and logo"""
        header = tk.Frame(self.root, bg=RetroStyle.BG_DARK, height=80)
        header.pack(fill=tk.X, padx=10, pady=(10, 5))
        header.pack_propagate(False)

        # ASCII art title
        title = tk.Label(
            header,
            text="╔═══════════════════════════════════════════════════╗\n"
            "║  Y O U R D I O  ░▒▓ Retro Lo-Fi Generator ▓▒░  ║\n"
            "╚═══════════════════════════════════════════════════╝",
            font=("Courier", 10, "bold"),
            fg=RetroStyle.ACCENT_GREEN,
            bg=RetroStyle.BG_DARK,
            justify=tk.LEFT,
        )
        title.pack(side=tk.LEFT, padx=10)

        # Version info
        version = tk.Label(
            header,
            text="v1.0\nAlgorithmic\nComposer",
            font=("Courier", 8),
            fg=RetroStyle.TEXT_DIM,
            bg=RetroStyle.BG_DARK,
            justify=tk.RIGHT,
        )
        version.pack(side=tk.RIGHT, padx=10)

    def build_tabs(self):
        """Build tabbed interface"""
        # Create notebook with retro style
        self.notebook = ttk.Notebook(self.root, style="Retro.TNotebook")
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Tab 1: Theme Generator (6-hour compositions)
        self.theme_tab = tk.Frame(self.notebook, bg=RetroStyle.BG_MEDIUM)
        self.notebook.add(self.theme_tab, text=" ♪ THEME GENERATOR ")
        self.build_theme_tab()

        # Tab 2: Event Soundscapes
        self.event_tab = tk.Frame(self.notebook, bg=RetroStyle.BG_MEDIUM)
        self.notebook.add(self.event_tab, text=" ⚡ EVENT SOUNDSCAPES ")
        self.build_event_tab()

    def build_theme_tab(self):
        """Build the 6-hour theme generator interface"""
        # Left side: Parameters
        left_frame = tk.Frame(self.theme_tab, bg=RetroStyle.BG_MEDIUM)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Right side: Preview and controls
        right_frame = tk.Frame(self.theme_tab, bg=RetroStyle.BG_MEDIUM, width=300)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10)
        right_frame.pack_propagate(False)

        # === LEFT SIDE: PARAMETERS ===

        # Scrollable parameter area
        canvas = tk.Canvas(left_frame, bg=RetroStyle.BG_MEDIUM, highlightthickness=0)
        scrollbar = tk.Scrollbar(left_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=RetroStyle.BG_MEDIUM)

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Store parameter widgets
        self.theme_widgets = {}

        # Theme Name
        self.add_section(scrollable_frame, "═══ THEME INFO ═══")
        self.theme_widgets["name"] = self.add_entry(scrollable_frame, "Theme Name", "My Theme")
        self.theme_widgets["description"] = self.add_entry(
            scrollable_frame, "Description", "Custom theme"
        )

        # Tempo
        self.add_section(scrollable_frame, "═══ TEMPO ═══")
        self.theme_widgets["tempo_base"] = self.add_slider(
            scrollable_frame, "Base BPM", 40, 120, 58
        )
        self.theme_widgets["tempo_min"] = self.add_slider(scrollable_frame, "Min BPM", 40, 120, 52)
        self.theme_widgets["tempo_max"] = self.add_slider(scrollable_frame, "Max BPM", 40, 120, 68)

        # Modal Center
        self.add_section(scrollable_frame, "═══ SCALE / MODE ═══")
        self.theme_widgets["modal_center"] = self.add_dropdown(
            scrollable_frame, "Modal Center", ["D_dorian", "A_aeolian", "E_phrygian"], "D_dorian"
        )

        # Harmony
        self.add_section(scrollable_frame, "═══ HARMONY ═══")
        self.theme_widgets["harmony_type"] = self.add_entry(
            scrollable_frame, "Harmony Type", "quartal"
        )
        self.theme_widgets["harmony_intervals"] = self.add_entry(
            scrollable_frame, "Intervals (e.g. 0,3,6)", "0,3,6"
        )

        # Dynamics
        self.add_section(scrollable_frame, "═══ DYNAMICS ═══")
        self.theme_widgets["harmonic_velocity"] = self.add_slider(
            scrollable_frame, "Harmonic Velocity", 20, 100, 45
        )
        self.theme_widgets["melodic_velocity"] = self.add_slider(
            scrollable_frame, "Melodic Velocity", 20, 100, 55
        )
        self.theme_widgets["drone_velocity"] = self.add_slider(
            scrollable_frame, "Drone Velocity", 20, 100, 50
        )

        # Chaos
        self.add_section(scrollable_frame, "═══ CHAOS PARAMETERS ═══")
        self.theme_widgets["logistic_r"] = self.add_slider(
            scrollable_frame, "Logistic R", 2.5, 4.0, 3.86, resolution=0.01
        )
        self.theme_widgets["lorenz_sigma"] = self.add_slider(
            scrollable_frame, "Lorenz Sigma", 5.0, 20.0, 10.0, resolution=0.1
        )

        # Structural Arc
        self.add_section(scrollable_frame, "═══ STRUCTURAL ARC ═══")
        self.theme_widgets["arc_type"] = self.add_dropdown(
            scrollable_frame,
            "Arc Type",
            ["parabolic", "slow_burn", "descending", "flat"],
            "parabolic",
        )
        self.theme_widgets["arc_min_intensity"] = self.add_slider(
            scrollable_frame, "Min Intensity", 0.0, 1.0, 0.2, resolution=0.1
        )
        self.theme_widgets["arc_max_intensity"] = self.add_slider(
            scrollable_frame, "Max Intensity", 0.0, 1.0, 0.8, resolution=0.1
        )

        # === RIGHT SIDE: CONTROLS ===

        # File operations
        file_frame = self.create_panel(right_frame, "FILE OPERATIONS")

        tk.Button(
            file_frame,
            text="📂 Load YAML",
            command=self.load_theme_yaml,
            bg=RetroStyle.BUTTON_BG,
            fg=RetroStyle.TEXT_BRIGHT,
            activebackground=RetroStyle.BUTTON_ACTIVE,
            font=("Courier", 10),
            relief=tk.RAISED,
            bd=2,
        ).pack(fill=tk.X, pady=2)

        tk.Button(
            file_frame,
            text="💾 Save YAML",
            command=self.save_theme_yaml,
            bg=RetroStyle.BUTTON_BG,
            fg=RetroStyle.TEXT_BRIGHT,
            activebackground=RetroStyle.BUTTON_ACTIVE,
            font=("Courier", 10),
            relief=tk.RAISED,
            bd=2,
        ).pack(fill=tk.X, pady=2)

        tk.Button(
            file_frame,
            text="🔄 Reset to Default",
            command=self.reset_theme_to_default,
            bg=RetroStyle.BUTTON_BG,
            fg=RetroStyle.TEXT_DIM,
            activebackground=RetroStyle.BUTTON_ACTIVE,
            font=("Courier", 9),
            relief=tk.RAISED,
            bd=2,
        ).pack(fill=tk.X, pady=2)

        # Generation
        gen_frame = self.create_panel(right_frame, "GENERATE 6-HOUR THEME")

        tk.Label(
            gen_frame,
            text="Output Directory:",
            font=("Courier", 9),
            fg=RetroStyle.TEXT_NORMAL,
            bg=RetroStyle.BG_LIGHT,
        ).pack(anchor=tk.W)

        output_frame = tk.Frame(gen_frame, bg=RetroStyle.BG_LIGHT)
        output_frame.pack(fill=tk.X, pady=5)

        self.theme_output_var = tk.StringVar(value="midi_output")
        tk.Entry(
            output_frame,
            textvariable=self.theme_output_var,
            font=("Courier", 9),
            bg=RetroStyle.LCD_BG,
            fg=RetroStyle.LCD_TEXT,
            insertbackground=RetroStyle.LCD_TEXT,
            relief=tk.SUNKEN,
            bd=2,
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Button(
            output_frame,
            text="...",
            command=self.browse_theme_output,
            bg=RetroStyle.BUTTON_BG,
            fg=RetroStyle.TEXT_BRIGHT,
            font=("Courier", 8),
            width=3,
        ).pack(side=tk.RIGHT, padx=(5, 0))

        tk.Button(
            gen_frame,
            text="▶ GENERATE 12 CHAPTERS",
            command=self.generate_theme,
            bg=RetroStyle.ACCENT_ORANGE,
            fg=RetroStyle.BG_DARK,
            activebackground=RetroStyle.ACCENT_CYAN,
            font=("Courier", 10, "bold"),
            relief=tk.RAISED,
            bd=3,
            height=2,
        ).pack(fill=tk.X, pady=10)

        # Progress info
        info_frame = self.create_panel(right_frame, "INFO")

        self.theme_info_label = tk.Label(
            info_frame,
            text="Duration: 6 hours\n12 chapters × 30 min\n\nAdjust parameters\nand generate!",
            font=("Courier", 9),
            fg=RetroStyle.TEXT_DIM,
            bg=RetroStyle.BG_LIGHT,
            justify=tk.LEFT,
        )
        self.theme_info_label.pack(fill=tk.BOTH, expand=True)

    def build_event_tab(self):
        """Build the event soundscapes interface"""
        # Left side: Event selection
        left_frame = tk.Frame(self.event_tab, bg=RetroStyle.BG_MEDIUM)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Right side: Controls
        right_frame = tk.Frame(self.event_tab, bg=RetroStyle.BG_MEDIUM, width=300)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10)
        right_frame.pack_propagate(False)

        # === LEFT SIDE: EVENT SELECTION ===

        self.add_section(left_frame, "═══ SELECT EVENTS TO GENERATE ═══")

        # Event checkboxes
        self.event_vars = {}

        events = EventSoundscapeGenerator.EVENT_CONFIGS

        for event_name, config in events.items():
            frame = tk.Frame(left_frame, bg=RetroStyle.BG_LIGHT, relief=tk.RAISED, bd=1)
            frame.pack(fill=tk.X, pady=3)

            var = tk.BooleanVar(value=True)
            self.event_vars[event_name] = var

            cb = tk.Checkbutton(
                frame,
                text=f"[{event_name.upper()}]",
                variable=var,
                font=("Courier", 10, "bold"),
                fg=RetroStyle.ACCENT_CYAN,
                bg=RetroStyle.BG_LIGHT,
                selectcolor=RetroStyle.BG_DARK,
                activebackground=RetroStyle.BG_LIGHT,
                activeforeground=RetroStyle.ACCENT_GREEN,
            )
            cb.pack(anchor=tk.W, padx=5, pady=2)

            desc = tk.Label(
                frame,
                text=f"  {config['description']} ({config['duration_minutes']} min)",
                font=("Courier", 8),
                fg=RetroStyle.TEXT_DIM,
                bg=RetroStyle.BG_LIGHT,
            )
            desc.pack(anchor=tk.W, padx=20, pady=(0, 5))

        # Select all / none buttons
        btn_frame = tk.Frame(left_frame, bg=RetroStyle.BG_MEDIUM)
        btn_frame.pack(fill=tk.X, pady=10)

        tk.Button(
            btn_frame,
            text="☑ Select All",
            command=lambda: self.toggle_all_events(True),
            bg=RetroStyle.BUTTON_BG,
            fg=RetroStyle.TEXT_BRIGHT,
            font=("Courier", 9),
            width=15,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="☐ Select None",
            command=lambda: self.toggle_all_events(False),
            bg=RetroStyle.BUTTON_BG,
            fg=RetroStyle.TEXT_BRIGHT,
            font=("Courier", 9),
            width=15,
        ).pack(side=tk.LEFT, padx=5)

        # === RIGHT SIDE: CONTROLS ===

        # Theme selection
        theme_frame = self.create_panel(right_frame, "THEME")

        tk.Label(
            theme_frame,
            text="Use current theme\nsettings from\nTheme Generator tab",
            font=("Courier", 9),
            fg=RetroStyle.TEXT_DIM,
            bg=RetroStyle.BG_LIGHT,
            justify=tk.CENTER,
        ).pack(pady=10)

        tk.Button(
            theme_frame,
            text="📂 Load Different YAML",
            command=self.load_event_theme_yaml,
            bg=RetroStyle.BUTTON_BG,
            fg=RetroStyle.TEXT_BRIGHT,
            font=("Courier", 9),
            relief=tk.RAISED,
            bd=2,
        ).pack(fill=tk.X, pady=5)

        # Output
        output_frame = self.create_panel(right_frame, "OUTPUT")

        tk.Label(
            output_frame,
            text="Output Directory:",
            font=("Courier", 9),
            fg=RetroStyle.TEXT_NORMAL,
            bg=RetroStyle.BG_LIGHT,
        ).pack(anchor=tk.W)

        output_dir_frame = tk.Frame(output_frame, bg=RetroStyle.BG_LIGHT)
        output_dir_frame.pack(fill=tk.X, pady=5)

        self.event_output_var = tk.StringVar(value="events_output")
        tk.Entry(
            output_dir_frame,
            textvariable=self.event_output_var,
            font=("Courier", 9),
            bg=RetroStyle.LCD_BG,
            fg=RetroStyle.LCD_TEXT,
            insertbackground=RetroStyle.LCD_TEXT,
            relief=tk.SUNKEN,
            bd=2,
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Button(
            output_dir_frame,
            text="...",
            command=self.browse_event_output,
            bg=RetroStyle.BUTTON_BG,
            fg=RetroStyle.TEXT_BRIGHT,
            font=("Courier", 8),
            width=3,
        ).pack(side=tk.RIGHT, padx=(5, 0))

        # Generate button
        tk.Button(
            output_frame,
            text="▶ GENERATE EVENTS",
            command=self.generate_events,
            bg=RetroStyle.ACCENT_ORANGE,
            fg=RetroStyle.BG_DARK,
            activebackground=RetroStyle.ACCENT_CYAN,
            font=("Courier", 10, "bold"),
            relief=tk.RAISED,
            bd=3,
            height=2,
        ).pack(fill=tk.X, pady=10)

        # Info
        info_frame = self.create_panel(right_frame, "EVENT INFO")

        self.event_info_label = tk.Label(
            info_frame,
            text="Select events above\nto generate short\nloopable soundscapes\n\nPerfect for games\nand interactive media",
            font=("Courier", 9),
            fg=RetroStyle.TEXT_DIM,
            bg=RetroStyle.BG_LIGHT,
            justify=tk.LEFT,
        )
        self.event_info_label.pack(fill=tk.BOTH, expand=True)

    def build_footer(self):
        """Build status footer"""
        self.footer = tk.Frame(self.root, bg=RetroStyle.BG_DARK, height=120)
        self.footer.pack(fill=tk.X, padx=10, pady=(5, 10))
        self.footer.pack_propagate(False)

        # Status label
        status_label = tk.Label(
            self.footer,
            text="═══ STATUS ═══",
            font=("Courier", 9, "bold"),
            fg=RetroStyle.ACCENT_GREEN,
            bg=RetroStyle.BG_DARK,
        )
        status_label.pack(anchor=tk.W, pady=(5, 2))

        # Scrolled text for log output
        self.status_text = scrolledtext.ScrolledText(
            self.footer,
            height=5,
            font=("Courier", 8),
            bg=RetroStyle.LCD_BG,
            fg=RetroStyle.LCD_TEXT,
            insertbackground=RetroStyle.LCD_TEXT,
            relief=tk.SUNKEN,
            bd=2,
        )
        self.status_text.pack(fill=tk.BOTH, expand=True)

        self.log("Yourdio initialized. Ready to generate music.")

    # === HELPER FUNCTIONS ===

    def create_panel(self, parent, title):
        """Create a styled panel with title"""
        container = tk.Frame(parent, bg=RetroStyle.BG_MEDIUM)
        container.pack(fill=tk.X, pady=5)

        tk.Label(
            container,
            text=f"═══ {title} ═══",
            font=("Courier", 9, "bold"),
            fg=RetroStyle.ACCENT_CYAN,
            bg=RetroStyle.BG_MEDIUM,
        ).pack(pady=(0, 5))

        panel = tk.Frame(container, bg=RetroStyle.BG_LIGHT, relief=tk.SUNKEN, bd=2)
        panel.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        return panel

    def add_section(self, parent, title):
        """Add a section header"""
        tk.Label(
            parent,
            text=title,
            font=("Courier", 10, "bold"),
            fg=RetroStyle.ACCENT_GREEN,
            bg=RetroStyle.BG_MEDIUM,
        ).pack(pady=(15, 5), anchor=tk.W)

    def add_entry(self, parent, label, default=""):
        """Add a text entry field"""
        frame = tk.Frame(parent, bg=RetroStyle.BG_LIGHT)
        frame.pack(fill=tk.X, pady=3)

        tk.Label(
            frame,
            text=f"{label}:",
            font=("Courier", 9),
            fg=RetroStyle.TEXT_NORMAL,
            bg=RetroStyle.BG_LIGHT,
            width=25,
            anchor=tk.W,
        ).pack(side=tk.LEFT, padx=5)

        var = tk.StringVar(value=default)
        entry = tk.Entry(
            frame,
            textvariable=var,
            font=("Courier", 9),
            bg=RetroStyle.LCD_BG,
            fg=RetroStyle.LCD_TEXT,
            insertbackground=RetroStyle.LCD_TEXT,
        )
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        return var

    def add_slider(self, parent, label, min_val, max_val, default, resolution=1):
        """Add a slider control"""
        frame = tk.Frame(parent, bg=RetroStyle.BG_LIGHT)
        frame.pack(fill=tk.X, pady=3)

        label_frame = tk.Frame(frame, bg=RetroStyle.BG_LIGHT)
        label_frame.pack(fill=tk.X)

        tk.Label(
            label_frame,
            text=f"{label}:",
            font=("Courier", 9),
            fg=RetroStyle.TEXT_NORMAL,
            bg=RetroStyle.BG_LIGHT,
            anchor=tk.W,
        ).pack(side=tk.LEFT, padx=5)

        value_var = tk.DoubleVar(value=default)
        value_label = tk.Label(
            label_frame,
            textvariable=value_var,
            font=("Courier", 9, "bold"),
            fg=RetroStyle.ACCENT_CYAN,
            bg=RetroStyle.BG_LIGHT,
            width=8,
            anchor=tk.E,
        )
        value_label.pack(side=tk.RIGHT, padx=5)

        slider = tk.Scale(
            frame,
            from_=min_val,
            to=max_val,
            resolution=resolution,
            orient=tk.HORIZONTAL,
            variable=value_var,
            showvalue=False,
            bg=RetroStyle.BG_LIGHT,
            fg=RetroStyle.TEXT_BRIGHT,
            troughcolor=RetroStyle.LCD_BG,
            activebackground=RetroStyle.ACCENT_GREEN,
            highlightthickness=0,
        )
        slider.pack(fill=tk.X, padx=5)

        return value_var

    def add_dropdown(self, parent, label, options, default):
        """Add a dropdown menu"""
        frame = tk.Frame(parent, bg=RetroStyle.BG_LIGHT)
        frame.pack(fill=tk.X, pady=3)

        tk.Label(
            frame,
            text=f"{label}:",
            font=("Courier", 9),
            fg=RetroStyle.TEXT_NORMAL,
            bg=RetroStyle.BG_LIGHT,
            width=25,
            anchor=tk.W,
        ).pack(side=tk.LEFT, padx=5)

        var = tk.StringVar(value=default)
        dropdown = ttk.Combobox(
            frame, textvariable=var, values=options, font=("Courier", 9), state="readonly"
        )
        dropdown.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        return var

    def log(self, message):
        """Add message to status log"""
        self.status_text.insert(tk.END, f"> {message}\n")
        self.status_text.see(tk.END)
        self.root.update_idletasks()

    # === THEME TAB FUNCTIONS ===

    def get_theme_from_widgets(self) -> Dict[str, Any]:
        """Build theme dict from widget values"""
        try:
            intervals = [
                int(x.strip()) for x in self.theme_widgets["harmony_intervals"].get().split(",")
            ]
        except Exception:
            intervals = [0, 3, 6]

        theme = {
            "name": self.theme_widgets["name"].get(),
            "description": self.theme_widgets["description"].get(),
            "modal_center": self.theme_widgets["modal_center"].get(),
            "harmony_rules": {
                "type": self.theme_widgets["harmony_type"].get(),
                "intervals": intervals,
            },
            "tempo": {
                "base": int(self.theme_widgets["tempo_base"].get()),
                "variation_range": [
                    int(self.theme_widgets["tempo_min"].get()),
                    int(self.theme_widgets["tempo_max"].get()),
                ],
            },
            "dynamics": {
                "harmonic_bed": {
                    "base_velocity": int(self.theme_widgets["harmonic_velocity"].get()),
                    "prime_mod_range": 20,
                },
                "melodic_texture": {
                    "base_velocity": int(self.theme_widgets["melodic_velocity"].get()),
                    "prime_mod_range": 25,
                },
                "drones": {"velocity": int(self.theme_widgets["drone_velocity"].get())},
                "ambient_events": {"base_velocity": 60, "intensity_scaling": 30},
            },
            "chaos": {
                "logistic_r": float(self.theme_widgets["logistic_r"].get()),
                "lorenz_sigma": float(self.theme_widgets["lorenz_sigma"].get()),
                "lorenz_rho": 28.0,
                "lorenz_beta": 8.0 / 3.0,
            },
            "structural_arc": {
                "type": self.theme_widgets["arc_type"].get(),
                "min_intensity": float(self.theme_widgets["arc_min_intensity"].get()),
                "max_intensity": float(self.theme_widgets["arc_max_intensity"].get()),
                "climax_chapter": 6,
            },
        }

        # Merge with default for missing fields
        return ThemeLoader._merge_with_defaults(theme)

    def set_widgets_from_theme(self, theme: Dict[str, Any]):
        """Update widgets from theme dict"""
        self.theme_widgets["name"].set(theme.get("name", "Theme"))
        self.theme_widgets["description"].set(theme.get("description", ""))

        tempo = theme.get("tempo", {})
        if isinstance(tempo, dict):
            self.theme_widgets["tempo_base"].set(tempo.get("base", 58))
            var_range = tempo.get("variation_range", [52, 68])
            self.theme_widgets["tempo_min"].set(var_range[0])
            self.theme_widgets["tempo_max"].set(var_range[1])

        self.theme_widgets["modal_center"].set(theme.get("modal_center", "D_dorian"))

        harmony = theme.get("harmony_rules", {})
        self.theme_widgets["harmony_type"].set(harmony.get("type", "quartal"))
        intervals = harmony.get("intervals", [0, 3, 6])
        self.theme_widgets["harmony_intervals"].set(",".join(map(str, intervals)))

        dynamics = theme.get("dynamics", {})
        self.theme_widgets["harmonic_velocity"].set(
            dynamics.get("harmonic_bed", {}).get("base_velocity", 45)
        )
        self.theme_widgets["melodic_velocity"].set(
            dynamics.get("melodic_texture", {}).get("base_velocity", 55)
        )
        self.theme_widgets["drone_velocity"].set(dynamics.get("drones", {}).get("velocity", 50))

        chaos = theme.get("chaos", {})
        self.theme_widgets["logistic_r"].set(chaos.get("logistic_r", 3.86))
        self.theme_widgets["lorenz_sigma"].set(chaos.get("lorenz_sigma", 10.0))

        arc = theme.get("structural_arc", {})
        self.theme_widgets["arc_type"].set(arc.get("type", "parabolic"))
        self.theme_widgets["arc_min_intensity"].set(arc.get("min_intensity", 0.2))
        self.theme_widgets["arc_max_intensity"].set(arc.get("max_intensity", 0.8))

    def load_theme_yaml(self):
        """Load theme from YAML file"""
        filename = filedialog.askopenfilename(
            title="Load Theme YAML",
            filetypes=[("YAML files", "*.yaml *.yml"), ("All files", "*.*")],
            initialdir=".",
        )

        if filename:
            try:
                theme = ThemeLoader.load(Path(filename))
                self.current_theme = theme
                self.theme_file_path = filename
                self.set_widgets_from_theme(theme)
                self.log(f"Loaded theme: {theme.get('name', 'Unnamed')}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load theme:\n{e}")
                self.log(f"ERROR: {e}")

    def save_theme_yaml(self):
        """Save current theme to YAML file"""
        filename = filedialog.asksaveasfilename(
            title="Save Theme YAML",
            defaultextension=".yaml",
            filetypes=[("YAML files", "*.yaml"), ("All files", "*.*")],
            initialdir=".",
            initialfile=self.theme_widgets["name"].get().lower().replace(" ", "_") + ".yaml",
        )

        if filename:
            try:
                theme = self.get_theme_from_widgets()
                with open(filename, "w") as f:
                    yaml.dump(theme, f, default_flow_style=False, sort_keys=False)
                self.log(f"Saved theme to: {filename}")
                messagebox.showinfo("Success", f"Theme saved to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save theme:\n{e}")
                self.log(f"ERROR: {e}")

    def reset_theme_to_default(self):
        """Reset to default theme"""
        if messagebox.askyesno("Reset", "Reset all parameters to default theme?"):
            self.current_theme = ThemeLoader.DEFAULT_THEME.copy()
            self.set_widgets_from_theme(self.current_theme)
            self.log("Reset to default theme")

    def browse_theme_output(self):
        """Browse for output directory"""
        dirname = filedialog.askdirectory(title="Select Output Directory", initialdir=".")
        if dirname:
            self.theme_output_var.set(dirname)

    def generate_theme(self):
        """Generate 6-hour composition in background thread"""
        output_dir = self.theme_output_var.get()

        if not output_dir:
            messagebox.showerror("Error", "Please specify output directory")
            return

        # Get current theme from widgets
        theme = self.get_theme_from_widgets()

        # Save theme temporarily
        temp_theme_path = Path("temp_theme.yaml")
        with open(temp_theme_path, "w") as f:
            yaml.dump(theme, f)

        self.log(f"Starting generation: {theme['name']}")
        self.log("Generating 12 chapters (this will take a while)...")

        # Run in background thread
        def generate():
            try:
                generate_full_composition(
                    theme_path=str(temp_theme_path), output_dir=Path(output_dir)
                )
                self.log("✓ Generation complete!")
                temp_theme_path.unlink()  # Clean up
                messagebox.showinfo("Success", f"Generated 12 chapters!\nSaved to: {output_dir}")
            except Exception as e:
                self.log(f"ERROR: {e}")
                messagebox.showerror("Error", f"Generation failed:\n{e}")

        thread = threading.Thread(target=generate, daemon=True)
        thread.start()

    # === EVENT TAB FUNCTIONS ===

    def toggle_all_events(self, state: bool):
        """Select or deselect all events"""
        for var in self.event_vars.values():
            var.set(state)

    def load_event_theme_yaml(self):
        """Load theme for event generation"""
        self.load_theme_yaml()  # Reuse the same function

    def browse_event_output(self):
        """Browse for event output directory"""
        dirname = filedialog.askdirectory(title="Select Output Directory", initialdir=".")
        if dirname:
            self.event_output_var.set(dirname)

    def generate_events(self):
        """Generate selected event soundscapes"""
        output_dir = self.event_output_var.get()

        if not output_dir:
            messagebox.showerror("Error", "Please specify output directory")
            return

        # Get selected events
        selected_events = [name for name, var in self.event_vars.items() if var.get()]

        if not selected_events:
            messagebox.showwarning("Warning", "No events selected!")
            return

        # Get current theme
        theme = self.get_theme_from_widgets()

        # Save theme temporarily
        temp_theme_path = Path("temp_event_theme.yaml")
        with open(temp_theme_path, "w") as f:
            yaml.dump(theme, f)

        self.log(f"Generating {len(selected_events)} events...")

        # Run in background thread
        def generate():
            try:
                files = EventSoundscapeGenerator.generate_event_set(
                    theme_path=str(temp_theme_path),
                    events=selected_events,
                    output_dir=Path(output_dir),
                )
                self.log(f"✓ Generated {len(files)} event soundscapes!")
                temp_theme_path.unlink()  # Clean up
                messagebox.showinfo(
                    "Success", f"Generated {len(files)} events!\nSaved to: {output_dir}"
                )
            except Exception as e:
                self.log(f"ERROR: {e}")
                messagebox.showerror("Error", f"Generation failed:\n{e}")

        thread = threading.Thread(target=generate, daemon=True)
        thread.start()


def main():
    """Launch the GUI"""
    root = tk.Tk()
    _app = YourdioGUI(root)  # noqa: F841
    root.mainloop()


if __name__ == "__main__":
    main()
