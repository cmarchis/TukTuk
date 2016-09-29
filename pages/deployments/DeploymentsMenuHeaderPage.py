from tools.WebdriverBase import WebdriverBase
import re

MENU_HEADER_CONTAINER_LOCATOR = 'div.grommetux-box--justify-end button'


class DeploymentsMenuHeaderPage(WebdriverBase):
    """
    Actions related to Deployments top action bar.
    """

    def click_on_header_menu_item(self, name):
        """
        Will select a menu item from the menu navigation side. A label name should be provided.
        :param name:
        :return:
        """
        menu_links_list = self.locate_elements_by_css_selector(MENU_HEADER_CONTAINER_LOCATOR)
        for item_now in menu_links_list:
            if item_now.text == name:
                item_now.click()
                break

    def create_list_of_menu_options(self):
        """
        Create a list of menu options name.
        :return: list of menu options name (ex: ['Scan Compliance'],...)
        """
        menu_links_list = self.locate_elements_by_css_selector(MENU_HEADER_CONTAINER_LOCATOR)
        list_items = []
        for item_now in menu_links_list:
            text=item_now.find_element_by_css_selector("span svg title span").text
            button_text=re.sub(text,'',item_now.text)
            list_items.append(button_text)
        return list_items
