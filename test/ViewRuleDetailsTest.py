import unittest

from pages.MenuNavigationPage import MenuNavigationPage
from pages.compliance.CompliancePage import CompliancePage
from pages.compliance.ComplianceRuleDetailsPage import ComplianceRuleDetailsPage
from pages.templates.TemplatesMenuListPage import TemplatesMenuListPage
from pages.templates.details.TemplateDetailsPage import TemplateDetailsPage
from pages.deployments.DeploymentsPage import DeploymentsPage
from tools.ConfigUtils import ConfigUtils
from tools.DriverUtils import DriverUtils
from tools.SoftAssert import SoftAssert
from tools.api.mock.DataSetup import DataSetup


class ViewRuleDetailsTest(unittest.TestCase):
    def setUp(self):
        self.base_url = ConfigUtils().read_config_file()['baseURL']
        self.api_url = ConfigUtils().read_config_file()['apiBaseURL']

        self.random_template_id = DataSetup().get_random_template_id()
        self.random_deployment_id = DataSetup().grab_random_deployment_by_template_id(self.random_template_id)
        self.random_resource_id = DataSetup().grab_random_resource_id_by_deployment_id(self.random_deployment_id)
        self.random_compliance_id = DataSetup().grab_random_compliance_id_by_resource_id(self.random_resource_id)

        self.compliance_details = DataSetup().grab_compliance_details(self.random_resource_id,
                                                                      self.random_compliance_id)

        self.browser = DriverUtils().start_driver()

    def test_ViewDeploymentComplianceStatusOverviewTest(self):
        menu_navigation_page = MenuNavigationPage(self.browser)
        menu_navigation_page.navigate_to("http://localhost:8014/provision")
        menu_navigation_page.navigate_to("http://localhost:8014/provision")

        templates_menu_list_page = TemplatesMenuListPage(self.browser)
        templates_menu_list_page.click_on_template_by_id(self.random_template_id)
        print "template"
        template_details_page = TemplateDetailsPage(self.browser)
        template_details_page.select_deployment_by_id(self.random_deployment_id)
        print "deployment"
        deployment_page = DeploymentsPage(self.browser)
        deployment_page.select_resource_by_id(self.random_resource_id)
        print "resources"
        compliance_page = CompliancePage(self.browser)
        compliance_page.click_compliance_by_id(self.random_compliance_id)

        compliance_rule_details_page = ComplianceRuleDetailsPage(self.browser)
        aplication_compliance_rule_details = compliance_rule_details_page.create_compliance_rule_details_list_of_dictionary()

        SoftAssert().verfy_equals_true("Scan message isn't being displayed properly",
                                       self.compliance_details, aplication_compliance_rule_details)

        self.assertEqual(SoftAssert().failures_size(), 0, str(SoftAssert().failures_list()))

    def tearDown(self):
        menuNavigationPage = MenuNavigationPage(self.browser)
        menuNavigationPage.close_driver()
