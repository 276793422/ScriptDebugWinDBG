# python3
# 作者        ：NemesisZoo
# 联系方式     ：276793422
# 创建日期     ：2020/11/9
# 文件名       ：ScriptHelper
# 文件简介     ：
# 文件说明     ：

"""
    脚本支持模块
"""
import codecs
from six import exec_


def RunScriptWithFile(source_code, script_file, scope):
    code = compile(source_code, script_file, 'exec')
    exec_(code, scope)
    return scope


def LoadRunScriptFile(script_file, scope):
    with codecs.open(script_file, encoding="utf-8") as f:
        source_code = f.read()

        # 这里补一个文件名
        source_code += "\n"
        source_code += "LOCAL_FILE = '" + script_file + "'"
    return RunScriptWithFile(source_code, script_file, scope)


def RunScriptFile(strategy_file_path):
    scope = {}
    scope = LoadRunScriptFile(strategy_file_path, scope)
    f = scope.get('ScriptDebugCommand', None)
    return f


