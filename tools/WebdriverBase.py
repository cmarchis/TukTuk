from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


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

    def close_driver(self):
        """
        Closes the webdriver. Should be called on each test after all acions are performed
        :return:
        """
        # self.driver.close()
        self.driver.quit()
