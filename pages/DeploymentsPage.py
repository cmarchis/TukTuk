from tools.WebdriverBase import WebdriverBase

RESOURCES_LIST_SELECTOR = 'ul.grommetux-list div.grommetux-columns--responsive'
POLICIES_LIST_SELECTOR = 'div.grommetux-box--pad-small div.grommetux-box--pad-medium:nth-child(2) div.grommetux-box--direction-row:not(.grommetux-box--justify-between)'


class DeploymentsPage(WebdriverBase):

    def create_list_of_dictionary_for_resources(self):
        resources_list = self.locate_elements_by_css_selector(RESOURCES_LIST_SELECTOR)
        return_list = []
        for item_now in resources_list:
            list_item = {}
            list_item['name'] = item_now.find_element_by_css_selector("div.grommetux-columns__column:first-child").text
            list_item['type'] = item_now.find_element_by_css_selector("div.grommetux-columns__column:last-child").text
            return_list.append(list_item)
        return return_list


    def create_list_of_dictionary_for_policies(self):
        policies_list = self.locate_elements_by_css_selector(POLICIES_LIST_SELECTOR)
        return_list = []
        for item_now in policies_list:
            list_item = {}
            list_item['type'] = item_now.find_element_by_css_selector("div label").text
            list_item['number'] = item_now.find_element_by_css_selector("div h5 span").text
            list_item['variances'] = item_now.find_element_by_css_selector("div h6 span").text
            return_list.append(list_item)
        return return_list


