# python3
# 作者        ：NemesisZoo
# 联系方式     ：276793422
# 创建日期     ：2020/11/8
# 文件名       ：ScriptDebug
# 文件简介     ：
# 文件说明     ：

"""

"""

import os

from Lib.Lib_head import *
from WinDBG.Windbg_head import *


def ScriptDebugInfo(dump, script, dir=None):
    # 如果脚本不存在，就滚蛋了
    if os.path.exists(script) is False:
        print("脚本文件不存在，需要传入有效文件")
        return None

    # 第一步，取内存所有信息
    if dir is None:
        dir = GetTempDirPath()

    # 第一步工作在这里，后续所有工作都再回调函数里面处理

    ScriptMain = RunScriptFile(script)
    if ScriptMain is None:
        print("脚本文件内容不正确，需要传入有效文件")
        print("脚本文件内部必须存在一个函数叫做：ScriptDebugCommand")
        print("函数原型：def ScriptDebugCommand(i, out_file, beginwith) -> string")
        return None

    out_file = GetFilePathInDir(dir, 1, True)

    RunCommandFileWithDebugerEvent(dump, out_file, ScriptMain)

    return out_file
    pass
