# coding:utf-8

import datetime

import numpy as np
import pandas as pd
from pytdx.hq import TdxHq_API
from pytdx.exhq import TdxExHq_API
from flyshare.util import (util_date_stamp, util_date_str2int,
                           util_date_valid, util_get_real_date,
                           util_get_real_datelist, log_info,
                           util_time_stamp, ping,
                           trade_date_sse)
import flyshare.ApiConfig as ac
#from pypinyin import lazy_pinyin
import tushare as ts

# 基于Pytdx的数据接口,好处是可以在linux/mac上联入通达信行情
# 具体参见rainx的pytdx(https://github.com/rainx/pytdx)
#


def ping(ip):
    api = TdxHq_API()
    __time1 = datetime.datetime.now()
    try:
        with api.connect(ip, 7709):
            if len(api.get_security_list(0, 1)) > 800:
                return datetime.datetime.now() - __time1
    except:
        print('Bad REPSONSE %s' % ip)
        return datetime.timedelta(9, 9, 0)


def select_best_ip():
    log_info('Selecting the Best Server IP of TDX')
    listx = ['218.75.126.9', '115.238.90.165',
             '124.160.88.183', '60.12.136.250', '218.108.98.244', '218.108.47.69',
             '14.17.75.71', '180.153.39.51']
    conn_times = [ping(x) for x in listx]
    best_ip = listx[conn_times.index(min(conn_times))]
    log_info('===The BEST SERVER is :  %s ===' % (best_ip))
    ac.TDX_BEST_IP = best_ip
    return best_ip


# best_ip = select_best_ip()

# return 1 if sh, 0 if sz


def __select_market_code(code):
    code = str(code)
    if code[0] in ['5', '6', '9'] or code[:3] in ["009", "126", "110", "201", "202", "203", "204"]:
        return 1
    return 0


def __select_type(level):
    if level in ['day', 'd', 'D', 'DAY', 'Day']:
        level = 9
    elif level in ['w', 'W', 'Week', 'week']:
        level = 5
    elif level in ['month', 'M', 'm', 'Month']:
        level = 6
    elif level in ['Q', 'Quarter', 'q']:
        level = 10
    elif level in ['y', 'Y', 'year', 'Year']:
        level = 11
    elif str(level) in ['5', '5m', '5min', 'five']:
        level, type_ = 0, '5min'
    elif str(level) in ['1', '1m', '1min', 'one']:
        level, type_ = 8, '1min'
    elif str(level) in ['15', '15m', '15min', 'fifteen']:
        level, type_ = 1, '15min'
    elif str(level) in ['30', '30m', '30min', 'half']:
        level, type_ = 2, '30min'
    elif str(level) in ['60', '60m', '60min', '1h']:
        level, type_ = 3, '60min'

    return level


def fetch_security_bars(code, _type, lens, ip=ac.TDX_BEST_IP, port=7709):
    api = TdxHq_API()
    with api.connect(ip, port):
        data = pd.concat([api.to_df(api.get_security_bars(__select_type(_type), __select_market_code(
            code), code, (i - 1) * 800, 800)) for i in range(1, int(lens / 800) + 2)], axis=0)
        if data is not None:
            return data
        else:
            return None


