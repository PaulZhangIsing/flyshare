# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2017 yutiansut/flyshare
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from functools import reduce

import numpy as np
import pandas as pd

from flyshare.indicator.Indicator_Series import *


"""
DataFrame 类

以下的函数都可以被直接add_func
开盘价：OPEN O
收盘价：CLOSE C
最高价：HIGH H
最低价：LOW L
成交量：VOLUME V VOL

"""


def indicator_OSC(DataFrame, N, M):
    """变动速率线

    :param DataFrame: 数据
    :param N: 统计天数
    :param M: 统计天数
    :return: osc maosc

    用法注释：

    OSC 以100 为中轴线，OSC>100 为多头市场；OSC<100 为空头市场；
    OSC 向上交叉其平均线时，买进；OSC 向下交叉其平均线时卖出；
    OSC 在高水平或低水平与股价产生背离时，应注意股价随时有反转的可能；
    OSC 的超买超卖界限值随个股不同而不同，使用者应自行调整

    """

    C = DataFrame['close']
    OS = (C - MA(C, N)) * 100
    MAOSC = EMA(OS, M)
    DICT = {'OSC': OS, 'MAOSC': MAOSC}

    return DICT


def indicator_BBI(DataFrame, N1, N2, N3, N4):
    """多空指标

    :param DataFrame: 数据
    :param N1: 统计天数
    :param N2: 统计天数
    :param N3: 统计天数
    :param N4: 统计天数
    :return: BBI

    用法注释：

    1.股价位于BBI 上方，视为多头市场；
    2.股价位于BBI 下方，视为空头市场。

    """
    C = DataFrame['close']
    bbi = (MA(C, N1) + MA(C, N2) + MA(C, N3) + MA(C, N4)) / 4
    DICT = {'BBI': bbi}

    return DICT


def indicator_PBX(DataFrame, N1, N2, N3, N4, N5, N6):
    """ 瀑布线 PBX

    :param DataFrame:
    :param N1: 统计天数
    :param N2: 统计天数
    :param N3: 统计天数
    :param N4: 统计天数
    :param N5: 统计天数
    :param N6: 统计天数
    :return: PBX

    用法注释：

    股价上升穿越轨道线上限时，回档机率大；
    股价下跌穿越轨道线下限时，反弹机率大；
    股价波动于轨道线内时，代表常态行情，此时，超买超卖指标可发挥效用；
    股价波动于轨道线外时，代表脱轨行情，此时，应使用趋势型指标。

    """

    ''
    C = DataFrame['close']
    PBX1 = (EMA(C, N1) + EMA(C, 2 * N1) + EMA(C, 4 * N1)) / 3
    PBX2 = (EMA(C, N2) + EMA(C, 2 * N2) + EMA(C, 4 * N2)) / 3
    PBX3 = (EMA(C, N3) + EMA(C, 2 * N3) + EMA(C, 4 * N3)) / 3
    PBX4 = (EMA(C, N4) + EMA(C, 2 * N4) + EMA(C, 4 * N4)) / 3
    PBX5 = (EMA(C, N5) + EMA(C, 2 * N5) + EMA(C, 4 * N5)) / 3
    PBX6 = (EMA(C, N6) + EMA(C, 2 * N6) + EMA(C, 4 * N6)) / 3
    DICT = {'PBX1': PBX1, 'PBX2': PBX2, 'PBX3': PBX3,
            'PBX4': PBX4, 'PBX5': PBX5, 'PBX6': PBX6}

    return DICT


def indicator_BOLL(DataFrame, N):
    """布林线

    其英文全称是“Bolinger Bands”，是研判股价运动趋势的一种中长期技术分析工具
    :param DataFrame:
    :param N:
    :return: 上轨线UB 、中轨线BOLL、下轨线LB 的值

    用法注释：

    1.股价上升穿越布林线上限时，回档机率大；
    2.股价下跌穿越布林线下限时，反弹机率大；
    3.布林线震动波带变窄时，表示变盘在即；
    4.BOLL须配合BB 、WIDTH 使用

    """
    C = DataFrame['close']
    boll = MA(C, N)
    UB = boll + 2 * STD(C, N)
    LB = boll - 2 * STD(C, N)
    DICT = {'BOLL': boll, 'UB': UB, 'LB': LB}

    return DICT


