from tools.WebdriverBase import WebdriverBase
from tools.ConfigUtils import ConfigUtils

PROVISION_SELECTOR = 'div.grommetux-box--clickable'


class LandingPage(WebdriverBase):
    api_type = ConfigUtils().read_config_file()['apiType']

    def select_provision(self):
        if self.api_type == 'real':
            provision_button = self.locate_element_by_css_selector(PROVISION_SELECTOR)
            provision_button.click()
