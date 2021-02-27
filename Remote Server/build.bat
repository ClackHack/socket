pyinstaller gui.py --noconsole --onefile
RMDIR /S /Q Build
del gui.spec
ren dist\gui.exe Chatroom.exe
del Chatroom.exe
move dist\Chatroom.exe .
RMDIR /S /Q dist