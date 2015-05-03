# -*- mode: python -*-
a = Analysis(['./src/compiler.py'],
             pathex=['/home/abhaykrpt/Desktop/asgn4'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='codegen',
          debug=False,
          strip=None,
          upx=True,
          console=True )
