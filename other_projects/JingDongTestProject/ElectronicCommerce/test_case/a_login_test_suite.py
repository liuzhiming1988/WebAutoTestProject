import unittest
import random
from ElectronicCommerce.test_case.models import function
from ElectronicCommerce.test_case.models import jduint
from ElectronicCommerce.test_case.page_object.loginPage import Login


class LoginTest(jduint.JdTest):
    '''京东登录功能测试'''


    def user_login_verify(self, username="", password=""):
        Login(self.driver).user_login(username, password)

    def test_login1(self):
        '''用户名密码为空登录'''
        self.user_login_verify()
        po = Login(self.driver)
        self.assertEqual(po.login_error_hint(), "请输入账户名和密码")
        function.insert_img(self.driver, "user_password_empty.jpg")

    def test_login2(self):
        '''用户名正确，密码为空登录'''
        self.user_login_verify(username = "pytest")
        po = Login(self.driver)
        self.assertEqual(po.login_error_hint(), "请输入密码")
        function.insert_img(self.driver, "password_empty.jpg")

    def test_login3(self):
        '''用户名为空，密码登录'''
        self.user_login_verify(password = "abc123456")
        po = Login(self.driver)
        self.assertEqual(po.login_error_hint(), "请输入账户名")
        function.insert_img(self.driver, "user_empty.jpg")

    def test_login4(self):
        '''用户名和密码不匹配'''
        character = random.choice('abcdefghijklmnopqrstuvwyz')
        username = "zhangsan" + character
        self.user_login_verify(username, password = "123456")
        po = Login(self.driver)
        self.assertEqual(po.login_error_hint(), "账户名与密码不匹配，请重新输入")
        function.insert_img(self.driver, "user_password_mismatch.jpg")

    def test_login5(self):
        '''用户名和密码正确'''
        self.user_login_verify(username="bwftestjingdong", password = "abc1234567")
        po = Login(self.driver)
        self.assertEqual(po.user_login_success(), "博为峰常城")
        function.insert_img(self.driver, "user_password_correct.jpg")

if __name__ == "__main__":
    unittest.main()