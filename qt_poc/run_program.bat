@echo off
@REM # Add in environment activation part here, eg. venv activate or conda activate
call conda activate ngif_qt_poc
@REM # Run part
python main.py
@echo on
call conda deactivate
@pause