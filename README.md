# ToolWrapper

ToolWrapper is a container of testing tool for NVMTG team.


## Features

- Wrap the testing tool in the application
- Auto-build the whole package of tool
- Auto-update tool/firmware
- Show/activate different tool simultaneously

## Tech

ToolWrapper uses a number of open source projects to work properly:

- [PyQt5] - Qt is set of cross-platform C++ libraries that implement high-level APIs for accessing many aspects of modern desktop and mobile systems.
- [PyCharm] - The Python IDE for Professional Developers
- [PyUIC] - A dev tool to make the conversion of .ui PyQt5 Designer's files to .py files easier.
- [pyqt5-tools] - The PyQt5 wheels do not provide tools such as Qt Designer that were included in the old binary installers. This package aims to provide those in a separate package which is useful for developers while the official PyQt5 wheels stay focused on fulfilling the dependencies of PyQt5 applications.
- [PyInstaller] - PyInstaller freezes (packages) Python applications into stand-alone executables, under Windows, GNU/Linux, Mac OS X, FreeBSD, Solaris and AIX.
- [PsExec] - Utilities like Telnet and remote control programs like Symantec's PC Anywhere let you execute programs on remote systems, but they can be a pain to set up and require that you install client software on the remote systems that you wish to access. PsExec is a light-weight telnet-replacement that lets you execute processes on other systems, complete with full interactivity for console applications, without having to manually install client software. PsExec's most powerful uses include launching interactive command-prompts on remote systems and remote-enabling tools like IpConfig that otherwise do not have the ability to show information about remote systems.

## Installation

ToolWrapper requires [PsExec] v2.34+ to run.

Install the dependencies and devDependencies and start the tool.

First Step (Download required packages):

```sh
pip install -r requirements.txt
```

Second Step (Freeze (packages) Python applications into stand-alone executables, under Windows):

```sh
pyinstaller -F main.py --noconsole --uac-admin
Copy main.exe.manifest under build/main to the folder where main.py is.
pyinstaller -F --uac-admin -r main.exe.manifest,1 main.py -i NVMTG.ico --noconsole
```

Third Step (put required files in the same folder):

```sh
Copy .ico file and settings.ini to the dist folder.
```

Fourth Step (Build batch file with following command and named it ToolWrapper.bat):

```sh
IF NOT EXIST %USERPROFILE%\Desktop\EXP (md %USERPROFILE%\Desktop\EXP) 
set workpath=%USERPROFILE%\Desktop\ToolWrapper
%workpath%\PsExec.exe -d -i -h -w %workpath% %workpath%\ToolWrapper.exe
```

## Usage

ToolWrapper is currently working with following external tools.
Instructions on how to use them in your own PC are shown below.

#### First Step (Make sure every required files are installed as following structure)
Desktop
 ┣ ToolWrapper.bat
 ┣ ToolWrapper
 ┃ ┗ ToolWrapper.exe
  ┃ ┗ Settings.ini
   ┃ ┗ PsExec.exe
    ┃ ┗ Icon.png
    
#### Second Step (How to execute the tool.)
```sh
Run the ToolWrapper.bat as administrator.
If it is your first time to use the tool, then you will see a dialog window. Plese press accept and re-run the batch file as admin.
```

## Reference

**PsExec usage:**
- **https://www.hackercat.org/windows/psexec-local-privilege-escalation**

**PyInstaller usage:**
- **https://kknews.cc/zh-tw/code/xqp46ro.html**
- **https://blog.csdn.net/qq_26373925/article/details/105373124**
- **https://tw511.com/a/01/2507.html**

MIT

**Free Software, Hell Yeah!**

[//]: # 

   [PsExec]: <https://docs.microsoft.com/en-us/sysinternals/downloads/psexec>
   [PyInstaller]: <https://www.pyinstaller.org/>
   [pyqt5-tools]: <https://pypi.org/project/pyqt5-tools/>
   [PyUIC]: <https://pypi.org/project/pyuic5-tool/>
   [PyQt5]: <https://pypi.org/project/PyQt5/>
   [PyCharm]: <https://www.jetbrains.com/pycharm/>

