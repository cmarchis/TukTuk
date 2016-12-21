from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time


class WebdriverBase(object):
    ELEMENT_WAIT = 30

    def __init__(self, driver):
        self.driver = driver
        self.driver.set_page_load_timeout(self.ELEMENT_WAIT)

    def navigate_to(self, url):
        """
        Changes the URL to the new value provided
        :param url: String
        :return:
        """
        self.driver.get(url)

    def execute_js(self, script, element):
        self.driver.execute_script(script, element)

    def locate_element_by_css_selector(self, css_locator):
        """
        Finds a web element based on a provided css locator.
        This method will also wait a given time for the element to appear
        :param css_locator: String
        :return: WebElement
        """
        return WebDriverWait(self.driver, self.ELEMENT_WAIT).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, css_locator)))

    def locate_elements_by_css_selector(self, css_locator):
        """
        Finds a web element based on a provided css locator.
        This method will also wait a given time for the element to appear
        :param css_locator: String
        :return: List[WebElement]
        """
        return WebDriverWait(self.driver, self.ELEMENT_WAIT).until(
            EC.visibility_of_any_elements_located((By.CSS_SELECTOR, css_locator)))

    def scroll_pg_down(self):
        """
        Scroll in webpage by simulating user action of pressing page down button
        :return:
        """
        time.sleep(4)
        scroll = self.driver.find_element_by_css_selector(
            "div.index-tiles__section:first-child div.grommetux-tile--selectable:first-child")
        scroll.send_keys(Keys.END)

    def scroll_to_home(self):
        """
        Scroll in webpage by simulating user action of pressing page down button
        :return:
        """
        time.sleep(1)
        scroll = self.driver.find_element_by_css_selector(
            "div.index-tiles__section:first-child div.grommetux-tile--selectable:first-child")
        scroll.send_keys(Keys.HOME)

    def close_driver(self):
        """
        Closes the webdriver. Should be called on each test after all acions are performed
        :return:
        """
        # self.driver.close()
        self.driver.quit()
