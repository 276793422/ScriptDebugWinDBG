# python3
# 作者        ：NemesisZoo
# 联系方式     ：276793422
# 创建日期     ：2020/9/25
# 文件名       ：UmdhMemory
# 文件简介     ：
# 文件说明     ：

"""

"""
import os

from Lib.Lib_head import *
from WinDBG.Windbg_head import *


def MemoryModify(file, line):
    strReturn = line
    count = 0
    for line in file:
        if len(line) == 1:
            count += 1
        if count == 2:
            break
        strReturn += line

    return strReturn
    pass


def DecodeUmdhInfo(file, file_out):
    strArray = []
    file = open(file)
    for line in file:
        # 去掉注释
        if line.startswith('//'):
            continue
        # 内存增加
        if line[0] == '+':
            strArray.append(MemoryModify(file, line))

        # 内存减少
        if line[0] == '-':
            strArray.append(MemoryModify(file, line))

    file.close()

    SaveStingArrayIntoFile(strArray, file_out, "[suanguade]")

    return strArray
    pass


def GetAllMemoryIncre(strArray):
    memory = 0
    nAlloc = 0
    nFree = 0
    for line in strArray:
        lines = line.split('\n')
        for linet in lines:
            if len(linet) <= 1:
                continue
            strLine = linet[:10]
            if strLine[0] == '+' and linet.find("allocs	") != -1:
                n = int(strLine[1:].strip(), 16)
                memory += n
                nAlloc += n
            if strLine[0] == '-' and linet.find("allocs	") != -1:
                n = int(strLine[1:].strip(), 16)
                memory -= n
                nFree += n

    print("nAlloc = [" + str(nAlloc) + "]")
    print("nFree = [" + str(nFree) + "]")
    return memory
    pass


def UmdhMemoryInfo(file, dir):
    output_dir = dir
    strArray = []

    print("step 1")
    file1 = output_dir + '/output.1.txt'
    if os.path.exists(file1):
        os.unlink(file1)
    strArray = DecodeUmdhInfo(file, file1)

    incre = GetAllMemoryIncre(strArray)
    print("Memory Incre :", incre / 1024 / 1024, "M")

    pass
