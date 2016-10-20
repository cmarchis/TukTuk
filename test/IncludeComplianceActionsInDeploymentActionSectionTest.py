import unittest

from pages.MenuNavigationPage import MenuNavigationPage
from pages.deployments.DeploymentsPage import DeploymentsPage
from pages.deployments.DeploymentsMenuHeaderPage import DeploymentsMenuHeaderPage
from pages.templates.TemplatesMenuListPage import TemplatesMenuListPage
from pages.templates.details.TemplateDetailsPage import TemplateDetailsPage

from tools.ApiUtils import ApiUtils
from tools.DriverUtils import DriverUtils
from tools.ListUtils import ListUtils
from tools.SoftAssert import SoftAssert


# random_deploymentName:  3 - Sample Deployment

class IncludeComplianceActionsInDeploymentActionSectionTest(unittest.TestCase):
    """
    Test contains 2 verifications steps:
    First step validate that list of menu option that is displayed in Deployments Page is the same as an expected list
    of menu options that should be displayed.
    In the second verification steps test is validating that the deployments info grabbed from application interface are
    the same as those from API call. A list of dictionary grabbed from interface is compared with a list of dictionary
    grabbed from API call.
    """

    def setUp(self):
        self.expected_menu_option_list = ['Scan Compliance', 'Remediate', 'Change Template']
        self.templtes_json = ApiUtils().grab_templates_json()
        self.list_of_templates = ListUtils().grab_template_names_and_id(self.templtes_json)
        random_template_list = ListUtils().return_random_from_list(self.list_of_templates)
        self.random_templateID = random_template_list.get('templateID')
        self.random_templateName = random_template_list.get('templateName')

        self.deployment_list = ListUtils().grab_deployment_name_and_id(self.random_templateID, self.templtes_json)
        random_deployment_list = ListUtils().return_random_from_list(self.deployment_list)
        self.random_deploymentName = random_deployment_list.get('deploymentName')
        self.random_deploymentID = random_deployment_list.get('deploymentId')
        self.api_deployment_info = ListUtils().grab_list_of_deployment_info(self.random_deploymentID,
                                                                            self.templtes_json)
        self.browser = DriverUtils().start_driver()

    def test_IncludeComplianceActionsInDeploymentActionSectionTest(self):
        menu_navigation_page = MenuNavigationPage(self.browser)
        menu_navigation_page.navigate_to("http://localhost:8014/provision")
        menu_navigation_page.navigate_to("http://localhost:8014/provision")
        templates_menu_list_page = TemplatesMenuListPage(self.browser)
        templates_menu_list_page.click_on_template_item(self.random_templateName)

        template_details_page = TemplateDetailsPage(self.browser)
        template_details_page.select_deployment(self.random_deploymentName)

        deployment_page = DeploymentsPage(self.browser)

        aplication_deployment_info = deployment_page.create_list_of_dictionary_of_deployment_info()
        deployments_menu_header_page = DeploymentsMenuHeaderPage(self.browser)
        aplication_menu_options_list = deployments_menu_header_page.create_list_of_menu_options()

        SoftAssert().verfy_equals_true("List of menu option doesn't matched ", self.expected_menu_option_list,
                                       aplication_menu_options_list)

        SoftAssert().verfy_equals_true("List of deployments info doesn't matched ", self.api_deployment_info,
                                       aplication_deployment_info)

        self.assertEqual(SoftAssert().failures_size(), 0, str(SoftAssert().failures_list()))

    def tearDown(self):
        menuNavigationPage = MenuNavigationPage(self.browser)
        menuNavigationPage.close_driver()
