
from flyshare.saveupdate import save_tdx as stdx
from flyshare.saveupdate import save_tdx_file as tdx_file
from flyshare.saveupdate import save_tushare as sts
from flyshare.saveupdate import save_wind as sw
from flyshare.saveupdate import update_tdx as utdx
from flyshare.saveupdate import update_tushare as uts
from flyshare.saveupdate import update_wind as uw
from flyshare.util import Setting


def SU_save_trade_date(engine, client=Setting.client):
    engine = select_save_engine(engine)
    engine.SU_save_trade_date(client)


def SU_save_stock_info(engine, client=Setting.client):
    engine = select_save_engine(engine)
    engine.SU_save_stock_info(client)


def SU_save_stock_list(engine, client=Setting.client):
    engine = select_save_engine(engine)
    engine.SU_save_stock_list(client)


def SU_save_stock_day(engine, client=Setting.client):
    engine = select_save_engine(engine)
    engine.SU_save_stock_day(client)


def SU_save_stock_min(engine, client=Setting.client):
    engine = select_save_engine(engine)
    engine.SU_save_stock_min(client)


def SU_save_index_day(engine, client=Setting.client):
    engine = select_save_engine(engine)
    engine.SU_save_index_day(client)


def SU_save_index_min(engine, client=Setting.client):
    engine = select_save_engine(engine)
    engine.SU_save_index_min(client)


def SU_save_etf_day(engine, client=Setting.client):
    engine = select_save_engine(engine)
    engine.SU_save_etf_day(client)


def SU_save_etf_min(engine, client=Setting.client):
    engine = select_save_engine(engine)
    engine.SU_save_etf_min(client)


def SU_save_stock_xdxr(engine, client=Setting.client):
    engine = select_save_engine(engine)
    engine.SU_save_stock_xdxr(client)

def SU_save_stock_block(engine, client=Setting.client):
    engine = select_save_engine(engine)
    engine.SU_save_stock_block(client)
def SU_save_stock_day_init(startDate, engine, client=Setting.client):
    engine = select_save_engine(engine)
    engine.SU_save_stock_day_init(startDate, client)


def SU_update_stock_day(engine, client=Setting.client):
    engine = select_update_engine(engine)
    engine.SU_update_stock_day(client)


def SU_update_stock_xdxr(engine, client=Setting.client):
    engine = select_update_engine(engine)
    engine.SU_update_stock_xdxr(client)


def SU_update_stock_min(engine, client=Setting.client):
    engine = select_update_engine(engine)
    engine.SU_update_stock_min(client)



def SU_update_index_day(engine, client=Setting.client):
    engine = select_update_engine(engine)
    engine.SU_update_index_day(client)


def SU_update_index_min(engine, client=Setting.client):
    engine = select_update_engine(engine)
    engine.SU_update_index_min(client)


def select_save_engine(engine):
    if engine in ['wind', 'Wind', 'WIND']:
        return sw
    elif engine in ['tushare', 'ts', 'Tushare']:
        return sts
    elif engine in ['tdx']:
        return stdx


def select_update_engine(engine):
    if engine in ['wind', 'Wind', 'WIND']:
        return uw
    elif engine in ['tushare', 'ts', 'Tushare']:
        return uts
    elif engine in ['tdx']:
        return utdx


def SU_save_stock_min_5(file_dir, client=Setting.client):
    return tdx_file.save_tdx_to_mongo(file_dir, client)
