from tools.WebdriverBase import WebdriverBase
import time

REQUIREMENT_DETAILS_CONTAINER_SELECTOR = 'div.grommetux-form-fields div.grommetux-box:nth-child(2)'
SUB_REQUIREMENTS_LIST_SELECTOR = 'div.grommetux-form-fields div.grommetux-box:nth-child(3) ul li'
RULES_LIST_SELECTOR = 'div.grommetux-form-fields div.grommetux-box:nth-child(4) ul.grommetux-list--selectable li'
SUB_REQUIREMENTS_RULLE_LIST_SELECTOR = 'div.grommetux-box--width-large ul.grommetux-list--selectable li'


class EditRequirementPage(WebdriverBase):
    """
    Actions related to Edit Requirements page
    """

    def grab_requirements_name_description_dictionary_list(self):
        requirement_details_container = self.locate_element_by_css_selector(REQUIREMENT_DETAILS_CONTAINER_SELECTOR)
        requirement_details_list = []
        requirement_details_data = {}
        requirement_details_data['name'] = requirement_details_container.find_element_by_css_selector(
            'div:first-child input').get_attribute('value')
        requirement_details_data['description'] = requirement_details_container.find_element_by_css_selector(
            'div:last-child span textarea').text
        requirement_details_list.append(requirement_details_data)
        return requirement_details_list

    def grab_sub_requirements(self):
        sub_requirement_list = self.locate_elements_by_css_selector(SUB_REQUIREMENTS_LIST_SELECTOR)
        sub_requiremnets_data_list = []
        for sub_requirement in sub_requirement_list:
            sub_requirement_data = {}
            sub_requirement_data['id'] = sub_requirement.get_attribute('id')
            sub_requirement_data['name'] = sub_requirement.find_element_by_css_selector('div div label').text
            sub_requiremnets_data_list.append(sub_requirement_data)
        return sub_requiremnets_data_list

    def grab_requirement_rules(self):
        requirement_rules_list = self.locate_elements_by_css_selector(RULES_LIST_SELECTOR)
        requirement_rules_data_list = []
        for requirement_rule in requirement_rules_list:
            requirement_rule_data = {}
            requirement_rule_data['id'] = requirement_rule.get_attribute('id')
            requirement_rule_data['name'] = requirement_rule.find_element_by_css_selector('div label').text
            requirement_rules_data_list.append(requirement_rule_data)
        return requirement_rules_data_list

    def select_sub_requirement_by_id(self, sub_requirement_id):
        sub_requirement_list = self.locate_elements_by_css_selector(SUB_REQUIREMENTS_LIST_SELECTOR)
        time.sleep(3)
        for sub_requirement in sub_requirement_list:
            if sub_requirement.get_attribute('id') == sub_requirement_id:
                sub_requirement.find_element_by_css_selector('div button').click()
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
