# python3
# 作者        ：NemesisZoo
# 联系方式     ：276793422
# 创建日期     ：2020/9/22
# 文件名       ：BaseLibrary.py
# 文件简介     ：
# 文件说明     ：

"""

"""

import os
import tempfile

# 符号文件路径，可以自动设置
import configparser
import win32event
import win32process

symbol_path = ''

# dump 文件路径，外面可以传入
dump_path = ''

# 调试器路径
debug_path = ''


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


# 创建进程并且等待返回

def RunProcessWaitReturn(exe, cmd):
    if exe == "" and cmd != "":
        handle = win32process.CreateProcess(None, cmd, None, None, 0,
                                            win32process.CREATE_NO_WINDOW, None, None,
                                            win32process.STARTUPINFO())
        win32event.WaitForSingleObject(handle[0], -1)
    elif exe != "" and cmd != "":
        handle = win32process.CreateProcess(None, exe + " " + cmd, None, None, 0,
                                            win32process.CREATE_NO_WINDOW, None, None,
                                            win32process.STARTUPINFO())
        win32event.WaitForSingleObject(handle[0], -1)
    elif exe != "" and cmd == "":
        handle = win32process.CreateProcess(exe, '', None, None, 0,
                                            win32process.CREATE_NO_WINDOW, None, None,
                                            win32process.STARTUPINFO())
        win32event.WaitForSingleObject(handle[0], -1)
    else:
        print("CreateProcess Error")
    pass


# 设置dump 文件路径，这个必须优先调用

def SetDumpPath(path):
    global dump_path
    if path != "":
        dump_path = path


# 设置dump 文件路径，这个必须优先调用

def SetSymbolPath(path):
    global symbol_path
    if path is not None and path != "":
        symbol_path = path


# 设置调试器文件路径，这个必须优先调用

def SetSymbolPath(path):
    global debug_path
    if path is not None and path != "":
        debug_path = path


# 取一个临时文件的路径，保证文件不存在，返回临时文件路径

def GetTempFilePath():
    script_file, script_path = tempfile.mkstemp()
    os.close(script_file)
    os.unlink(script_path)
    return script_path
    pass


# 保存内容到一个临时文件，返回临时文件路径

def SaveStringToTempFile(msg):
    script_path = GetTempFilePath()
    script_path += ".txt"
    with open(script_path, "w") as f:
        f.write(msg)
        f.close()
    return script_path
    pass


# 创建一个脚本执行的命令行，通过它可以让windbg 执行脚本，返回这个命令行

def MakeScriptCommand(script_path):
    global symbol_path
    global dump_path
    if dump_path == "":
        return ""
    return '-y "' + symbol_path + '" -z "' + dump_path + '" -cf "' + script_path + '"'
    pass


# 创建一个路径，这个路径是windbg 的调试器，执行脚本的程序路径，返回这个路径

def MakeDebugToolPath():
    global debug_path
    return '"' + debug_path + '/cdb.exe' + '"'
    pass


# 判断当前字符是否是一个16进制数字

def IsANumber(x):
    if x == '0' or x == '1' or x == '2' or x == '3' or x == '4' or x == '5' or x == '6' or x == '7' or x == '8' or x == '9' or x == 'a' or x == 'b' or x == 'c' or x == 'd' or x == 'e' or x == 'f' or x == 'A' or x == 'B' or x == 'C' or x == 'D' or x == 'E' or x == 'F':
        return True
        pass
    return False


# 判断当前字符串是否是一个十六进制数字

def IsNumber(x):
    for t in x:
        if not IsANumber(t):
            return False
    return True


# 执行一个脚本文件

def RunFileWithDebuger(file):
    script_path = file
    debug_tool = MakeDebugToolPath()
    debug_cmd = MakeScriptCommand(script_path)
    try:
        RunProcessWaitReturn(debug_tool, debug_cmd)
        pass
    except Exception as e:
        print(e)
    os.unlink(script_path)
    pass


# 执行一段脚本

def RunScriptWithDebuger(script):
    RunFileWithDebuger(SaveStringToTempFile(script))


# 执行一条命令

def RunCommandWithDebuger(cmd, out_path):
    script_text = '''
.logopen ''' + out_path + '''
''' + cmd + '''
.logclose
q
'''
    RunScriptWithDebuger(script_text)
    pass


# 执行多条命令

def RunLotCommandWithDebuger(cmds, out_path):
    cmd = ""
    for line in cmds:
        if cmd == "":
            pass
        else:
            if cmd[len(cmd) - 1] != "\n":
                cmd += "\n"
        cmd += line

    RunCommandWithDebuger(cmd, out_path)
    pass


# 执行一个命令文件

def RunCommandFileWithDebuger(infile, outfile):
    cmds = LoadFileToArray(infile)
    RunLotCommandWithDebuger(cmds, outfile)


# 数据写入文件

def SaveStingIntoFile(info, save_file):
    with open(save_file, "w") as f:
        f.write(info)
        f.close()


# 数据写入文件

def SaveStingArrayIntoFile(info, save_file, split=""):
    with open(save_file, "w") as f:
        for line in info:
            f.write(line + split)
        f.close()


# 加载一个文件到数组

def LoadFileToArray(path):
    file_line = []
    file = open(path)
    for line in file.readlines():
        line = line.strip('\n')
        file_line.append(line)
    file.close()
    return file_line
