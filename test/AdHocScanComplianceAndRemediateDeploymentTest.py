import unittest

from pages.MenuNavigationPage import MenuNavigationPage
from pages.templates.TemplatesMenuListPage import TemplatesMenuListPage
from pages.templates.details.TemplateDetailsPage import TemplateDetailsPage
from pages.deployments.DeploymentsMenuHeaderPage import DeploymentsMenuHeaderPage
from pages.deployments.DeploymentsPage import DeploymentsPage

from tools.DriverUtils import DriverUtils
from tools.SoftAssert import SoftAssert
from tools.ListUtils import ListUtils
from tools.ApiUtils import ApiUtils


class AdHocScanComplianceAndRemediateDeploymentTest(unittest.TestCase):
    """
    Test contains 3 verification steps for each of scan compliance and remediate actions:
    In the setUp phase is grabbed: - a random template and form that template a random deployment.
                                   - the list of jobs for chosen deployment
                                   - the last scan/remediate date
    Test is navigating to the chosen template and deployment and select Scan Compliance and Remediate menu action.
     After selecting those two option is validating:
        - the pop up message that is displayed after those action contains expected message
        - the started date that is displayed in the pop up message matches with the date grabbed from deployment jobs json
        - that in the time that pop up message is displayed the menu options are disabled
    """

    def setUp(self):
        self.expected_scan_message = 'SCAN in progress'
        self.expected_remediate_message = 'REMEDIATE in progress'
        self.expected_menu_option_state = 'Disabled'
        self.templtes_json = ApiUtils().grab_templates_json()
        self.list_of_templates = ListUtils().grab_template_names_and_id(self.templtes_json)
        random_template_dictionary = ListUtils().return_random_from_list(self.list_of_templates)
        self.random_templateID = random_template_dictionary.get('templateID')
        self.random_templateName = random_template_dictionary.get('templateName')
        self.deployment_list = ListUtils().grab_deployment_name_and_id(self.random_templateID, self.templtes_json)
        random_deployment_list = ListUtils().return_random_from_list(self.deployment_list)
        random_deployment_id = random_deployment_list.get('deploymentId')
        self.random_deployment = random_deployment_list.get('deploymentName')
        job_list = ApiUtils().grab_job_json(random_deployment_id)
        self.api_last_scan_message_date = 'Started ' + ListUtils().get_last_remediate_scan_date(job_list)

        self.browser = DriverUtils().start_driver()

    def test_AdHocScanComplianceAndRemediateDeploymentTest(self):
        menu_navigation_page = MenuNavigationPage(self.browser)
        menu_navigation_page.navigate_to("http://localhost:8014/provision")
        menu_navigation_page.navigate_to("http://localhost:8014/provision")
        templates_menu_list_page = TemplatesMenuListPage(self.browser)
        templates_menu_list_page.click_on_template_item(self.random_templateName)

        template_details_page = TemplateDetailsPage(self.browser)
        template_details_page.select_deployment(self.random_deployment)

        deployment_menu_header_page = DeploymentsMenuHeaderPage(self.browser)
        deployment_menu_header_page.click_on_header_menu_item("Scan Compliance")
        deployment_page = DeploymentsPage(self.browser)

        aplication_notification_message = deployment_page.get_notification_message()
        aplication_notification_date = deployment_page.get_notification_date()

        SoftAssert().verfy_equals_true("Scan message isn't being displayed properly",
                                       self.expected_scan_message, aplication_notification_message)

        SoftAssert().verfy_equals_true("Scan date doesn't matched",
                                       self.api_last_scan_message_date, aplication_notification_date)

        aplication_menu_option_state = deployment_menu_header_page.get_menu_option_state()
        SoftAssert().verfy_equals_true("Menu options aren't disable",
                                       self.expected_menu_option_state, aplication_menu_option_state)

        deployment_page.wait_until_notification_disappear()

        deployment_menu_header_page.click_on_header_menu_item("Remediate")
        aplication_notification_message = deployment_page.get_notification_message()
        aplication_notification_date = deployment_page.get_notification_date()

        SoftAssert().verfy_equals_true("Remediate message isn't being displayed properly",
                                       self.expected_remediate_message, aplication_notification_message)

        SoftAssert().verfy_equals_true("Remediate date doesn't matched",
                                       self.api_last_scan_message_date, aplication_notification_date)

        aplication_menu_option_state = deployment_menu_header_page.get_menu_option_state()
        SoftAssert().verfy_equals_true("Menu options aren't disable",
                                       self.expected_menu_option_state, aplication_menu_option_state)

        self.assertEqual(SoftAssert().failures_size(), 0, str(SoftAssert().failures_list()))

    def tearDown(self):
        menuNavigationPage = MenuNavigationPage(self.browser)
        menuNavigationPage.close_driver()
