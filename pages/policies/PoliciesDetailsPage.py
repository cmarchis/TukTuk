from tools.WebdriverBase import WebdriverBase
import time

REQUIREMENTS_LIST_SELECTOR = 'ul ul.grommetux-list li'
CLONE_POLICY_BUTTON_SELECTOR = 'svg.grommetux-control-icon-edit'


class PoliciesDetailsPage(WebdriverBase):
    """
    Actions related to Policies details page
    """

    def grab_requirements_name_and_id_list(self):
        requirements_list = self.locate_elements_by_css_selector(REQUIREMENTS_LIST_SELECTOR)
        requirements_name_id_list = []
        for requirements in requirements_list:
            requirements_data = {}
            requirements_data['id'] = requirements.get_attribute('id')
            requirements_data['name'] = requirements.find_element_by_css_selector('label').text
            requirements_name_id_list.append(requirements_data)
        return requirements_name_id_list

    def click_edit_policy_button(self):
        edit_button = self.locate_element_by_css_selector(CLONE_POLICY_BUTTON_SELECTOR)
        time.sleep(3)
        edit_button.click()
        time.sleep(3)

    def select_requirement_by_id(self, requirement_id):
        requirements_list = self.locate_elements_by_css_selector(REQUIREMENTS_LIST_SELECTOR)
        time.sleep(3)
        for requirement in requirements_list:
            if requirement.get_attribute('id') == requirement_id:
                requirement.click()
                break