def fetch_get_stock_day(code, start_date, end_date, if_fq='00', level='day', ip=ac.TDX_BEST_IP, port=7709):
    api = TdxHq_API()
    with api.connect(ip, port):

        if level in ['day', 'd', 'D', 'DAY', 'Day']:
            level = 9
        elif level in ['w', 'W', 'Week', 'week']:
            level = 5
        elif level in ['month', 'M', 'm', 'Month']:
            level = 6
        elif level in ['Q', 'Quarter', 'q']:
            level = 10
        elif level in ['y', 'Y', 'year', 'Year']:
            level = 11

        data = pd.concat([api.to_df(api.get_security_bars(level, __select_market_code(
            code), code, (9 - i) * 800, 800)) for i in range(10)], axis=0)
        data = data[data['open'] != 0]

        if if_fq in ['00', 'bfq']:
            data = data.assign(date=data['datetime'].apply(lambda x: str(x[0:10]))).assign(code=str(code))\
                .assign(date_stamp=data['datetime'].apply(lambda x: util_date_stamp(str(x)[0:10]))).set_index('date', drop=False, inplace=False)
            return data.drop(['year', 'month', 'day', 'hour', 'minute', 'datetime'], axis=1)[start_date:end_date].assign(date=data['date'].apply(lambda x: str(x)[0:10]))

        elif if_fq in ['01', 'qfq']:

            xdxr_data = fetch_get_stock_xdxr(code)
            bfq_data = data.assign(date=pd.to_datetime(data['datetime'].apply(lambda x: str(x[0:10])))).assign(code=str(code))\
                .assign(date_stamp=data['datetime'].apply(lambda x: util_date_stamp(str(x)[0:10]))).set_index('date', drop=False, inplace=False)
            bfq_data = bfq_data.drop(
                ['year', 'month', 'day', 'hour', 'minute', 'datetime'], axis=1)
            #
            if xdxr_data is not None:
                info = xdxr_data[xdxr_data['category'] == 1]
                bfq_data['if_trade'] = True
                data = pd.concat([bfq_data, info[['category']]
                                  [bfq_data.index[0]:]], axis=1)

                data['date'] = data.index
                data['if_trade'].fillna(value=False, inplace=True)
                data = data.fillna(method='ffill')
                data = pd.concat([data, info[['fenhong', 'peigu', 'peigujia',
                                              'songzhuangu']][bfq_data.index[0]:]], axis=1)
                data = data.fillna(0)

                data['preclose'] = (data['close'].shift(1) * 10 - data['fenhong'] + data['peigu']
                                    * data['peigujia']) / (10 + data['peigu'] + data['songzhuangu'])
                data['adj'] = (data['preclose'].shift(-1) /
                               data['close']).fillna(1)[::-1].cumprod()
                data['open'] = data['open'] * data['adj']
                data['high'] = data['high'] * data['adj']
                data['low'] = data['low'] * data['adj']
                data['close'] = data['close'] * data['adj']
                data['preclose'] = data['preclose'] * data['adj']

                data = data[data['if_trade']]
                return data.drop(['fenhong', 'peigu', 'peigujia', 'songzhuangu', 'if_trade', 'category'], axis=1)[data['open'] != 0].assign(date=data['date'].apply(lambda x: str(x)[0:10]))[start_date:end_date]
            else:

                bfq_data['preclose'] = bfq_data['close'].shift(1)
                bfq_data['adj'] = 1
                return bfq_data[start_date:end_date]
        elif if_fq in ['03', 'ddqfq']:
            xdxr_data = fetch_get_stock_xdxr(code)

            info = xdxr_data[xdxr_data['category'] == 1]

            bfq_data = data\
                .assign(date=pd.to_datetime(data['datetime'].apply(lambda x: x[0:10])))\
                .assign(code=str(code))\
                .assign(date_stamp=data['datetime'].apply(lambda x: util_date_stamp(str(x)[0:10])))\
                .set_index('date', drop=False, inplace=False)\
                .drop(['year', 'month', 'day', 'hour',
                       'minute', 'datetime'], axis=1)

            bfq_data['if_trade'] = True
            data = pd.concat([bfq_data, info[['category']]
                              [bfq_data.index[0]:end_date]], axis=1)

            data['date'] = data.index
            data['if_trade'].fillna(value=False, inplace=True)
            data = data.fillna(method='ffill')
            data = pd.concat([data, info[['fenhong', 'peigu', 'peigujia',
                                          'songzhuangu']][bfq_data.index[0]:end_date]], axis=1)
            data = data.fillna(0)

            data['preclose'] = (data['close'].shift(1) * 10 - data['fenhong'] + data['peigu']
                                * data['peigujia']) / (10 + data['peigu'] + data['songzhuangu'])
            data['adj'] = (data['preclose'].shift(-1) /
                           data['close']).fillna(1)[::-1].cumprod()
            data['open'] = data['open'] * data['adj']
            data['high'] = data['high'] * data['adj']
            data['low'] = data['low'] * data['adj']
            data['close'] = data['close'] * data['adj']
            data['preclose'] = data['preclose'] * data['adj']

            data = data[data['if_trade']]
            return data.drop(['fenhong', 'peigu', 'peigujia', 'songzhuangu', 'if_trade', 'category'], axis=1)[data['open'] != 0].assign(date=data['date'].apply(lambda x: str(x)[0:10]))[start_date:end_date]

        elif if_fq in ['02', 'hfq']:
            xdxr_data = fetch_get_stock_xdxr(code)

            info = xdxr_data[xdxr_data['category'] == 1]

            bfq_data = data\
                .assign(date=pd.to_datetime(data['datetime'].apply(lambda x: x[0:10])))\
                .assign(code=str(code))\
                .assign(date_stamp=data['datetime'].apply(lambda x: util_date_stamp(str(x)[0:10])))\
                .set_index('date', drop=False, inplace=False)\
                .drop(['year', 'month', 'day', 'hour',
                       'minute', 'datetime'], axis=1)

            bfq_data['if_trade'] = True
            data = pd.concat([bfq_data, info[['category']]
                              [bfq_data.index[0]:]], axis=1)

            data['date'] = data.index
            data['if_trade'].fillna(value=False, inplace=True)
            data = data.fillna(method='ffill')
            data = pd.concat([data, info[['fenhong', 'peigu', 'peigujia',
                                          'songzhuangu']][bfq_data.index[0]:]], axis=1)
            data = data.fillna(0)

            data['preclose'] = (data['close'].shift(1) * 10 - data['fenhong'] + data['peigu']
                                * data['peigujia']) / (10 + data['peigu'] + data['songzhuangu'])
            data['adj'] = (data['preclose'].shift(-1) /
                           data['close']).fillna(1).cumprod()
            data['open'] = data['open'] / data['adj']
            data['high'] = data['high'] / data['adj']
            data['low'] = data['low'] / data['adj']
            data['close'] = data['close'] / data['adj']
            data['preclose'] = data['preclose'] / data['adj']
            data = data[data['if_trade']]
            return data.drop(['fenhong', 'peigu', 'peigujia', 'songzhuangu', 'if_trade', 'category'], axis=1)[data['open'] != 0].assign(date=data['date'].apply(lambda x: str(x)[0:10]))[start_date:end_date]

        elif if_fq in ['04', 'ddhfq']:
            xdxr_data = fetch_get_stock_xdxr(code)

            info = xdxr_data[xdxr_data['category'] == 1]

            bfq_data = data\
                .assign(date=pd.to_datetime(data['datetime'].apply(lambda x: x[0:10])))\
                .assign(code=str(code))\
                .assign(date_stamp=data['datetime'].apply(lambda x: util_date_stamp(str(x)[0:10])))\
                .set_index('date', drop=False, inplace=False)\
                .drop(['year', 'month', 'day', 'hour',
                       'minute', 'datetime'], axis=1)

            bfq_data['if_trade'] = True
            data = pd.concat([bfq_data, info[['category']]
                              [bfq_data.index[0]:end_date]], axis=1)

            data['date'] = data.index
            data['if_trade'].fillna(value=False, inplace=True)
            data = data.fillna(method='ffill')
            data = pd.concat([data, info[['fenhong', 'peigu', 'peigujia',
                                          'songzhuangu']][bfq_data.index[0]:end_date]], axis=1)
            data = data.fillna(0)

            data['preclose'] = (data['close'].shift(1) * 10 - data['fenhong'] + data['peigu']
                                * data['peigujia']) / (10 + data['peigu'] + data['songzhuangu'])
            data['adj'] = (data['preclose'].shift(-1) /
                           data['close']).fillna(1).cumprod()
            data['open'] = data['open'] / data['adj']
            data['high'] = data['high'] / data['adj']
            data['low'] = data['low'] / data['adj']
            data['close'] = data['close'] / data['adj']
            data['preclose'] = data['preclose'] / data['adj']
            data = data[data['if_trade']]
            return data.drop(['fenhong', 'peigu', 'peigujia', 'songzhuangu', 'if_trade', 'category'], axis=1)[data['open'] != 0].assign(date=data['date'].apply(lambda x: str(x)[0:10]))[start_date:end_date]


