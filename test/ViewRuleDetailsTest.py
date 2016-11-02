import unittest

from pages.MenuNavigationPage import MenuNavigationPage
from pages.compliance.CompliancePage import CompliancePage
from pages.compliance.ComplianceRuleDetailsPage import ComplianceRuleDetailsPage
from pages.templates.TemplatesMenuListPage import TemplatesMenuListPage
from pages.templates.details.TemplateDetailsPage import TemplateDetailsPage
from pages.deployments.DeploymentsPage import DeploymentsPage
from tools.ConfigUtils import ConfigUtils
from tools.DriverUtils import DriverUtils
from tools.ListUtils import ListUtils
from tools.api.mock.MockApiUtils import MockApiUtils
from tools.SoftAssert import SoftAssert


class ViewRuleDetailsTest(unittest.TestCase):
    def setUp(self):
        self.base_url = ConfigUtils().read_config_file()['baseURL']
        self.api_url = ConfigUtils().read_config_file()['apiBaseURL']

        # get Template
        templates_json = MockApiUtils().grab_templates_json(self.api_url)
        list_of_templates = ListUtils().grab_template_names_and_id(templates_json)
        random_template_list = ListUtils().return_random_from_list(list_of_templates)
        random_templateID = random_template_list.get('templateID')
        self.random_templateName = random_template_list.get('templateName')

        # get Deployment
        deployments_json = MockApiUtils().grab_deployments_from_templates_json(self.api_url, random_templateID)
        deployment_list = ListUtils().grab_deployment_name_and_id(deployments_json)
        random_deployment_list = ListUtils().return_random_from_list(deployment_list)
        self.random_deploymentName = random_deployment_list.get('deploymentName')
        random_deploymentID = random_deployment_list.get('deploymentId')

        # get Resources
        deployment_json_resources = MockApiUtils().grab_deployments_json(self.api_url, random_templateID)
        resource_list = ListUtils().grab_resources_from_deployment_mock(deployment_json_resources)
        print resource_list
        random_resource_list = ListUtils().return_random_from_list(resource_list)

        self.random_resource_id = random_resource_list.get('resourceId')

        # get Compliance
        compliance_json = MockApiUtils().grab_compliance_json_for_resource_id(self.api_url, self.random_resource_id)
        compliance_list = ListUtils().grab_compliance_name_and_id(compliance_json)
        random_compliance = ListUtils().return_random_from_list(compliance_list)
        self.random_compliance_id = random_compliance.get('compliance_id')
        print 'self.random_compliance: ', self.random_compliance_id
        self.compliance_details = ListUtils().grab_compliance_details_list(compliance_json, self.random_compliance_id)
        print 'self.compliance_details: ', self.compliance_details

        self.browser = DriverUtils().start_driver()

    def test_ViewDeploymentComplianceStatusOverviewTest(self):
        menu_navigation_page = MenuNavigationPage(self.browser)
        menu_navigation_page.navigate_to("http://localhost:8014/provision")
        menu_navigation_page.navigate_to("http://localhost:8014/provision")

        templates_menu_list_page = TemplatesMenuListPage(self.browser)
        templates_menu_list_page.click_on_template_item('self.random_templateName')
        template_details_page = TemplateDetailsPage(self.browser)
        template_details_page.select_deployment(self.random_deploymentName)
        deployment_page = DeploymentsPage(self.browser)
        deployment_page.select_resource_by_id(self.random_resource_id)

        compliance_page = CompliancePage(self.browser)
        compliance_page.click_compliance(self.random_compliance_id)

        compliance_rule_details_page = ComplianceRuleDetailsPage(self.browser)
        aplication_compliance_rule_details = compliance_rule_details_page.create_compliance_rule_details_list_of_dictionary()

        SoftAssert().verfy_equals_true("Scan message isn't being displayed properly",
                                       self.compliance_details, aplication_compliance_rule_details)

        self.assertEqual(SoftAssert().failures_size(), 0, str(SoftAssert().failures_list()))

    def tearDown(self):
        menuNavigationPage = MenuNavigationPage(self.browser)
        menuNavigationPage.close_driver()
