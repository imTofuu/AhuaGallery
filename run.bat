@echo off

if exist .\main.py goto run

echo main.py not found in current directory. Move into the root directory of the project.
goto :EOF
:run

python main.py cls