from tools.ListUtils import ListUtils
from tools.api.mock.MockDeploymentsApiUtils import MockDeploymentsApiUtils
from tools.api.real.RealApiUtils import RealApiUtils
from tools.utilsList.DeploymentsListUtils import DeploymentsListUtils
from tools.ConfigUtils import ConfigUtils


class DeploymentDataSetup(object):
    api_url = ConfigUtils().read_config_file()['apiBaseURL']
    api_type = ConfigUtils().read_config_file()['apiType']

    def grab_all_deployments_json(self):
        deployment_json = ''
        if self.api_type == 'real':
            deployment_json = RealApiUtils().grab_all_deployments_json(self.api_url)
        elif self.api_type == 'mock':
            deployment_json = MockDeploymentsApiUtils().grab_all_deployments_json(self.api_url)
        return deployment_json

    def grab_deployment_json(self, deployment_id):
        deployment_json = ''
        if self.api_type == 'real':
            deployment_json = RealApiUtils().grab_deployment_json(self.api_url, deployment_id)
        elif self.api_type == 'mock':
            deployment_json = MockDeploymentsApiUtils().grab_deployment_json(self.api_url, deployment_id)
        return deployment_json

    def grab_random_deployment_id(self):
        deployments_json = self.grab_all_deployments_json()
        deployments_list = DeploymentsListUtils().grab_all_deployments_name_id_list(deployments_json)
        random_deployment_list = ListUtils().return_random_from_list(deployments_list)
        return random_deployment_list.get('deploymentId')

    def grab_deployments_list(self):
        deployments_json = self.grab_all_deployments_json()
        deployments_list = DeploymentsListUtils().grab_all_deployments_name_id_list(deployments_json)
        return deployments_list

    def grab_total_number_of_policies_for_deployment(self, deployment_id):
        deployment_json = self.grab_deployment_json(deployment_id)
        return DeploymentsListUtils().grab_number_of_total_policies_for_deployment(deployment_json)

    def grab_deployment_info(self, deployment_id, number_of_policies):
        deployment_json = self.grab_deployment_json(deployment_id)
        return DeploymentsListUtils().grab_list_of_deployment_info(deployment_json, number_of_policies)

    def grab_policies_types_dictionary_list_for_deployment_id(self, deployment_id):
        deployment_json = self.grab_deployment_json(deployment_id)
        policies_types = DeploymentsListUtils().grab_list_of_dictionary_of_policies_types_for_deployment_id(deployment_json)
        policies_list = DeploymentsListUtils().convert_policies_type_dictionary_list_in_string_elements(policies_types)
        sorted_policies_list = ListUtils().sort_dictionary_list_alphabetically_ascending_by('type', policies_list)
        return sorted_policies_list

    def grab_list_dictionary_of_resources_for_deployment_id(self, deployment_id):
        deployment_json = self.grab_deployment_json(deployment_id)
        return DeploymentsListUtils().grab_list_dictionary_of_resources_for_deployment_id(deployment_json)



    def grab_list_of_policies_bar_dimensions(self, deployment_id, dimension):
        deployment_json = self.grab_deployment_json(deployment_id)
        policies_list = self.grab_policies_types_dictionary_list_for_deployment_id(deployment_id)
        policy_list = ListUtils().create_policy_list_from_policy_dictionary_list(policies_list)
        return ListUtils().create_list_of_policies_bar_dimensions(policy_list, dimension, deployment_json)
