from tools.WebdriverBase import WebdriverBase
import time

POLICY_CONTAINERS_SECTIONS_SELECTOR = 'section.grommetux-section'
POLICIES_LIST_SELECTOR = 'section.grommetux-section a'


# SPINNER_SELECTOR = 'svg.grommetux-icon-spinning'


class PoliciesPage(WebdriverBase):
    """
    Actions related to Policies list
    """

    def grab_policies_dictionary_list(self):
        section_list = self.locate_elements_by_css_selector(POLICY_CONTAINERS_SECTIONS_SELECTOR)
        result_list = []
        for section in section_list:
            policies_list = section.find_elements_by_css_selector('a')
            for item_now in policies_list:
                policy_data = {}
                policy_data['id'] = item_now.get_attribute('id')
                policy_data['policyType'] = section.find_element_by_css_selector('header label').text
                policy_data['name'] = item_now.find_element_by_css_selector('label:first-child').text
                policy_data['description'] = item_now.find_element_by_css_selector('label:last-child').text
                result_list.append(policy_data)
        return result_list

    def select_policy_by_policy_id(self, policy_id):
        policies_list = self.locate_elements_by_css_selector(POLICIES_LIST_SELECTOR)
        for policy in policies_list:
            if policy.get_attribute('id') == policy_id:
                time.sleep(3)
                policy.click()
                time.sleep(3)
                break

    def grab_policies_dictionary_list_for_policy_id(self, policy_id):
        section_list = self.locate_elements_by_css_selector(POLICY_CONTAINERS_SECTIONS_SELECTOR)
        result_list = []
        for section in section_list:
            policies_list = section.find_elements_by_css_selector('a')
            for item_now in policies_list:
                if item_now.get_attribute('id') == policy_id:
                    policy_data = {}
                    policy_data['policyType'] = section.find_element_by_css_selector('header label').text
                    policy_data['name'] = item_now.find_element_by_css_selector('label:first-child').text
                    policy_data['description'] = item_now.find_element_by_css_selector('label:last-child').text
                    result_list.append(policy_data)
        return result_list
