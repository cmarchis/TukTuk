from tools.WebdriverBase import WebdriverBase

TEMPLATE_LIST_CONTAINER = 'div.grommetux-box--full-vertical'

class TemplatesMenuListPage(WebdriverBase):
    """
    Actions related to Templates list
    """

    def click_on_template_item(self, name):
        template_container = self.locate_element_by_css_selector(TEMPLATE_LIST_CONTAINER)
        menu_links_list = template_container.find_elements_by_css_selector('strong')
        for menu_item in menu_links_list:
            if menu_item.text == name:
                menu_item.click()
                break

    def grab_names_list(self):
        result_list = []
        template_container = self.locate_element_by_css_selector(TEMPLATE_LIST_CONTAINER)
        menu_links_list = template_container.find_elements_by_css_selector('strong')
        for menu_item in menu_links_list:
            result_list.append(menu_item.text)

        return result_list