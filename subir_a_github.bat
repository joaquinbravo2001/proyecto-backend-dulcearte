@echo off
title Subir Dulce Arte a GitHub
cd /d "%~dp0"
echo ========================================================
echo       Subiendo proyecto Dulce Arte a GitHub
echo ========================================================
echo.
git branch -M main
echo Enviando archivos a GitHub...
git push -u origin main
echo.
if %errorlevel% equ 0 (
    echo ========================================================
    echo  LISTO! Tu proyecto fue subido exitosamente a GitHub.
    echo ========================================================
) else (
    echo ========================================================
    echo  Hubo un problema o cancelaste la autorizacion.
    echo ========================================================
)
echo.
pause
