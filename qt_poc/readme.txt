Note that building packages between conda and pip can be painful, pyside6 not on conda but pyside2 is. 
Also, matplotlib installs a version of qt as well

If you install via pip then you get broken dependencies somehow
Maybe install simultaneously in pip or conda? Or use pyside2 exclusively?
ie. conda install -c conda-forge pyside2

At the moment given our dependencies, just use pyside2

Pyqt has more docs, but pyside is strictly speaking the official one now, also lgpl licensing as opposed to whatever pyqt has/had

See the following for working with UI files
https://doc.qt.io/qtforpython/tutorials/basictutorial/uifiles.html
Use pyside2-uic.bat to compile the .ui file to the python classes but... lol it has issues with spaces in names
Try using pyside6-uic? and changing to 2?
eg. pyside6-uic mainwindow.ui > ui_mainwindow.py
Try "pyside6-uic file.ui | out-file foo.txt -encoding utf8" instead to not have to deal with utf-8/utf-16 

2021-09-22

Okay, got basics down, sort of

Need to remember how signals, slots work again in pyside but still

2021-09-24

Okay, adjusting the pyside4-uic.bat script, has issues with spaces in names
%~dp0 gives drive and path of batch file
According to this https://github.com/winpython/winpython/issues/299 we'll need some quotes for spaces

Contents of the batch file: python %~dp0pyside2-uic %*
Runs a python file at USER\anaconda3\envs\test\Library\bin\pyside2-uic

That python script doesn't work on python 3.9, due to some methods being deprecated 
https://github.com/g-provost/lightgallery-markdown/issues/6

TODO: Work out how to set this out in a more user angostic way
python  "C:\Users\Scott Williams\anaconda3\envs\qt_poc_test\Library\bin\pyside2-uic" .\test.ui --output ui_test.py
python "C:\Users\Scott Williams\anaconda3\envs\qt_poc_test\Library\bin\pyside2-uic" .\main_window.ui -o ui_main_window.py

To setup:
Create new conda environment with the listed stuff
That may or may not bring in QT desigenr

NOTE: Order of import does matter, because you can end up in a situation where QT4 is set when it should be QT5 and nothing quite works.

2021-10-10

Got the POC basically up to the TK example level, sans some of the rolling mean plots

Due to how conda/pip interact, setting up your own environment can be an issue, but Scott should be able to sort out (either install matplotlib and pyside completely from conda or pip, issues when mixing on Windows)

2021-10-18
Pyuic/pyqt5 also have issues with spaces in user profile
In powershell, to find location: (Get-Command pyuic5.bat).Source
Should return $env:USERPROFILE\anaconda3\Library\bin\pyuic5.bat

Open up that batch file, see that it calls @USER/anaconda3\python.exe -m PyQt5.uic.pyuic %1 %2 %3 %4 %5 %6 %7 %8 %9 (with USER subbed in for user profile path)

Do a similar python -m PyQt5.uic.pyuic .\main_window.ui -o temp.py to get similar result to prev

2021-12-03

Rebuild UI with ./build_ui.ps1