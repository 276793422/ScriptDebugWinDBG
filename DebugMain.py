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
from shutil import copyfile


def RunDebugDump(opt, args):
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
    elif opt.Errline:
        # --errline -d D:\dump\3\MEMORY\MEMORY.DMP --outdir D:\dump\2.2
        # 参数1 ，dmp 文件，必须是32位的
        # 参数2 ，结果输出路径
        if IsStringValid(opt.Dump):
            if IsStringValid(opt.OutDir) or opt.DefaultShow:
                out_file = GetErrorLine(opt.Dump, opt.OutDir, opt.Answer)
        if out_file is None:
            print("需要参数 -d , --outdir")
    else:
        print("关键参数啥都没有，去看帮助吧")

    if IsStringValid(out_file):
        RemoveFileLogInfo(out_file)

    # 如果要求默认展示
    if opt.DefaultShow and IsStringValid(out_file):
        RunProcess("notepad.exe", out_file)

    # 如果不要求默认展示，就需要保存
    elif not opt.DefaultShow and IsStringValid(out_file):
        if IsStringValid(opt.Dump):
            dump_name = os.path.basename(opt.Dump)
            dump_name = os.path.dirname(out_file) + "\\" + dump_name + ".dmp.out.txt"
            copyfile(out_file, dump_name)
            os.remove(out_file)
            out_file = dump_name

    return out_file


# 执行调试功能，这里主要分两部分，一部分是单一的dump 调试，一部分是多个dump 调试

def RunDebug():
    opt, args = GetArgsInfo()
    dumpArray = []

    if not IsStringValid(opt.Dump):
        print("Dump 文件路径异常，无法继续，提前退出，检查 -d 参数")
        return

    print("DumpFile : [" + opt.Dump + "]")

    # 单个dump
    if opt.MulDump is None or opt.MulDump == False:
        # 直接把自己压进去就完事了
        dumpArray.append(opt.Dump)

    # 多个dump
    else:
        # 已经进来了，就不需要它了
        opt.MulDump = None
        if not IsStringValid(opt.Dump):
            print("多个dump分析，但是dump文件列表不明")
        else:
            szDump = opt.Dump
            if os.path.isdir(szDump):
                # 目录，枚举目录中的所有dmp文件到列表
                dumpArray = LoadAllFileInDir(szDump, ".dmp")
            else:
                # 文件，加载文件，然后调试每个文件
                dumpArray = LoadFileToArray(szDump)

    if len(dumpArray) > 0:
        i = 1
        for line in dumpArray:
            opt.Dump = line
            out = str(i) + "/" + str(len(dumpArray))
            out = out + " " * (20 - len(out)) + ": " + line + "  --┐"
            print(out)
            ret = RunDebugDump(opt, args)
            print(" " * (len(out) - 1) + "└-->  " + ret)
            i += 1


# 主函数

if __name__ == "__main__":
    # 初始化调试器必须的环境变量
    if not InitDebugLibrary():
        print("配置出错，环境变量不足")
    else:
        RunDebug()
