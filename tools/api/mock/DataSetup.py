from tools.ListUtils import ListUtils
from tools.api.mock.MockApiUtils import MockApiUtils
from tools.ConfigUtils import ConfigUtils


class DataSetup(object):
    api_url = ConfigUtils().read_config_file()['apiBaseURL']

    def grab_template_data(self):
        return MockApiUtils().grab_templates_json(self.api_url)

    def get_random_template_id(self):
        list_of_templates = ListUtils().grab_template_names_and_id(self.grab_template_data())
        random_template_list = ListUtils().return_random_from_list(list_of_templates)
        return random_template_list.get('templateID')

    # def grab_deployment_data_random(self):
    #     return MockApiUtils().grab_deployments_from_templates_json(self.api_url, self.get_random_template_id())
    #
    # def grab_deployment_data_by_template_id(self, template_id):
    #     return MockApiUtils().grab_deployments_from_templates_json(self.api_url,template_id)
    #
    # def grab_random_deployment_id(self):
    #     random_deployment_list = ListUtils().return_random_from_list(self.grab_deployment_data_random())
    #     return random_deployment_list.get('deploymentId')

    def grab_random_deployment_by_template_id(self, template_id):
        deployments_list = MockApiUtils().grab_deployments_from_templates_json(self.api_url, template_id)
        random_deployment_list = ListUtils().return_random_from_list(deployments_list)
        return random_deployment_list.get('deploymentId')

    # def grab_resource_data(self):
    #     deployment_json_resources = MockApiUtils().grab_deployments_json(self.api_url, self.get_random_template_id())
    #     return ListUtils().grab_resources_from_deployment_mock(deployment_json_resources)

    def grab_random_resource_id_by_deployment_id(self, deployment_id):
        deployment_json_resources = MockApiUtils().grab_deployments_json(self.api_url, deployment_id)
        resource_list = ListUtils().grab_resources_from_deployment_mock(deployment_json_resources)
        random_resource_list = ListUtils().return_random_from_list(resource_list)
        return random_resource_list.get('resourceId')

    # def grab_random_resource_id(self):
    #     random_resource_list = ListUtils().return_random_from_list(self.grab_resource_data())
    #     return random_resource_list.get('resourceId')

    # def grab_random_resource_id_by_deployment(self):
    #     resource_json = MockApiUtils().grab_deployments_json(api_url, deployment_id)
    #     random_resource_list = ListUtils().return_random_from_list(self.grab_resource_data())
    #     return random_resource_list.get('resourceId')

    # def grab_compliance_data_by_resource_id(self, resource_id):
    #     compliance_json = MockApiUtils().grab_compliance_json_for_resource_id(self.api_url, resource_id)
    #     return compliance_json

    def grab_random_compliance_id_by_resource_id(self, resource_id):
        compliance_json = MockApiUtils().grab_compliance_json_for_resource_id(self.api_url, resource_id)
        compliance_list = ListUtils().grab_compliance_name_and_id(compliance_json)
        return ListUtils().return_random_from_list(compliance_list).get('compliance_id')

    def grab_compliance_details(self, resource_id, compliance_id):
        compliance_json = MockApiUtils().grab_compliance_json_for_resource_id(self.api_url, resource_id)
        return ListUtils().grab_compliance_details_list(compliance_json, compliance_id)

    def get_number_of_compliance(self, resource_id):
        compliance_json = MockApiUtils().grab_compliance_json_for_resource_id(self.api_url, resource_id)
        compliance_list = ListUtils().grab_compliance_name_and_id(compliance_json)
        return len(compliance_list)

    def grab_compliance_list_by_resource(self, resource_id):
        compliance_json = MockApiUtils().grab_compliance_json_for_resource_id(self.api_url, resource_id)
        compliance_list = ListUtils().grab_compliance_resources(compliance_json)
        return compliance_list

    def grab_compliance_list_by_resource_of_given_status(self, resource_id, key):
        compliance_list = self.grab_compliance_list_by_resource(resource_id)
        list_of_given_status = ListUtils().create_compliance_list(key, compliance_list)
        return list_of_given_status

    def grab_compliance_list_by_resources_sorted_by_key(self, sort_option, resource_id):
        compliance_json = MockApiUtils().grab_compliance_json_for_resource_id(self.api_url, resource_id)
        compliance_list = ListUtils().grab_compliance_resources_key_sorted_by_key(sort_option, compliance_json)
        return compliance_list

    def grab_last_remediate_scan_date(self, deployment_id):
        jobs_json = MockApiUtils().grab_job_json(deployment_id)
        return ListUtils().get_last_remediate_scan_date(jobs_json)


if __name__ == "__main__":
    print DataSetup().get_random_template_id()

    print DataSetup().grab_random_deployment_by_template_id('2468')
    print "aaa", DataSetup().grab_random_resource_id_by_deployment_id('2468')
