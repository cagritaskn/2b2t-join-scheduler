# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['schedulerapp.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

a.datas += [('play_button.png','play_button.png', "DATA")]
a.datas += [('multiplayer_button.png','multiplayer_button.png', "DATA")]
a.datas += [('direct_connect_button.png','direct_connect_button.png', "DATA")]
a.datas += [('icon.ico','icon.ico', "DATA")]

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
	a.binaries,
    a.datas,
    [],
    name='schedulerapp',
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
    icon=['icon.ico'],
)
