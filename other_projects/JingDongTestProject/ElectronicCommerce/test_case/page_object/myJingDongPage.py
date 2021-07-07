from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from ElectronicCommerce.test_case.models import function
from ElectronicCommerce.test_case.page_object.homePage import HomePage
from .base import Page
from time import sleep


class MyProducts(Page):

    url = 'http://127.0.0.1:8000/index/'

    def open_myjd(self):
        self.open()
        sleep(10)

    def window_scroll_to(self, y):
        js = "window.scrollTo(0," + y + ");"
        # "document.documentElement.scrollTop=450"
        self.script(js)
        sleep(10)

    all_product_prices = (By.CSS_SELECTOR, "ul.gl-warp.clearfix strong > i")

    def load_product_number(self):
        return len(self.find_elements(*self.all_product_prices))
