from tools.WebdriverBase import WebdriverBase

RESOURCES_LIST_SELECTOR = 'ul.grommetux-list div.grommetux-columns--responsive'


class DeploymentsPage(WebdriverBase):
    def create_list_of_dictionary_for_policies(self):
        resources_list = self.locate_elements_by_css_selector(RESOURCES_LIST_SELECTOR)
        return_list = []
        for item_now in resources_list:
            list_item = {}
            list_item['name'] = item_now.find_element_by_css_selector("div.grommetux-columns__column:first-child").text
            list_item['type'] = item_now.find_element_by_css_selector("div.grommetux-columns__column:last-child").text
            return_list.append(list_item)
        return return_list
