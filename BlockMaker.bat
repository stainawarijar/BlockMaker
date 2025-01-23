@echo off

REM Below only required when using packages not part of Python's standard library
REM @echo Creating virtual environment...
REM python -m venv venv

REM @echo Activating virtual environment...
REM call venv\Scripts\activate

REM @echo Installing required packages...
REM pip install -r requirements.txt

@echo Running BlockMaker
python BlockMaker.py

REM Pause to keep the window open
pause