#!/usr/bin/env python
# coding: utf-8




class Person:
    def __init__(self,firstname,lastname,username,password):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.password = password
        
    # FirstName Getter
    @property
    def firstname(self):
        return self._firstname

    # FirstName Setter
    @firstname.setter
    def firstname(self,name):
        self._firstname = name

    # LastName Getter
    @property
    def lastname(self):
        return self._lastname

    # LastName Setter
    @lastname.setter
    def lastname(self,name):
        self._lastname = name

    # Username Getter
    @property
    def username(self):
        return self._username
        
    # Username Setter    
    @username.setter   
    def username(self,user):      
        self._username = user

    # Password Getter
    @property
    def password(self):
        return self._password
        
    # Password Setter
    @password.setter
    def password(self,passcode):  
        self._password = passcode

