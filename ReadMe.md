# Zoo WinDBG脚本工具

### 目前最简单的使用方法是，
##### 1：配置当前目录下的 config.ini 文件，符号路径可以不填，调试器路径一定要填，否则还调个鸡毛啊
##### 2：安装python3
##### 3：安装相关包，缺啥补啥
##### 4：输入【python3 DebugMain.py --cmd -c "!analyze -v" --defshow -d D:/123.dmp】
#####    含义是，启动当前脚本，执行 cmd 命令，功能是输出 D:/123.dmp 的调试信息，然后默认展示，最后弹出个 notepad 出来

# 目前支持：
###### 第一部分，命令参数，必须存在
    parser.add_option("--address", dest="Address", action="store_true", help="address命令内存分析")
    parser.add_option("--heap", dest="Heap", action="store_true", help="heap命令内存分析")
    parser.add_option("--umdh", dest="Umdh", action="store_true", help="Umdh工具返回信息处理")
    parser.add_option("--analyze", dest="Analyze", action="store_true", help="dump文件自动分析")
    parser.add_option("--callstack", dest="Callstack", action="store_true", help="dump文件自动分析")
    parser.add_option("--cmdfile", dest="CmdFile", action="store_true", help="命令文件模式，输入一个命令文件，执行此文件内命令脚本")
    parser.add_option("--cmd", dest="Cmd", action="store_true", help="命令模式，输入一行命令，会执行此命令，支持多条")
    
###### 第二部分功能参数，配合命令参数存在
    parser.add_option("--defshow", dest="DefaultShow", action="store_true", help="默认展示最终结果，使用默认的编辑器")
    parser.add_option("-p", "--path", dest="Path", type="string", help="如果需要指定WinDBG路径")
    parser.add_option("-d", "--dump", dest="Dump", type="string", help="输入需要的dump文件")
    parser.add_option("-s", "--symbol", dest="Symbol", type="string", help="如果需要指定符号路径")
    parser.add_option("-c", "--cmdline", dest="CmdLine", type="string", help="输入的命令")
    parser.add_option("--infile", dest="InFile", type="string", help="输入需要的普通文件")
    parser.add_option("--indir", dest="InDir", type="string", help="输入需要的目录")
    parser.add_option("--outfile", dest="OutFile", type="string", help="输入需要的普通文件")
    parser.add_option("--outdir", dest="OutDir", type="string", help="输入需要的目录")
    


# 开发者

### NemesisZoo

### QQ：276793422



# 遵循GPL协议就可以了
