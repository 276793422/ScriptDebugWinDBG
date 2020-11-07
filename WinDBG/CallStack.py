# python3
# 作者        ：NemesisZoo
# 联系方式     ：276793422
# 创建日期     ：2020/9/26
# 文件名       ：CallStack.py
# 文件简介     ：
# 文件说明     ：

"""

"""

import os

from Lib.Lib_head import *
from WinDBG.Windbg_head import *


def GetAnalyze(dump, output_file):
    RunCommandWithDebuger(dump, "!analyze -v", output_file)
    pass


def GetCallStack(dump, input_file, output_file):
    file_line = LoadFileToArray(input_file)
    for line in file_line:
        if line.startswith("STACK_COMMAND:"):
            RunCommandWithDebuger(dump, line[len("STACK_COMMAND:"):], output_file)
            break
    pass


def CallStack(dump, dir=None):
    # 第一步，取内存所有信息
    if dir is None:
        dir = GetTempDirPath()

    print("step 1")
    file1 = GetFilePathInDir(dir, 1, True)
    GetAnalyze(dump, file1)

    print("step 2")
    file2 = GetFilePathInDir(dir, 2, True)
    GetCallStack(dump, file1, file2)

    return file2
    pass


def GetAnalyzeS(dump, output_file):
    RunCommandWithDebuger(dump, "!analyze -v", output_file)
    pass
