setlocal enabledelayedexpansion
set option=""
if "%1"=="-s" set option="%1" "%2"
del %2_meminfo.txt
for /L %%g in (1,1,7200) do (
adb %option% shell dumpsys meminfo >> %2_meminfo.txt
timeout /t 60 /nobreak
)
