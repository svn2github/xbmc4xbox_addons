@ECHO OFF
CLS
COLOR 1B

:PluginType
SET PluginType=programs

:Begin
:: Set plugin name based on current directory
FOR /F "Delims=" %%D IN ('ECHO %CD%') DO SET PluginName=%%~nD

:: Set window title
TITLE %PluginName% Build Script!

:MakeBuildFolder
:: Create Build folder
ECHO ----------------------------------------------------------------------
ECHO.
ECHO Creating \BUILD\%PluginName%\ folder . . .
IF EXIST BUILD (
    RD BUILD /S /Q
)
MD BUILD
ECHO.

:MakeExcludeFile
:: Create exclude file
ECHO ----------------------------------------------------------------------
ECHO.
ECHO Creating exclude.txt file . . .
ECHO.
ECHO .svn>"BUILD\exclude.txt"
ECHO Thumbs.db>>"BUILD\exclude.txt"
ECHO Desktop.ini>>"BUILD\exclude.txt"
ECHO .pyo>>"BUILD\exclude.txt"
ECHO .pyc>>"BUILD\exclude.txt"
ECHO .bak>>"BUILD\exclude.txt"

:MakeReleaseBuild
:: Create release build
ECHO ----------------------------------------------------------------------
ECHO.
ECHO Copying required files to \Build\%PluginType%\%PluginName%\ folder . . .
XCOPY resources "BUILD\%PluginType%\%PluginName%\resources" /E /Q /I /Y /EXCLUDE:BUILD\exclude.txt
COPY default.py "BUILD\%PluginType%\%PluginName%\"
COPY default.tbn "BUILD\%PluginType%\%PluginName%\"
COPY changelog.txt "BUILD\%PluginType%\%PluginName%\"
ECHO.

:Cleanup
:: Delete exclude.txt file
ECHO ----------------------------------------------------------------------
ECHO.
ECHO Cleaning up . . .
DEL "BUILD\exclude.txt"
ECHO.
ECHO.

ECHO ----------------------------------------------------------------------
ECHO.
SET /P zipplugin=Do you want create a zip of the Plugin.? [Y/N]:
IF "%zipplugin:~0,1%"=="y" (
    GOTO ZIP_BUILD
) ELSE (
    GOTO Finish
)

:ZIP_BUILD
set ZIP="%ProgramFiles%\7-Zip\7z.exe"
set ZIP_ROOT=7z.exe
set ZIPOPS_EXE=a -tzip -mx=9 "%PluginName%.zip" "%PluginName%"
ECHO IF EXIST %ZIP% ( %ZIP% %ZIPOPS_EXE%>>"BUILD\%PluginType%\zip_build.bat"
ECHO   ) ELSE (>>"BUILD\%PluginType%\zip_build.bat"
ECHO   IF EXIST %ZIP_ROOT% ( %ZIP_ROOT% %ZIPOPS_EXE%>>"BUILD\%PluginType%\zip_build.bat"
ECHO     ) ELSE (>>"BUILD\%PluginType%\zip_build.bat"
ECHO     ECHO  not installed!  Skipping .zip compression...>>"BUILD\%PluginType%\zip_build.bat"
ECHO     )>>"BUILD\%PluginType%\zip_build.bat"
ECHO   )>>"BUILD\%PluginType%\zip_build.bat"
cd BUILD\%PluginType%\
ECHO Compressing "BUILD\%PluginType%\%PluginName%.zip"...
CALL zip_build.bat
::cd ..
::DEL "BUILD\zip_build.bat"
DEL zip_build.bat
GOTO Finish


:Finish
:: Notify user of completion
ECHO ======================================================================
ECHO.
ECHO Build Complete - Scroll up to check for errors.
ECHO.
ECHO Final build is located in the \BUILD\%PluginType%\ folder.
ECHO.
ECHO copy: \%PluginName%\ folder from the \BUILD\%PluginType%\ folder.
ECHO to: /XBMC/plugins/%PluginType%/ folder.
ECHO.
ECHO ======================================================================
ECHO.
PAUSE

:END
ECHO Scroll up to check for errors.
PAUSE
