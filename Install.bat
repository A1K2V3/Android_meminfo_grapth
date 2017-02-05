setlocal enabledelayedexpansion
set var=-s

REM get a list of all of the attached Android devices
adb devices > temp1.txt
PING 10.10.10.10 -n 1 -w 2000 >NUL
find "device" temp1.txt > devices.txt

for /F "skip=3 tokens=1" %%i in (.\devices.txt) DO (
	echo "%%i"
	start cmd /k Call meminfo.bat %var% %%i
)

@echo on