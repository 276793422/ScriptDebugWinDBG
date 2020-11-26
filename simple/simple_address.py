# python3
# 作者        ：NemesisZoo
# 联系方式     ：276793422
# 创建日期     ：2020/11/8
# 文件名       ：simple_self
# 文件简介     ：
# 文件说明     ：

"""
外部脚本支持特殊函数，以便于快速处理内容
        def LoadFileToArray(path) -> array                                  加载文件，到一个字符串数组中
        def SaveStingArrayIntoFile(info, save_file, split="") -> file       保存字符串数组，到一个文件中
        def SaveStingIntoFile(info, save_file) -> file                      保存一个字符串到一个文件中
        def GetTempFilePath() -> file                                       获取一个临时文件的路径，可以保证这个文件是不存在的
        def GetTempDirPath() -> dir                                         获取临时目录路径

提供的全局变量
        LOCAL_FILE                  当前文件的完整路径
"""
import math
import multiprocessing
import os
import tempfile
import threading
from zoo_lib.Lib_head import *


# 获取上一阶段得到的返回内容

def GetLastAnswer(file, begin):
    lines = LoadFileToArray(file)
    return_lines = []
    bCopy = False
    for line in lines:
        if bCopy:
            return_lines.append(line)
        elif line.find(begin) != -1:
            bCopy = True

    return return_lines, lines


# 比较函数

def cmplist(x):
    num = x[20:28]
    nRet = 0  # 如果不是数字，返回0，排最后去
    if len(num) == 8:
        while num[0] == ' ':
            num = num[1:]
        if IsNumber(num):
            nRet = int(num, 16)  # 如果是数字，返回数字，
    return nRet


def GetAddressUsedInfo(memory_list, begin, output_file):
    strCommand = ""
    file_line = GetLastAnswer(memory_list, begin)[0]
    result_list = sorted(file_line, key=cmplist, reverse=True)
    for line in result_list:
        if len(line) < 90:
            continue
        if line[1] == ' ':  # 如果第八位是空格
            x = line
            if ' TEB ' in x:
                # TEB 内存
                pass
            if ' PEB ' in x:
                # PEB 内存
                pass
            if ' Image ' in x:
                # 文件镜像内存
                pass
            if ' Stack ' in x:
                # 栈内存
                pass
            if ' Other ' in x:
                # 其他内存
                pass
            if ' <unknown> ' in x:
                # 未知内存
                pass
            if ' Heap ' in x:
                # 堆内存
                addr = line[1:]
                while addr[0] == " ":
                    addr = addr[1:]
                i = addr.find(" ")
                if i == -1:
                    continue
                addr = addr[:i]
                if IsNumber(addr):
                    strCommand += "s -d 0 l?-1 " + addr + "\n"
                pass

    SaveStingIntoFile(strCommand, output_file)

    return output_file


def GetAddressHeapInfo(memory_list, begin, output_file):
    strCommand = ""
    file_line = GetLastAnswer(memory_list, begin)[0]
    for line in file_line:
        if len(line) > 11:
            if IsNumber(line[:8]) and line[8] == ' ' and line[9] == ' ':
                cmd = "!address " + line[:8]
                if cmd in strCommand:
                    pass
                else:
                    strCommand += cmd + "\n"
                pass

    SaveStingIntoFile(strCommand, output_file)

    return output_file


def GetAddressFinalCallStack(memory_list, begin, output_file):
    file_line = GetLastAnswer(memory_list, begin)[0]
    cmd_array = []
    for line in file_line:
        if ": !heap -x " in line:
            nIndex = line.find("!heap -x 0x")
            cmd = line[nIndex:]
            if cmd in cmd_array:
                pass
            else:
                cmd_array.append(cmd)

    SaveStingArrayIntoFile(cmd_array, output_file, "\n")

    return output_file


def ScriptDebugCommand(i, out_file, beginwith):
    if i == 0:
        ret_file = GetTempFilePath()
        return SaveStingIntoFile("!address", ret_file)

    if i == 1:
        ret_file = GetTempFilePath()
        return GetAddressUsedInfo(out_file, beginwith, ret_file)

    if i == 2:
        ret_file = GetTempFilePath()
        return GetAddressHeapInfo(out_file, beginwith, ret_file)

    if i == 3:
        ret_file = GetTempFilePath()
        return GetAddressFinalCallStack(out_file, beginwith, ret_file)

    if i == 4:
        return ""

    else:
        return ""
