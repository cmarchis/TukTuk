from tools.ListUtils import ListUtils
from tools.api.mock.MockApiUtils import MockApiUtils
from tools.api.real.RealApiUtils import RealApiUtils
from tools.ConfigUtils import ConfigUtils


class DataSetup(object):
    api_url = ConfigUtils().read_config_file()['apiBaseURL']
    api_type = ConfigUtils().read_config_file()['apiType']

    # def grab_template_data(self):
    #     template_data = ''
    #     if self.api_type == 'real':
    #         template_data = RealApiUtils().grab_templates_json(self.api_url)
    #     elif self.api_type == 'mock':
    #         template_data = MockApiUtils().grab_templates_json(self.api_url)
    #     return template_data

    # def get_random_template_id(self):
    #     list_of_templates = ListUtils().grab_template_names_and_id(self.grab_template_data())
    #     random_template_list = ListUtils().return_random_from_list(list_of_templates)
    #     return random_template_list.get('templateID')

    # def grab_deployment_data_random(self):
    #     return MockApiUtils().grab_deployments_from_templates_json(self.api_url, self.get_random_template_id())
    #
    # def grab_deployment_data_by_template_id(self, template_id):
    #     return MockApiUtils().grab_deployments_from_templates_json(self.api_url,template_id)
    #
    # def grab_random_deployment_id(self):
    #     random_deployment_list = ListUtils().return_random_from_list(self.grab_deployment_data_random())
    #     return random_deployment_list.get('deploymentId')

    # def grab_deployments_json_from_templates_json(self, template_id):
    #     deployment_json = ''
    #     if self.api_type == 'real':
    #         deployment_json = RealApiUtils().grab_deployments_json_by_template_id(self.api_url, template_id)
    #     elif self.api_type == 'mock':
    #         deployment_json = MockApiUtils().grab_deployments_json_by_template_id(self.api_url, template_id)
    #     return deployment_json

    # def grab_random_deployment_by_template_id(self, template_id):
    #     deployments_json = self.grab_deployments_json_from_templates_json(template_id)
    #     random_deployment_list = ListUtils().return_random_from_list(deployments_json)
    #     return random_deployment_list.get('deploymentId')

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

    def grab_compliance_json(self):
        compliance_json = ''
        if self.api_type == 'real':
            compliance_json = RealApiUtils().grab_compliance_json(self.api_url)
        elif self.api_type == 'mock':
            compliance_json = MockApiUtils().grab_compliance_json(self.api_url)
        return compliance_json

    def grab_random_compliance_id_by_resource_id(self, resource_id):
        compliance_json = self.grab_compliance_json_for_resource_id(resource_id)
        compliance_list = ListUtils().grab_compliance_name_and_id(compliance_json)
        return ListUtils().return_random_from_list(compliance_list).get('compliance_id')

    def get_number_of_compliance(self, resource_id):
        compliance_json = self.grab_compliance_json_for_resource_id(resource_id)
        compliance_list = ListUtils().grab_compliance_name_and_id(compliance_json)
        return len(compliance_list)

    def grab_compliance_list_by_resource(self, resource_id):
        compliance_json = self.grab_compliance_json_for_resource_id(resource_id)
        compliance_list = ListUtils().grab_compliance_resources(compliance_json)
        return compliance_list

    def grab_all_compliance_list(self):
        compliance_json = self.grab_compliance_json()
        compliance_list = ListUtils().grab_compliance_resources(compliance_json)
        return compliance_list

    def grab_compliance_list_by_resource_of_given_status(self, resource_id, key):
        compliance_list = self.grab_compliance_list_by_resource(resource_id)
        list_of_given_status = ListUtils().create_compliance_list(key, compliance_list)
        return list_of_given_status

    def grab_compliance_list_of_given_status(self, key):
        compliance_list = self.grab_all_compliance_list()
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

    def grab_deployment_json(self, deployment_id):
        deployment_json = ''
        if self.api_type == 'real':
            deployment_json = RealApiUtils().grab_deployments_json(self.api_url, deployment_id)
        elif self.api_type == 'mock':
            deployment_json = MockApiUtils().grab_deployments_json(self.api_url, deployment_id)
        return deployment_json

    def grab_credential_json(self):
        credential_json = ''
        if self.api_type == 'real':
            credential_json = RealApiUtils().grab_credential_json(self.api_url)
        elif self.api_type == 'mock':
            credential_json = MockApiUtils().grab_credential_json(self.api_url)
        return credential_json

    def grab_credential_data_list(self):
        credntial_json = self.grab_credential_json()
        return ListUtils().grab_credential_data_list(credntial_json)

    def grab_random_credential_id(self):
        credential_json = self.grab_credential_json()
        credential_list = ListUtils().grab_credential_data_list(credential_json)
        random_credential_id = ListUtils().return_random_from_list(credential_list)
        return random_credential_id.get('id')

    def grab_credential_data_by_id(self, credential_id):
        credntial_json = self.grab_credential_json()
        credential_list = ListUtils().grab_credential_list_by_id(credntial_json, credential_id)
        credential_dictionary_list_by_id = ListUtils().grab_credential_data_from_credential_list(credential_list)
        return credential_dictionary_list_by_id

    def grab_credential_data_by_name(self, credential_name):
        credntial_json = self.grab_credential_json()
        credential_list = ListUtils().grab_credential_list_by_name(credntial_json, credential_name)
        credential_dictionary_list_by_name = ListUtils().grab_credential_data_from_credential_list(credential_list)
        return credential_dictionary_list_by_name

    def grab_policy_details_json_by_policy_id(self, policy_id):
        policy_details_json = ''
        if self.api_type == 'real':
            policy_details_json = RealApiUtils().grab_policy_details_by_id(self.api_url)
        elif self.api_type == 'mock':
            policy_details_json = MockApiUtils().grab_policy_details_by_id(self.api_url, policy_id)
        return policy_details_json

    def grab_policy_details_by_policy_id(self, policy_id):
        policy_details_json = self.grab_policy_details_json_by_policy_id(policy_id)
        policy_details = ListUtils().grab_policy_details(policy_details_json)
        return policy_details


        # if __name__ == "__main__":
        # print DataSetup().get_random_template_id()
        #
        # print DataSetup().grab_random_deployment_by_template_id('2468')
        # print "aaa", DataSetup().grab_random_resource_id_by_deployment_id('2468')

        # print 'grab_list_of_policies_bar_dimensions ', DataSetup().grab_list_of_policies_bar_dimensions('1234',192)
        # abc = DataSetup().get_random_template_id()
        #     cde = DataSetup().grab_compliance_list_for_resource_id('1234')
        # print "cde: ", cde
