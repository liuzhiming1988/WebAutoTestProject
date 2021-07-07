import csv
import unittest
from ElectronicCommerce.test_case.models import function
from ElectronicCommerce.test_case.models import jduint
from ElectronicCommerce.test_case.page_object.productPage import Product
from ElectronicCommerce.test_case.page_object.thumbnailPage import Thumbnail


class ProductIntegrateTest(jduint.JdTest):
    """商品一览页面和商品详情页面的集成测试"""

    csv_file_path_test_data = 'thumbnail_image_test_data.csv'
    data_list = function.read_csv_file(csv_file_path_test_data)

    def image_navigate_verify(self, query, top, item):
        Thumbnail(self.driver).navigate_to_product_page(query, top, item)

    def thumbnail_image_src_verify(self, item):
        return Thumbnail(self.driver).thumbnail_image_src(item)

    def test_image_navigate1(self):
        """商品图片对比测试"""
        for data in self.data_list:
            query = data[0]
            top = data[1]
            item = int(data[2])
            Thumbnail(self.driver).jingdong_thumbnail(query)
            t_src = self.thumbnail_image_src_verify(item)
            print("商品一览页面的链接图片：" + t_src)
            self.image_navigate_verify(query, top, item)
            p_src = Product(self.driver).get_image_n1_src()
            print("产品详情页的展示图片：" + p_src)
            print(t_src[-1:30])
            self.assertTrue(t_src[-1:30] == p_src[-1:30])
            function.insert_img(self.driver, query + "_image_navigate_test_result.jpg")


if __name__ == "__main__":
    unittest.main()
