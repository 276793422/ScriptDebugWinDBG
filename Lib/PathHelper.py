# python3
# 作者        ：NemesisZoo
# 联系方式     ：276793422
# 创建日期     ：2020/9/30
# 文件名       ：PathHelper
# 文件简介     ：
# 文件说明     ：

"""

"""
import os
import tempfile
import uuid


# 取一个临时文件的路径，保证文件不存在，返回临时文件路径


def GetTempFilePath():
    script_file, script_path = tempfile.mkstemp()
    os.close(script_file)
    os.unlink(script_path)
    return script_path
    pass


# 获取临时文件目录

def GetTempDirPath():
    return os.getenv('TEMP')
    pass


# 从一个目录中，获取指定索引的一个文件名字，并且保证这个文件在文件名字获取的时候，是不存在，可用的

def GetFilePathInDir(dir, step, uuid = False):
    file = dir + '\\output.' + str(step) + '.txt'
    if uuid:
        file += '.' + uuid1() + '.txt'
    if os.path.exists(file):
        os.unlink(file)
    return file


# 创建一个 UUID

def uuid1():
    return str(uuid.uuid1()).replace("-","")
