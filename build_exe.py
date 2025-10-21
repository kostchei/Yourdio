#!/usr/bin/env python3
"""
Build script for creating Yourdio Windows executable
"""

import PyInstaller.__main__
from pathlib import Path


def build_exe():
    """Build the Windows executable using PyInstaller"""

    # Get the directory where this script is located
    script_dir = Path(__file__).parent.absolute()

    # PyInstaller arguments
    args = [
        str(script_dir / "yourdio_gui.py"),  # Main script
        "--name=Yourdio",  # Executable name
        "--onefile",  # Single file executable
        "--windowed",  # No console window
        "--icon=NONE",  # No icon (can add one later)
        "--clean",  # Clean cache
        "--noconfirm",  # Overwrite without asking
        # Hidden imports that might not be detected automatically
        "--hidden-import=yaml",
        "--hidden-import=midiutil",
        "--hidden-import=pygame",
        "--hidden-import=numpy",
        "--hidden-import=tkinter",
        "--hidden-import=tkinter.ttk",
        "--hidden-import=tkinter.filedialog",
        "--hidden-import=tkinter.messagebox",
        "--hidden-import=tkinter.scrolledtext",
        # Add application data
        f'--add-data={script_dir / "yourdio.py"};.',
        f'--add-data={script_dir / "theme_loader.py"};.',
        f'--add-data={script_dir / "event_generator.py"};.',
        f'--add-data={script_dir / "theme_schema.yaml"};.',
    ]

    # Add themes directory if it exists
    themes_dir = script_dir / "themes"
    if themes_dir.exists():
        args.append(f"--add-data={themes_dir};themes")

    print("Building Yourdio.exe...")
    print(f"Output will be in: {script_dir / 'dist'}")

    # Run PyInstaller
    PyInstaller.__main__.run(args)

    print("\n" + "=" * 60)
    print("Build complete!")
    print(f"Executable location: {script_dir / 'dist' / 'Yourdio.exe'}")
    print("=" * 60)


if __name__ == "__main__":
    build_exe()