def fetch_get_stock_min(code, start, end, level='1min', ip=ac.TDX_BEST_IP, port=7709):
    api = TdxHq_API()
    type_ = ''
    if str(level) in ['5', '5m', '5min', 'five']:
        level, type_ = 0, '5min'
    elif str(level) in ['1', '1m', '1min', 'one']:
        level, type_ = 8, '1min'
    elif str(level) in ['15', '15m', '15min', 'fifteen']:
        level, type_ = 1, '15min'
    elif str(level) in ['30', '30m', '30min', 'half']:
        level, type_ = 2, '30min'
    elif str(level) in ['60', '60m', '60min', '1h']:
        level, type_ = 3, '60min'
    with api.connect(ip, port):

        data = pd.concat([api.to_df(api.get_security_bars(level, __select_market_code(
            str(code)), str(code), (25 - i) * 800, 800)) for i in range(26)], axis=0)

        data = data\
            .assign(datetime=pd.to_datetime(data['datetime']), code=str(code))\
            .drop(['year', 'month', 'day', 'hour', 'minute'], axis=1, inplace=False)\
            .assign(date=data['datetime'].apply(lambda x: str(x)[0:10]))\
            .assign(date_stamp=data['datetime'].apply(lambda x: util_date_stamp(x)))\
            .assign(time_stamp=data['datetime'].apply(lambda x: util_time_stamp(x)))\
            .assign(type=type_).set_index('datetime', drop=False, inplace=False)[start:end]
        return data.assign(datetime=data['datetime'].apply(lambda x: str(x)))


