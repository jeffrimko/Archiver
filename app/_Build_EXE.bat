:: Fixme
:: __Dependencies__: Fixme

::=============================================================::
:: COPYRIGHT 2013, REVISED 2013, Jeff Rimko.                   ::
::=============================================================::

:: Set up environment.
@set TITLE=%~n0 "%~dp0"
@cd /d %~dp0 && echo off && title %TITLE%

::=============================================================::
:: SECTION: Main Body                                          ::
::=============================================================::

call pyinstaller --out=__output__ --onefile --windowed gui.pyw
pause
exit /b 0
