#Zoo WinDBG脚本工具


#目前支持：
    parser.add_option("--address", dest="Address", action="store_true", help="address命令内存分析")
    parser.add_option("--heap", dest="Heap", action="store_true", help="heap命令内存分析")
    parser.add_option("--umdh", dest="Umdh", action="store_true", help="Umdh工具返回信息处理")
    parser.add_option("--analyze", dest="Analyze", action="store_true", help="dump文件自动分析")
    parser.add_option("--callstack", dest="Callstack", action="store_true", help="dump文件自动分析")
    parser.add_option("--cmd", dest="Cmd", action="store_true", help="命令模式，输入一个命令文件，会执行此文件内所有脚本")
    parser.add_option("-p", "--path", dest="Path", type="string", help="如果需要指定WinDBG路径")
    parser.add_option("-d", "--dump", dest="Dump", type="string", help="输入需要的dump文件")
    parser.add_option("-s", "--symbol", dest="Symbol", type="string", help="如果需要指定符号路径")
    parser.add_option("--infile", dest="InFile", type="string", help="输入需要的普通文件")
    parser.add_option("--indir", dest="InDir", type="string", help="输入需要的目录")
    parser.add_option("--outfile", dest="OutFile", type="string", help="输入需要的普通文件")
    parser.add_option("--outdir", dest="OutDir", type="string", help="输入需要的目录")



#开发者
###NemesisZoo
###QQ：276793422


