:: Runs all tests.
:: **Dependencies**:
:: Python 2.6+ on PATH.

::=============================================================::
:: COPYRIGHT 2013, REVISED 2013, Jeff Rimko.                   ::
::=============================================================::

:: Set up environment.
@setlocal EnableDelayedExpansion
@set TITLE=%~n0 "%~dp0"
@cd /d %~dp0 && echo off && title %TITLE%

::-------------------------------------------------------------::
:: SECTION: Main Body                                          ::
::-------------------------------------------------------------::

:: Run each found test.
for /R . %%X in (*_test_*.py) do (
    echo Running %%~nX...
    start /wait cmd /c call python %%X
    if 0 neq !ERRORLEVEL! (
        echo     FAILED^^!
        pause
        exit /b 1
    ) else (
        echo     DONE.
    )
)

title [DONE] %TITLE%
echo --------
echo All tests passed successfully^^!
pause
exit /b 0
