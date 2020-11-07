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

# 主函数

if __name__ == "__main__":

    # 初始化调试器必须的环境变量
    if not InitDebugLibrary():
        print("配置出错，环境变量不足")
    else:
        RunDebug()
