# python3
# 作者        ：NemesisZoo
# 联系方式     ：276793422
# 创建日期     ：2020/10/28
# 文件名       ：ErrorLineGet.py
# 文件简介     ：
# 文件说明     ：

"""

"""

from Lib.Lib_head import *
from WinDBG.Windbg_head import *


def GetAnalyze(dump, output_file):
    RunCommandWithDebuger(dump, "!analyze -v", output_file)
    pass


def GetErrorLineInfo(dump, input_file, output_file):
    file_line = LoadFileToArray(input_file)
    FAULTING_SOURCE_FILE = ""
    FAULTING_SOURCE_LINE_NUMBER = ""
    FAULTING_SOURCE_LINE = ""
    for line in file_line:
        if line.startswith("FAULTING_SOURCE_FILE:") and FAULTING_SOURCE_FILE == "":
            FAULTING_SOURCE_FILE = line[len("FAULTING_SOURCE_FILE:"):]
            # 这个判断写在里面，确实很难看，但是目的是为了少做几次判断，否则每一次迭代都要整体判断一次，太慢了
            if FAULTING_SOURCE_FILE != "" and FAULTING_SOURCE_LINE_NUMBER != "" and FAULTING_SOURCE_LINE != "":
                break
        elif line.startswith("FAULTING_SOURCE_LINE_NUMBER:") and FAULTING_SOURCE_LINE_NUMBER == "":
            FAULTING_SOURCE_LINE_NUMBER = line[len("FAULTING_SOURCE_LINE_NUMBER:"):]
            if FAULTING_SOURCE_FILE != "" and FAULTING_SOURCE_LINE_NUMBER != "" and FAULTING_SOURCE_LINE != "":
                break
        elif line.startswith("FAULTING_SOURCE_LINE:") and FAULTING_SOURCE_LINE == "":
            FAULTING_SOURCE_LINE = line[len("FAULTING_SOURCE_LINE:"):]
            if FAULTING_SOURCE_FILE != "" and FAULTING_SOURCE_LINE_NUMBER != "" and FAULTING_SOURCE_LINE != "":
                break
    outlines = ["FAULTING_SOURCE_FILE:" + (30 - len("FAULTING_SOURCE_FILE:")) * " " + FAULTING_SOURCE_FILE,
                "FAULTING_SOURCE_LINE_NUMBER:" + (
                            30 - len("FAULTING_SOURCE_LINE_NUMBER:")) * " " + FAULTING_SOURCE_LINE_NUMBER,
                "FAULTING_SOURCE_LINE:" + (30 - len("FAULTING_SOURCE_LINE:")) * " " + FAULTING_SOURCE_LINE]

    SaveStingArrayIntoFile(outlines, output_file, "\n")


def GetErrorLine(dump, dir=None, answer=False):
    # 第一步，取内存所有信息
    if dir is None:
        dir = GetTempDirPath()

    print("step 1")
    file1 = GetFilePathInDir(dir, 1, True)
    GetAnalyze(dump, file1)

    print("step 2")
    file2 = GetFilePathInDir(dir, 2, True)
    GetErrorLineInfo(dump, file1, file2)

    # 如果要求只看结果，那么就只看结果文件，不看过程
    if answer:
        os.remove(file1)

    return file2
    pass
