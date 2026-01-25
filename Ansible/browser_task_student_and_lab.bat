@echo off
set "CMD_FILE=C:\Users\Student\user_behavior_generation\worker\current_cmd.txt"
set "WORKER_DIR=C:\Users\Student\user_behavior_generation\worker"

:: --- FASE 1: RICEZIONE DA ANSIBLE ---
if NOT "%~1"=="" goto :MODE_RECEIVE
goto :MODE_EXECUTE

:MODE_RECEIVE
:: Ansible ci passa: %1=FILE_PATH/URL, %2=ACTION, %3=DURATION
set INPUT_TARGET=%~1
set ACTION=%~2
set DURATION=%~3

if "%ACTION%"=="" set ACTION=generic
if "%DURATION%"=="" set DURATION=300

:: Scriviamo nel file: TYPE DURATION TARGET (senza spazi extra in fondo)
echo %ACTION% %DURATION% %INPUT_TARGET%> "%CMD_FILE%"

:: Avvia Task Scheduler (visibile)
schtasks /run /tn OpenBrowser
exit /b 0

:MODE_EXECUTE
:: --- FASE 2: ESECUZIONE VISIBILE ---
set /p MY_CMD=<"%CMD_FILE%"

:: Parsiamo: TYPE (token 1), DURATION (token 2), TARGET (token 3 e successivi per gli spazi)
for /f "tokens=1,2* delims= " %%a in ("%MY_CMD%") do (
    set TYPE=%%a
    set DURATION=%%b
    set FILE_TARGET=%%c
)

taskkill /IM msedge.exe /F /T 2>nul
taskkill /IM python.exe /F /T 2>nul

cd /d "%WORKER_DIR%"

:: --- SELEZIONE SCRIPT ---
if "%TYPE%"=="pdf" (
    :: Chiama script PDF con durata
    .\venv\Scripts\python.exe pdf_worker.py "%FILE_TARGET%" %DURATION%
) else (
    :: Chiama script Web con durata
    .\venv\Scripts\python.exe smart_worker.py "%FILE_TARGET%" %TYPE% %DURATION%
)

exit /b 0