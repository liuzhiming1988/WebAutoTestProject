
from selenium import webdriver
import pytest
import time
import os
from public.config import ConfigRead
from public.common import *
from selenium.webdriver.common.by import By
import inspect



class MyClass:
    def function_one(self):
        print("{0}.{1}".format(self.__class__.__name__, get_current_function_name()))

    def tte(self):
        pass


def f():
    a = inspect.stack()[1][3]
    return inspect.stack()[1][3]


if __name__ == '__main__':
    FIND_LIST = {
        # selenium
        'css': 'By.CSS_SELECTOR',
        'id_': By.ID,
        'name': By.NAME,
        'xpath': By.XPATH,
        'link_text': By.LINK_TEXT,
        'class_name': By.CLASS_NAME,
    }
    a = FIND_LIST['css']
    print(type(a))
    print(type(By.ID))
    print(f())

