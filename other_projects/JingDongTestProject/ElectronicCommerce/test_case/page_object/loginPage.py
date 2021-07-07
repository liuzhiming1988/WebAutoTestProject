from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from ElectronicCommerce.test_case.models import function
from .base import Page
from time import sleep


# 用户登录页面
class Login(Page):

    url = 'https://www.jd.com/'

    # Action
    jingdong_login_user_loc = (By.CLASS_NAME, "link-login")
    jingdong_account_login = (By.LINK_TEXT, "账户登录")

    def jingdong_login(self):
        self.find_element(*self.jingdong_login_user_loc).click()
        sleep(1)
        self.find_element(*self.jingdong_account_login).click()
        sleep(1)

    login_username_loc = (By.ID, "loginname")
    login_password_loc = (By.ID, "nloginpwd")
    login_button_loc = (By.ID, "loginsubmit")

    # input username
    def login_username(self, username):
        self.find_element(*self.login_username_loc).send_keys(username)

    # input password
    def login_password(self, password):
        self.find_element(*self.login_password_loc).send_keys(password)

    # click sign in button
    def login_button(self):
        self.find_element(*self.login_button_loc).click()

    # define login entry point
    def user_login(self, username="bwftestjingdong", password="abc1234567"):
        self.open()
        self.jingdong_login()
        self.login_username(username)
        self.login_password(password)
        self.login_button()
        sleep(10)

    error_hint_loc = (By.CLASS_NAME, "msg-error")
    user_login_success_loc = (By.CLASS_NAME, "nickname")

    # obtain error message for incorrect user name or password
    def login_error_hint(self):
        function.highlight_element_by_class(self.driver, "msg-error")
        return self.find_element(*self.error_hint_loc).text

    # obtain message when login successfully
    def user_login_success(self):
        user_name = self.find_element(*self.user_login_success_loc)
        function.highlight_element(self.driver, user_name)
        return user_name.text
    
