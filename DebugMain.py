# python3
# 作者        ：NemesisZoo
# 联系方式     ：276793422
# 创建日期     ：2020/9/22
# 文件名       ：DebugMain.py
# 文件简介     ：
# 文件说明     ：

"""

"""
import sys

from Stdafx_head import *



def RunDebug():
    opt, args = GetArgsInfo()

    # 如果符号路径存在，就设置
    if opt.Symbol is not None and opt.Symbol != "":
        SetSymbolPath(opt.Symbol)

    # 如果调试器路径存在，就设置
    if opt.Path is not None and opt.Path != "":
        SetDebugPath(opt.Path)

    # 上面的是可选参数，后面的就都是必须的参数了

    out_file = None

    if opt.Cmd:
        if IsStringValid(opt.Dump) and IsStringValid(opt.CmdLine):
            if IsStringValid(opt.OutFile) or opt.DefaultShow:
                out_file = CommandLineControl(opt.Dump, opt.CmdLine, opt.OutFile)
        if out_file is None:
            print("需要参数 -d , -c , --outfile")
    elif opt.CmdFile:
        if IsStringValid(opt.Dump) and IsStringValid(opt.InFile):
            if IsStringValid(opt.OutFile) or opt.DefaultShow:
                out_file = CommandControl(opt.Dump, opt.InFile, opt.OutFile)
        if out_file is None:
            print("需要参数 -d , --infile , --outfile")
    elif opt.Heap:
        if IsStringValid(opt.Dump):
            if IsStringValid(opt.OutDir) or opt.DefaultShow:
                out_file = HeapMemoryInfo(opt.Dump, opt.OutDir)
        if out_file is None:
            print("需要参数 -d , --outdir")
    elif opt.Address:
        if IsStringValid(opt.Dump):
            if IsStringValid(opt.OutDir) or opt.DefaultShow:
                out_file = AddressMemoryInfo(opt.Dump, opt.OutDir)
        if out_file is None:
            print("需要参数 -d , --outdir")
    elif opt.Umdh:
        # 参数1 ，umdh 结果文件
        # 参数2 ，结果输出路径
        if IsStringValid(opt.InFile):
            if IsStringValid(opt.OutDir) or opt.DefaultShow:
                out_file = UmdhMemoryInfo(opt.InFile, opt.OutDir)
        if out_file is None:
            print("需要参数 --infile , --outdir")
    elif opt.Callstack:
        # --callstack -d D:\dump\3\MEMORY\MEMORY.DMP --outdir D:\dump\2.2
        # 参数1 ，dmp 文件，必须是32位的
        # 参数2 ，结果输出路径
        if IsStringValid(opt.Dump):
            if IsStringValid(opt.OutDir) or opt.DefaultShow:
                out_file = CallStack(opt.Dump, opt.OutDir)
        if out_file is None:
            print("需要参数 -d , --outdir")
    elif opt.Analyze:
        # 参数1 ，dmp 文件，必须是32位的
        # 参数2 ，结果输出路径
        if IsStringValid(opt.Dump):
            if IsStringValid(opt.OutDir) or opt.DefaultShow:
                out_file = AnalyzeDebug(opt.Dump, opt.OutDir)
        if out_file is None:
            print("需要参数 -d , --outdir")
    else:
        print("关键参数啥都没有，去看帮助吧")

    if opt.DefaultShow and IsStringValid(out_file):
        RunProcess("notepad.exe", out_file)

    pass


if __name__ == "__main__":
    # 初始化调试器必须的环境变量
    if not InitDebugLibrary():
        print("配置出错，环境变量不足")
    else:
        RunDebug()
