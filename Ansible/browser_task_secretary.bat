@echo off
set "CMD_FILE=C:\Users\Secretary\user_behavior_generation\worker\current_cmd.txt"
set "WORKER_DIR=C:\Users\Secretary\user_behavior_generation\worker"

:: --- FASE 1: RICEZIONE DA ANSIBLE ---
if NOT "%~1"=="" goto :MODE_RECEIVE
goto :MODE_EXECUTE

:MODE_RECEIVE
set "P1=%~1"
set "P2=%~2"
set "P3=%~3"
set "P4=%~4"

:: Logica Split URL aggiornata con Durata
:: Caso Split (es. youtube id): 4 argomenti (P1=Part1, P2=Part2, P3=Action, P4=Duration)
if NOT "%P4%"=="" (
    set "INPUT_TARGET=%P1%=%P2%"
    set "ACTION=%P3%"
    set "DURATION=%P4%"
) else (
    :: Caso Standard: 3 argomenti (P1=Target, P2=Action, P3=Duration)
    set "INPUT_TARGET=%P1%"
    set "ACTION=%P2%"
    set "DURATION=%P3%"
)

if "%ACTION%"=="" set ACTION=generic
if "%DURATION%"=="" set DURATION=300

:: Scriviamo nel file: TYPE DURATION TARGET (Ordine sicuro per parsing)
echo %ACTION% %DURATION% %INPUT_TARGET%> "%CMD_FILE%"
schtasks /run /tn OpenBrowser
exit /b 0

:MODE_EXECUTE
:: --- FASE 2: ESECUZIONE VISIBILE ---
set /p MY_CMD=<"%CMD_FILE%"

:: Parsiamo la stringa: TYPE=1, DURATION=2, TARGET=Tutto il resto (*)
for /f "tokens=1,2* delims= " %%a in ("%MY_CMD%") do (
    set "TYPE=%%a"
    set "DURATION=%%b"
    set "TARGET=%%c"
)

cd /d "%WORKER_DIR%"

:: --- SELEZIONE AZIONE ---

:: CASO 1: STAMPA (Ignora durata, fa azione one-shot)
if "%TYPE%"=="print" (
    echo Esecuzione Print...
    .\PDFtoPrinter.exe "%TARGET%"
    timeout /t 15 /nobreak
    taskkill /IM AcroRd32.exe /F /T 2>nul
    taskkill /IM msedge.exe /F /T 2>nul
    goto :EOF
)

:: CASO 2: MAIL (Apre solo la pagina)
if "%TYPE%"=="mail" (
    echo Esecuzione Mail...
    start "" msedge.exe --app=https://mail.google.com/mail/u/0/
    goto :EOF
)

:: CASO 3: PDF (Passiamo la DURATA)
if "%TYPE%"=="pdf" (
    echo Esecuzione PDF Reader per %DURATION%s...
    taskkill /IM msedge.exe /F /T 2>nul
    .\venv\Scripts\python.exe pdf_worker.py "%TARGET%" %DURATION%
    pause
    goto :EOF
)

:: CASO 4: WEB (Passiamo la DURATA)
echo Esecuzione Web Script per %DURATION%s...
taskkill /IM msedge.exe /F /T 2>nul

.\venv\Scripts\python.exe smart_worker.py "%TARGET%" "%TYPE%" %DURATION%
echo.
echo Script Python terminato.
pause

:EOF
exit /b 0