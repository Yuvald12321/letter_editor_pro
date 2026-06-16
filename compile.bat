pyinstaller --onefile --noconsole --noconfirm --icon "logo.ico" -n "The letter editor pro" main.py
rd /S /Q "build"
"D:\Inno Setup\ISCC.exe" setup.iss
