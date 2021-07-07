import unittest
from ElectronicCommerce.test_case.models import function
from ElectronicCommerce.test_case.models import jduint
from ElectronicCommerce.test_case.page_object.homePage import HomePage


class SearchTest(jduint.JdTest):
    """主页搜索功能测试"""

    csv_file_path_test_data = 'search_page_test_data.csv'


    def search_result_verify(self, query="abc"):
        HomePage(self.driver).jingdong_search(query)


    def test_search1(self):
        """单字节搜索测试"""
        data_list = function.read_csv_file(self.csv_file_path_test_data)
        for data in data_list:
            if data[0] == "SingleByte":
                query = data[1]
                self.search_result_verify(query)
                po = HomePage(self.driver)
                self.assertEqual("\"" + query + "\"", po.search_result())
                function.insert_img(self.driver, "Chinese_search_" + query + ".jpg")

    def test_search2(self):
        """双字节搜索测试"""
        data_list = function.read_csv_file(self.csv_file_path_test_data)
        for data in data_list:
            if data[0] == "DoubleByte":
                query = data[1]
                self.search_result_verify(query)
                po = HomePage(self.driver)
                self.assertEqual(po.search_result(), "\"" + query + "\"")
                function.insert_img(self.driver, "Chinese_search_" + query + ".jpg")

    def test_search3(self):
        """拼写修正测试"""
        data_list = function.read_csv_file(self.csv_file_path_test_data)
        for data in data_list:
            if data[0] == "Correct":
                query = data[1]
                self.search_result_verify(query)
                po = HomePage(self.driver)
                print(po.check_error())
                self.assertIn("我们为您显示", po.check_error())
                function.insert_img(self.driver, "Chinese_search_" + query + ".jpg")

    def test_search4(self):
        """拼写建议测试"""
        data_list = function.read_csv_file(self.csv_file_path_test_data)
        for data in data_list:
            if data[0] == "Suggestion":
                query = data[1]
                self.search_result_verify(query)
                po = HomePage(self.driver)
                self.assertEqual("\"" + query + "\"", po.search_result())
                # self.assertIn("您是不是想找", po.check_error())
                # self.assertIn("您是不是想找“lenovo”的相关商品？点击查看", po.check_error())
                function.insert_img(self.driver, "Chinese_search_" + query + ".jpg")

    def test_search5(self):
        """没有搜索结果"""
        data_list = function.read_csv_file(self.csv_file_path_test_data)
        for data in data_list:
            if data[0] == "NoResult":
                query = data[1]
                self.search_result_verify(query)
                po = HomePage(self.driver)
                print(po.no_search_result())
                self.assertIn("抱歉，没有找到与", po.no_search_result())
                function.insert_img(self.driver, "Chinese_search_" + query + ".jpg")

if __name__ == "__main__":
    unittest.main()