def indicator_ROC(DataFrame, N, M):
    """变动率指标

    :param DataFrame:
    :param N:
    :param M:
    :return: ROC

    用法注释：

    1.本指标的超买超卖界限值随个股不同而不同，使用者应自行调整；
    2.本指标的超买超卖范围，一般介于±6.5之间；
    3.本指标用法请参考MTM 指标用法；
    4.本指标可设参考线。
    """
    C = DataFrame['close']
    roc = 100 * (C - REF(C, N)) / REF(C, N)
    MAROC = MA(roc, M)
    DICT = {'ROC': roc, 'MAROC': MAROC}

    return DICT


def indicator_MTM(DataFrame, N, M):
    """动量线

    其英文全称是“Momentom Index”，是一种专门研究股价波动的中短期技术分析工具

    :param DataFrame:
    :param N:
    :param M:
    :return:

    用法注释：

    MTM线　:当日收盘价与N日前的收盘价的差；
    MTMMA线:对上面的差值求N日移动平均；
    参数：N 间隔天数，也是求移动平均的天数，一般取6用法：
    1.MTM从下向上突破MTMMA，买入信号；
    2.MTM从上向下跌破MTMMA，卖出信号；
    3.股价续创新高，而MTM未配合上升，意味上涨动力减弱；
    4.股价续创新低，而MTM未配合下降，意味下跌动力减弱；
    5.股价与MTM在低位同步上升，将有反弹行情；反之，从高位同步下降，将有回落走势。

    """

    C = DataFrame['close']
    mtm = C - REF(C, N)
    MTMMA = MA(mtm, M)
    DICT = {'MTM': mtm, 'MTMMA': MTMMA}

    return DICT

def indicator_KDJ(DataFrame, N=9, M1=3, M2=3):
    """随机指标(Stochastics)KDJ

    其综合动量观念，强弱指标及移动平均线的优点，后被广泛用于股市的中短期趋势分析；
    由 George C．Lane 创制。它综合了动量观念、强弱指标及移动平均线的优点，用来度量股价脱离价格正常范围的变异程度。

    :param DataFrame:
    :param N:
    :param M1:
    :param M2:
    :return:
    """

    C = DataFrame['close']
    H = DataFrame['high']
    L = DataFrame['low']

    RSV = (C - LLV(L, N)) / (HHV(H, N) - LLV(L, N)) * 100
    K = SMA(RSV, M1)
    D = SMA(K, M2)
    J = 3 * K - 2 * D
    DICT = {'KDJ_K': K, 'KDJ_D': D, 'KDJ_J': J}

    return DICT


def indicator_MFI(DataFrame, N=14):
    """
    资金指标

    TYP := (HIGH + LOW + CLOSE)/3;
    V1:=SUM(IF(TYP>REF(TYP,1),TYP*VOL,0),N)/SUM(IF(TYP<REF(TYP,1),TYP*VOL,0),N);
    MFI:100-(100/(1+V1));
    赋值: (最高价 + 最低价 + 收盘价)/3
    V1赋值:如果TYP>1日前的TYP,返回TYP*成交量(手),否则返回0的N日累和/如果TYP<1日前的TYP,返回TYP*成交量(手),否则返回0的N日累和
    输出资金流量指标:100-(100/(1+V1))
    """

    C = DataFrame['close']
    H = DataFrame['high']
    L = DataFrame['low']
    VOL = DataFrame['volume']
    TYP = (C + H + L) / 3
    V1 = SUM(IF(TYP > REF(TYP, 1), TYP * VOL, 0), N) / \
        SUM(IF(TYP < REF(TYP, 1), TYP * VOL, 0), N)
    mfi = 100 - (100 / (1 + V1))
    DICT = [{'MFI': mfi}]

    return DICT


def indicator_ATR(DataFrame, N):
    C = DataFrame['close']
    H = DataFrame['high']
    L = DataFrame['low']
    TR1 = MAX(MAX((H - L), ABS(REF(C, 1) - H)), ABS(REF(C, 1) - L))
    atr = MA(TR1, N)
    return atr


