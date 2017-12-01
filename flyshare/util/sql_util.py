# coding:utf-8

import pymongo
import re
import datetime
import time
import motor
import asyncio
from motor import motor_asyncio
from motor.motor_asyncio import (AsyncIOMotorCollection, AsyncIOMotorClient, AsyncIOMotorDatabase,
                                 AsyncIOMotorCommandCursor)
from .logs import log_info


def util_sql_mongo_setting(ip='127.0.0.1', port=27017):
    sql_mongo_client = pymongo.MongoClient(ip, int(port))
    log_info('ip:{},port:{}'.format(str(ip), str(port)))
    return sql_mongo_client

# async


def util_sql_async_mongo_setting(ip='127.0.0.1', port=27017):
    sql_async_mongo_client = AsyncIOMotorClient(ip, int(port))
    log_info('ip:{},port{}'.format(str(ip), str(port)))
    return sql_async_mongo_client


if __name__=='__main__':
    # test async_mongo
    client=util_sql_async_mongo_setting().quantaxis.stock_day
    print(client)