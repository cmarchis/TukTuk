from tools.WebdriverBase import WebdriverBase
from tools.ConfigUtils import ConfigUtils

PROVISION_SELECTOR = 'a[href*="provision"]'
SETTINGS_SELECTOR = 'a[href*="settings"]'
AUTHOR_SELECTOR = 'a[href*="author"]'


class LandingPage(WebdriverBase):
    api_type = ConfigUtils().read_config_file()['apiType']

    def select_resource_management_from_menu(self):
        resource_management_button = self.locate_element_by_css_selector(PROVISION_SELECTOR)
        resource_management_button.click()

    def select_settings_from_menu(self):
        settings_button = self.locate_element_by_css_selector(SETTINGS_SELECTOR)
        settings_button.click()

    def select_author_from_menu(self):
        author_button = self.locate_element_by_css_selector(AUTHOR_SELECTOR)
        author_button.click()
