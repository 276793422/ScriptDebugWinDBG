# python3
# 作者        ：NemesisZoo
# 联系方式     ：276793422
# 创建日期     ：2020/9/25
# 文件名       ：AnalyzeDebug.p
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


def AnalyzeDebug(dump, dir=None):
    # 第一步，取内存所有信息
    if dir is None:
        dir = GetTempDirPath()

    print("step 1")
    file1 = GetFilePathInDir(dir, 1, True)
    GetAnalyze(dump, file1)

    return file1
    pass
