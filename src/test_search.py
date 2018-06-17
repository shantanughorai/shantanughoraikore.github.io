import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

class TestTitle(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome("../venv/chromedriver.exe")
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()

    def testSearchCase(self):
        driver = self.driver
        driver.get("https://www.wikipedia.org/")
        #self.assertEqual(driver.title, "Wikipedia")
        driver.find_element_by_xpath("//select[@id=\"searchLanguage\"]/option[text()='English']").click()
        driver.find_element_by_xpath("//*[@id=\"searchInput\"]").send_keys("furry rabbits")
        driver.find_element_by_xpath("/html/body/div[2]/form/fieldset/button/i").click()
        WebDriverWait(driver,10)
        text = driver.find_element_by_class_name("searchdidyoumean")
        self.assertTrue(text)

    def testClickSuggestion(self):
        driver = self.driver
        driver.get("https://www.wikipedia.org")
        driver.find_element_by_xpath("//select[@id=\"searchLanguage\"]/option[text()='English']").click()
        driver.find_element_by_xpath("//*[@id=\"searchInput\"]").send_keys("furry rabbits")
        driver.find_element_by_xpath("/html/body/div[2]/form/fieldset/button/i").click()
        driver.find_element_by_link_text("fury rabbit").click()
        WebDriverWait(driver,10)
        self.assertEqual(driver.title,"fury rabbit - Search results - Wikipedia")
    def tearDown(self):
        self.driver.quit()

if __name__=="__main__":
    unittest.main()