def fetch_get_stock_latest(code, ip=ac.TDX_BEST_IP, port=7709):
    code = [code] if isinstance(code, str) else code
    api = TdxHq_API(multithread=True)
    with api.connect(ip, port):
        data = pd.concat([api.to_df(api.get_security_bars(
            9, __select_market_code(item), item, 0, 1)).assign(code=item) for item in code], axis=0)
        return data\
            .assign(date=pd.to_datetime(data['datetime']
                                        .apply(lambda x: x[0:10])), date_stamp=data['datetime']
                    .apply(lambda x: util_date_stamp(str(x[0:10]))))\
            .set_index('date', drop=False)\
            .drop(['year', 'month', 'day', 'hour', 'minute', 'datetime'], axis=1)


def fetch_get_stock_realtime(code=['000001', '000002'], ip=ac.TDX_BEST_IP, port=7709):
    api = TdxHq_API()
    __data = pd.DataFrame()
    with api.connect(ip, port):
        code = [code] if type(code) is str else code
        for id_ in range(int(len(code) / 80) + 1):
            __data = __data.append(api.to_df(api.get_security_quotes(
                [(__select_market_code(x), x) for x in code[80 * id_:80 * (id_ + 1)]])))
            __data['datetime'] = datetime.datetime.now()
        data = __data[['datetime', 'last_close', 'code', 'open', 'high', 'low', 'price', 'cur_vol',
                       's_vol', 'b_vol', 'vol', 'ask1', 'ask_vol1', 'bid1', 'bid_vol1', 'ask2', 'ask_vol2',
                       'bid2', 'bid_vol2', 'ask3', 'ask_vol3', 'bid3', 'bid_vol3', 'ask4',
                       'ask_vol4', 'bid4', 'bid_vol4', 'ask5', 'ask_vol5', 'bid5', 'bid_vol5']]
        return data.set_index('code', drop=False, inplace=False)


