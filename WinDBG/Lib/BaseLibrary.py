# python3
# 作者        ：NemesisZoo
# 联系方式     ：276793422
# 创建日期     ：2020/9/22
# 文件名       ：BaseLibrary.py
# 文件简介     ：
# 文件说明     ：

"""

"""
from Lib.Lib_head import *

# 符号文件路径，可以自动设置
import configparser

import win32event
import win32process

# 符号路径
symbol_path = ''

# 调试器路径
debug_path = ''

# 调试器程序名字
debugger_name = 'cdb.exe'


# -z 指定dump
# -p 指定 PID
# 什么都不带，直接执行程序

# 初始化调试器相关功能

def InitDebugLibrary():
    global symbol_path
    global debug_path

    # 先找环境变量，环境变量是最低优先级

    # 这个是符号变量
    strEnv = os.environ.get('_NT_SYMBOL_PATH')
    if strEnv is not None and strEnv != "":
        symbol_path = strEnv

    # 这个是自定义的调试器路径
    strEnv = os.environ.get('_WINDBG_DIR')
    if strEnv is not None and strEnv != "":
        debug_path = strEnv

    # 找本地文件，本地文件优先级较高

    confile = os.getcwd() + "\\config.ini"
    if not os.path.isfile(confile):
        # 如果配置文件不存在，那么就创建一个，并且填入数据
        save_info = '''[Path]
symbol_path=
debug_path=
'''
        SaveStingIntoFile(save_info, confile)
        return False
    else:
        # 如果配置文件存在，那么就读配置文件
        # 读取.ini文件
        conf = configparser.ConfigParser()
        conf.read(confile)

        # get()函数读取section里的参数值
        # 如果正确读出数据并且数据正常那么就加载
        name = conf.get("Path", "symbol_path")
        if name is not None and name != "":
            symbol_path = name

        name = conf.get("Path", "debug_path")
        if name is not None and name != "":
            debug_path = name

    if symbol_path == "":
        return False

    if debug_path == "":
        return False

    return True


# 创建进程不等待

def RunProcess(exe, cmd):
    handle = None
    if exe == "" and cmd != "":
        handle = win32process.CreateProcess(None, cmd, None, None, 0,
                                            win32process.CREATE_NO_WINDOW, None, None,
                                            win32process.STARTUPINFO())
    elif exe != "" and cmd != "":
        handle = win32process.CreateProcess(None, exe + " " + cmd, None, None, 0,
                                            win32process.CREATE_NO_WINDOW, None, None,
                                            win32process.STARTUPINFO())
    elif exe != "" and cmd == "":
        handle = win32process.CreateProcess(exe, '', None, None, 0,
                                            win32process.CREATE_NO_WINDOW, None, None,
                                            win32process.STARTUPINFO())
    else:
        print("CreateProcess Error")

    return handle


# 创建进程并且等待返回

def RunProcessWaitReturn(exe, cmd, wait=True):
    handle = RunProcess(exe, cmd)
    if handle is not None and wait:
        win32event.WaitForSingleObject(handle[0], -1)


# 设置dump 文件路径，这个必须优先调用

def SetSymbolPath(path):
    global symbol_path
    if path is not None and path != "":
        symbol_path = path


# 设置调试器文件路径，这个必须优先调用

def SetDebugPath(path):
    global debug_path
    if path is not None and path != "":
        debug_path = path


# 创建一个脚本执行的命令行，通过它可以让windbg 执行脚本，返回这个命令行

def MakeScriptCommand(dump, script_path):
    global symbol_path
    strCommand = '-z "' + dump + '" -cf "' + script_path + '"'
    # 这里要支持，如果没有符号，那么就不拼符号参数
    if IsStringValid(symbol_path):
        return '-y "' + symbol_path + '" ' + strCommand
    else:
        return strCommand
    pass


# 创建一个路径，这个路径是windbg 的调试器，执行脚本的程序路径，返回这个路径

def MakeDebugToolPath():
    global debug_path
    global debugger_name
    return '"' + debug_path + '/' + debugger_name + '"'
    pass


# 执行一个脚本文件

def RunFileWithDebuger(dump, file, wait=True):
    script_path = file
    debug_tool = MakeDebugToolPath()
    debug_cmd = MakeScriptCommand(dump, script_path)
    try:
        RunProcessWaitReturn(debug_tool, debug_cmd, wait)
        pass
    except Exception as e:
        print(e)
    if wait:
        os.unlink(script_path)
    pass


# 执行一段脚本

def RunScriptWithDebuger(dump, script, wait=True):
    RunFileWithDebuger(dump, SaveStringToTempFile(script), wait)


# 执行一条命令

def RunCommandWithDebuger(dump, cmd, out_path, wait=True):
    script_text = '''
.logopen ''' + out_path + '''
''' + cmd + '''
.logclose
q
'''
    RunScriptWithDebuger(dump, script_text, wait)
    pass


# 执行多条命令

def RunLotCommandWithDebuger(dump, cmds, out_path, wait=True):
    cmd = ""
    for line in cmds:
        if cmd == "":
            pass
        else:
            if cmd[len(cmd) - 1] != "\n":
                cmd += "\n"
        cmd += line

    RunCommandWithDebuger(dump, cmd, out_path, wait)


# 执行一个命令文件

def RunCommandFileWithDebuger(dump, infile, outfile, wait=True):
    cmds = LoadFileToArray(infile)
    RunLotCommandWithDebuger(dump, cmds, outfile, wait)
    return outfile


# 去除文件中log 部分信息

def RemoveFileLogInfo(file):
    strFile = LoadFileToArray(file)
    os.remove(file)
    strArray = []
    start = 0
    end = len(strFile) + 1
    for line in strFile:
        start += 1
        # 第一行去掉
        if start == 1 and line.startswith("Opened log file "):
            continue
        # 加载wait 插件的模块去掉
        if start == 2 and line.find("kd> .load ") != -1 and line.endswith("zoo_event.dll"):
            continue

        # set 功能函数去掉
        if line.find("kd> !zoo_set") != -1:
            continue
        if line.startswith("Info:    Set Event Name = "):
            continue
        if line.startswith("Info:    Set Event "):
            continue
        # wait 功能函数去掉
        if line.find("kd> !zoo_wait") != -1:
            continue
        if line.startswith("Info:    Wait Event Name = "):
            continue
        if line.startswith("Info:    Wait Event "):
            continue
        # 加载脚本功能去掉
        if line.find("kd> $$>< ") != -1:
            continue

        # 倒数第三行
        if start == end - 2 and "> .logclose" in line:
            continue
        # 倒数第二行
        if start == end - 1 and line.startswith("Closing open log file "):
            continue
        # 倒数第一行
        if start == end and line == "":
            continue
        strArray.append(line + "\n")
    SaveStingArrayIntoFile(strArray, file)
    return file
