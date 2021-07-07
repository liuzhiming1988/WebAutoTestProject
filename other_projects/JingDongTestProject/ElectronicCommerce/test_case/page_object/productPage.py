from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from ElectronicCommerce.test_case.models import function
from ElectronicCommerce.test_case.page_object.thumbnailPage import Thumbnail
from ElectronicCommerce.test_case.page_object.base import Page
from time import sleep
from ElectronicCommerce.test_case.page_object.homePage import HomePage


class Product(Page):

    url = 'https://www.jd.com/'

    def jingdong_product(self, query, top, item):
        HomePage(self.driver).jingdong_search(query)
        Thumbnail(self.driver).navigate_to_product_page(self, query, top, item)
        function.switch_windows(self.driver)

    target_page_image_loc = (By.CSS_SELECTOR, "div#spec-n1.jqzoom > img")
    # target_page_image_loc = (By.CSS_SELECTOR, "ul.gl-warp.clearfix div.p-img a img")

    def get_image_n1_src(self):
        # print(self.find_element(*self.target_page_image_loc).get_attribute("src"))
        function.highlight_element_by_id(self.driver,"spec-n1")
        # function.highlight_element(self.driver, self.find_element(*self.target_page_image_loc))
        return self.find_element(*self.target_page_image_loc).get_attribute("src")
