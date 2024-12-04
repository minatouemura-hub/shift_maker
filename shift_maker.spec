from PyInstaller.utils.hooks import collect_all
import os

# EXEファイルに作成者情報を埋め込む
a = Analysis(['main.py'],
             pathex=['main.py'],
             binaries=[],
             datas=[],
             hiddenimports=['pandas', 'pandas._libs.tslibs.timedeltas'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[])

# 作成者情報をバージョンリソースに埋め込む
exe = EXE(a.pure, a.binaries, a.scripts,a.datas,a.zipfiles, [],
          name='shift_maker',
          author='Uemura Minato',  # 作成者名を指定# 会社名を指定
          description='Shift Maker Application',  # アプリケーションの説明
          icon=None,  # アイコンの設定が必要であれば指定
          bundle_files=3,
          runtime_tmpdir=None, 
          upx = False,
          console=False)