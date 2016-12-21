from tools.ListUtils import ListUtils
from tools.utilsList.PoliciesListUtils import PoliciesListUtils
from tools.api.mock.MockPoliciesApiUtils import MockPoliciesApiUtils
from tools.api.real.RealApiUtils import RealApiUtils
from tools.ConfigUtils import ConfigUtils
from tools.api.real.RealPoliciesApiUtils import RealPoliciesApiUtils


class PoliciesDataSetup(object):
    api_url = ConfigUtils().read_config_file()['apiBaseURL']
    api_type = ConfigUtils().read_config_file()['apiType']

    def grab_policy_json(self):
        policy_data = ''
        if self.api_type == 'real':
            policy_data = RealPoliciesApiUtils().grab_policy_json(self.api_url)
        if self.api_type == 'mock':
            policy_data = MockPoliciesApiUtils().grab_policy_json(self.api_url)
        return policy_data

    def grab_requirements_by_policy_id(self, policy_id):
        requirements_json = ''
        if self.api_type == 'real':
            requirements_json = RealPoliciesApiUtils().grab_requirements_by_policy_id(self.api_url, policy_id)
        elif self.api_type == 'mock':
            requirements_json = MockPoliciesApiUtils().grab_requirements_by_policy_id(self.api_url, policy_id)
        return requirements_json

    def grab_policy_requirement_tree_by_policy_id(self, policy_id):
        requirements_json = ''
        if self.api_type == 'real':
            requirements_json = RealPoliciesApiUtils().grab_policy_requirement_tree_by_policy_id(self.api_url,
                                                                                                 policy_id)
        elif self.api_type == 'mock':
            requirements_json = MockPoliciesApiUtils().grab_policy_requirement_tree_by_policy_id(self.api_url,
                                                                                                 policy_id)
        return requirements_json

    def grab_policies_dictionary_list(self):
        policies_json = self.grab_policy_json()
        policies_dictionary_list = PoliciesListUtils().grab_policies_list(policies_json)
        return policies_dictionary_list

    def grab_random_policy_id(self):
        policies_list = self.grab_policies_dictionary_list()
        random_policy = ListUtils().return_random_from_list(policies_list)
        return random_policy.get('id')

    def grab_requirements_name_list_by_policy_id(self, policy_id):
        requirements_json = self.grab_requirements_by_policy_id(policy_id)
        requirements_list = PoliciesListUtils().grab_requirements_name_and_id_list(requirements_json)
        return requirements_list

    def grab_random_requirement_id_by_policy_id(self, policy_id):
        requirements_list = self.grab_requirements_name_list_by_policy_id(policy_id)
        random_requirement = ListUtils().return_random_from_list(requirements_list)
        random_requirement_id = random_requirement.get('id')
        return random_requirement_id

    def grab_requirement_name_and_description(self, policy_id, requirement_id):
        requirement_tree_json = self.grab_policy_requirement_tree_by_policy_id(policy_id)
        requirement_name_description = PoliciesListUtils().grab_requirement_name_and_description_by_requirement_id(
            requirement_id, requirement_tree_json)
        return requirement_name_description

    def grab_requirement_rules_list_by_requirement_id(self, requirement_id, policy_id):
        requirement_tree_json = self.grab_policy_requirement_tree_by_policy_id(policy_id)
        requirement_rules_list = PoliciesListUtils().grab_requirements_rule_list(requirement_id, requirement_tree_json)
        return requirement_rules_list

    def grab_sub_requirement_rule_list_by_subrequirement_id(self, requirement_id, sub_requirement_id, policy_id):
        requirement_tree_json = self.grab_policy_requirement_tree_by_policy_id(policy_id)
        sub_requirement_rule_list = PoliciesListUtils().grab_sub_requirements_rule_dictionary_list(
            requirement_id, sub_requirement_id, requirement_tree_json, )
        return sub_requirement_rule_list

    def grab_sub_requirements_list_by_requirement_id(self, requirement_id, policy_id, ):
        requirement_tree_json = self.grab_policy_requirement_tree_by_policy_id(policy_id)
        list = PoliciesListUtils().grab_sub_requirements_dictionary_list(requirement_tree_json, requirement_id)
        return list

    def grab_requirements_list_edit_flow(self, requirement_id, policy_id):
        requirement_tree_json = self.grab_policy_requirement_tree_by_policy_id(policy_id)
        list = PoliciesListUtils().grab_sub_requirements_dictionary_list_clone_flow(requirement_tree_json,
                                                                                    requirement_id)
        return list


if __name__ == "__main__":
    print 'AAA: ', PoliciesDataSetup().grab_sub_requirement_rule_list_by_subrequirement_id('1234', '14808', '1234')
