from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http.cookies import CookieJar
from selenium import webdriver
from evaluate.items import EvaluateItem
import scrapy



class LoginSpider(Spider):
    name = "webdriver2"
    allowed_domains = [
        'http://ids.xidian.edu.cn',
        'http://jwxt.xidian.edu.cn'
    ]
    start_urls = [
        'http://ids.xidian.edu.cn/authserver/login?service=http%3A%2F%2Fjwxt.xidian.edu.cn%2Fcaslogin.jsp'
    ]

    def parse(self, response):
        self.log("now open your browser")
        self.log("Preparing to login...")

        driver = webdriver.Firefox()
        driver.get(response.url)
        driver.implicitly_wait(30)
        driver.find_element_by_name('username').send_keys('username')
        driver.find_element_by_name('password').send_keys('password')
        driver.find_element_by_name('submit').click()

        self.log("login successfully")

        driver.switch_to_frame("topFrame")
        driver.find_element_by_xpath('//a[@cindex="3"]').click()
        self.log("click over")

        driver.switch_to_default_content()
        driver.switch_to_frame("bottomFrame")
        driver.switch_to_frame("menuFrame")
        driver.find_element_by_xpath('//a[@code="010001002"]').click()
        self.log("evaluate begin")

        driver.switch_to_default_content()
        driver.switch_to_frame("bottomFrame")
        driver.switch_to_frame("mainFrame")
        # sel = Selector(text=driver.page_source)
        # cook = driver.get_cookies()
        # driver.close()
        self.log("analysing...")

        teacher = driver.find_elements_by_xpath('//img[@align="middle" and @onclick="evaluation(this)"]')
        while teacher:
            teacher[0].click()
            radio = driver.find_elements_by_xpath("//input[@value[contains(.,'1')] and @type='radio']")
            for x in radio:
                x.click()
            driver.find_element_by_name('zgpj').send_keys('good')
            driver.find_element_by_xpath('//img[@onclick="check()"]').click()
            driver.switch_to_alert().accept()
            teacher = driver.find_elements_by_xpath('//img[@align="middle" and @onclick="evaluation(this)"]')

        self.log("over")
        driver.close()


















