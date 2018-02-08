:: Builds a Windows EXE from the Python scripts.
:: **Dependencies**:
:: Python must be installed and on the PATH.
:: PyInstaller must be installed and on the PATH.

::=============================================================::
:: DEVELOPED 2013, REVISED 2018, Jeff Rimko.                   ::
::=============================================================::

:: Set up environment.
@set TITLE=%~n0 "%~dp0"
@cd /d %~dp0 && echo off && title %TITLE%

::=============================================================::
:: SECTION: Global Definitions                                 ::
::=============================================================::

:: Output directory for build.
set OUTDIR=__output__

:: Main Python directory.
set PYDIR=C:\python36

::=============================================================::
:: SECTION: Main Body                                          ::
::=============================================================::

set PATH=%PYDIR%;%PATH%
set PYTHONPATH="%PYDIR%\DLLs;%PYDIR%\Lib;%PYDIR%\Lib\site-packages"
set PYTHONHOME=%PYDIR%

mkdir %OUTDIR% 2>NUL
pyinstaller --specpath=%OUTDIR% --name=archiver --onefile --console archiver.py
pyinstaller --specpath=%OUTDIR% --name=garchiver --onefile --windowed garchiver.py
mv build %OUTDIR% 2>NUL
mv dist %OUTDIR% 2>NUL
mv *.log %OUTDIR% 2>NUL
pause
exit /b 0
