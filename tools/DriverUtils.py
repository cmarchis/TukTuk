import os

from selenium import webdriver
from ConfigUtils import ConfigUtils


class DriverUtils(object):
    def start_driver(self):
        """
        Based on properties received from the config files it will initialize the driver in the specified form
        :return:
        """
        config_map = ConfigUtils().read_config_file()
        if config_map['browser'] == 'chrome':
            driver_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), config_map['chromePath'])
            options = webdriver.ChromeOptions()
            driver = webdriver.Chrome(driver_path, chrome_options=options)
            driver.maximize_window()
        if config_map['browser'] == 'firefox':
            driver = webdriver.Firefox()
            driver.maximize_window()
        return driver
