#!/usr/bin/env python
# coding: utf-8




class Funds:

    instance_count = 0
    
    def __init__(self,fund,amount=0):
        self.fund = fund 
        self.amount = amount

    @classmethod
    def get_instance_count(cls):
        return cls.instance_count
        
    # Fund Getter
    @property
    def fund(self):
        return self._fund

    # Fund Setter
    @fund.setter
    def fund(self,fund):
        self._fund = fund

    # Amount Getter
    @property
    def amount(self):
        return self._amount

    # Amount Setter
    @amount.setter
    def amount(self,amount):
        self._amount = amount




