#!/usr/bin/env python
# coding: utf-8


# NOTE: When the user inputs a cost amount, it's stored in memory as a string. When doing arithmetic on theses amounts, keep in mind
#       of that! 




class Expense:
    
    instance_count = 0
    
    def __init__(self,expense,cost=0): 
        self.expense = expense
        self.cost = cost 

    @classmethod
    def get_instance_count(cls):
        return cls.instance_count

    # Expense Getter
    @property
    def expense(self):
        return self._expense

    # Expense Setter
    @expense.setter
    def expense(self,expense):
        self._expense = expense

    # Cost Getter
    @property
    def cost(self):
        return self._cost

    # Cost Setter
    @cost.setter
    def cost(self,cost):
        self._cost = cost





