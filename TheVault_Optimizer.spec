# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('Dark Fantasy - shahi77.mp3', '.'),
        ('icon.ico', '.'),
        ('bmp_anim1_0.bmp', '.'),
        ('bmp_anim1_1.bmp', '.'),
        ('bmp_anim1_2.bmp', '.'),
        ('bmp_anim1_3.bmp', '.'),
        ('bmp_anim1_4.bmp', '.'),
        ('bmp_anim1_5.bmp', '.'),
        ('bmp_anim1_6.bmp', '.'),
        ('bmp_anim1_7.bmp', '.'),
        ('bmp_anim1_8.bmp', '.'),
    ],
    hiddenimports=['PIL', 'PIL._tkinter_finder'],
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
    name='NormieTools',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='version_info.txt',
    icon=['gamephoto.ico'],
)
