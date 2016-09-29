import os
from selenium import webdriver


class DriverUtils(object):
    def start_driver(self):
        driver_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "drivers/chromedriver.exe")
        driver = webdriver.Chrome(driver_path)
        driver.maximize_window()
        return driver