def fetch_get_stock_list(type_='stock', ip=ac.TDX_BEST_IP, port=7709):

    api = TdxHq_API()
    with api.connect(ip, port):
        data = pd.concat([pd.concat([api.to_df(api.get_security_list(j, i * 1000)).assign(sse='sz' if j == 0 else 'sh').set_index(
            ['code', 'sse'], drop=False) for i in range(int(api.get_security_count(j) / 1000) + 1)], axis=0) for j in range(2)], axis=0)
        if type_ in ['stock', 'gp']:
            return pd.concat([data[data['sse'] == 'sz'][data.assign(code=data['code'].apply(lambda x: int(x)))['code'] // 10000 <= 30][data.assign(code=data['code'].apply(lambda x: int(x)))['code'] // 100000 != 2][data.assign(code=data['code'].apply(lambda x: int(x)))['code'] // 100000 != 1],
                              data[data['sse'] == 'sh'][data.assign(code=data['code'].apply(lambda x: int(x)))['code'] // 100000 == 6]]).assign(code=data['code'].apply(lambda x: str(x))).assign(name=data['name'].apply(lambda x: str(x)[0:4]))
            #.assign(szm=data['name'].apply(lambda x: ''.join([y[0] for y in lazy_pinyin(x)])))\
            #.assign(quanpin=data['name'].apply(lambda x: ''.join(lazy_pinyin(x))))
        elif type_ in ['index', 'zs']:

            return pd.concat([data[data['sse'] == 'sz'][data.assign(code=data['code'].apply(lambda x: int(x)))['code'] // 1000 >= 399],
                              data[data['sse'] == 'sh'][data.assign(code=data['code'].apply(lambda x: int(x)))['code'] // 1000 == 0]]) \
                .sort_index()\
                .assign(name=data['name'].apply(lambda x: str(x)[0:4]))\
                .assign(code=data['code'].apply(lambda x: str(x)))
            #.assign(szm=data['name'].apply(lambda x: ''.join([y[0] for y in lazy_pinyin(x)])))\
            #.assign(quanpin=data['name'].apply(lambda x: ''.join(lazy_pinyin(x))))
        elif type_ in ['etf', 'ETF']:
            return pd.concat([data[data['sse'] == 'sz'][data.assign(code=data['code'].apply(lambda x: int(x)))['code'] // 10000 == 15],
                              data[data['sse'] == 'sh'][data.assign(code=data['code'].apply(lambda x: int(x)))['code'] // 10000 == 51]]).sort_index().assign(code=data['code'].apply(lambda x: str(x))).assign(name=data['name'].apply(lambda x: str(x)[0:4]))\
                #.assign(szm=data['name'].apply(lambda x: ''.join([y[0] for y in lazy_pinyin(x)])))\
            #.assign(quanpin=data['name'].apply(lambda x: ''.join(lazy_pinyin(x))))

        else:
            return data.assign(code=data['code'].apply(lambda x: str(x))).assign(name=data['name'].apply(lambda x: str(x)[0:4]))
            #.assign(szm=data['name'].apply(lambda x: ''.join([y[0] for y in lazy_pinyin(x)])))\
            #    .assign(quanpin=data['name'].apply(lambda x: ''.join(lazy_pinyin(x))))


def fetch_get_index_day(code, start_date, end_date, level='day', ip=ac.TDX_BEST_IP, port=7709):
    '指数日线'
    api = TdxHq_API()
    if level in ['day', 'd', 'D', 'DAY', 'Day']:
        level = 9
    elif level in ['w', 'W', 'Week', 'week']:
        level = 5
    elif level in ['month', 'M', 'm', 'Month']:
        level = 6
    elif level in ['Q', 'Quarter', 'q']:
        level = 10
    elif level in ['y', 'Y', 'year', 'Year']:
        level = 11

    with api.connect(ip, port):
        if str(code)[0] in ['5', '1']:  # ETF
            data = pd.concat([api.to_df(api.get_security_bars(
                level, 1 if str(code)[0] in ['0', '8', '9', '5'] else 0, code, (25 - i) * 800, 800)) for i in range(26)], axis=0)
        else:
            data = pd.concat([api.to_df(api.get_index_bars(
                level, 1 if str(code)[0] in ['0', '8', '9', '5'] else 0, code, (25 - i) * 800, 800)) for i in range(26)], axis=0)
        data = data.assign(date=data['datetime'].apply(lambda x: str(x[0:10]))).assign(code=str(code))\
            .assign(date_stamp=data['datetime'].apply(lambda x: util_date_stamp(str(x)[0:10])))\
            .set_index('date', drop=False, inplace=False)\
            .drop(['year', 'month', 'day', 'hour',
                   'minute', 'datetime'], axis=1)[start_date:end_date]
        return data.assign(date=data['date'].apply(lambda x: str(x)[0:10]))


def fetch_get_index_min(code, start, end, level='1min', ip=ac.TDX_BEST_IP, port=7709):
    '指数分钟线'
    api = TdxHq_API()
    type_ = ''
    if str(level) in ['5', '5m', '5min', 'five']:
        level, type_ = 0, '5min'
    elif str(level) in ['1', '1m', '1min', 'one']:
        level, type_ = 8, '1min'
    elif str(level) in ['15', '15m', '15min', 'fifteen']:
        level, type_ = 1, '15min'
    elif str(level) in ['30', '30m', '30min', 'half']:
        level, type_ = 2, '30min'
    elif str(level) in ['60', '60m', '60min', '1h']:
        level, type_ = 3, '60min'
    with api.connect(ip, port):
        if str(code)[0] in ['5', '1']:  # ETF
            data = pd.concat([api.to_df(api.get_security_bars(
                level, 1 if str(code)[0] in ['0', '8', '9', '5'] else 0, code, (25 - i) * 800, 800)) for i in range(26)], axis=0)
        else:
            data = pd.concat([api.to_df(api.get_index_bars(
                level, 1 if str(code)[0] in ['0', '8', '9', '5'] else 0, code, (25 - i) * 800, 800)) for i in range(26)], axis=0)
        data = data\
            .assign(datetime=pd.to_datetime(data['datetime']), code=str(code))\
            .drop(['year', 'month', 'day', 'hour', 'minute'], axis=1, inplace=False)\
            .assign(date=data['datetime'].apply(lambda x: str(x)[0:10]))\
            .assign(date_stamp=data['datetime'].apply(lambda x: util_date_stamp(x)))\
            .assign(time_stamp=data['datetime'].apply(lambda x: util_time_stamp(x)))\
            .assign(type=type_).set_index('datetime', drop=False, inplace=False)[start:end]
        # data
        return data.assign(datetime=data['datetime'].apply(lambda x: str(x)))


def __fetch_get_stock_transaction(code, day, retry, api):
    data_ = pd.concat([api.to_df(api.get_history_transaction_data(
        __select_market_code(str(code)), str(code), (20 - i) * 800, 800, util_date_str2int(day))) for i in range(21)], axis=0)

    for _ in range(retry):
        if len(data_) < 2:
            return __fetch_get_stock_transaction(code, day, 0, api)
        else:
            return data_.assign(date=day).assign(datetime=pd.to_datetime(data_['time'].apply(lambda x: str(day) + ' ' + x)))\
                        .assign(code=str(code)).assign(order=range(len(data_.index))).set_index('datetime', drop=False, inplace=False)


def fetch_get_stock_transaction(code, start, end, retry=2, ip=ac.TDX_BEST_IP, port=7709):
    '逐笔成交'
    api = TdxHq_API()

    real_start, real_end = util_get_real_datelist(start, end)
    real_id_range = []
    with api.connect(ip, port):
        data = pd.DataFrame()
        for index_ in range(trade_date_sse.index(real_start), trade_date_sse.index(real_end) + 1):

            try:
                data_ = __fetch_get_stock_transaction(
                    code, trade_date_sse[index_], retry, api)
                if len(data_) < 1:
                    return None
            except:
                log_info('Wrong in Getting %s history transaction data in day %s' % (
                    code, trade_date_sse[index_]))
            else:
                log_info('Successfully Getting %s history transaction data in day %s' % (
                    code, trade_date_sse[index_]))
                data = data.append(data_)

        return data.assign(datetime=data['datetime'].apply(lambda x: str(x)[0:19]))


def fetch_get_stock_xdxr(code, ip=ac.TDX_BEST_IP, port=7709):
    '除权除息'
    api = TdxHq_API()
    market_code = __select_market_code(code)
    with api.connect(ip, port):
        category = {
            '1': '除权除息', '2': '送配股上市', '3': '非流通股上市', '4': '未知股本变动', '5': '股本变化',
            '6': '增发新股', '7': '股份回购', '8': '增发新股上市', '9': '转配股上市', '10': '可转债上市',
            '11': '扩缩股', '12': '非流通股缩股', '13':  '送认购权证', '14': '送认沽权证'}
        data = api.to_df(api.get_xdxr_info(market_code, code))
        if len(data) >= 1:
            data = data\
                .assign(date=pd.to_datetime(data[['year', 'month', 'day']]))\
                .drop(['year', 'month', 'day'], axis=1)\
                .assign(category_meaning=data['category'].apply(lambda x: category[str(x)]))\
                .assign(code=str(code))\
                .rename(index=str, columns={'panhouliutong': 'liquidity_after',
                                            'panqianliutong': 'liquidity_before', 'houzongguben': 'shares_after',
                                            'qianzongguben': 'shares_before'})\
                .set_index('date', drop=False, inplace=False)
            return data.assign(date=data['date'].apply(lambda x: str(x)[0:10]))
        else:
            return None

def fetch_get_stock_info(code, ip=ac.TDX_BEST_IP, port=7709):
    '除权除息'
    api = TdxHq_API()
    market_code = __select_market_code(code)
    with api.connect(ip, port):
        return api.to_df(api.get_finance_info(market_code, code))

def fetch_get_stock_block(ip=ac.TDX_BEST_IP, port=7709):
    '板块数据'
    api = TdxHq_API()
    with api.connect(ip, port):

        data = pd.concat([api.to_df(api.get_and_parse_block_info("block_gn.dat")).assign(type='gn'),
                          api.to_df(api.get_and_parse_block_info(
                              "block.dat")).assign(type='yb'),
                          api.to_df(api.get_and_parse_block_info(
                              "block_zs.dat")).assign(type='zs'),
                          api.to_df(api.get_and_parse_block_info("block_fg.dat")).assign(type='fg')])

        if len(data) > 10:
            return data.assign(source='tdx').drop(['block_type', 'code_index'], axis=1).set_index('code', drop=False, inplace=False).drop_duplicates()
        else:
            log_info('Wrong with fetch block ')

# if __name__ == '__main__':
#     # print(fetch_get_stock_day('000001','2017-07-03','2017-07-10'))
#     # print(fetch_get_stock_day('000001', '2013-07-01', '2013-07-09'))
#     print(fetch_get_stock_realtime('000001'))
#     #print(fetch_get_index_day('000001', '2017-01-01', '2017-07-01'))
#     # print(fetch_get_stock_transaction('000001', '2017-07-03', '2017-07-10'))
#
#     print(fetch_get_stock_info('600116'))
