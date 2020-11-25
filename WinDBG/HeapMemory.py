# python3
# 作者        ：NemesisZoo
# 联系方式     ：276793422
# 创建日期     ：2020/9/22
# 文件名       ：DebugMain.py
# 文件简介     ：
# 文件说明     ：

"""

"""
import os

from Lib.Lib_head import *
from WinDBG.Windbg_head import *


# 执行获取内存信息的命令，返回结果保存到文件中

def GetMemoryInfoInDump(dump, out_path):
    RunCommandWithDebuger(dump, "!heap -s", out_path)
    pass


# 从文件中取所有内存块的信息，然后再保存到文件中

def GetMemoryUsedInfo(dump, memory_list, output_file):
    strCommand = ""
    file = open(memory_list)
    for line in file:
        if line[8] == ' ':  # 如果第八位是空格
            strSub = line[:8]
            if IsNumber(strSub):  # 判断前八位是否都是数字，十六进制的
                strCommand += "!heap -stat -h " + strSub + "\n"

    file.close()

    # 这里最后多了个换行，要去掉，否则windbg要多执行一次命令
    RunCommandWithDebuger(dump, strCommand[:len(strCommand) - 1], output_file)
    pass


def GetSize(x):
    line = x
    n = line.find(" - ")
    line = line[n + 3:]
    n = line.find("  (")
    line = line[:n]
    return int(line, 16)


def cmplist(x):
    return GetSize(x)


# 根据所有内存块位置，获取完整的内存信息

def GetMemoryAllInfo(memory_file, save_file):
    file_line = []
    file = open(memory_file)
    for line in file:
        # 如果是四个空格开头，但是不是四个空格加size 开头
        if line.startswith("    ") and not line.startswith("    size") and line.find(" - ") != -1:
            file_line.append(line[4:])
    file.close()

    # 排序
    result_list = sorted(file_line, key=cmplist, reverse=True)

    size_all = 0
    # 将排序结果送入文件
    with open(save_file, "w") as f:
        for line in result_list:
            size = GetSize(line)
            size_all += size
            num = str(size / 1024)
            if len(num) > 20:
                num = num[:20]
            elif len(num) < 20:
                num = num + (20 - len(num)) * ' '
            f.write(num + " |" + line)

        f.write("All Size = [" + str(size_all) + "]:[" + str(size_all / 1024 / 1024) + "M]")
        f.close()


def GetCallStack(dump, memory_file, save_file):
    file_array = LoadFileToArray(memory_file)
    address_array = []
    for line in file_array:
        index = line.find("|")
        if index == -1:
            continue
        line = line[index + 1:]
        index = line.find(" ")
        if index == -1:
            continue
        line = line[:index]
        address_array.append(line)

    # address_array = list(set(address_array))
    for i in range(0, len(address_array)):
        address_array[i] = "!heap -flt s " + address_array[i]

    RunLotCommandWithDebuger(dump, address_array, save_file)


def GetAllCallStack(dump, memory_file, save_file):
    file_array = LoadFileToArray(memory_file)
    address_array = []
    for line in file_array:
        if not line.startswith("        "):
            continue
        line = line[8:]
        if not IsANumber(line[0]):
            continue
        line = line[27:]
        index = line.find(" ")
        if index == -1:
            continue
        line = line[:index]
        if not IsNumber(line):
            continue

        address_array.append(line)

    for i in range(0, len(address_array)):
        address_array[i] = "!heap -p -a " + address_array[i]

    RunLotCommandWithDebuger(dump, address_array, save_file)


# 参数1 ，dmp 文件，必须是32位的
# 参数2 ，结果输出路径
# 返回，最终输出结果的文件

def HeapMemoryInfo(dump, dir=None):
    # 第一步，取内存所有信息
    if dir is None:
        dir = GetTempDirPath()

    print("step 1")
    file1 = GetFilePathInDir(dir, 1, True)
    GetMemoryInfoInDump(dump, file1)

    # 第二步，根据内存信息，取所有内存块位置
    print("step 2")
    file2 = GetFilePathInDir(dir, 2, True)
    GetMemoryUsedInfo(dump, file1, file2)

    # 第三步，根据所有内存块位置，取所有内存信息
    print("step 3")
    file3 = GetFilePathInDir(dir, 3, True)
    GetMemoryAllInfo(file2, file3)

    # 第四步，!heap -flt s [16进制长度]
    # 查看所有对应长度的内存调用栈，如果没有调用栈，就是所有使用了这个长度内存的位置
    # 目前这一步没有加，因为太多了
    #   如果第四步没有调用栈，那么还要增加第五步
    # 第四步是非常耗时的，如果要执行，需要想清楚，否则的话，这里是会死人的
    print("step 4")
    file4 = GetFilePathInDir(dir, 4, True)
    GetCallStack(dump, file3, file4)

    # 第五步，!heap -p -a [UserSize]
    # 查看指定一个 UserSize 的调用栈，
    # 如果第四步看不到调用栈的话，这里大概率也看不到
    print("step 5")
    file5 = GetFilePathInDir(dir, 5, True)
    GetAllCallStack(dump, file4, file5)

    print("over")
    return file5
    pass
