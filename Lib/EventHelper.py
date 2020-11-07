# python3
# 作者        ：NemesisZoo
# 联系方式     ：276793422
# 创建日期     ：2020/11/7
# 文件名       ：EventHelper
# 文件简介     ：
# 文件说明     ：

"""

"""
import win32event

# 创建一个命名Event，创建之前会先尝试打开，如果能打开就打开，否则就真的创建
from multiprocessing import Event

import win32security
from win32api import CloseHandle, Sleep


def CreateNameEvent(name):
    event = Event()
    return None


# 删除一个命名Event


def DeleteNameEvent(event):
    pass


# 等待一个event，timeout=0则立刻返回，否则就超时返回


def WaitEvent(event, timeout=0):
    pass


# 唤醒一个命名Event


def SetEvent(event):
    pass


# 创建一个命名信号并且等待这个命名信号


def CreateNameEventWait(name, timeout=-1):
    # print("create event = [" + name + "]")
    # 根据名字搞个Event
    event = win32event.CreateEvent(None, True, False, name)
    if event is None:
        return False
    # 等这个 Event
    wv = win32event.WaitForSingleObject(event, timeout)
    CloseHandle(event)
    if wv == 0:
        return True
    else:
        return False


# 打开一个命名信号，并且设置这个信号
# 参数2 是执行Open 的次数，由于Open 是可能失败的，所以需要记录一个Open次数
def OpenNameEventSet(name, loop=1):
    # print("open event = [" + name + "]")
    event = None
    for i in range(0, loop):
        # 打开
        event = win32event.OpenEvent(0x1F0003, False, name)
        if event is not None:
            break
        # 打不开就sleep 然后再打开
        Sleep(500)
    if event is None:
        return False
    win32event.SetEvent(event)
    CloseHandle(event)
    return True





