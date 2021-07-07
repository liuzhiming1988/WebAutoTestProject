from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from ElectronicCommerce.test_case.models import function
from .base import Page
from time import sleep


class HomePage(Page):

    url = 'https://www.jd.com/'

    homepage_input_textbox_loc = (By.ID, "key")
    homepage_search_button_loc = (By.CSS_SELECTOR, "button.button")

    def input_query(self, query="abc"):
        self.find_element(*self.homepage_input_textbox_loc).clear()
        self.find_element(*self.homepage_input_textbox_loc).send_keys(query)

    def click_search_button(self):
        self.find_element(*self.homepage_search_button_loc).click()
        sleep(1)

    def jingdong_search(self, query):
        self.open()
        self.input_query(query)
        self.click_search_button()
        sleep(5)

    search_result_loc = (By.CLASS_NAME, "search-key")

    def search_result(self):
        function.highlight_element_by_class(self.driver, "search-key")
        return self.find_element(*self.search_result_loc).text

    check_error_loc = (By.CLASS_NAME, "check-error")

    def check_error(self):
        element_check_error = self.find_element(*self.check_error_loc)
        function.highlight_element(self.driver, element_check_error)
        return element_check_error.text

    no_search_result_loc = (By.CLASS_NAME, "ns-content")

    def no_search_result(self):
        function.highlight_element_by_class(self.driver, "ns-content")
        return self.find_element(*self.no_search_result_loc).text

