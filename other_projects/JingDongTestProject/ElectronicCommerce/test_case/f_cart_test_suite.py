from selenium import webdriver


driver = webdriver.Chrome()
driver.get("http://baidu.com")
driver.switch_to.active_element.send_keys("assd")

# print(a)
# print(type(a))