# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['D:\\Code\\Yourdio\\yourdio_gui.py'],
    pathex=[],
    binaries=[],
    datas=[('D:\\Code\\Yourdio\\yourdio.py', '.'), ('D:\\Code\\Yourdio\\theme_loader.py', '.'), ('D:\\Code\\Yourdio\\event_generator.py', '.'), ('D:\\Code\\Yourdio\\theme_schema.yaml', '.'), ('D:\\Code\\Yourdio\\themes', 'themes')],
    hiddenimports=['yaml', 'midiutil', 'pygame', 'numpy', 'tkinter', 'tkinter.ttk', 'tkinter.filedialog', 'tkinter.messagebox', 'tkinter.scrolledtext'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Yourdio',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['D:\\Code\\Yourdio\\yourdio_icon.ico'],
)
