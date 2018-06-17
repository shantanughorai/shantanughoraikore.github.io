from selenium import webdriver

class Login(object):

    def __init__(self,driver):
        self.driver = driver

    def username(self,username):
        self.driver.find_element_by_id("email").clear()
        self.driver.find_element_by_id("email").send_keys(username)

    def password(self, password):
        self.driver.find_element_by_id("pass").clear()
        self.driver.find_element_by_id("pass").send_keys(password)
    def searchField(self,search):
        self.driver.find_element_by_xpath("//*[@id=\"searchInput\"]").clear()
        self.driver.find_element_by_xpath("//*[@id=\"searchInput\"]").send_keys(search)
    def search(self):
        self.driver.find_element_by_xpath("//select[@id=\"searchLanguage\"]/option[text()='English']").click()
        self.driver.find_element_by_xpath("/html/body/div[2]/form/fieldset/button/i").click()