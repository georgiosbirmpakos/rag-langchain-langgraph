@echo off
REM Windows batch script to update vector database every hour
REM Use Windows Task Scheduler to run this script

REM Set the working directory
cd /d "%~dp0\.."

REM Set environment variables
set PYTHONPATH=%PYTHONPATH%;%CD%

REM Log file location
set LOG_FILE=%CD%\scheduler\update_logs.log

REM Create log directory if it doesn't exist
if not exist "scheduler" mkdir scheduler

REM Run the update script
echo %date% %time%: Starting vector database update... >> "%LOG_FILE%"
python scheduler\update_vector_db_windows.py >> "%LOG_FILE%" 2>&1

REM Check if the update was successful
if %errorlevel% equ 0 (
    echo %date% %time%: Vector database update completed successfully >> "%LOG_FILE%"
) else (
    echo %date% %time%: Vector database update failed >> "%LOG_FILE%"
)

echo %date% %time%: Update cycle finished >> "%LOG_FILE%"
echo --- >> "%LOG_FILE%"
