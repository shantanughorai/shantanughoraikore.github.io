import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

class TestTitle(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome("../venv/chromedriver.exe")
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()

    def testSuggestionCount(self):
        driver = self.driver
        driver.get("https://www.wikipedia.org")
        driver.find_element_by_xpath("//select[@id=\"searchLanguage\"]/option[text()='English']").click()
        driver.find_element_by_xpath("//*[@id=\"searchInput\"]").send_keys("furry rabbits")
        driver.find_element_by_xpath("/html/body/div[2]/form/fieldset/button/i").click()
        driver.find_element_by_link_text("fury rabbit").click()
        WebDriverWait(driver,10)
        searchList = driver.find_element_by_class_name("mw-search-results")
        itemsList = searchList.find_elements_by_tag_name("li")
        #print(itemsList[1])
        self.assertEqual(len(itemsList),20)

    def testTableOfContent(self):
        driver = self.driver
        driver.get("https://www.wikipedia.org")
        driver.find_element_by_xpath("//select[@id=\"searchLanguage\"]/option[text()='English']").click()
        driver.find_element_by_xpath("//*[@id=\"searchInput\"]").send_keys("furry rabbits")
        driver.find_element_by_xpath("/html/body/div[2]/form/fieldset/button/i").click()
        driver.find_element_by_link_text("fury rabbit").click()
        WebDriverWait(driver, 10)
        driver.find_element_by_xpath("/html/body/div[3]/div[3]/div[3]/div/ul/li[1]/div[1]/a").click()
        tableOfContent = driver.find_element_by_id("toc")
        self.assertTrue(tableOfContent)

    def testSuggestionTitle(self):
        driver = self.driver
        driver.get("https://www.wikipedia.org")
        driver.find_element_by_xpath("//select[@id=\"searchLanguage\"]/option[text()='English']").click()
        driver.find_element_by_xpath("//*[@id=\"searchInput\"]").send_keys("furry rabbits")
        driver.find_element_by_xpath("/html/body/div[2]/form/fieldset/button/i").click()
        driver.find_element_by_link_text("fury rabbit").click()
        WebDriverWait(driver, 10)
        driver.find_element_by_xpath("/html/body/div[3]/div[3]/div[3]/div/ul/li[1]/div[1]/a").click()
        title = driver.find_element_by_class_name("firstHeading")
        self.assertTrue(title)

    def tearDown(self):
        self.driver.quit()

if __name__=="__main__":
    unittest.main()