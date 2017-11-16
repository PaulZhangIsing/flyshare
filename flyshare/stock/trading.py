# -*- coding:utf-8 -*- 
"""
Trading Data API 
Created on 2017/10/27
@author: Rubing Duan
@group : abda
@contact: rubing.duan@gmail.com
"""
from __future__ import division

import time
import json
import urllib2
from bson.json_util import loads
import pandas as pd
import numpy as np
from pymongo import MongoClient
from flyshare.stock import cons
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

import json
import bson.json_util as ju
import flyshare.ApiConfig as ac
import tushare as ts
import datetime
import flyshare.util as util

def get_hist_data(code=None, start=None, end=None, ktype='D', data_source='tushare'):
    """
    Parameters
    ------
      code:string
                  Stock code e.g. 600848
      start:string
                  Start Date format：YYYY-MM-DD 
      end:string
                  End Date format：YYYY-MM-DD
      ktype：string
                  Data Type，D=Day W=Week M=Month 5=5min 15=15min 30=30min 60=60min，Default is 'D'
      data_source: string
                  tushare, datareader, flyshare
    return
    -------
      DataFrame
        amount  close    code        date    date_stamp   high    low   open        vol
    """
    if '.HK' in code:
        util.log_info("HK data is only available in Datareader!")
        data_source='datareader'

    if util.is_tushare(data_source):
        return ts.get_hist_data(code = code, start= start, end= end, ktype= ktype)
    elif util.is_datareader(data_source):
        import pandas_datareader.data as web
        start = datetime.datetime.strptime(start, '%Y-%m-%d')
        end = datetime.datetime.strptime(end, '%Y-%m-%d')
        data = None
        try:
            data  =  web.DataReader(code, 'yahoo', start, end)
        except:
            pass
        if data is not None:
            util.log_info("Datareader-Yahoo data:")
            return data
        else:
            try:
                data = web.DataReader(code, 'google', start, end)
            except:
                pass
            if data is not None:
                util.log_info("Datareader-Google data:")
                return data
    elif util.is_flyshare('flyshare'):
        url = cons.DATA_SOURCE+'/histdata?'
        if code is None:
            return None
        else:
            url += 'code='+code

        if start is not None:
            url += '&start='+start
        if end is not None:
            url += '&end='+end

        url += '&api_key='+ ac.api_key

        data = json.loads(ju.loads(urlopen(url).read()))
        df = pd.DataFrame(data)
        if '_id' in df:
            df = df.drop('_id',1)
        return df

def get_tick_data(code=None, date=None, retry_count=3, pause=0.001,
                  src='sn', data_source = 'tusahre'):
    if util.is_today(date):
        return ts.get_today_ticks(code, retry_count, pause)
    if util.is_tushare(data_source):
        return ts.get_tick_data(code, date, retry_count, pause, src)

def get_large_order(code=None, date=None, vol=400, retry_count=3, pause=0.001 , data_source = 'tusahre'):
    if util.is_tushare(data_source):
        return ts.get_sina_dd(code, date, vol, retry_count, pause)

def get_today_all(data_source='tushare'):
    if util.is_tushare(data_source):
        return ts.get_today_all()

def get_realtime_quotes(symbols=None, data_source='tushare'):
    if util.is_tushare(data_source):
        return ts.get_realtime_quotes(symbols)

def get_h_data(code, start=None, end=None, autype='qfq',
               index=False, retry_count=3, pause=0.001, drop_factor=True, data_source='tushare'):
    if util.is_tushare(data_source):
        return ts.get_h_data(code, start, end, autype, index, retry_count, pause, drop_factor)

def get_index(data_source='tushare'):
    if util.is_tushare(data_source):
        return ts.get_index()




def _code_to_symbol(code):
    """
        convert code to symbol
    """
    if code in cons.INDEX_LABELS:
        return cons.INDEX_LIST[code]
    else:
        if len(code) != 6 :
            return code
        else:
            return 'sh%s'%code if code[:1] in ['5', '6', '9'] else 'sz%s'%code

if __name__ == '__main__':
    # print get_hist_data('AAPL',start='2017-01-01', end='2017-10-10', data_source='datareader').head(2)
    print get_hist_data('0700.HK',start='2017-01-01', end='2017-10-10').head(2)