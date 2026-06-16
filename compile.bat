pyinstaller --onefile --noconsole --icon "logo.ico" -n "The letter editor pro" main.py
rd /S /Q "build"
del /Q "The letter editor pro.spec"
"D:\Inno Setup\ISCC.exe" setup.iss
