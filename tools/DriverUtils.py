# import os
# from selenium import webdriver
#
#
# class DriverUtils(object):
#     def start_driver(self):
#         driver_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "drivers/chromedriver.exe")
#         driver = webdriver.Chrome(driver_path)
#         driver.maximize_window()
#         return driver
import os

#from pyvirtualdisplay import Display
from selenium import webdriver
from ConfigUtils import ConfigUtils

from FileUtils import FileUtils

class DriverUtils(object):
    """
    This class applies the driver configuration based on the config file currently selected.
    The driver is used in WebdriverBase class
    """

    # def start_linux_headless(self):
    #     ## This headless configuration will work only on linux machines
    #     #display = Display(visible=0, size=(800, 600))
    #     # display.start()
    #     pass

    def start_driver(self):
        """
        Based on properties received from the config files it will initialize the driver in the specified form
        :return:
        """
        config_map = ConfigUtils().read_config_file()
        language = FileUtils().read_property('lang.ini', 'language')
        # if config_map['headlessMode'] == 'true':
            # self.start_linux_headless()
        if config_map['browser'] == 'chrome':
            driver_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), config_map['chromePath'])
            options = webdriver.ChromeOptions()
            options.add_argument('--lang=' + language)
            driver = webdriver.Chrome(driver_path,chrome_options=options)
        if config_map['browser'] == 'firefox':
            driver = webdriver.Firefox()
        return driver