def indicator_SKDJ(DataFrame, N, M):
    CLOSE = DataFrame['close']
    LOWV = LLV(DataFrame['low'], N)
    HIGHV = HHV(DataFrame['high'], N)
    RSV = EMA((CLOSE - LOWV) / (HIGHV - LOWV) * 100, M)
    K = EMA(RSV, M)
    D = MA(K, M)
    DICT = {'SKDJ_K': K, 'SKDJ_D': D}

    return DICT


def indicator_WR(DataFrame, N, N1):
    """威廉指标

    又叫威廉超买超卖指标，简称威廉指标，是目前股市技术分析中比较常用的短期研判指标
    :param DataFrame:
    :param N:
    :param N1:
    :return:

    方法注释：

    WR波动于0 - 100，100置于顶部，0置于底部。
    本指标以50为中轴线，高于50视为股价转强；低于50视为股价转弱
    本指标高于20后再度向下跌破20，卖出；低于80后再度向上突破80，买进。
    WR连续触底3 - 4次，股价向下反转机率大；连续触顶3 - 4次，股价向上反转机率大。

    """

    HIGH = DataFrame['high']
    LOW = DataFrame['low']
    CLOSE = DataFrame['close']
    WR1 = 100 * (HHV(HIGH, N) - CLOSE) / (HHV(HIGH, N) - LLV(LOW, N))
    WR2 = 100 * (HHV(HIGH, N1) - CLOSE) / (HHV(HIGH, N1) - LLV(LOW, N1))
    DICT = {'WR1': WR1, 'WR2': WR2}

    return DICT


def indicator_BIAS(DataFrame, N1, N2, N3):
    """乖离率

    又叫Y值，是由移动平均原理派生出来的一种技术分析指标，是目前股市技术分析中一种短中长期皆可的技术分析工具；

    :param DataFrame:
    :param N1:
    :param N2:
    :param N3:
    :return:


    用法注释：

    1.本指标的乖离极限值随个股不同而不同，使用者可利用参考线设定，固定其乖离范围；
    2.当股价的正乖离扩大到一定极限时，股价会产生向下拉回的作用力；
    3.当股价的负乖离扩大到一定极限时，股价会产生向上拉升的作用力；
    4.本指标可设参考线。
    """

    CLOSE = DataFrame['close']
    BIAS1 = (CLOSE - MA(CLOSE, N1)) / MA(CLOSE, N1) * 100
    BIAS2 = (CLOSE - MA(CLOSE, N2)) / MA(CLOSE, N2) * 100
    BIAS3 = (CLOSE - MA(CLOSE, N3)) / MA(CLOSE, N3) * 100
    DICT = {'BIAS1': BIAS1, 'BIAS2': BIAS2, 'BIAS3': BIAS3}

    return DICT


def indicator_RSI(DataFrame, N1, N2, N3):
    """相对强弱指标RSI

    又叫力度指标，其英文全称为“Relative Strength Index”，是目前股市技术分析中比较常用的中短线指标

    :param DataFrame:
    :param N1:
    :param N2:
    :param N3:
    :return:
    """

    '相对强弱指标RSI1:SMA(MAX(CLOSE-LC,0),N1,1)/SMA(ABS(CLOSE-LC),N1,1)*100;'
    CLOSE = DataFrame['close']
    LC = REF(CLOSE, 1)
    RSI1 = SMA(MAX(CLOSE - LC, 0), N1) / SMA(ABS(CLOSE - LC), N1) * 100
    RSI2 = SMA(MAX(CLOSE - LC, 0), N2) / SMA(ABS(CLOSE - LC), N2) * 100
    RSI3 = SMA(MAX(CLOSE - LC, 0), N3) / SMA(ABS(CLOSE - LC), N3) * 100
    DICT = {'RSI1': RSI1, 'RSI2': RSI2, 'RSI3': RSI3}

    return DICT


def indicator_ADTM(DataFrame, N, M):
    '动态买卖气指标'
    HIGH = DataFrame['high']
    LOW = DataFrame['low']
    OPEN = DataFrame['open']
    DTM = IF(OPEN <= REF(OPEN, 1), 0, MAX(
        (HIGH - OPEN), (OPEN - REF(OPEN, 1))))
    DBM = IF(OPEN >= REF(OPEN, 1), 0, MAX((OPEN - LOW), (OPEN - REF(OPEN, 1))))
    STM = SUM(DTM, N)
    SBM = SUM(DBM, N)
    ADTM1 = IF(STM > SBM, (STM - SBM) / STM,
               IF(STM == SBM, 0, (STM - SBM) / SBM))
    MAADTM = MA(ADTM1, M)
    DICT = {'ADTM': ADTM1, 'MAADTM': MAADTM}

    return DICT


