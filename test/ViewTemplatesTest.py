import unittest
from pages.MenuNavigationPage import MenuNavigationPage
from pages.templates.TemplatesMenuListPage import TemplatesMenuListPage
from pages.templates.details.TemplateDetailsPage import TemplateDetailsPage
from tools.DriverUtils import DriverUtils
from tools.ApiUtils import ApiUtils
from tools.ListUtils import ListUtils
from tools.SoftAssert import SoftAssert


class ViewTemplatesTest(unittest.TestCase):
    def setUp(self):
        self.template_name = 'MySql Provision Template'
        templates_list = ApiUtils().grab_templates_json()
        self.template_names_list = ListUtils().grab_template_names(templates_list)
        self.template_data = ListUtils().grab_template_data(self.template_name, templates_list)

        self.browser = DriverUtils().start_driver()

    def test_ViewTemplatesTest(self):
        menu_navigation_page = MenuNavigationPage(self.browser)
        menu_navigation_page.navigate_to("http://localhost:8014/provision")
        menu_navigation_page.navigate_to("http://localhost:8014/provision")

        template_menu = TemplatesMenuListPage(self.browser)
        templates_list = template_menu.grab_names_list()

        print "Template List"
        print self.template_names_list
        print templates_list
        SoftAssert().verify_all_elements_are_present(self.template_names_list, templates_list)

        template_menu.click_on_template_item(self.template_name)

        template_details = TemplateDetailsPage(self.browser)

        # print template_details.grab_resources_data()
        # print template_details.grab_policies_data()
        # print template_details.grab_deployments_data()
        print "Resources List"
        print self.template_data['resourceTypes']
        print template_details.grab_resources_data()
        SoftAssert().verify_all_elements_are_present(self.template_data['resourceTypes'],
                                                     template_details.grab_resources_data())
        print "Policies List"
        print self.template_data['attachedPolicies']
        print template_details.grab_policies_data()
        SoftAssert().verify_all_elements_are_present(self.template_data['attachedPolicies'],
                                                     template_details.grab_policies_data())

        print "Deploy List"
        print self.template_data['noOfDeployments']
        print template_details.grab_deployments_data()
        SoftAssert().verfy_equals_true("Number of deploys does not match", self.template_data['noOfDeployments'],
                                       len(template_details.grab_deployments_data()))

        # template_actions = TemplatActionsPage(self.browser)
        # print template_actions.grab_actions_label()
        # template_actions.click_deploy()
        # time.sleep(5)
        # self.browser.back()
        # time.sleep(5)
        # template_actions.click_schedule()
        # time.sleep(5)
        self.assertEqual(SoftAssert().failures_size(), 0, str(SoftAssert().failures_list()))

    def tearDown(self):
        menuNavigationPage = MenuNavigationPage(self.browser)
        menuNavigationPage.close_driver()
