@echo off
setlocal enabledelayedexpansion

REM Configuration automatique de l'environnement NLP pour Windows

REM Vérification de Python
where python3.9 > nul 2>&1
if %errorlevel% neq 0 (
    echo Python 3.9 n'est pas installé

    REM Téléchargement automatique de Python
    echo Téléchargement de Python 3.9...
    powershell -Command "& {Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))}"
    choco install python --version=3.9.7
)

REM Configuration de l'environnement virtuel
python3.9 -m venv nlp_env

REM Activation de l'environnement
call nlp_env\Scripts\activate

REM Mise à jour de pip
python -m pip install --upgrade pip setuptools wheel

REM Installation des dépendances
pip install -r requirements.txt

echo Environnement NLP configuré avec succès!
echo Pour activer : nlp_env\Scripts\activate

pause