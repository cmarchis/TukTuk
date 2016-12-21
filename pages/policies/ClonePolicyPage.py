from tools.WebdriverBase import WebdriverBase
import time
from selenium.webdriver.support.ui import Select
from tools.ListUtils import ListUtils

NAME_INPUT_SELECTOR = 'input#name'
DESCRIPTION_INPUT_SELECTOR = 'input#description'
POLICY_TYPE_INPUT_SELECTOR = 'select[name=policyType]'
SAVE_BUTTON_SELECTOR = 'footer button.grommetux-button'
OPTION_LIST_SELECTOR = 'select[name=policyType] option'
REQUIREMENTS_LIST_SELECTOR = 'ul ul.grommetux-list li'
LAYER_REQUIREMENTS_SELECTOR = 'div.grommetux-box--size ul.grommetux-list li'
SUB_REQUIREMENTS_RULLE_LIST_SELECTOR = 'div.grommetux-box--width-large ul.grommetux-list--selectable li'


class ClonePolicyPage(WebdriverBase):
    """
    Actions related to Policies details page
    """

    def edit_name(self, new_name):
        name = self.locate_element_by_css_selector(NAME_INPUT_SELECTOR)
        name.clear()
        name.send_keys(new_name)

    def edit_description(self, new_description):
        description = self.locate_element_by_css_selector(DESCRIPTION_INPUT_SELECTOR)
        description.clear()
        description.send_keys(new_description)

    def edit_policy_type(self, new_policyType):
        select = Select(self.locate_element_by_css_selector(POLICY_TYPE_INPUT_SELECTOR))
        select.select_by_visible_text(new_policyType)

    def edit_policy(self, new_name, new_description, new_policy_type):
        self.edit_name(new_name)
        time.sleep(1)
        self.edit_description(new_description)
        time.sleep(1)
        self.edit_policy_type(new_policy_type)

    def click_save_button(self):
        save_button = self.locate_element_by_css_selector(SAVE_BUTTON_SELECTOR)
        save_button.click()
        time.sleep(5)

    def grab_policy_dictionary_list(self):
        policy_list = []
        policy = {}
        policy['name'] = self.locate_element_by_css_selector(NAME_INPUT_SELECTOR).get_attribute('value')
        policy['description'] = self.locate_element_by_css_selector(DESCRIPTION_INPUT_SELECTOR).get_attribute('value')
        policy_type_id = self.locate_element_by_css_selector(POLICY_TYPE_INPUT_SELECTOR).get_attribute('value')
        option_list = self.locate_elements_by_css_selector(OPTION_LIST_SELECTOR)
        for option in option_list:
            if option.get_attribute('value') == policy_type_id:
                policy['policyType'] = option.text

        policy_list.append(policy)
        return policy_list

    def grab_random_policy_type(self):
        element_list = self.locate_elements_by_css_selector('span.grommetux-form-field__contents select option')
        credential_list = []
        for credential in element_list:
            credential_list.append(credential.text)
        random_credential = ListUtils().return_random_from_list(credential_list)
        return random_credential

    def select_requirement_by_id(self, requirement_id):
        requirements_list = self.locate_elements_by_css_selector(REQUIREMENTS_LIST_SELECTOR)
        time.sleep(3)
        for requirement in requirements_list:
            if requirement.get_attribute('id') == requirement_id:
                requirement.click()
                time.sleep(3)
                break

    def grab_sub_requirements_list(self):
        layer_requirements_list = self.locate_elements_by_css_selector(LAYER_REQUIREMENTS_SELECTOR)
        layer_requirements_data_list = []
        for requirement in layer_requirements_list:
            layer_requirement_data = {}
            layer_requirement_data['id'] = requirement.get_attribute('id')
            layer_requirement_data['name'] = requirement.find_element_by_css_selector('div label').text
            layer_requirements_data_list.append(layer_requirement_data)
        return layer_requirements_data_list

    def select_sub_requirement_by_id(self, sub_requirement_id):
        layer_requirements_list = self.locate_elements_by_css_selector(LAYER_REQUIREMENTS_SELECTOR)
        time.sleep(3)
        for sub_requirement in layer_requirements_list:
            if sub_requirement.get_attribute('id') == sub_requirement_id:
                sub_requirement.find_element_by_css_selector('div button').click()
                time.sleep(3)
                break

    def grab_sub_requirement_rule(self):
        sub_requirement_rule_list = self.locate_elements_by_css_selector(SUB_REQUIREMENTS_RULLE_LIST_SELECTOR)
        sub_requirement_rule_data_list = []
        for sub_requirement_rule in sub_requirement_rule_list:
            sub_requirement_rule_data = {}
            sub_requirement_rule_data['id'] = sub_requirement_rule.get_attribute('id')
            sub_requirement_rule_data['name'] = sub_requirement_rule.find_element_by_css_selector('label').text
            sub_requirement_rule_data_list.append(sub_requirement_rule_data)
        return sub_requirement_rule_data_list
