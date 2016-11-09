from tools.WebdriverBase import WebdriverBase

ADD_CREDENTIAL_BUTTON_SELECTOR = 'h3.grommetux-heading--strong'
CREDENTIAL_LIST_SELECTOR = 'li.grommetux-box--pad-medium'


class CredentialPage(WebdriverBase):
    def __init__(self, driver):
        self.driver = driver

    def add_credential(self):
        add_credential_button = self.locate_element_by_css_selector(ADD_CREDENTIAL_BUTTON_SELECTOR)
        add_credential_button.click()

    def edit_credential(self, credential_name):
        credential_list = self.locate_elements_by_css_selector(CREDENTIAL_LIST_SELECTOR)
        for credential in credential_list:
            if credential.find_element_by_css_selector('div>span').text == credential_name:
                credential.find_element_by_css_selector('svg.grommetux-control-icon-edit').click()
                break

    def delete_credential(self, credential_name):
        credential_list = self.locate_elements_by_css_selector(CREDENTIAL_LIST_SELECTOR)
        for credential in credential_list:
            if credential.find_element_by_css_selector('div>span').text == credential_name:
                credential.find_element_by_css_selector('grommetux-control-icon-close').click()
                break
