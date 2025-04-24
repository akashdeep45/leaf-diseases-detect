@echo off
echo Starting Plant Disease Detection System...
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed! Please install Python 3.8 or higher.
    pause
    exit /b
)

:: Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Failed to create virtual environment!
        pause
        exit /b
    )
)

:: Activate virtual environment using full path
echo Activating virtual environment...
set VIRTUAL_ENV=%CD%\venv
set PATH=%VIRTUAL_ENV%\Scripts;%PATH%
set PYTHONPATH=%VIRTUAL_ENV%\Lib\site-packages

:: Install requirements if needed
if not exist venv\Lib\site-packages\streamlit (
    echo Installing required packages...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo Failed to install requirements!
        pause
        exit /b
    )
)

:: Run the application
echo Starting the application...
echo Please wait while the application loads...
echo.
echo Once the application starts, open your browser and go to:
echo http://localhost:8501
echo.
python -m streamlit run main.py

:: Keep the window open if there's an error
if errorlevel 1 (
    echo.
    echo An error occurred while running the application.
    pause
) 