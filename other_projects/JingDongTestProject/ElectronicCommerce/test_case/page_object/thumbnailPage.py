from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from ElectronicCommerce.test_case.models import function
from ElectronicCommerce.test_case.page_object.homePage import HomePage
from .base import Page
from time import sleep


class Thumbnail(Page):

    url = 'https://www.jd.com/'

    # def def_thumbnail_page(self, query):
        # self.url = "https://search.jd.com/Search?keyword=" + query + "&enc=utf-8&wq=" + query
        # print(self.url)
        # https://search.jd.com/Search?keyword=iphone7&enc=utf-8&wq=iphone7

    def jingdong_thumbnail(self, query):
        HomePage(self.driver).jingdong_search(query)

    price_sort_loc = ((By.CLASS_NAME, "fs-tit"),4)
    rating_sort_loc = ((By.CLASS_NAME, "fs-tit"),2)
    product_image_link_loc = (By.CSS_SELECTOR, "ul.gl-warp.clearfix div.p-img a")
    product_image_loc = (By.CSS_SELECTOR, "ul.gl-warp.clearfix div.p-img a img")

    def click_image(self, item):
        function.highlight_element_by_class(self.driver, "p-img")
        self.find_elements(*self.product_image_link_loc)[item].click()

    def thumbnail_image_src(self, item):
        return self.find_elements(*self.product_image_loc)[item].get_attribute("src")

    def window_scroll_to(self, y):
        js = "window.scrollTo(0," + y + ");"
        # "document.documentElement.scrollTop=450"
        self.script(js)
        sleep(10)

    def price_sort(self):
        self.find_elements(*self.price_sort_loc[0])[self.price_sort_loc[1]].click()
        # function.highlight_element_by_class(self.driver, "curr")
        sleep(10)

    def rating_sort(self):
        self.find_elements(*self.rating_sort_loc[0])[self.rating_sort_loc[1]].click()
        # function.highlight_element_by_class(self.driver, "curr")
        sleep(10)

    def thumbnail_price_sort(self, query, top):
        self.jingdong_thumbnail(query)
        self.window_scroll_to(top)
        self.price_sort()

    def thumbnail_price_desc(self, query, top):
        self.jingdong_thumbnail(query)
        self.window_scroll_to(top)
        self.price_sort()
        self.price_sort()

    def thumbnail_rating_sort(self, query, top):
        self.jingdong_thumbnail(query)
        self.window_scroll_to(top)
        self.rating_sort()


    def navigate_to_product_page(self, query, top, item):
        self.jingdong_thumbnail(query)
        self.window_scroll_to(top)
        self.click_image(item)
        sleep(10)
        function.switch_windows(self.driver)

    all_product_prices = (By.CSS_SELECTOR, "ul.gl-warp.clearfix strong > i")
    all_product_ratings = (By.CSS_SELECTOR, "ul.gl-warp.clearfix div.p-commit > strong > a")

    def is_sorted_prices_list(self):
        prices_list = self.find_elements(*self.all_product_prices)
        for i in range(0, len(prices_list)-1):
            j = i + 1
            if prices_list[i].text <= prices_list[j].text:
                print(str(i+1) + ". " + prices_list[i].text)
                continue
            else:
                return False
        return True

    def is_sort_ratings_list(self):
        rating_list = self.find_elements(*self.all_product_ratings)
        for i in range(0, len(rating_list)-1):
            i_rating_list = rating_list[i].text[:-1]
            j_rating_list = rating_list[i+1].text[:-1]
            if i_rating_list[-1] == '万':
                i_rating_list = int(float(i_rating_list[:-1]) * 10000)
            else:
                i_rating_list = int(i_rating_list)
            if j_rating_list[-1] == '万':
                j_rating_list = int(float(j_rating_list[:-1]) * 10000)
            else:
                j_rating_list = int(j_rating_list)
            if i_rating_list >= j_rating_list:
                print(str(i+1) + ". " + str(i_rating_list) + "+")
                continue
            else:
                return False
        return True

    def is_desc_prices_list(self):
        prices_list = self.find_elements(*self.all_product_prices)
        for i in range(0, 10):
            j = i + 1
            int_price = float(prices_list[i].text)
            int_price_next = float(prices_list[j].text)
            if int_price >= int_price_next:
                print(str(j) + ". " + prices_list[i].text)
                continue
            else:
                return False
        return True

    def first_load_product_number(self):
        return len(self.find_elements(*self.all_product_prices))
