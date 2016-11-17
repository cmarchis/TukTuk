from tools.WebdriverBase import WebdriverBase
import time

POLICIES_ROW_LIST_CONTAINER = '.index-tiles__section'


class PoliciesListPage(WebdriverBase):
    """
    Actions related to Policies list
    """
    def grab_policies_dictionary_list(self):
        result_list = []
        policies_rows = self.locate_elements_by_css_selector(POLICIES_ROW_LIST_CONTAINER)
        for row_now in policies_rows:
            row_items = row_now.find_elements_by_css_selector('div.grommetux-box--align-stretch')
            for item_now in row_items:
                policy_data = {}
                policy_data['group'] = row_now.find_element_by_css_selector('header').text
                policy_data['name'] = item_now.find_element_by_css_selector('label:first-child').text
                policy_data['description'] = item_now.find_element_by_css_selector('label:last-child').text
                result_list.append(policy_data)
        return result_list


