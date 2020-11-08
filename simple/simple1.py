# python3
# 作者        ：NemesisZoo
# 联系方式     ：276793422
# 创建日期     ：2020/11/8
# 文件名       ：simple1.py
# 文件简介     ：
# 文件说明     ：

"""
当前文件为脚本指令执行的测试文件
"""

import os


def ScriptDebugCommand(i, out_file, beginwith):
    global LOCAL_FILE
    dir = os.path.dirname(os.path.abspath(LOCAL_FILE)) + "\\simple1"
    if i == 0:
        return dir + "\\1.txt"
    if i == 1:
        return dir + "\\2.txt"
    if i == 2:
        return dir + "\\3.txt"
    else:
        return ""
