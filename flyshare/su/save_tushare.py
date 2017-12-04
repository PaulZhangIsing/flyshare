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

import datetime
import json
import re
import time

import tushare as ts

from flyshare.fetch.tushare import fetch_get_stock_day, fetch_get_stock_list, fetch_get_trade_date, fetch_get_stock_info
from flyshare.util import util_date_stamp, util_time_stamp, log_info, trade_date_sse, util_to_json_from_pandas
from flyshare.util.setting import Setting


def save_stock_day_all(client=Setting.client):
    df = ts.get_stock_basics()
    __coll = client.flyshares.stock_day
    __coll.ensure_index('code')

    def saving_work(i):
        log_info('Now Saving ==== %s' % (i))
        try:
            data_json = fetch_get_stock_day(
                i, startDate='1990-01-01')

            __coll.insert_many(data_json)
        except:
            log_info('error in saving ==== %s' % str(i))

    for i_ in range(len(df.index)):
        log_info('The %s of Total %s' % (i_, len(df.index)))
        log_info('DOWNLOAD PROGRESS %s ' % str(
            float(i_ / len(df.index) * 100))[0:4] + '%')
        saving_work(df.index[i_])

    saving_work('hs300')
    saving_work('sz50')


def SU_save_stock_list(client=Setting.client):
    data = fetch_get_stock_list()
    date = str(datetime.date.today())
    date_stamp = util_date_stamp(date)
    coll = client.flyshares.stock_list
    coll.insert({'date': date, 'date_stamp': date_stamp,
                 'stock': {'code': data}})


def SU_save_trade_date_all(client=Setting.client):
    data = fetch_get_trade_date('', '')
    coll = client.flyshares.trade_date
    coll.insert_many(data)


def SU_save_stock_info(client=Setting.client):
    data = fetch_get_stock_info('all')
    coll = client.flyshares.stock_info
    coll.insert_many(data)


def save_stock_day_all_bfq(client=Setting.client):
    df = ts.get_stock_basics()

    __coll = client.flyshares.stock_day_bfq
    __coll.ensure_index('code')

    def saving_work(i):
        log_info('Now Saving ==== %s' % (i))
        try:
            data_json = fetch_get_stock_day(
                i, startDate='1990-01-01', if_fq='00')

            __coll.insert_many(data_json)
        except:
            log_info('error in saving ==== %s' % str(i))

    for i_ in range(len(df.index)):
        log_info('The %s of Total %s' % (i_, len(df.index)))
        log_info('DOWNLOAD PROGRESS %s ' % str(
            float(i_ / len(df.index) * 100))[0:4] + '%')
        saving_work(df.index[i_])

    saving_work('hs300')
    saving_work('sz50')


def save_stock_day_with_fqfactor(client=Setting.client):
    df = ts.get_stock_basics()

    __coll = client.flyshares.stock_day
    __coll.ensure_index('code')

    def saving_work(i):
        log_info('Now Saving ==== %s' % (i))
        try:
            data_hfq = fetch_get_stock_day(
                i, startDate='1990-01-01', if_fq='02', type_='pd')
            data_json = util_to_json_from_pandas(data_hfq)
            __coll.insert_many(data_json)
        except:
            log_info('error in saving ==== %s' % str(i))
    for i_ in range(len(df.index)):
        log_info('The %s of Total %s' % (i_, len(df.index)))
        log_info('DOWNLOAD PROGRESS %s ' % str(
            float(i_ / len(df.index) * 100))[0:4] + '%')
        saving_work(df.index[i_])

    saving_work('hs300')
    saving_work('sz50')

    log_info('Saving Process has been done !')
    return 0


if __name__ == '__main__':
    save_stock_day_with_fqfactor()
