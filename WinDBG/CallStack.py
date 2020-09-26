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


def GetAnalyze(output_file):
    RunCommandWithDebuger("!analyze -v", output_file)
    pass


def GetCallStack(input_file, output_file):
    file_line = LoadFileToArray(input_file)
    for line in file_line:
        if line.startswith("STACK_COMMAND:"):
            RunCommandWithDebuger(line[len("STACK_COMMAND:"):], output_file)
            break
    pass


def CallStack(dir):
    # 第一步，取内存所有信息
    output_dir = dir

    print("step 1")
    file1 = output_dir + '/output.1.txt'
    if os.path.exists(file1):
        os.unlink(file1)
    GetAnalyze(file1)

    print("step 2")
    file2 = output_dir + '/output.2.txt'
    if os.path.exists(file2):
        os.unlink(file2)
    GetCallStack(file1, file2)

    file_line = LoadFileToArray(file2)
    for line in file_line:
        print(line)


    pass


