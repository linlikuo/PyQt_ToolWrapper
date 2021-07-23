import sys, os, traceback, types
import win32api, win32con, win32event, win32process
from win32com.shell.shell import ShellExecuteEx
from win32com.shell import shellcon
from PyQt5 import QtCore

def isUserAdmin():
    if os.name == 'nt':
        import ctypes
        # WARNING: requires Windows XP SP2 or higher!
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            traceback.print_exc()
            print('Admin check failed, assuming not an admin.')
            return False
    elif os.name == 'posix':
        # Check for root on posix
        return os.getuid() == 0
    else:
        raise (RuntimeError, 'Unsupported operating system for this module: %s' % (os.name,))

def runAsAdmin(cmdLine=None, wait=True):
    if os.name != 'nt':
        raise (RuntimeError, 'This function is only implemented on Windows.')

    python_exe = sys.executable

    if cmdLine is None:
        cmdLine = [python_exe] + sys.argv
    elif not isinstance(cmdLine, (tuple, list)):
        raise ValueError('cmdLine is not a sequence.')
    cmd = '"{}"'.format(cmdLine[0])
    params = ' '.join(['"%s"' % (x,) for x in cmdLine[1:]])
    cmdDir = ''
    showCmd = win32con.SW_SHOWNORMAL
    lpVerb = 'runas'

    procInfo = ShellExecuteEx(nShow=showCmd,
                              fMask=shellcon.SEE_MASK_NOCLOSEPROCESS,
                              lpVerb=lpVerb,
                              lpFile=cmd,
                              lpParameters=params)

    if wait:
        procHandle = procInfo['hProcess']
        obj = win32event.WaitForSingleObject(procHandle, win32event.INFINITE)
        rc = win32process.GetExitCodeProcess(procHandle)
    else:
        rc = None

    return rc

def runTool(folderpath, new_toolname=''):
    prev_wd = os.getcwd()
    os.chdir(folderpath)

    exe_file = ''
    for file in os.listdir(folderpath):
        if file.endswith('.exe'):
            exe_file = os.path.join(folderpath, file)
            break
    if exe_file:
        #runAsAdmin([exe_file, new_toolname], False)
        #win32api.ShellExecute(0, 'runas', exe_file, new_toolname, '', 1)
        win32api.ShellExecute(0, 'runas', os.path.join(os.environ['HOMEPATH'], 'Desktop', 'ToolWrapper', 'PsExec.exe'), r'-d -i -h -w {work_dir} {exe} {name}'.format(work_dir=folderpath, exe=exe_file, name=new_toolname), '', 1)
        win32api.ShellExecute(0, 'open', folderpath, '', '', 1)
    os.chdir(prev_wd)
    return exe_file
