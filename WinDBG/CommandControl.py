# python3
# 作者        ：NemesisZoo
# 联系方式     ：276793422
# 创建日期     ：2020/9/26
# 文件名       ：CommandControl.py
# 文件简介     ：
# 文件说明     ：

"""

"""

from Lib.Lib_head import *
from WinDBG.Windbg_head import *


def CommandControl(dump, infile, outfile=None):
    if not IsStringValid(outfile):
        outfile = GetTempFilePath()
    RunCommandFileWithDebuger(dump, infile, outfile)

    return outfile


# 如果输出文件参数不存在，那么就内部创建一个

def CommandLineControl(dump, cmd, outfile=None):
    if not IsStringValid(outfile):
        outfile = GetTempFilePath()
    f = SaveStingIntoFile(cmd, GetTempFilePath())
    CommandControl(dump, f, outfile)
    return outfile
