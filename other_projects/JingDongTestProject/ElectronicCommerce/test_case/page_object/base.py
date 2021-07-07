# Page Object 设计模式：页面基础类，用于所有页面的继承
class Page(object):
    jingdong_homepage = 'https://www.jd.com/'
    
    def __init__(self, selenium_driver, base_url=jingdong_homepage, parent=None):
        self.base_url = base_url           
        self.driver = selenium_driver
        self.timeout = 30
        self.parent = parent

    def _open(self, custom_url):
        url = custom_url
        self.driver.get(url)
        assert self.on_page(), 'Did not land on %s' % url

    def find_element(self, *loc):
        return self.driver.find_element(*loc)

    def find_elements(self, *loc):
        return self.driver.find_elements(*loc)

    def open(self):
        self._open(self.url)

    def on_page(self):
        return self.driver.current_url == self.url

    def script(self, src):
        return self.driver.execute_script(src)

    
	
		

	    
