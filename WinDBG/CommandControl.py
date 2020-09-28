# python3
# 作者        ：NemesisZoo
# 联系方式     ：276793422
# 创建日期     ：2020/9/26
# 文件名       ：CommandControl.py
# 文件简介     ：
# 文件说明     ：

"""

"""

from WinDBG.Windbg_head import *


def CommandControl(dump, infile, outfile):
    RunCommandFileWithDebuger(dump, infile, outfile)

    return outfile
    pass
