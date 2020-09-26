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
    if opt.Symbol != "":
        SetSymbolPath(opt.Symbol)

    # 如果调试器路径存在，就设置
    if opt.Path != "":
        SetSymbolPath(opt.Path)

    # 上面的是可选参数，后面的就都是必须的参数了

    if opt.Cmd:
        # -d --infile --outfile
        if opt.Dump != "" and opt.InFile != "" and opt.OutFile != "":
            SetDumpPath(opt.Dump)
            CommandControl(opt.Dump, opt.InFile, opt.OutFile)
        else:
            print("需要参数 -d , --infile , --outfile")
    elif opt.Heap:
        # -d --outdir
        if opt.Dump != "" and opt.OutDir != "":
            SetDumpPath(opt.Dump)
            HeapMemoryInfo(opt.OutDir)
        else:
            print("需要参数 -d , --outdir")
    elif opt.Address:
        # -d --outdir
        if opt.Dump != "" and opt.OutDir != "":
            SetDumpPath(opt.Dump)
            AddressMemoryInfo(opt.OutDir)
        else:
            print("需要参数 -d , --outdir")
    elif opt.Umdh:
        # 参数1 ，umdh 结果文件
        # 参数2 ，结果输出路径
        if opt.InFile != "" and opt.OutDir != "":
            UmdhMemoryInfo(opt.InFile, opt.OutDir)
        else:
            print("需要参数 --infile , --outdir")
    elif opt.Callstack:
        # --callstack -d D:\dump\3\MEMORY\MEMORY.DMP --outdir D:\dump\2.2
        # 参数1 ，dmp 文件，必须是32位的
        # 参数2 ，结果输出路径
        if opt.Dump != "" and opt.OutDir != "":
            SetDumpPath(opt.Dump)
            CallStack(opt.OutDir)
        else:
            print("需要参数 -d , --outdir")
    elif opt.Analyze:
        # 参数1 ，dmp 文件，必须是32位的
        # 参数2 ，结果输出路径
        if opt.Dump != "" and opt.OutDir != "":
            SetDumpPath(opt.Dump)
            AnalyzeDebug(opt.OutDir)
        else:
            print("需要参数 -d , --outdir")
    else:
        print("关键参数啥都没有，去看帮助吧")

    pass


if __name__ == "__main__":
    # 初始化调试器必须的环境变量
    if not InitDebugLibrary():
        print("配置出错，环境变量不足")
    else:
        RunDebug()
