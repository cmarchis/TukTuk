from __future__ import division

import random
import time
from operator import itemgetter

import natsort
from tools.api.real.RealApiUtils import RealApiUtils
from tools.DateUtils import DateUtils


class ListUtils(object):
    def sort_list_alphabetically_by(self, field_key, list):
        """
        Sort provided list by the values of the given field_key
        :return sorted_list:
        """
        sorted_list = sorted(list, key=lambda k: k[field_key])
        return sorted_list

    def sort_list_dictionary_natural_ascending(self, list):
        """
        Sort ascending a list of dictionary by specified key in a natural order. (in a human way not ascii order)
        :param list:
        :return:
        """
        new_list = natsort.natsorted(list, key=itemgetter(*['key']))
        return new_list

    def sort_list_dictionary_natural_descending(self, list):
        """
        Sort ascending a list of dictionary by specified key in a natural order. (in a human way not ascii order)
        :param list:
        :return:
        """
        new_list = natsort.natsorted(list, key=itemgetter(*['key']), reverse=True)
        return new_list

    def remove_duplicates_from_list(self, list):
        """
        Remove duplicated value from a list.
        :return: list with unique values
        """
        output = []
        seen = set()
        for value in list:
            if value not in seen:
                output.append(value)
                seen.add(value)
        return output

    def return_random_from_list(self, list):
        """
        Return a random element from a list.
        :param list:
        :return:
        """
        return random.choice(list)

    def create_list_of_policies_bar_dimensions(self, policies_type_list, dimension, deployment_json):
        """
        For every policy type that is in policies list create a list of policies bar dimension
        :param dimension: the entire dimension of the bar
        :return:[{'blue': 57, 'gray': 36, 'type': u'Policy type', 'red': 72, 'yellow': 29},{...}]
        """
        # for template_now in policies_list:
        #     for details in template_now['deploymentDetails']:
        #         if details['deployment']['deploymentId'] == deployment_id:


        return_list = []
        for element in policies_type_list:
            list_item = {}
            list_item['type'] = element
            total = self.return_total_compliant_value(element, deployment_json)
            print "element: ", element, ' total: ', total
            if self.grab_compliant_in_MSLO_of_same_policy_type(element, deployment_json) != 0:
                actual = self.grab_compliant_in_MSLO_of_same_policy_type(element, deployment_json) \
                         + self.grab_exceptBeforeExp_of_same_policy_type(element, deployment_json)
                list_item['green'] = self.value(self.percent(total, actual), dimension)
            if self.grab_noncompliant_in_RSLO_of_same_policy_type(element, deployment_json) != 0:
                actual = self.grab_noncompliant_in_RSLO_of_same_policy_type(element, deployment_json)
                list_item['yellow'] = self.value(self.percent(total, actual), dimension)
            if self.grab_noncompliant_out_RSLO_of_same_policy_type(element, deployment_json) != 0:
                actual = self.grab_noncompliant_out_RSLO_of_same_policy_type(element, deployment_json)
                list_item['red'] = self.value(self.percent(total, actual), dimension)
            if self.grab_failed_of_same_policy_type(element, deployment_json) != 0:
                actual = self.grab_failed_of_same_policy_type(element, deployment_json)
                list_item['gray'] = self.value(self.percent(total, actual), dimension)
            return_list.append(list_item)
        return return_list

    def grab_compliant_in_MSLO_of_same_policy_type(self, policy_type, deployment_json):
        """
        Return 'compliant in MSLO' value for every policy type from deployment_json
        """
        sum = 0

        for policies in deployment_json['attachedPolicies']:
            if policies['policy']['policyType']['name'] == policy_type:
                sum += policies['policy']['complianceScore']['compliantInMSLO']
        return sum

    def grab_noncompliant_in_RSLO_of_same_policy_type(self, policy_type, deployment_json):
        """
        Return 'noncompliant in RSLO' value for every policy type from policies_list
        """
        sum = 0

        for policies in deployment_json['attachedPolicies']:
            if policies['policy']['policyType']['name'] == policy_type:
                sum += policies['policy']['complianceScore']['noncompliantInRSLO']

        return sum

    def grab_noncompliant_out_RSLO_of_same_policy_type(self, policy_type, deployment_json):
        """
         Return 'noncompliant out RSLO' value for every policy type from policies_list
        """
        sum = 0
        for policies in deployment_json['attachedPolicies']:
            if policies['policy']['policyType']['name'] == policy_type:
                sum += policies['policy']['complianceScore']['noncompliantOutRSLO']
        return sum

    def grab_failed_of_same_policy_type(self, policy_type, deployment_json):
        """
        Return 'unknown' value for every policy type from policies_list
        """
        sum = 0
        for policies in deployment_json['attachedPolicies']:
            if policies['policy']['policyType']['name'] == policy_type:
                sum += policies['policy']['complianceScore']['failed']
        return sum

    def grab_exceptBeforeExp_of_same_policy_type(self, policy_type, deployment_json):
        """
        Return 'unknown' value for every policy type from policies_list
        """
        sum = 0
        for policies in deployment_json['attachedPolicies']:
            if policies['policy']['policyType']['name'] == policy_type:
                sum += policies['policy']['complianceScore']['exceptBeforeExp']
        return sum

    def return_total_compliant_value(self, policy_type, policies_list):
        """
        Return total compliant value for every policy type in policies_list
        """
        sum = self.grab_compliant_in_MSLO_of_same_policy_type(policy_type, policies_list) \
              + self.grab_noncompliant_in_RSLO_of_same_policy_type(policy_type, policies_list) \
              + self.grab_noncompliant_out_RSLO_of_same_policy_type(policy_type, policies_list) \
              + self.grab_failed_of_same_policy_type(policy_type, policies_list) \
              + self.grab_exceptBeforeExp_of_same_policy_type(policy_type, policies_list)

        return sum

    def percent(self, total, actual):
        """
         Return the percent of a specific compliant from the entire compliant score percentage
        :param total: total score
        :param actual: actual score for specific compliant
        :return:
        """
        procent = (float(actual) * 100) / float(total)
        return procent

    def value(self, percent, dimension):
        """
        Return the value of each bar by calculating it considering the percent of compliant and the entire dimension of bar
        :param percent:percent of compliant
        :param dimension:entire dimension of bar
        :return: dimension of bar
        """
        val = ((dimension * percent) / 100)
        val2 = int(val)
        val = val2 + 1
        return val

    def grab_list_of_dictionary_of_policies_types_for_deployment_id(self, deployment_json):
        """
        From deployment json, return the list of policy type names
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

    def add_variances_termination_to_policies_type_dictionary_list(self, policy_type_list):
        for policy in policy_type_list:
            policy['variances'] = str(policy['variances']) + ' Variances'
        return policy_type_list

    def grab_total_of_same_policy_type(self, deployment_id, policy_type, templtes_list):
        """
        From the policies list, return the number of policies items with the same type
        :return: total
        """
        sum = 0
        for template_now in templtes_list:
            for details in template_now['deploymentDetails']:
                if details['deployment']['deploymentId'] == deployment_id:
                    for policies in details['deployment']['attachedPolicies']:
                        if policies['policy']['policyType']['name'] == policy_type:
                            sum += 1

        return sum

    def grab_undefined_policies(self, policy_type, policies_list):
        """
        From the policies list, return the total of undefined policies with the same type
        :return: total
        """
        sum = 0
        for policy_now in policies_list:
            if policy_now['policyType']['name'] == policy_type:
                sum += policy_now['complianceScore']['unknown']

        return sum

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

    def grab_template_names_and_id(self, templtes_list):
        """
        From list of templates, returns a list of dictionary with template names and ids as a result
        :return list(item{templateName,id},...):
        """
        return_list = []
        for template_now in templtes_list:
            list_item = {}
            list_item['templateName'] = template_now['templateName']
            list_item['templateID'] = template_now['templateID']
            # list_item['templateName'] = template_now['template']['template']['templateName']
            # list_item['templateID'] = template_now['template']['template']['templateID']
            return_list.append(list_item)

        return return_list

    def grab_template_data(self, template_name, templtes_list):
        """
        Grabbes template date as displayed on the template details page.
        :param template_name:
        :param templtes_list:
        :return item{resourceTypes[],attachedPolicies[],noOfDeployments}:
        """
        policy_details = {}
        for template_now in templtes_list:

            if template_now['template']['template']['templateName'] == template_name:
                resource_types = []
                for resource_now in template_now['template']['template']['resourceTypes']:
                    resource_types.append(resource_now['resourceName'])
                policy_details['resourceTypes'] = resource_types

                policies_list = []
                for policy_now in template_now['template']['template']['attachedPolicies']:
                    policies_list.append(policy_now['policy']['name'])
                policy_details['attachedPolicies'] = policies_list

                policy_details['noOfDeployments'] = template_now['noOfDeployments']

        return policy_details

    def grab_list_of_deployment_info(self, deployment_id, templtes_list):
        """
        From json grabbed from api, returns a list of deployment info
        :return: list{'status': 'SUCCESS','template': 'Oracle', 'last_scanned':'September 26, 2016'}
        """
        list_item = {}
        for template_now in templtes_list:
            for details in template_now['deploymentDetails']:
                if details['deploymentId'] == deployment_id:
                    list_item['status'] = details['status']
                    list_item['template'] = details['templateName']
                    list_item['last_scanned'] = DateUtils().convert_long_to_aplication_format_date(
                        details['complianceScore']['lastScanDate'])
                    list_item['compliant'] = str(
                        details['complianceScore']['compliantPolicies']) + ' of ' + \
                                             str(details['complianceScore']['totalPolicies']) + ' Compliant'
        return list_item

    # def grab_deployment_name_and_id(self, deployments_json):
    #     """
    #     From json grabbed from api, return a list of deployments name for a given template
    #     :param template_name:
    #     :param templtes_list:
    #     :return:
    #     """
    #     deployment_list = []
    #     for resource_now in deployments_json:
    #         list_item = {}
    #         list_item['deploymentName'] = resource_now['deploymentName']
    #         list_item['deploymentId'] = resource_now['deploymentId']
    #         deployment_list.append(list_item)
    #
    #     return deployment_list

    def get_last_remediate_scan_date(self, jobs_json):
        """
        For a given json of jobs return the timestamp of the first remediate or scan job
        :param jobs_json:
        :return:
        """
        list_remediate = []
        list_scan = []
        for job in jobs_json:
            if job['type'] == "REMEDIATE":
                list_remediate.append(job['startDT'])
            if job['type'] == "SCAN":
                list_scan.append(job['startDT'])
        if len(list_remediate) != 0:
            return DateUtils().convert_long_to_aplication_format_date(min(list_remediate))
        else:
            return DateUtils().convert_long_to_aplication_format_date(min(list_scan))

    # def grab_resources_from_deployment(self, deployment_id, templtes_list):
    #     """
    #     Create a list of dictionary for resources of a given deployment id
    #     :param deployment_id:
    #     :param templtes_list:
    #     :return:
    #     """
    #     resource_list = []
    #     for template_now in templtes_list:
    #         for details in template_now['deploymentDetails']:
    #             if details['deployment']['deploymentId'] == deployment_id:
    #                 for resource in details['deployment']['resources']:
    #                     list_item = {}
    #                     list_item['resourceName'] = resource['resourceName']
    #                     list_item['resourceId'] = resource['resourceId']
    #                     resource_list.append(list_item)
    #     return resource_list

    def grab_resources_from_deployment_mock(self, specific_deployment_json):
        """
        Create a list of dictionary for resources of a given deployment id
        :param deployment_id:
        :param templtes_list:
        :return:
        """
        resource_list = []
        for details in specific_deployment_json['resources']:
            list_item = {}
            list_item['resourceName'] = details['resourceName']
            list_item['resourceId'] = details['resourceId']
            resource_list.append(list_item)
        return resource_list

    def grab_compliance_details_list(self, compliance_json, rule_id):
        compliance_resources = []
        for compliance in compliance_json['members']:
            list_item = {}
            if compliance['rule']['id'] == rule_id:
                list_item['compliance_name'] = compliance['rule']['name']
                if compliance['status'] == "ERROR":
                    list_item['compliance_status'] = "Failed"
                elif compliance['status'] == "NOT COMPLIANT":
                    list_item['compliance_status'] = "Non Compliant"
                else:
                    list_item['compliance_status'] = compliance['status'].title()
                list_item['compliance_policy'] = compliance['policy']['name']
                list_item['compliance_requirement'] = compliance['requirement']['name']
                list_item['compliance_control'] = compliance['control']['name']
                compliance_resources.append(list_item)
        return compliance_resources

    def grab_compliance_name_and_id(self, compliance_json):
        compliance_resources = []
        for compliance in compliance_json['members']:
            list_item = {}
            list_item['compliance_name'] = compliance['rule']['name']
            list_item['compliance_id'] = compliance['rule']['id']

            compliance_resources.append(list_item)
        return compliance_resources

    def grab_compliance_resources(self, compliance_json):
        """
        Create a list of dictionary for compliance
        :param compliance_json:
        :return:
        """
        compliance_resources = []
        for compliance in compliance_json['members']:
            list_item = {}
            list_item["name"] = compliance['rule']['name']
            if compliance['status'] == 'NOT COMPLIANT':
                list_item["status"] = 'Non Compliant'
            elif compliance['status'] == "ERROR":
                list_item['status'] = "Failed"
            else:
                list_item["status"] = compliance['status'].title()
            list_item["key"] = compliance['policy']['name']
            compliance_resources.append(list_item)
        return compliance_resources

    def grab_compliance_resources_key_sorted_by_key(self, key_name, compliance_json):
        """
        Create a list of dictionary for compliance with specified key
        :param key_name:
        :param compliance_json:
        :return:
        """
        compliance_resources = []
        for compliance in compliance_json['members']:
            list_item = {}
            list_item["name"] = compliance['rule']['name']
            if compliance['status'] == 'NOT COMPLIANT':
                list_item["status"] = 'Non Compliant'
            elif compliance['status'] == "ERROR":
                list_item['status'] = "Failed"
            else:
                list_item["status"] = compliance['status'].title()
            if key_name == "Policy":
                list_item["key"] = compliance['policy']['name']
            if key_name == "Resource":
                list_item["key"] = compliance['resource']['name']
            if key_name == "Requirement":
                list_item["key"] = compliance['requirement']['name']
            compliance_resources.append(list_item)
        return compliance_resources

    def create_compliance_list(self, key, list):
        """
        Create a list of dictionary for compliance with the given status from compliance dictionary list
        :param key:
        :param list:
        :return:
        """
        compliance_list = []
        for item in list:
            item_list = {}
            if item['status'] == key:
                item_list['status'] = item['status'].title()
                item_list['name'] = item['name']
                item_list['key'] = item['key']
                compliance_list.append(item_list)
        return compliance_list

    def create_compliance_time_list(self, compliance_json):
        """
        Create a list of dictionary for compliance from compliance json.
        :param compliance_json:
        :return:
        """
        compliance_list = []
        for compliance in compliance_json['members']:
            list_item = {}
            list_item["name"] = compliance['rule']['ruleName']
            if compliance['status'] == 'NOT COMPLIANT':
                list_item["status"] = 'NON COMPLIANT'
            else:
                list_item["status"] = compliance['status']

            list_item["date"] = self.convert_timpestamp_to_compliance_sort_time(compliance['createdDT'])
            compliance_list.append(list_item)
        return compliance_list

    def convert_timpestamp_to_compliance_sort_time(self, timestamp):
        """
        For a given timestamp is returning a string witch specifies the difference between given timestamp and the
         system date.
        :param timestamp:
        :return:
        """
        date = ''
        self.found = False
        today = time.strftime('%Y-%m-%d')
        start_week = DateUtils().get_date_before_current_date(7)
        end_week = DateUtils().get_date_before_current_date(1)
        start_month = DateUtils().get_date_before_current_date(29)
        end_month = DateUtils().get_date_before_current_date(8)
        if DateUtils().date_between(DateUtils().convert_long_y_m_d(timestamp), today, today):
            date = 'Today'
            self.found = True
        elif DateUtils().date_between(DateUtils().convert_long_y_m_d(timestamp), start_week, end_week):
            date = 'Last 7 days'
            self.found = True
        elif DateUtils().date_between(DateUtils().convert_long_y_m_d(timestamp), start_month, end_month):
            date = 'Last month'
            self.found = True
        elif self.found != True:
            date = 'Older'
        return date

    def grab_template_dictionary_list(self, template_json):
        template_list = []
        for template_now in template_json:
            template = {}
            template['name'] = template_now['templateName']
            template['deployments'] = str(template_now['noOfDeployments']) + ' Deployments'
            template_list.append(template)
        return template_list

    def grab_template_resources_types_for_template_id(self, template_id, template_json):
        resources_types = []
        for template_now in template_json:
            if template_now['templateID'] == template_id:
                i = 0
                for resource_type_now in template_now['resourceTypes']:
                    i += 1
                    resources_types.append(str(i) + '.   ' + resource_type_now['resourceName'])
        return resources_types

    def grab_template_policies_for_template_id(self, template_id, template_json):
        policies = []
        for template_now in template_json:
            if template_now['templateID'] == template_id:
                for policy_now in template_now['attachedPolicies']:
                    policies.append(policy_now['name'])
        return policies

    def grab_template_deployments_for_template_id(self, template_id, template_json):
        deployments_list = []
        for template_now in template_json:
            if template_now['templateID'] == template_id:
                deployment = {}
                for deployments_now in template_now['deploymentDetails']:
                    deployment['name'] = deployments_now['deploymentName']
                    if deployments_now['status'] == 'RUNNING':
                        deployment['status'] = 'In Progress'
                    else:
                        deployment['status'] = deployments_now['status'].title()
                    deployments_list.append(deployment)
        return deployments_list

    def create_policy_list_from_policy_dictionary_list(self, policy_dictionary_list):
        policy_list = []
        for policy in policy_dictionary_list:
            policy_list.append(policy['type'])
        return policy_list

    def grab_credential_list_by_name(self, credential_list_json, name):
        """
        From the credential request, it will grab the list of credentials, from the data section, for a given name
        :param credential_list_json:
        :param name:
        :return:
        """
        credential_list = []
        for credential_now in credential_list_json:
            if credential_now['name'] == name:
                for credential_item in credential_now['data']:
                    credential_data = {}
                    credential_data['id'] = credential_item['id']
                    credential_data['key'] = credential_item['key']
                    credential_data['value'] = credential_item['value']
                    credential_list.append(credential_data)

        return credential_list

    def grab_credential_name_list(self, credential_json):
        credential_list = []
        for credential in credential_json:
            credential_list.append(credential['name'])
        return credential_list



if __name__ == "__main__":
    # print "grab_resources_from_deployment: ", ListUtils().grab_resources_from_deployment('1234', )
    print "aa", 'AAAA'.title()

    credential_json = RealApiUtils().grab_credential_json()
    print ListUtils().grab_credential_list_by_name(credential_json, 'credCHAN')
    print ListUtils().grab_credential_list_by_name(credential_json, 'blbla')
