from tools.WebdriverBase import WebdriverBase
from tools.ListUtils import ListUtils
import time

TEMPLATE_LIST_SELECTOR = 'section.grommetux-box div a div[id]'


class TemplatesPage(WebdriverBase):
    """
    Actions related to Templates list
    """

    def click_on_template_by_name(self, name):
        template_list = self.locate_element_by_css_selector(TEMPLATE_LIST_SELECTOR)
        template_name_list = template_list.find_elements_by_css_selector('strong')
        for template in template_name_list:
            if template.text == name:
                template.click()
                break

    def click_on_template_by_id(self, id):
        template_list = self.locate_elements_by_css_selector(TEMPLATE_LIST_SELECTOR)
        for template in template_list:
            if template.get_attribute('id') == id:
                template.click()
                time.sleep(2)
                break

    def grab_templates_dictionary_list(self):
        result_list = []
        template_list = self.locate_elements_by_css_selector(TEMPLATE_LIST_SELECTOR)
        for template_now in template_list:
            template_data = {}
            template_data['name'] = template_now.find_element_by_css_selector('strong').text
            template_data['deployments'] = template_now.find_element_by_css_selector('label:last-child').text
            result_list.append(template_data)
        return ListUtils().sort_dictionary_list_alphabetically_ascending_by('name', result_list)
