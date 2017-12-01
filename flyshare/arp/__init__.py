# coding:utf-8
#

from .Account import Account
from .QARisk import Risk
from .Portfolio import Portfolio

from flyshare.arp.QARisk import (risk_account_freeCash_currentAssets,
                                 risk_account_freeCash_frozenAssets,
                                 risk_account_freeCash_initAssets, risk_eva_account)


class ARP():
    def __init__(self):
        pass

    def ARP_A2R(self, Account, Risk):

        pass

    def ARP_R2P(self, Risk, Portfolio):
        pass

    def ARP_P2R(self, Risk, Portfolio):
        pass

    def ARP_R2A(self, Account, Risk):
        pass
