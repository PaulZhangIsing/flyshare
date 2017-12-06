# coding:utf-8


import numpy as np
import pandas as pd
from functools import reduce


"""
Series 类

这个是下面以DataFrame为输入的基础函数
"""

# exponential weighted function
def EMA(Series, N):
    return pd.Series.ewm(Series, span=N, min_periods=N - 1, adjust=True).mean()


def MA(Series, N):
    return pd.Series.rolling(Series, N).mean()

# 威廉SMA  参考https://www.joinquant.com/post/867


def SMA(Series, N):
    '威廉SMA'
    Series = pd.Series(Series).fillna(0)
    return reduce(lambda x, y: ((N - 1) * x + y) / N, Series)


def DIFF(Series, N=1):
    return pd.Series(Series).diff(N)


def HHV(Series, N):
    """ N天内最大值

    :param Series:
    :param N:
    :return:
    """
    return pd.Series(Series).rolling(N).max().values


def LLV(Series, N):
    """ N天内最小值

    :param Series:
    :param N:
    :return:
    """
    return pd.Series(Series).rolling(N).min().values


def SUM(Series, N):
    return pd.Series.rolling(Series, N).sum()


def ABS(Series):
    return abs(Series)


def MAX(A, B):
    var = IF(A > B, A, B)
    return var


def MIN(A, B):
    var = IF(A < B, A, B)
    return var


def CROSS(A, B):
    if A[-2] < B[-2] and A[-1] > B[-1]:
        return True
    else:
        return False


def COUNT(COND, N):
    var = np.where(COND, 1, 0)
    return var[-N:].sum()


def IF(COND, V1, V2):
    var = np.where(COND, V1, V2)
    return pd.Series(var, index=V1.index)


def REF(Series, N):
    var = Series.diff(N)
    var = Series - var
    return var


def STD(Series, N):
    return pd.Series.rolling(Series, N).std()


def AVEDEV(Series, N):
    '平均绝对偏差 mean absolute deviation'
    return pd.Series(Series).tail(N).mad()


def MACD(Series, FAST, SLOW, MID):
    EMAFAST = EMA(Series, FAST)
    EMASLOW = EMA(Series, SLOW)
    DIFF = EMAFAST - EMASLOW
    DEA = EMA(DIFF, MID)
    MACD = (DIFF - DEA) * 2
    DICT = {'DIFF': DIFF, 'DEA': DEA, 'MACD': MACD}
    VAR = pd.DataFrame(DICT)
    return VAR


def BBIBOLL(Series, N1, N2, N3, N4, N, M):  # 多空布林线

    bbiboll = BBI(Series, N1, N2, N3, N4)
    UPER = bbiboll + M * STD(bbiboll, N)
    DOWN = bbiboll - M * STD(bbiboll, N)
    DICT = {'BBIBOLL': bbiboll, 'UPER': UPER, 'DOWN': DOWN}
    VAR = pd.DataFrame(DICT)
    return VAR


def BBI(Series, N1, N2, N3, N4):
    '多空指标'

    bbi = (MA(Series, N1) + MA(Series, N2) +
           MA(Series, N3) + MA(Series, N4)) / 4
    DICT = {'BBI': bbi}
    VAR = pd.DataFrame(DICT)
    return VAR
