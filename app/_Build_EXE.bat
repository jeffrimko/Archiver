:: Builds a Windows EXE from the Python scripts.
:: __Dependencies__:
:: PyInstaller must have a wrapper batch file on the PATH.

::=============================================================::
:: COPYRIGHT 2013, REVISED 2013, Jeff Rimko.                   ::
::=============================================================::

:: Set up environment.
@set TITLE=%~n0 "%~dp0"
@cd /d %~dp0 && echo off && title %TITLE%

::=============================================================::
:: SECTION: Global Definitions                                 ::
::=============================================================::

:: Output directory for build.
set OUTDIR=__output__

::=============================================================::
:: SECTION: Main Body                                          ::
::=============================================================::

mkdir %OUTDIR% 2>NUL
call pyinstaller --out=%OUTDIR% --name=archiver --onefile --console archiver.py
call pyinstaller --out=%OUTDIR% --name=garchiver --onefile --windowed gui.pyw
mv *.log %OUTDIR%
pause
exit /b 0
