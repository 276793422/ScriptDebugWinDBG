# python3
# 作者        ：NemesisZoo
# 联系方式     ：276793422
# 创建日期     ：2020/9/22
# 文件名       ：AddressMemory.py
# 文件简介     ：
# 文件说明     ：

"""

"""
import os

from Lib.Lib_head import *
from WinDBG.Windbg_head import *


# 执行获取内存信息的命令，返回结果保存到文件中

def GetAddressInfoInDump(out_path):
    RunCommandWithDebuger("!address", out_path)
    pass


# 比较函数

def cmplist(x):
    num = x[20:28]
    nRet = 0                # 如果不是数字，返回0，排最后去
    if len(num) == 8:
        while num[0] == ' ':
            num = num[1:]
        if IsNumber(num):
            nRet = int(num, 16)     # 如果是数字，返回数字，
    return nRet


# 从文件中取所有内存块的信息，然后再保存到文件中

def GetAddressUsedInfo(memory_list, output_file):
    strCommand = ""
    file_line = LoadFileToArray(memory_list)
    result_list = sorted(file_line, key=cmplist, reverse=True)
    for line in result_list:
        if len(line) < 90:
            continue
        if line[1] == ' ' and line[2] == ' ' and line[10] == ' ' and line[11] == ' ':  # 如果第八位是空格
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
                addr = line[3:9]
                if IsNumber(addr):
                    strCommand += "s -d 0 l?-1 " + addr + "\n"
                pass

    # 这里最后多了个换行，要去掉，否则windbg要多执行一次命令
    RunCommandWithDebuger(strCommand[:len(strCommand) - 1], output_file)
    pass


# 从文件中取所有内存块的信息，然后再保存到文件中

def GetAddressHeapInfo(memory_list, output_file):
    strCommand = ""
    file_line = LoadFileToArray(memory_list)
    for line in file_line:
        if len(line) > 11:
            if IsNumber(line[:8]) and line[8] == ' ' and line[9] == ' ':
                cmd = "!address " + line[:8]
                if cmd in strCommand:
                    pass
                else:
                    strCommand += cmd + "\n"
                pass

    RunCommandWithDebuger(strCommand[:len(strCommand) - 1], output_file)
    pass


# 最后取结果

def GetAddressFinalCallStack(memory_list, output_file):
    strCommand = ""
    file_line = LoadFileToArray(memory_list)
    for line in file_line:
        if ": !heap -x " in line:
            nIndex = line.find("!heap -x 0x")
            cmd = line[nIndex:]
            if cmd in strCommand:
                pass
            else:
                strCommand += cmd + "\n"
            pass
        pass

    RunCommandWithDebuger(strCommand[:len(strCommand) - 1], output_file)

    pass


def AddressMemoryInfo(dir):
    # 第一步，取内存所有信息
    output_dir = dir

    print("step 1")
    file1 = output_dir + '/output.1.txt'
    if os.path.exists(file1):
        os.unlink(file1)
    GetAddressInfoInDump(file1)

    # 第二步，根据内存信息，取所有内存块位置
    print("step 2")
    file2 = output_dir + '/output.2.txt'
    if os.path.exists(file2):
        os.unlink(file2)
    GetAddressUsedInfo(file1, file2)

    # 第三步，根据地址信息，取所有可用得 address 命令
    print("step 3")
    file3 = output_dir + '/output.3.txt'
    if os.path.exists(file3):
        os.unlink(file3)
    GetAddressHeapInfo(file2, file3)

    # 第四步，根据第三步得结果，取相关的内存信息，这里最好的情况下，是能得到所有调用栈的
    print("step 4")
    file4 = output_dir + '/output.4.txt'
    if os.path.exists(file4):
        os.unlink(file4)
    GetAddressFinalCallStack(file3, file4)


    pass
