
from selenium import webdriver
import pytest
import time


def choice_driver(driver_name="chrome"):
    if driver_name == "chrome":
        driver = webdriver.Chrome()
        return driver


choice_driver()

time.sleep(3)
