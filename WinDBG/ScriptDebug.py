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

import codecs
from six import exec_


class CodeLoader:
    def __init__(self, strategyfile):
        self._strategyfile = strategyfile

    def compile_strategy(self, source_code, strategyfile, scope):
        code = compile(source_code, strategyfile, 'exec')
        exec_(code, scope)
        return scope

    #
    def load(self, scope):
        with codecs.open(self._strategyfile, encoding="utf-8") as f:
            source_code = f.read()

            source_code += "\n"
            source_code += "LOCAL_FILE = '" + self._strategyfile + "'"
        return self.compile_strategy(source_code, self._strategyfile, scope)


def run_file(strategy_file_path):
    loader = CodeLoader(strategy_file_path)
    scope = {}
    scope = loader.load(scope)
    f = scope.get('ScriptDebugCommand', None)
    return f


"""
def _ScriptDebugCommand(out_file, i):
    if i == 0:
        return "E:\\temp\\1.txt"
    if i == 1:
        return "E:\\temp\\2.txt"
    if i == 2:
        return "E:\\temp\\3.txt"
    else:
        print("default _ScriptDebugCommand")
        return ""
"""


def ScriptDebugInfo(dump, script, dir=None):
    # 如果脚本不存在，就滚蛋了
    if os.path.exists(script) is False:
        print("脚本文件不存在，需要传入有效文件")
        return None

    # 第一步，取内存所有信息
    if dir is None:
        dir = GetTempDirPath()

    out_file = GetFilePathInDir(dir, 1, True)

    # 第一步工作在这里，后续所有工作都再回调函数里面处理

    ScriptMain = run_file(script)
    if ScriptMain is None:
        print("脚本文件内容不正确，需要传入有效文件")
        print("脚本文件内部必须存在一个函数叫做：ScriptDebugCommand")
        print("函数原型：def ScriptDebugCommand(out_file, i) -> string")

    RunCommandFileWithDebugerEvent(dump, out_file, ScriptMain)

    return out_file
    pass
