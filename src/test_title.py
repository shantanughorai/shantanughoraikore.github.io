import unittest
from selenium import webdriver

class TestTitle(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome("../venv/chromedriver.exe")
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()

    def testTitleCase(self):
        driver = self.driver
        driver.get("https://www.wikipedia.org/")
        self.assertEqual(driver.title, "Wikipedia")

    def tearDown(self):
        self.driver.quit()

if __name__=="__main__":
    unittest.main()