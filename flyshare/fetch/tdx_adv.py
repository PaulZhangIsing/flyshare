# coding:utf-8

import datetime
import queue
from concurrent.futures import ThreadPoolExecutor
from threading import Event, Thread, Timer

import pandas as pd
from pytdx.hq import TdxHq_API
from flyshare.util.mongodbsetting import info_ip_list, MongoDBSetting as ms
from flyshare.util.transform import util_to_json_from_pandas

"""
准备做一个多连接的连接池执行器Executor

当持续获取数据/批量数据的时候,可以减小服务器的压力,并且可以更快的进行并行处理

"""


class Tdx_Executor():
    def __init__(self, thread_num=2, *args, **kwargs):
        self.thread_num = thread_num
        self._queue = queue.Queue(maxsize=200)
        self.api_no_connection = TdxHq_API()
        self._api_worker = Thread(
            target=self.api_worker, args=(), name='API Worker')
        self._api_worker.start()

        self.executor = ThreadPoolExecutor(self.thread_num)

    def __getattr__(self, item):
        try:
            api = self.get_available()
            func = api.__getattribute__(item)

            def wrapper(*args, **kwargs):
                res = self.executor.submit(func, *args, **kwargs)
                self._queue.put(api)
                return res
            return wrapper
        except:
            return self.__getattr__(item)

    def _queue_clean(self):
        self._queue = queue.Queue(maxsize=200)

    def _test_speed(self, ip, port=7709):

        api = TdxHq_API(raise_exception=True, auto_retry=False)
        #api.need_setup = False
        _time = datetime.datetime.now()
        try:
            with api.connect(ip, port, time_out=0.05):
                if len(api.get_security_list(0, 1)) > 800:
                    return (datetime.datetime.now() - _time).total_seconds()
                else:
                    return datetime.timedelta(9, 9, 0).total_seconds()
        except Exception as e:
            #print('BAD IP {}, DEL for Reason{}'.format(ip,e))
            return datetime.timedelta(9, 9, 0).total_seconds()

    def get_market(self, code):
        code = str(code)
        if code[0] in ['5', '6', '9'] or code[:3] in ["009", "126", "110", "201", "202", "203", "204"]:
            return 1
        return 0

    def get_level(self, level):
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
            level = 0
        elif str(level) in ['1', '1m', '1min', 'one']:
            level = 8
        elif str(level) in ['15', '15m', '15min', 'fifteen']:
            level = 1
        elif str(level) in ['30', '30m', '30min', 'half']:
            level = 2
        elif str(level) in ['60', '60m', '60min', '1h']:
            level = 3

        return level

    @property
    def ipsize(self):
        return len(self._queue.qsize())

    @property
    def api(self):
        return self.get_available()

    def get_available(self):

        if self._queue.empty() is False:
            return self._queue.get_nowait()
        else:
            Timer(0, self.api_worker).start()
            return self._queue.get()

    def api_worker(self):
        data = []
        if self._queue.qsize() < 80:
            for item in info_ip_list:
                _sec = self._test_speed(item)
                if _sec < 0.1:
                    self._queue.put(
                        TdxHq_API(heartbeat=False).connect(ip=item, time_out=0.05))
        else:
            self._queue_clean()
            Timer(0, self.api_worker).start()
        Timer(300, self.api_worker).start()

    def _singal_job(self, context, id_, time_out=0.5):
        try:
            _api = self.get_available()

            __data = context.append(self.api_no_connection.to_df(_api.get_security_quotes(
                [(self._select_market_code(x), x) for x in code[80 * id_:80 * (id_ + 1)]])))
            __data['datetime'] = datetime.datetime.now()
            self._queue.put(_api)  # 加入注销
            return __data
        except:
            return self.singal_job(context, id_)

    def get_realtime(self, code):
        context = pd.DataFrame()

        code = [code] if type(code) is str else code
        try:
            for id_ in range(int(len(code) / 80) + 1):
                context = self._singal_job(context, id_)

            data = context[['datetime', 'last_close', 'code', 'open', 'high', 'low', 'price', 'cur_vol',
                            's_vol', 'b_vol', 'vol', 'ask1', 'ask_vol1', 'bid1', 'bid_vol1', 'ask2', 'ask_vol2',
                            'bid2', 'bid_vol2', 'ask3', 'ask_vol3', 'bid3', 'bid_vol3', 'ask4',
                            'ask_vol4', 'bid4', 'bid_vol4', 'ask5', 'ask_vol5', 'bid5', 'bid_vol5']]
            return data.set_index('code', drop=False, inplace=False)
        except:
            return None

    def get_realtime_concurrent(self, code):
        code = [code] if type(code) is str else code

        try:
            # for id_ in range(int(len(code) / 80) + 1):
            data = {self.get_security_quotes([(self.get_market(
                x), x) for x in code[80 * pos:80 * (pos + 1)]]) for pos in range(int(len(code) / 80) + 1)}
            return (pd.concat([self.api_no_connection.to_df(i.result()) for i in data]), datetime.datetime.now())
        except:
            pass

    def get_security_bar_concurrent(self, code, _type, lens):
        #code = [code] if type(code) is str else code
        try:
            data = {[self.get_security_bars(self.get_level(_type), self.get_market(
                str(code)), str(code), (25 - i) * 800, 800) for i in range(int(lens / 800) + 1)]}
            print([i.result() for i in data])

        except:
            raise Exception

    def _get_security_bars(self, context, code, _type, lens):
        try:
            _api = self.get_available()
            for i in range(1, int(lens / 800) + 2):
                context.extend(_api.get_security_bars(self.get_level(
                    _type), self.get_market(str(code)), str(code), (i - 1) * 800, 800))
                # print(context)
            self._queue.put(_api)
            return context
        except Exception as e:
            # print(e)
            return self._get_security_bars(context, code, _type, lens)

    def get_security_bars(self, code, _type, lens):
        code = [code] if type(code) is str else code
        context = []
        try:
            for item in code:
                context = self._get_security_bars(context, item, _type, lens)
            return context
        except Exception as e:
            raise e

    def save_mongo(self, data, client=ms.client.flyshare.realtime):
        client.insert_many(util_to_json_from_pandas(data))


if __name__ == '__main__':
    import time
    _time1 = datetime.datetime.now()
    from flyshare.fetch.query_advance import fetch_stock_block_adv
    code = fetch_stock_block_adv().code
    print(len(code))
    x = Tdx_Executor()
    print(x._queue.qsize())
    print(x.get_available())
    #data = x.get_security_bars(code[0], '15min', 20)
    # print(data)
    # for i in range(5):
    #     print(x.get_realtime_concurrent(code))

    for i in range(100000):
        _time = datetime.datetime.now()
        #data = x.get_realtime(code)
        data = x.get_realtime_concurrent(code)

        data[0]['datetime'] = data[1]
        x.save_mongo(data[0])
        # print(code[0])
        #data = x.get_security_bars(code, '15min', 20)
        # if data is not None:
        print(len(data[0]))
        # print(data)
        print('Time {}'.format((datetime.datetime.now() - _time).total_seconds()))
        time.sleep(1)
        print('Connection Pool NOW LEFT {} Available IP'.format(x._queue.qsize()))
        print('Program Last Time {}'.format(
            (datetime.datetime.now() - _time1).total_seconds()))
        # print(threading.enumerate())
# #
