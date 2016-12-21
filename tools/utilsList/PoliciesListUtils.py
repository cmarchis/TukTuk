requirements_list = []
requirements_list_clone_flow = []
sub_requirement_rule_list = []


class PoliciesListUtils(object):
    def grab_policies_list(self, policies_json):
        policies_list = []
        for policy_now in policies_json['members']:
            policies_data = {}
            policies_data['id'] = policy_now['id']
            policies_data['name'] = policy_now['name']
            policies_data['description'] = policy_now['description']
            policies_data['policyType'] = policy_now['policyType']['name']
            policies_list.append(policies_data)
        return policies_list

    def grab_requirements_name_and_id_list(self, requirements_list):
        requrements_name_id_list = []
        for requirements in requirements_list:
            requrements_data = {}
            requrements_data['id'] = requirements['id']
            requrements_data['name'] = requirements['name']
            requrements_name_id_list.append(requrements_data)
        return requrements_name_id_list

    def grab_requirement_name_and_description_by_requirement_id(self, requirement_id, requirement_tree_json):
        requirement_info = []
        for requirement in requirement_tree_json:
            if requirement['id'] == requirement_id:
                requirement_data = {}
                requirement_data['name'] = requirement['name']
                requirement_data['description'] = requirement['description']
                requirement_info.append(requirement_data)
        return requirement_info

    def grab_sub_requirements_list(self, requirement_id, requirement_tree_json):
        sub_requirement_list = []
        for requirement in requirement_tree_json:
            if requirement['id'] == requirement_id:
                for sub_requirement in requirement['children']:
                    requirement_data = {}
                    requirement_data['id'] = sub_requirement['id']
                    requirement_data['name'] = sub_requirement['name']
                    sub_requirement_list.append(requirement_data)
        return sub_requirement_list

    def grab_requirements_rule_list(self, requirement_id, requirement_tree_json):
        requirement_rule_list = []
        for requirement in requirement_tree_json:
            if requirement['id'] == requirement_id:
                for sub_requirement in requirement['rules']:
                    requirement_data = {}
                    requirement_data['id'] = sub_requirement['id']
                    requirement_data['name'] = sub_requirement['ruleName']
                    requirement_rule_list.append(requirement_data)
        return requirement_rule_list

    def grab_sub_requirements_dictionary_list(self, json, resource_id):
        list = []
        for item_now in json:
            if item_now['id'] == resource_id:
                for item in item_now['children']:
                    list = self.grab_sub_requirements_dictionary_list_recursively(item)
        return list

    def grab_sub_requirements_dictionary_list_recursively(self, dict):
        if 'children' in dict:
            data = {}
            data['id'] = dict['id']
            data['name'] = dict['name']
            requirements_list.append(data)
        for child in dict.get('children', []):
            self.grab_sub_requirements_dictionary_list_recursively(child)
        return requirements_list

    def grab_sub_requirements_rule_dictionary_list(self, requirement_id, sub_requirement_id, json):
        list = []
        for item_now in json:
            if item_now['id'] == requirement_id:
                for item in item_now['children']:
                    list = self.grab_sub_requirement_rule_list_recursively(sub_requirement_id, item)
        return list

    def grab_sub_requirement_rule_list_recursively(self, sub_requirement_id, dict):
        if 'children' in dict:
            if dict['id'] == sub_requirement_id:
                for rule in dict['rules']:
                    data = {}
                    data['id'] = rule['id']
                    data['name'] = rule['ruleName']
                    sub_requirement_rule_list.append(data)
        for child in dict.get('children', []):
            self.grab_sub_requirement_rule_list_recursively(sub_requirement_id,child)
        return sub_requirement_rule_list

    def grab_sub_requirements_dictionary_list_clone_flow(self, json, resource_id):
        list = []
        for item_now in json:
            if item_now['id'] == resource_id:
                list = self.grab_sub_requirements_dictionary_list_recursively(item_now)
        return list

    def grab_sub_requirements_dictionary_list_recursively_clone_flow(self, dict):
        if 'children' in dict:
            data = {}
            data['id'] = dict['id']
            data['name'] = dict['name']
            requirements_list_clone_flow.append(data)
        for child in dict.get('children', []):
            self.grab_sub_requirements_dictionary_list_recursively(child)
        return requirements_list_clone_flow
