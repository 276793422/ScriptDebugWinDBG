# python3
# 作者        ：NemesisZoo
# 联系方式     ：276793422
# 创建日期     ：2020/11/8
# 文件名       ：simple1.py
# 文件简介     ：
# 文件说明     ：

"""
当前文件为脚本指令执行的测试文件

外部脚本支持特殊函数，以便于快速处理内容
        def LoadFileToArray(path) -> array                                  加载文件，到一个字符串数组中
        def SaveStingArrayIntoFile(info, save_file, split="") -> file       保存字符串数组，到一个文件中
        def SaveStingIntoFile(info, save_file) -> file                      保存一个字符串到一个文件中
        def GetTempFilePath() -> file                                       获取一个临时文件的路径，可以保证这个文件是不存在的
        def GetTempDirPath() -> dir                                         获取临时目录路径

提供的全局变量
        LOCAL_FILE                  当前文件的完整路径
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
