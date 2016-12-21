from tools.WebdriverBase import WebdriverBase

NAVIGATION_CONTAINER_LOCATOR = 'nav.grommetux-box a'


class MenuNavigationPage(WebdriverBase):
    """
    Page corresponding to top menu. Contains application Tab Navigation.
    """

    def click_on_menu_item(self, name):
        """
        Will select a menu item from the navigation. A label name should be provided.
        :param tab name:
        """
        menu_links_list = self.locate_elements_by_css_selector(NAVIGATION_CONTAINER_LOCATOR)
        for item_now in menu_links_list:
            if item_now.text == name:
                item_now.click()
                break
