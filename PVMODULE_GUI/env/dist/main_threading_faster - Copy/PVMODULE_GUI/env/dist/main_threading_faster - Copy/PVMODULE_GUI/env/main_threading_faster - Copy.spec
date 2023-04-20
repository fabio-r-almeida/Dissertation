# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['C:/Users/Fabio/Desktop/Github/Dissertation/PVMODULE_GUI/main_threading_faster - Copy.py'],
             pathex=[],
             binaries=[],
             datas=[('C:/Users/Fabio/Desktop/Github/Dissertation/PVMODULE_GUI/env/projectName/Lib/site-packages/customtkinter', 'customtkinter/')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)


exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='main_threading_faster - Copy',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               Tree('C:\\Users\\Fabio\\Desktop\\Github\\Dissertation\\PVMODULE_GUI', prefix='PVMODULE_GUI\\'),
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main_threading_faster - Copy')
