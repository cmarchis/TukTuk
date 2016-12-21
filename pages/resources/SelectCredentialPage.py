from tools.WebdriverBase import WebdriverBase
from tools.ListUtils import ListUtils
import time

SELECT_CREDENTIAL_INPUT_SELECTOR = 'svg.grommetux-control-icon-caret-down'
SAVE_BUTTON_SELECTOR = 'footer.grommetux-footer button'


class SelectCredentialPage(WebdriverBase):
    def select_credential(self, credential_name):
        credential_list = self.locate_elements_by_css_selector('ol.grommetux-select__options li')
        for credential in credential_list:
            if credential.text == credential_name:
                credential.click()
                break

    def grab_random_credential(self):
        element_list = self.locate_elements_by_css_selector('ol.grommetux-select__options li')
        credential_list = []
        for credential in element_list:
            credential_list.append(credential.text)
        random_credential = ListUtils().return_random_from_list(credential_list)
        return random_credential

    def click_select_credential_drop_down(self):
        select_credential_button = self.locate_element_by_css_selector(SELECT_CREDENTIAL_INPUT_SELECTOR)
        select_credential_button.click()

    def click_save_button(self):
        save_button = self.locate_element_by_css_selector(SAVE_BUTTON_SELECTOR)
        save_button.click()
        time.sleep(5)
