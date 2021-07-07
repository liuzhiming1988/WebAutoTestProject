from threading import Thread
from selenium.webdriver import Remote
from selenium import webdriver


# start browser
def browser():
    # browser (chrome, firefox, ie ...)
    driver = webdriver.Chrome()
    # driver = webdriver.Ie()
    # driver = webdriver.Firefox()
    # dc = {'platform': 'ANY', 'browserName': 'chrome', 'version': '', 'javascriptEnabled': True}
    # dc = {'browserName': dc_browser}

    # host = '127.0.0.1:4444'  # host: port (default: 127.0.0.1:4444)
    # dc = {'browserName': 'chrome'}
    # driver = Remote(command_executor='http://' + host + '/wd/hub', desired_capabilities=dc)
    return driver

"""
if __name__ == '__main__':
    host_list = {'127.0.0.1:4444': 'internet explorer', '127.0.0.1:5555': 'chrome'}
    threads = []
    files = range(len(host_list))

    for host_name, browser_name in host_list.items():
        t = Thread(target=browser, args=(host_name, browser_name))
        threads.append(t)

    for i in files:
        threads[i].start()

    for i in files:
        threads[i].join()
"""

if __name__ == '__main__':
    driver = browser()
    driver.get("http://www.baidu.com")
    driver.quit()
