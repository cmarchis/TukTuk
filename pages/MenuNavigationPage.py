from tools.WebdriverBase import WebdriverBase

NAVIGATION_CONTAINER_LOCATOR = 'ul.grommetux-tabs a'


class MenuNavigationPage(WebdriverBase):
    def click_on_menu_item(self, name):
        """
        Will select a menu item from the Left side navigation. A label name should be provided.
        :param name:
        :return:
        """
        menu_links_list = self.locate_elements_by_css_selector(NAVIGATION_CONTAINER_LOCATOR)
        for item_now in menu_links_list:
            if item_now.text == name:
                item_now.click()
                break
