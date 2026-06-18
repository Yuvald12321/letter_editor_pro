call ".venv\Scripts\pyinstaller.exe" --specpath "build" --onefile --noconsole --icon "logo.ico" -n "The letter editor pro" main.py
rd /S /Q "build"
"D:\Inno Setup\ISCC.exe" setup.iss