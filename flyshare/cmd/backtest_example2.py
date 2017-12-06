# coding=utf-8

import flyshare as fs
from flyshare import Backtest as B
import numpy as np
from datetime import datetime
"""
写在前面:
===============flyshare BACKTEST STOCK_DAY中的变量
常量:
B.backtest_type 回测类型 day/1min/5min/15min/30min/60min/index_day/index_1min/index_5min/index_15min/index_30min/index_60min/
B.account.message  当前账户消息
B.account.cash  当前可用资金
B.account.hold  当前账户持仓
B.account.history  当前账户的历史交易记录
B.account.assets 当前账户总资产
B.account.detail 当前账户的交易对账单
B.account.init_assest 账户的最初资金
B.strategy_gap 前推日期
B.strategy_name 策略名称

B.strategy_stock_list 回测初始化的时候  输入的一个回测标的
B.strategy_start_date 回测的开始时间
B.strategy_end_date  回测的结束时间

B.setting.setting_user_name = str('admin') #回测账户
B.setting.setting_user_password = str('admin') #回测密码

B.today  在策略里面代表策略执行时的日期
B.now  在策略里面代表策略执行时的时间
B.benchmark_code  策略业绩评价的对照行情
B.benchmark_type  对照行情是股票还是指数


B.backtest_print_log = True  # 是否在屏幕上输出结果

函数:
获取市场(基于gap)行情:
B.backtest_get_market_data(B,code,B.today)
获取单个bar
B.backtest_get_market_data_bar(B,code,B.today/B.now)

拿到开高收低量
Open,High,Low,Close,Volume=B.backtest_get_OHLCV(B,B.backtest_get_market_data(B,item,B.today))

获取市场自定义时间段行情:
fs.fetch_stock_day(code,start,end,model)

一键平仓:
B.backtest_sell_all(B)

报单:
B.backtest_send_order(B, code,amount,towards,order: dict)

order有三种方式:
1.限价成交 order['bid_model']=0或者l,L
  注意: 限价成交需要给出价格:
  order['price']=xxxx

2.市价成交 order['bid_model']=1或者m,M,market,Market  [其实是以bar的开盘价成交]
3.严格成交模式 order['bid_model']=2或者s,S
    及 买入按bar的最高价成交 卖出按bar的最低价成交
3.收盘价成交模式 order['bid_model']=3或者c,C

#查询当前一只股票的持仓量
B.backtest_hold_amount(B,code)
#查询当前一只股票的可卖数量
B.backtest_sell_available(B,code)
#查询当前一只股票的持仓平均成本
B.backtest_hold_price(B,code)

近期新增:
B.backtest_get_market_data_panel(B,time,type_)

B.backtest_get_block(B,block_list)  # 获取股票的板块代码  输入是一个板块的list ['钢铁','昨日涨停']  输出是不重复的股票列表
"""


@B.backtest_init
def init():
    # 回测的类别
    # day/1min/5min/15min/30min/60min/index_day/index_1min/index_5min/index_15min/index_30min/index_60min/
    B.backtest_type = 'day'
    # B.backtest_type='5min' # 日线回测
    # 策略的名称
    B.strategy_name = 'test_daily'
    # 数据库位置
    B.setting.util_sql_mongo_ip = '127.0.0.1'  # 回测数据库
    B.setting.setting_user_name = str('admin')  # 回测账户
    B.setting.setting_user_password = str('admin')  # 回测密码
    B.topic_name = 'EXAMPLE'  #回测的主题
    B.stratey_version = 'V1'  #回测的版本号
    
    B.account.init_assest = 2000000  # 初始资金

    # benchmark
    B.benchmark_code = '000300'
    # benchmark 可以是个股，也可以是指数
    B.benchmark_type = 'index'
    # 手续费系数
    B.commission_fee_coeff = 0.0015  # 千五的手续费(单向)

    B.strategy_gap = 30  # 在取数据的时候 向前取多少个bar(会按回测的时间动态移动)
    B.strategy_stock_list = B.backtest_get_block(B,['MSCI成份'])

    B.strategy_start_date = '2017-06-01 10:30:00'  # 回测开始日期
    B.strategy_end_date = '2017-10-01'  # 回测结束日期
    B.backtest_print_log = False  # 是否在屏幕上输出结果


@B.before_backtest
def before_backtest():
    global start_time
    start_time = datetime.now()
    global risk_position


@B.load_strategy
def strategy():
    global risk_position  # 在这个地方global变量 可以拿到before_backtest里面的东西
    fs.util_log_info(B.account.sell_available)
    fs.util_log_info('LEFT Cash: %s' % B.account.cash_available)
    # B.backtest_get_market_data_panel(B,time,type_) 面板数据
    # time 如果不填 就是默认的B.now/B.today
    # type_ 如果不填 默认是 'lt' 如果需要当日的数据 'lte'
    each_capital = int(B.account.cash_available/(len(B.strategy_stock_list)-len(B.account.sell_available)))

    for item in B.strategy_stock_list:
        if B.backtest_find_bar(B, item, B.today) is not None: #今日开盘-能取到数据
            market_data = B.backtest_get_market_data(B, item, B.today,type_='lte')  #type_='lte' 才能取到今日
            Open, High, Low, Close, Volume = B.backtest_get_OHLCV(B,market_data)

            MA = market_data.add_func(fs.indicator_MA,10)
            MA_s = MA[0][-1]
            if not np.isnan(MA_s):
                if B.backtest_hold_amount(B, item) == 0:  # 如果不持仓
                    if Close[-1] >= MA_s:
                        B.backtest_send_order(B, code=item, amount=int(each_capital/Close[-1]/100)*100,towards= 1,order_type= {'bid_model': 'c'})
                elif B.backtest_sell_available(B, item) > 0:  # 如果可卖数量大于0
                    hold_price = B.backtest_hold_price(B, item)

                    if Close[-1] <= MA_s:
                        B.backtest_send_order(B, code=item, amount=B.backtest_sell_available(B,item), towards=-1, order_type={'bid_model': 'c'})

        else:
            fs.util_log_info('{} HAS NO DATA IN {}'.format(item, B.today))  # 如果是分钟回测 用B.now
    pcg_total = len(fs.util_get_trade_range(B.strategy_start_date,B.strategy_end_date))
    pcg_now = len(fs.util_get_trade_range(B.strategy_start_date,B.today))
    fs.util_log_info('Now Completed {}%'.format(int(100*pcg_now/pcg_total)))



# #查询当前一只股票的持仓量
# B.backtest_hold_amount(B,code)
# #查询当前一只股票的可卖数量
# B.backtest_sell_available(B,code)
# #查询当前一只股票的持仓平均成本
# B.backtest_hold_price(B,code)
@B.end_backtest
def after_backtest():
    global start_time
    end_time = datetime.now()
    cost_time = (end_time - start_time).total_seconds()
    fs.util_log_info('耗费时间 {} {}'.format(cost_time,'seconds'))

    B.if_save_to_csv=True
    B.if_save_to_mongo=True