import unittest
from ElectronicCommerce.test_case.models import function
from ElectronicCommerce.test_case.models import jduint
from ElectronicCommerce.test_case.page_object.myJingDongPage import MyProducts
from ElectronicCommerce.test_case.page_object.thumbnailPage import Thumbnail
import pymysql
import time


class PriceSortTest(jduint.JdTest):
    """商品数量和测试库比对测试"""

    def search_result_verify(self):
        MyProducts(self.driver).open_myjd()
        time.sleep(10)

    def test_products_num(self):
        """商品数量和测试库比对测试"""
        self.search_result_verify()
        po = MyProducts(self.driver)
        n = str(int(po.load_product_number()))
        print('页面中存在' + n + '商品信息')
        self.assertEqual(po.load_product_number(), self.execute_sql_command())
        function.insert_img(self.driver, "price_sort_page.jpg")

    @staticmethod
    def execute_sql_command():
        connection = pymysql.connect(host='127.0.0.1',
                                     port=3307,
                                     user='user1',
                                     password='password',
                                     db='myjd',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                # 执行sql语句，进行查询
                sql = 'SELECT count(*) FROM products_djangoproducts'
                cursor.execute(sql)
                # 获取查询结果
                for item in dict(cursor.fetchone()).values():
                    result = str(item)
                print('数据库中共有' + result + '条记录')
            # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
            connection.commit()
            return int(result)

        finally:
            connection.close()


if __name__ == "__main__":
    unittest.main()
