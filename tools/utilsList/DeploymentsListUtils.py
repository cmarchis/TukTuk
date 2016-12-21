from tools.DateUtils import DateUtils


class DeploymentsListUtils(object):
    def grab_all_deployments_name_id_list(self, deployments_json):
        deployments_list = []
        for deployment in deployments_json['members']:
            deployment_data = {}
            deployment_data['deploymentName'] = deployment['deploymentName']
            deployment_data['deploymentId'] = deployment['deploymentId']
            deployments_list.append(deployment_data)
        return deployments_list

    def grab_number_of_total_policies_for_deployment(self, deployment_json):
        number_of_total_policies = deployment_json['complianceScore']['totalPolicies']
        return number_of_total_policies

    def grab_list_of_deployment_info(self, deployment_json, number_of_policies):
        """
        From json grabbed from api, returns a list of deployment info
        :return: list{'status': 'SUCCESS','template': 'Oracle', 'last_scanned':'September 26, 2016'}
        """
        list_item = {}
        list_item['status'] = deployment_json['status']
        list_item['template'] = deployment_json['templateName']
        if number_of_policies != 0:
            list_item['last_scanned'] = DateUtils().convert_long_to_aplication_format_date(
                deployment_json['complianceScore']['lastScanDate'])
            list_item['compliant'] = str(
                deployment_json['complianceScore']['compliantPolicies']) + ' of ' + \
                                     str(deployment_json['complianceScore']['totalPolicies']) + ' Compliant'

        return list_item

    def grab_list_of_dictionary_of_policies_types_for_deployment_id(self, deployment_json):
        """
        From deployment json, return the list of dictionary of policy type names, the number of appearances, variances
        :return: list(policy_name,...)
        """
        policy_type_list = []
        policy_type_name_list = []

        for policy_now in deployment_json['attachedPolicies']:
            for store_policy in policy_type_list:
                policy_type_name_list.append(store_policy['type'])
            policy_type = {}
            if policy_now['policy']['policyType']['name'] not in policy_type_name_list:
                policy_type['type'] = policy_now['policy']['policyType']['name']
                policy_type['number'] = 1
                policy_type['variances'] = policy_now['policy']['complianceScore']['noncompliantInRSLO'] + \
                                           policy_now['policy']['complianceScore']['noncompliantOutRSLO']
                policy_type_list.append(policy_type)
            if policy_now['policy']['policyType']['name'] in policy_type_name_list:
                for policy in policy_type_list:
                    if policy_now['policy']['policyType']['name'] == policy['type']:
                        policy['number'] += 1
                        policy['variances'] += policy_now['policy']['complianceScore']['noncompliantInRSLO'] + \
                                               policy_now['policy']['complianceScore']['noncompliantOutRSLO']
        return policy_type_list

    def convert_policies_type_dictionary_list_in_string_elements(self, policy_type_list):
        """
        Convert int type element from dictionary list in str type element
        :param policy_type_list:
        :return:
        """
        for policy in policy_type_list:
            policy['variances'] = str(policy['variances']) + ' Variances'
            policy['number'] = str(policy['number'])
        return policy_type_list

    def grab_list_dictionary_of_resources_for_deployment_id(self, deployment_json):
        """
        From list of policies, returns a list of resource name into correct compliance category
        :return list(item[name, status],...):
        """
        return_list = []
        for resources in deployment_json['resources']:
            list_item = {}
            list_item['name'] = resources['resourceName']
            if resources['complianceScore']['unknown'] != 0:
                list_item['status'] = "Unknown"
            elif resources['complianceScore']['noncompliantOutRSLO'] != 0:
                list_item['status'] = "Non Compliant"
            elif resources['complianceScore']['noncompliantInRSLO'] != 0:
                list_item['status'] = "Warning"
            elif resources['complianceScore']['compliantInMSLO'] != 0:
                list_item['status'] = "Compliant"

            return_list.append(list_item)
        return return_list
