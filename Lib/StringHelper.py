# python3
# 作者        ：NemesisZoo
# 联系方式     ：276793422
# 创建日期     ：2020/9/30
# 文件名       ：StringHelper.py
# 文件简介     ：
# 文件说明     ：

"""

"""


# 判断当前字符是否是一个16进制数字


def IsANumber(x):
    if x == '0' or x == '1' or x == '2' or x == '3' or x == '4' or x == '5' or x == '6' or x == '7' or x == '8' or x == '9' or x == 'a' or x == 'b' or x == 'c' or x == 'd' or x == 'e' or x == 'f' or x == 'A' or x == 'B' or x == 'C' or x == 'D' or x == 'E' or x == 'F':
        return True
        pass
    return False


# 判断当前字符串是否是一个十六进制数字

def IsNumber(x):
    if x.startswith("0x"):
        x = x[2:]
    x = x.replace("`", "")
    for t in x:
        if not IsANumber(t):
            return False
    return True


# 判断字符串是否有效

def IsStringValid(p):
    if p is not None and p != "":
        return True
    return False
