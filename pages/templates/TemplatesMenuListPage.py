from tools.WebdriverBase import WebdriverBase
import time

TEMPLATE_LIST_CONTAINER = 'div.grommetux-box--full-vertical'
TEMPLATE_LIST_ITEMS = 'div[id][class*=box]:not([tabindex])'


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

    def click_on_template_by_id(self, id):
        menu_links_list = self.locate_elements_by_css_selector(TEMPLATE_LIST_ITEMS)
        for menu_item in menu_links_list:
            if menu_item.get_attribute('id') == id:
                menu_item.click()
                time.sleep(2)
                break

    def grab_templates_dictionary_list(self):
        result_list = []
        template_list = self.locate_elements_by_css_selector(TEMPLATE_LIST_ITEMS)
        for menu_item in template_list:
            template = {}
            template['name'] = menu_item.find_element_by_css_selector('strong').text
            template['deployments'] = menu_item.find_element_by_css_selector('div').text
            result_list.append(template)
        return result_list
