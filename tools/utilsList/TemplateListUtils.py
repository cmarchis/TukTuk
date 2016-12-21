class TemplateListUtils(object):

    def grab_template_names_and_id(self, templtes_json):
        """
        From list of templates, returns a list of dictionary with template names and ids as a result
        :return list(item{templateName,id},...):
        """
        return_list = []
        for template_now in templtes_json['members']:
            if template_now.get('noOfDeployments') != None:
                list_item = {}
                list_item['templateName'] = template_now['templateName']
                list_item['templateID'] = template_now['templateID']
                return_list.append(list_item)
        return return_list

    def grab_deployment_list_from_template_json_by_template_id(self, template_json, template_id):
        deployment_list = []
        for template in template_json['members']:
            if template['templateID'] == template_id:
                for deployment in template['deploymentDetails']:
                    deployment_data = {}
                    deployment_data['deploymentId'] = deployment['deploymentId']
                    deployment_data['deploymentName'] = deployment['deploymentName']
                    deployment_data['status'] = deployment['status']
                    deployment_list.append(deployment_data)
        return deployment_list

    def create_policy_list_from_policy_dictionary_list(self, policy_dictionary_list):
        policy_list = []
        for policy in policy_dictionary_list:
            policy_list.append(policy['type'])
        return policy_list

    def grab_template_dictionary_list(self, template_json):
        template_list = []
        for template_now in template_json['members']:
            template = {}
            template['name'] = template_now['templateName']
            template['deployments'] = str(template_now['noOfDeployments']) + ' Deployments'
            template_list.append(template)
        return template_list

    def grab_template_resources_types_for_template_id(self, template_id, template_json):
        resources_types = []
        for template_now in template_json['members']:
            if template_now['templateID'] == template_id:
                i = 0
                for resource_type_now in template_now['resourceTypes']:
                    i += 1
                    resources_types.append(str(i) + '.   ' + resource_type_now['resourceName'])
        return resources_types

    def grab_template_policies_for_template_id(self, template_id, template_json):
        policies = []
        for template_now in template_json['members']:
            if template_now['templateID'] == template_id:
                for policy_now in template_now['attachedPolicies']:
                    policies.append(policy_now['name'])
        return policies
