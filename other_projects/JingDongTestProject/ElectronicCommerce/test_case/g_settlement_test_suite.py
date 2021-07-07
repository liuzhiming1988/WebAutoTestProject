# import pymysql
# from selenium import webdriver
# import csv
#
# driver = webdriver.Chrome()
# driver.implicitly_wait(30)
# driver.get("http://localhost:8000/admin/")
# driver.find_element_by_id("id_username").send_keys("v-checha")
# driver.find_element_by_id("id_password").send_keys("password123")
# driver.find_element_by_id("id_username").submit()
# driver.find_element_by_css_selector("#content-main > div.app-products.module > table > tbody > tr > td:nth-child(2) > a").click()
#
# path = "D:/51Testing/JingDongTestProject/ElectronicCommerce/data/zengjia_shang_pin.csv"
# file = open(path, 'r')
# table = csv.reader(file)
# for line in table:
#     driver.find_element_by_id("id_title").send_keys(line[0])
#     driver.find_element_by_id("id_src").send_keys(line[1])
#     driver.find_element_by_id("id_price").send_keys(line[2])
#     driver.find_element_by_name("_save").click()
#
# conn = pymysql.connect(host='127.0.0.1',
#                              port=3307,
#                              user='user1',
#                              password='password',
#                              db='myjd',
#                              charset='utf8mb4'
#                        # ,cursorclass=pymysql.cursors.DictCursor
#                        )
# with conn.cursor() as cursor:
#     sql = 'select * from products_djangoproducts order by id desc limit 0,1;'
#     cursor.execute(sql)
#     for item in cursor:
#         print(item[0])
#
#
#
#
#
