# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['C:/Users/Fabio/Desktop/Github/Dissertation/PVMODULE_GUI/Main.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/Users/Fabio/Desktop/Github/Dissertation/PVMODULE_GUI/Plot.py', '.'), ('C:/Users/Fabio/Desktop/Github/Dissertation/PVMODULE_GUI/Map.py', '.'), ('C:/Users/Fabio/Desktop/Github/Dissertation/PVMODULE_GUI/Splash.py', '.'), ('C:/Users/Fabio/Desktop/Github/Dissertation/PVMODULE_GUI/Loading.py', '.'), ('C:/Users/Fabio/Desktop/Github/Dissertation/PVMODULE_GUI/Get_Data_Threads.py', '.'), ('C:/Users/Fabio/Desktop/Github/Dissertation/PVMODULE_GUI/images', 'images/'), ('C:/Users/Fabio/AppData/Local/Programs/Python/Python38/Lib/site-packages/customtkinter', 'customtkinter/')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
splash = Splash(
    'C:/Users/Fabio/Desktop/Github/Dissertation/PVMODULE_GUI/images/bg_gradient.jpg',
    binaries=a.binaries,
    datas=a.datas,
    text_pos=None,
    text_size=12,
    minify_script=True,
    always_on_top=True,
)

exe = EXE(
    pyz,
    a.scripts,
    splash,
    [],
    exclude_binaries=True,
    name='Main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    splash.binaries,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Main',
)
