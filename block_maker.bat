@echo off

REM Below only required when using packages not part of Python's standard library
@echo Creating virtual environment...
python -m venv venv

@echo Activating virtual environment...
call venv\Scripts\activate

@echo Installing required packages...
pip install -r requirements.txt

@echo Running BlockMaker
python block_maker.py

REM Pause to keep the window open
pause
