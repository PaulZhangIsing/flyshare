# -*- coding:utf-8 -*-
"""
Trading Data API
Created on 2017/10/27
@author: Rubing Duan
@group : abda
@contact: rubing.duan@gmail.com
"""

import pandas as pd
import lxml.html
from lxml import etree
import re
import time
from pandas.compat import StringIO
from flyshare.stock import cons
import json
import bson.json_util as ju
import tushare as ts
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

def get_stock_basics(date=None, data_source = 'tushare'):
    """


        Get the basic info of Shanghai and Shenzhen listed companies
    Parameters
    date: YYYY-MM-DD，Default is the last trading day, currently only provide historical data after 2016-08-09

    Return
    --------
    DataFrame
               code,
               name,
               industry,
               area,
               pe,
               outstanding,
               totals,
               totalAssets,
               liquidAssets,
               fixedAssets,
               reserved,
               reservedPerShare,
               eps,
               bvps,
               pb,
               timeToMarket
    """
    if data_source == 'tushare':
        print 'tushare'
        return ts.get_stock_basics(date=date)

    url = cons.DATA_SOURCE + '/stockbasics'
    if date is not None:
        url += '?date='+date
    data = json.loads(ju.loads(urlopen(url).read()))
    df = pd.DataFrame(data)
    if '_id' in df:
        df = df.drop('_id', 1)
    return df


if __name__ == '__main__':
    print get_stock_basics()