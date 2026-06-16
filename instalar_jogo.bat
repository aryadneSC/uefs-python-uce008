@echo off
echo Instalando dependências do jogo...
python -m install --user pygame-ce

echo.
echo   Iniciando o Jogo...
python jogo.py
pause
