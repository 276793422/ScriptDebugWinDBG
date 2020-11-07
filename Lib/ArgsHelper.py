# python3
# 作者        ：NemesisZoo
# 联系方式     ：276793422
# 创建日期     ：2020/9/25
# 文件名       ：ArgsHelper.py
# 文件简介     ：
# 文件说明     ：

"""

"""
import optparse


def GetArgsInfo():
    parser = optparse.OptionParser()
    # 命令参数，全部互斥，决定执行哪些操作
    parser.add_option("--address", dest="Address", action="store_true", help="address命令内存分析")
    parser.add_option("--heap", dest="Heap", action="store_true", help="heap命令内存分析")
    parser.add_option("--umdh", dest="Umdh", action="store_true", help="Umdh工具返回信息处理")
    parser.add_option("--analyze", dest="Analyze", action="store_true", help="dump文件自动分析")
    parser.add_option("--callstack", dest="Callstack", action="store_true", help="dump文件自动分析")
    parser.add_option("--callstacks", dest="CallstackS", action="store_true", help="dump文件自动分析S")
    parser.add_option("--errline", dest="Errline", action="store_true", help="自动获取导致崩溃的文件以及行号，这个参数使用要注意，因为不是所有dump都能取到错误行号，很可能没有输出")
    parser.add_option("--cmdfile", dest="CmdFile", action="store_true", help="命令文件模式，输入一个命令文件，执行此文件内命令脚本")
    parser.add_option("--cmd", dest="Cmd", action="store_true", help="命令模式，输入一行命令，会执行此命令，支持多条")
    # 功能参数，可以同时存在
    parser.add_option("--muldump", dest="MulDump", action="store_true", help="判断是否有多个dump要执行，如果是的话，则-d参数可以为一个dump列表文件，内部每一行为一个dump，也可以为一个目录，目录里面存放的.dmp后缀的文件都会被当成dump文件")
    parser.add_option("--defshow", dest="DefaultShow", action="store_true", help="默认展示最终结果，使用默认的编辑器")
    parser.add_option("--answer", dest="Answer", action="store_true", help="只保留最终结果，不保留每一步过程记录")
    parser.add_option("-p", "--path", dest="Path", type="string", help="如果需要指定WinDBG路径")
    parser.add_option("-d", "--dump", dest="Dump", type="string", help="输入需要的dump文件")
    parser.add_option("-s", "--symbol", dest="Symbol", type="string", help="如果需要指定符号路径")
    parser.add_option("-c", "--cmdline", dest="CmdLine", type="string", help="输入的命令")
    parser.add_option("--infile", dest="InFile", type="string", help="输入需要的普通文件")
    parser.add_option("--indir", dest="InDir", type="string", help="输入需要的目录")
    parser.add_option("--outfile", dest="OutFile", type="string", help="输入需要的普通文件")
    parser.add_option("--outdir", dest="OutDir", type="string", help="输入需要的目录")

    return parser.parse_args()
