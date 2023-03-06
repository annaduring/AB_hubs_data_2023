%~d0
cd %~dp0
REM @echo off

REM Create virtual environment
python -m venv env


REM Activate virtual environment
call env\Scripts\activate.bat


REM Install dependencies from requirements.txt
REM pip install -r requirements.txt
pip install pandas==1.4.4
pip install psycopg2-binary
pip install pyarrow
REM pip install psycopg2==2.9.3

REM Run Python scripts in sequence
python main_eltl.py

REM Deactivate virtual environment
deactivate


