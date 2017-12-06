#coding=utf-8
'''
Created on 2017/10/27
@author: Rubing Duan
'''
import unittest
import flyshare.stock.trading as fd
import flyshare.ApiConfig as ac
import flyshare.util as util

class Test(unittest.TestCase):

    def set_data(self):
        self.code = '600848'
        self.start = '2015-01-03'
        self.end = '2015-04-07'
        self.year = 2014
        self.quarter = 4
        
    def test_get_hist_data(self):
        self.set_data()
        print(fd.get_hist_data(self.code, self.start))

    def test_set_api_key(self):
        ac.api_key = 'default key'

    def test_util_log(self):
        util.util_log_critical("critical")

    def test_ping(self):
        print(util.ping("www.google.com"))



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()