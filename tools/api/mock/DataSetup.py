from tools.ListUtils import ListUtils
from tools.api.mock.MockApiUtils import MockApiUtils
from tools.api.real.RealApiUtils import RealApiUtils
from tools.ConfigUtils import ConfigUtils


class DataSetup(object):
    api_url = ConfigUtils().read_config_file()['apiBaseURL']
    api_type = ConfigUtils().read_config_file()['apiType']

    def grab_template_data(self):
        template_data = ''
        if self.api_type == 'real':
            template_data = RealApiUtils().grab_templates_json(self.api_url)
        elif self.api_type == 'mock':
            template_data = MockApiUtils().grab_templates_json(self.api_url)
        return template_data

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
        deployments_list = ''
        if self.api_type == 'real':
            deployments_list = RealApiUtils().grab_deployments_from_templates_json(self.api_url, template_id)
        elif self.api_type == 'mock':
            deployments_list = MockApiUtils().grab_deployments_from_templates_json(self.api_url, template_id)
        random_deployment_list = ListUtils().return_random_from_list(deployments_list)
        return random_deployment_list.get('deploymentId')

    # def grab_resource_data(self):
    #     deployment_json_resources = MockApiUtils().grab_deployments_json(self.api_url, self.get_random_template_id())
    #     return ListUtils().grab_resources_from_deployment_mock(deployment_json_resources)

    def grab_random_resource_id_by_deployment_id(self, deployment_id):
        deployment_json_resources = ''
        if self.api_type == 'real':
            deployment_json_resources = RealApiUtils().grab_deployments_json(self.api_url, deployment_id)
        elif self.api_type == 'mock':
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
    def grab_compliance_json_for_resource_id(self, resource_id):
        compliance_json = ''
        if self.api_type == 'real':
            compliance_json = RealApiUtils().grab_compliance_json_for_resource_id(self.api_url, resource_id)
        elif self.api_type == 'mock':
            compliance_json = MockApiUtils().grab_compliance_json_for_resource_id(self.api_url, resource_id)
        return compliance_json

    def grab_random_compliance_id_by_resource_id(self, resource_id):
        compliance_json = self.grab_compliance_json_for_resource_id(resource_id)
        compliance_list = ListUtils().grab_compliance_name_and_id(compliance_json)
        return ListUtils().return_random_from_list(compliance_list).get('compliance_id')

    def grab_compliance_details(self, resource_id, compliance_id):
        compliance_json = self.grab_compliance_json_for_resource_id(resource_id)
        return ListUtils().grab_compliance_details_list(compliance_json, compliance_id)

    def get_number_of_compliance(self, resource_id):
        compliance_json = self.grab_compliance_json_for_resource_id(resource_id)
        compliance_list = ListUtils().grab_compliance_name_and_id(compliance_json)
        return len(compliance_list)

    def grab_compliance_list_by_resource(self, resource_id):
        compliance_json = self.grab_compliance_json_for_resource_id(resource_id)
        compliance_list = ListUtils().grab_compliance_resources(compliance_json)
        return compliance_list

    def grab_compliance_list_by_resource_of_given_status(self, resource_id, key):
        compliance_list = self.grab_compliance_list_by_resource(resource_id)
        list_of_given_status = ListUtils().create_compliance_list(key, compliance_list)
        return list_of_given_status

    def grab_compliance_list_by_resources_sorted_by_key(self, sort_option, resource_id):
        compliance_json = self.grab_compliance_json_for_resource_id(resource_id)
        compliance_list = ListUtils().grab_compliance_resources_key_sorted_by_key(sort_option, compliance_json)
        return compliance_list

    def grab_last_remediate_scan_date(self, deployment_id):
        jobs_json = ''
        if self.api_type == 'real':
            jobs_json = RealApiUtils().grab_job_json(self.api_url, deployment_id)
        elif self.api_type == 'mock':
            jobs_json = MockApiUtils().grab_job_json(self.api_url, deployment_id)
        return ListUtils().get_last_remediate_scan_date(jobs_json)

    def create_new_scan_job(self, deployment_id):
        if self.api_type == 'real':
            RealApiUtils().create_new_scan_job_for_deployment(self.api_url, deployment_id)
        elif self.api_type == 'mock':
            MockApiUtils().create_new_scan_job_for_deployment(self.api_url, deployment_id)

    def grab_deployment_info_from_templates(self, deployment_id):
        template_json = self.grab_template_data()
        return ListUtils().grab_list_of_deployment_info(deployment_id, template_json)

    def grab_template_dictionary_list(self):
        template_json = self.grab_template_data()
        return ListUtils().grab_template_dictionary_list(template_json)

    def grab_template_resources_types_for_template_id(self, template_id):
        template_json = self.grab_template_data()
        return ListUtils().grab_template_resources_types_for_template_id(template_id, template_json)

    def grab_template_policies_for_template_id(self, template_id):
        template_json = self.grab_template_data()
        return ListUtils().grab_template_policies_for_template_id(template_id, template_json)

    def grab_template_deployments_for_template_id(self, template_id):
        template_json = self.grab_template_data()
        return ListUtils().grab_template_deployments_for_template_id(template_id, template_json)

    def grab_deployment_json(self, deployment_id):
        deployment_json = ''
        if self.api_type == 'real':
            deployment_json = RealApiUtils().grab_deployments_json(self.api_url, deployment_id)
        elif self.api_type == 'mock':
            deployment_json = MockApiUtils().grab_deployments_json(self.api_url, deployment_id)
        return deployment_json

    def grab_policies_types_dictionary_list_for_deployment_id(self, deployment_id):
        deployment_json = self.grab_deployment_json(deployment_id)
        policies_types = ListUtils().grab_list_of_dictionary_of_policies_types_for_deployment_id(deployment_json)
        return ListUtils().add_variances_termination_to_policies_type_dictionary_list(policies_types)

    def grab_list_dictionary_of_resources_for_deployment_id(self, deployment_id):
        deployment_json = self.grab_deployment_json(deployment_id)
        return ListUtils().grab_list_dictionary_of_resources_for_deployment_id(deployment_json)

    def grab_list_of_policies_bar_dimensions(self, deployment_id, dimension):
        deployment_json = self.grab_deployment_json(deployment_id)
        policies_list = self.grab_policies_types_dictionary_list_for_deployment_id(deployment_id)
        policy_list = ListUtils().create_policy_list_from_policy_dictionary_list(policies_list)
        return ListUtils().create_list_of_policies_bar_dimensions(policy_list, dimension, deployment_json)


if __name__ == "__main__":
    # print DataSetup().get_random_template_id()
    #
    # print DataSetup().grab_random_deployment_by_template_id('2468')
    # print "aaa", DataSetup().grab_random_resource_id_by_deployment_id('2468')

    # print 'grab_list_of_policies_bar_dimensions ', DataSetup().grab_list_of_policies_bar_dimensions('1234',192)
    abc = DataSetup().grab_policies_types_dictionary_list_for_deployment_id('1234')
    print "aaa: ", ListUtils().add_variances_termination_to_policies_type_dictionary_list(abc)
