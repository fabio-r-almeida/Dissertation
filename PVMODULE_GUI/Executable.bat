set /p COUNTER=<1_current_version.txt


set "search=%COUNTER%"
set /A COUNTER=COUNTER+1
set "replace=%COUNTER%"

for /f "tokens=1-4 delims=/ " %%i in ("%date%") do (
     set month=%%j
     set year=%%k
     )

set datestr=__version__ = '%year%.%month%.
set verstr=%year%.%month%.

@echo off

    set "textFile=VERSION.txt"

    for /f "delims=" %%i in ('type "%textFile%" ^& break ^> "%textFile%" ') do (
        set "line=%%i"
        setlocal enabledelayedexpansion
        >>"%textFile%" echo(%datestr%%replace%'!
        endlocal
    )
@echo off

    set "textFile=VERSION_ini.txt"

    for /f "delims=" %%i in ('type "%textFile%" ^& break ^> "%textFile%" ') do (
        set "line=%%i"
        setlocal enabledelayedexpansion
        >>"%textFile%" echo(%verstr%%replace%!
        endlocal
    )

<NUL set /p=%COUNTER%> 1_current_version.txt
copy VERSION.txt version.py
copy VERSION_ini.txt version.ini

rd /q /s "build" 2>nul
rd /q /s "dist" 2>nul

pyinstaller --noconsole --noconfirm --onedir --windowed --clean --add-data "C:/Users/Fabio/Desktop/Github/Dissertation/PVMODULE_GUI/config.ini;." --splash "C:/Users/Fabio/Desktop/Github/Dissertation/PVMODULE_GUI/images/bg_gradient.png" --add-data "C:/Users/Fabio/Desktop/Github/Dissertation/PVMODULE_GUI/PPFD_Plot.py;." --add-data "C:/Users/Fabio/Desktop/Github/Dissertation/PVMODULE_GUI/VERSION.txt;." --add-data "C:/Users/Fabio/Desktop/Github/Dissertation/PVMODULE_GUI/Plot.py;." --add-data "C:/Users/Fabio/Desktop/Github/Dissertation/PVMODULE_GUI/Map.py;." --add-data "C:/Users/Fabio/Desktop/Github/Dissertation/PVMODULE_GUI/Splash.py;." --add-data "C:/Users/Fabio/Desktop/Github/Dissertation/PVMODULE_GUI/Get_Data_Threads.py;." --add-data "C:/Users/Fabio/Desktop/Github/Dissertation/PVMODULE_GUI/images;images/" --add-data "C:/Users/Fabio/AppData/Local/Programs/Python/Python38/Lib/site-packages/customtkinter;customtkinter/" --icon "C:/Users/Fabio/Desktop/Github/Dissertation/PVMODULE_GUI/images/icon.ico" "C:/Users/Fabio/Desktop/Github/Dissertation/PVMODULE_GUI/PVModule.py" 

rd /q /s "build" 2>nul

iscc UninsIS.iss

git add -A
git commit -m "Automatic Push"
git pull origin main
git push -u origin main 