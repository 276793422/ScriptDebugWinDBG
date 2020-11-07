# python3
# 作者        ：NemesisZoo
# 联系方式     ：276793422
# 创建日期     ：2020/9/22
# 文件名       ：BaseLibrary.py
# 文件简介     ：
# 文件说明     ：

"""

"""
from .BaseLibrary import *
from Lib.Lib_head import *

# 符号文件路径，可以自动设置
import configparser

import win32event
import win32process


# 加载脚本，并且让脚本合规
# infile ： 原始脚本文件
# py_wait_name ： python 等待的信号名字
# py_set_name ： python 设置的信号名字
# next_script_file ： 下一轮要执行的脚本文件名

def GetScriptFillToList(infile, py_wait_name, py_set_name, next_script_file):
    cmds = []
    # 加载全部命令
    cmds.extend(LoadFileToArray(infile))
    # 设置一阶段信号，设置的信号是 python 等待的信号
    cmds.append("!zoo_set \"" + py_wait_name + "\"")
    # 等待一阶段信号，等待的信号是 python 设置的信号
    cmds.append("!zoo_wait \"" + py_set_name + "\"")
    # 加载下一步的操作脚本，执行的时候，脚本是空的，信号回复之后脚本就有内容了，
    cmds.append("$$>< " + next_script_file)

    return cmds


# 这里的功能是让WinDBG执行一个脚本之后，卡住，停一下，停下之后等待下一步的功能
# 通过回调函数来设置下一步操作
# dump ： 要调试的dump 文件
# infile ： 第一阶段的脚本命令，所在文件
# outfile ： 输出结果文件

def RunCommandFileWithDebugerEvent(dump, infile, outfile, function, wait=False):

    next_script_file = GetFilePathInDir(GetTempDirPath(), 0, True)
    out_file = GetFilePathInDir(GetTempDirPath(), 0, True)
    wait_name_src = "Global\\\\ZooTestWait"
    py_wait_name = wait_name_src
    set_name_src = "Global\\\\ZooTestSet"
    py_set_name = set_name_src
    cmds = []

    rootPath = os.path.abspath(os.path.dirname(__file__) + "\\..\\..\\Bin\\zoo_event.dll")

    # 加载信号模块
    cmds.append(".load " + rootPath)
    # 加载脚本指令
    cmds.extend(GetScriptFillToList(infile, py_wait_name, py_set_name, next_script_file))
    # 执行脚本，以后全部执行都是在这里做的
    RunLotCommandWithDebuger(dump, cmds, out_file, wait)

    # 循环无限次，理论上无限
    for i in range(0, 0xFFFFFFFF):
        # 脚本等待调试器的信号
        CreateNameEventWait(py_wait_name.replace("\\\\", "\\"))
        # 参数1 ，之前输出的所有结果
        # 返回值，下一阶段执行的脚本路径,如果下一阶段没有任务了，那么会返回None 或者 空字符串
        next_file = function(out_file)

        if next_file is None or next_file == "":
            SaveStingIntoFile("", next_script_file)
            pass
        else:
            # 下一次需要用到的文件
            temp_next_file = GetFilePathInDir(GetTempDirPath(), 0, True)

            # next_script_file 下一轮要执行的脚本
            lines = GetScriptFillToList(next_file, wait_name_src + str(i), set_name_src + str(i), temp_next_file)

            # 把脚本放到上一轮循环中，要求放到的位置
            SaveStingArrayIntoFile(lines, next_script_file, "\n")

            # 把下一次需要用到的文件路径保存起来，下次循环需要用
            next_script_file = temp_next_file

        # 脚本告诉调试器，该干活了
        OpenNameEventSet(py_set_name.replace("\\\\", "\\"))

        # 如果返回下一轮的脚本是空的，那么认为调试结束了，退出了
        if next_file is None or next_file == "":
            break

        # 调整下一轮的信号
        py_wait_name = wait_name_src + str(i)
        py_set_name = set_name_src + str(i)

    # 退出之后，需要处理完整的输出内容，放到 outfile 里面
    lines = LoadFileToArray(out_file)
    SaveStingArrayIntoFile(lines, outfile, "\r")

    # 处理，删掉不需要的代码
    return RemoveFileLogInfo(outfile)


