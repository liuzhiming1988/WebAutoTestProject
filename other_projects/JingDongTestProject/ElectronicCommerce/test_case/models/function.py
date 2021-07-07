import csv
from selenium import webdriver
import os
import time


# capture screen shot
def insert_img(driver, file_name):
    base_dir = os.path.dirname(__file__)
    base_dir = str(base_dir)
    base_dir = base_dir.replace('\\','/')
    base = base_dir.split('/test_case')[0]
    file_path = base + "/report/image/" + file_name
    driver.get_screenshot_as_file(file_path)


def switch_windows(driver):
    init_windows = driver.current_window_handle
    all_handles = driver.window_handles
    for handle in all_handles:
        if handle != init_windows:
            driver.switch_to.window(handle)


def read_csv_file(file_name):
    base_dir = os.path.dirname(__file__)
    base_dir = str(base_dir)
    base_dir = base_dir.replace('\\', '/')
    base = base_dir.split('/test_case')[0]
    file_path = base + "/data/" + file_name
    data_list = csv.reader(open(file_path, 'r'))
    return data_list


def highlight_element_by_id(driver, id):
    # src = "{0}.style.border=\"5px solid red\"".format(element)
    src = "document.getElementById(\"{0}\").setAttribute('style',\"border: 5px solid red;\");".format(id)
    driver.execute_script(src)
    time.sleep(3)


def highlight_element_by_class(driver, id):
    # src = "{0}.style.border=\"5px solid red\"".format(element)
    src = "document.getElementsByClassName(\"{0}\")[0].setAttribute('style',\"border: 5px solid red;\");".format(id)
    driver.execute_script(src)
    time.sleep(3)

def highlight_element(driver, web_element):
    # src = "{0}.style.border=\"5px solid red\"".format(element)
    driver.execute_script("arguments[0].setAttribute('style',\"border: 5px solid red;\");", web_element)
    time.sleep(3)

if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get("https://www.baidu.com")
    insert_img(driver, 'baidu.jpg')
    driver.quit()
                               
    
