import unittest
from ElectronicCommerce.test_case.models import function
from ElectronicCommerce.test_case.models import jduint
from ElectronicCommerce.test_case.page_object.thumbnailPage import Thumbnail


class PriceSortTest(jduint.JdTest):
    """商品按价格排序测试"""
    data_list = function.read_csv_file('thumbnail_sort_test_data.csv')

    def price_sort_verify(self, query, top):
        Thumbnail(self.driver).thumbnail_price_sort(query, top)

    def price_desc_verify(self, query, top):
        Thumbnail(self.driver).thumbnail_price_desc(query, top)

    def rating_sort_verify(self, query, top):
        Thumbnail(self.driver).thumbnail_rating_sort(query, top)

    def test_price_sort1(self):
        """价格由底到高测试"""
        for data in self.data_list:
            self.price_sort_verify(data[0], data[1])
            po = Thumbnail(self.driver)
            self.assertEqual(30, po.first_load_product_number())
            print("首次加载页面展示30个产品图片,(需求变更为60)")
            self.assertTrue(po.is_sorted_prices_list())
            function.insert_img(self.driver, "price_sort_page.jpg")

    def test_price_sort2(self):
        """价格由高到底测试"""
        for data in self.data_list:
            self.price_desc_verify(data[0], data[1])
            po = Thumbnail(self.driver)
            self.assertTrue(po.is_desc_prices_list())
            function.insert_img(self.driver, data[0]+"price_desc_page.jpg")

    def test_rating_sort(self):
        """评论数由高到底测试"""
        for data in self.data_list:
            self.rating_sort_verify(data[0], data[1])
            po = Thumbnail(self.driver)
            self.assertTrue(po.is_sort_ratings_list())
            function.insert_img(self.driver, data[0]+"rating_sort_page.jpg")

if __name__ == "__main__":
    unittest.main()
