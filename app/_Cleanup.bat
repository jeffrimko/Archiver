:: Removes all generated project files.
:: **Dependencies**: None

::=============================================================::
:: COPYRIGHT 2013, REVISED 2013, Jeff Rimko.                   ::
::=============================================================::

:: Set up environment.
@set TITLE=%~n0 "%~dp0"
@cd /d %~dp0 && echo off && title %TITLE%

::=============================================================::
:: SECTION: Main Body                                          ::
::=============================================================::

rd /S /Q __output__
rd /S /Q __pycache__
rd /S /Q dist
rd /S /Q build
del /S /Q *.log
del /S /Q *.pyc
