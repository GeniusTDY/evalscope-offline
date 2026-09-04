@echo off
rem EvalScope Offline one-click deploy (Windows)
rem Usage: install.bat [数据集缓存绝对路径]
rem Note: LAN pip index is configured globally, no index URL needed here
setlocal

set "ROOT=%~dp0"
if "%~1"=="" (
    set "CACHE_DIR=%ROOT%datasets_cache\modelscope"
) else (
    set "CACHE_DIR=%~1"
)

echo ==^> Creating virtual env
python -m venv .venv
call .venv\Scripts\activate.bat

echo ==^> Installing evalscope (offline wheel)
pip install --no-deps "%ROOT%dist\evalscope-1.11.1-py3-none-any.whl"

echo ==^> Installing deps from global pip source
pip install -r "%ROOT%requirements.txt"

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