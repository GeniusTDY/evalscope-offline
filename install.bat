@echo off
rem EvalScope Offline one-click deploy (Windows)
rem Usage: install.bat <局域网pip源URL> [数据集缓存绝对路径]
rem   <URL> required, e.g. http://192.168.1.10/simple/
rem   [path] optional, default is the bundled datasets_cache\modelscope
setlocal

if "%~1"=="" (
    echo Usage: install.bat ^<局域网pip源URL^> [数据集缓存绝对路径]
    exit /b 1
)
set "INDEX_URL=%~1"
set "ROOT=%~dp0"
if "%~2"=="" (
    set "CACHE_DIR=%ROOT%datasets_cache\modelscope"
) else (
    set "CACHE_DIR=%~2"
)

echo ==^> Creating virtual env
python -m venv .venv
call .venv\Scripts\activate.bat

echo ==^> Installing evalscope (offline wheel)
pip install --no-deps "%ROOT%dist\evalscope-1.11.1-py3-none-any.whl"

echo ==^> Installing deps from LAN mirror: %INDEX_URL%
pip install -r "%ROOT%requirements.txt" --index-url "%INDEX_URL%"

echo.
echo =============================================
echo   Deploy done. Set dataset-cache env vars:
echo =============================================
echo   set MODELSCOPE_CACHE=%CACHE_DIR%
echo   set EVALSCOPE_CACHE=%CACHE_DIR%\datasets
echo.
echo   Verify with:
echo   evalscope --help
echo   evalscope benchmark-info --list
echo =============================================
endlocal