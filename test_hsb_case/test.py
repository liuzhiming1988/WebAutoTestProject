
from selenium import webdriver
import pytest
import time
import os
from public.config import ConfigRead
from public.common import *



class MyClass:
    def function_one(self):
        print("{0}.{1}".format(self.__class__.__name__, get_current_function_name()))

    def tte(self):
        pass

if __name__ == '__main__':

    mc = MyClass().function_one()
    print(get_current_function_name())
