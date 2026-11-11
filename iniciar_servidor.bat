@echo off
title Dulce Arte - Servidor de Desarrollo
cd /d "%~dp0"
set USE_SQLITE=True
echo ========================================================
echo       Pasteleria Artesanal Dulce Arte - Django
echo ========================================================
echo Iniciando servidor en http://127.0.0.1:8000/ ...
echo Presiona CTRL+C para detener el servidor.
echo.
call .venv\Scripts\activate.bat
python manage.py runserver
pause
