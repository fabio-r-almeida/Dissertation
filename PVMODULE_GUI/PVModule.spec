# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['C:/Users/Fabio/Desktop/Github/Dissertation/PVMODULE_GUI/PVModule.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/Users/Fabio/Desktop/Github/Dissertation/PVMODULE_GUI/config.ini', '.'), ('C:/Users/Fabio/Desktop/Github/Dissertation/PVMODULE_GUI/PPFD_Plot.py', '.'), ('C:/Users/Fabio/Desktop/Github/Dissertation/PVMODULE_GUI/VERSION.txt', '.'), ('C:/Users/Fabio/Desktop/Github/Dissertation/PVMODULE_GUI/Plot.py', '.'), ('C:/Users/Fabio/Desktop/Github/Dissertation/PVMODULE_GUI/Map.py', '.'), ('C:/Users/Fabio/Desktop/Github/Dissertation/PVMODULE_GUI/Splash.py', '.'), ('C:/Users/Fabio/Desktop/Github/Dissertation/PVMODULE_GUI/Get_Data_Threads.py', '.'), ('C:/Users/Fabio/Desktop/Github/Dissertation/PVMODULE_GUI/images', 'images/'), ('C:/Users/Fabio/AppData/Local/Programs/Python/Python38/Lib/site-packages/customtkinter', 'customtkinter/')],
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

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PVModule',
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
    icon=['C:\\Users\\Fabio\\Desktop\\Github\\Dissertation\\PVMODULE_GUI\\images\\icon.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PVModule',
)
