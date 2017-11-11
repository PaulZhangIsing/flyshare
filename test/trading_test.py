# -*- coding:utf-8 -*- 
'''
Created on 2017/10/27
@author: Rubing Duan
'''
import unittest
import flyshare.stock.trading as fd

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

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()