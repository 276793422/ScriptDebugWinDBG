# python3
# 作者        ：NemesisZoo
# 联系方式     ：276793422
# 创建日期     ：2020/9/30
# 文件名       ：FileHelper.py
# 文件简介     ：
# 文件说明     ：

"""

"""

from .Lib_head import *


# 保存内容到一个临时文件，返回临时文件路径

def SaveStringToTempFile(msg):
    script_path = GetTempFilePath()
    script_path += ".txt"
    with open(script_path, "w") as f:
        f.write(msg)
        f.close()
    return script_path
    pass


# 数据写入文件

def SaveStingIntoFile(info, save_file):
    with open(save_file, "w") as f:
        f.write(info)
        f.close()
    return save_file


# 数据写入文件

def SaveStingArrayIntoFile(info, save_file, split=""):
    with open(save_file, "w") as f:
        for line in info:
            f.write(line + split)
    return save_file


# 加载一个文件到数组

def LoadFileToArray(path):
    file_line = []
    file = open(path)
    for line in file.readlines():
        line = line.strip('\n')
        file_line.append(line)
    file.close()
    return file_line


# 加载目录里的所有文件
# 参数1：目录
# 参数2：扩展名

def LoadAllFileInDir(file_dir, ext=None):
    list = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if ext is not None and os.path.splitext(file)[1] == ext:
                list.append(os.path.join(root, file))
    return list