def indicator_DDI(DataFrame, N, N1, M, M1):
    '方向标准离差指数'
    H = DataFrame['high']
    L = DataFrame['low']
    DMZ = IF((H + L) <= (REF(H, 1) + REF(L, 1)), 0,
             MAX(ABS(H - REF(H, 1)), ABS(L - REF(L, 1))))
    DMF = IF((H + L) >= (REF(H, 1) + REF(L, 1)), 0,
             MAX(ABS(H - REF(H, 1)), ABS(L - REF(L, 1))))
    DIZ = SUM(DMZ, N) / (SUM(DMZ, N) + SUM(DMF, N))
    DIF = SUM(DMF, N) / (SUM(DMF, N) + SUM(DMZ, N))
    ddi = DIZ - DIF
    ADDI = SMA(ddi, N1, M)
    AD = MA(ADDI, M1)
    DICT = {'DDI': ddi, 'ADDI': ADDI, 'AD': AD}

    return DICT


def indicator_CCI(DataFrame, N=14):
    """CCI指标

    又叫顺势指标，其英文全称为“Commodity Channel Index”，是一种重点研判股价偏离度的股市分析工具
    :param DataFrame:
    :param N:
    :return:
    """


    """
    TYP:=(HIGH+LOW+CLOSE)/3;
    CCI:(TYP-MA(TYP,N))/(0.015*AVEDEV(TYP,N));
    返回一个值
    """
    typ = (DataFrame['high'] + DataFrame['low'] + DataFrame['close']) / 3
    return ((typ - MA(typ, N)) / (0.015 * AVEDEV(typ, N))).tail(1)

def indicator_ASI(DataFrame,M1,M2):
    """
    LC=REF(CLOSE,1);
    AA=ABS(HIGH-LC);
    BB=ABS(LOW-LC);
    CC=ABS(HIGH-REF(LOW,1));
    DD=ABS(LC-REF(OPEN,1));
    R=IF(AA>BB AND AA>CC,AA+BB/2+DD/4,IF(BB>CC AND BB>AA,BB+AA/2+DD/4,CC+DD/4));
    X=(CLOSE-LC+(CLOSE-OPEN)/2+LC-REF(OPEN,1));
    SI=16*X/R*MAX(AA,BB);
    ASI:SUM(SI,M1);
    ASIT:MA(ASI,M2);
    """
    CLOSE=DataFrame['close']
    HIGH=DataFrame['high']
    LOW=DataFrame['low']
    OPEN=DataFrame['open']
    LC=REF(CLOSE,1)
    AA=ABS(HIGH-LC)
    CC=ABS(HIGH-REF(LOW,1))
    DD=ABS(LC-REF(OPEN,1))
    
    #R=IF(AA>BB AND AA>CC,AA+BB/2+DD/4,IF(BB>CC AND BB>AA,BB+AA/2+DD/4,CC+DD/4))
    X=(CLOSE-LC+(CLOSE-OPEN)/2+LC-REF(OPEN,1))

def indicator_MA(DataFrame,N):
    CLOSE = DataFrame['close']
    return MA(CLOSE,N)

def indicator_EMA(DataFrame,N):
    CLOSE = DataFrame['close']
    return EMA(CLOSE,N)

def indicator_SMA(DataFrame,N):
    CLOSE = DataFrame['close']
    return SMA(CLOSE,N)


def lower_shadow(DataFrame):#下影线
    return abs(DataFrame.low-MIN(DataFrame.open,DataFrame.close))

def upper_shadow(DataFrame):#上影线
    return abs(DataFrame.high-MAX(DataFrame.open,DataFrame.close))

def body_abs(DataFrame):
    return abs(DataFrame.open-DataFrame.close)

def body(DataFrame):
    return DataFrame.close-DataFrame.open

def price_pcg(DataFrame):
    return body(DataFrame)/DataFrame.open

def amplitude(DataFrame):
    return (DataFrame.high-DataFrame.low)/DataFrame.low