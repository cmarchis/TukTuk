from __future__ import division

import random
import time
from operator import itemgetter

import natsort

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

    def create_list_of_policies_model(self, deployment_id, policies_list, policies_type_list):
        """
        Create a minified list from the policies_list JSON
        :return: list(item[type, number, variances],...)
        """
        return_list = []
        for element in policies_type_list:
            list_item = {}
            list_item['type'] = element
            list_item['number'] = str(self.grab_total_of_same_policy_type(deployment_id, element, policies_list))
            list_item['variances'] = str(self.grab_variances(deployment_id, element, policies_list)) + " Variances"
            return_list.append(list_item)
        return return_list

    def create_list_of_policies_bar_dimensions(self, deployment_id, policies_type_list, policies_list, dimension):
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
            total = self.return_total_compliant_value(deployment_id, element, policies_list)
            if self.grab_compliant_in_MSLO_of_same_policy_type(deployment_id, element, policies_list) != 0:
                actual = self.grab_compliant_in_MSLO_of_same_policy_type(deployment_id, element, policies_list)
                list_item['blue'] = self.value(self.percent(total, actual), dimension)
            if self.grab_noncompliant_in_RSLO_of_same_policy_type(deployment_id, element, policies_list) != 0:
                actual = self.grab_noncompliant_in_RSLO_of_same_policy_type(deployment_id, element, policies_list)
                list_item['yellow'] = self.value(self.percent(total, actual), dimension)
            if self.grab_noncompliant_out_RSLO_of_same_policy_type(deployment_id, element, policies_list) != 0:
                actual = self.grab_noncompliant_out_RSLO_of_same_policy_type(deployment_id, element, policies_list)
                list_item['red'] = self.value(self.percent(total, actual), dimension)
            if self.grab_unknown_of_same_policy_type(deployment_id, element, policies_list) != 0:
                actual = self.grab_unknown_of_same_policy_type(deployment_id, element, policies_list)
                list_item['gray'] = self.value(self.percent(total, actual), dimension)
            return_list.append(list_item)
        return return_list

    def grab_compliant_in_MSLO_of_same_policy_type(self, deployment_id, policy_type, policies_list):
        """
        Return 'compliant in MSLO' value for every policy type from policies_list
        """
        sum = 0
        for template_now in policies_list:
            for details in template_now['deploymentDetails']:
                if details['deployment']['deploymentId'] == deployment_id:
                    for policies in details['deployment']['attachedPolicies']:
                        if policies['policy']['policyType']['name'] == policy_type:
                            sum += policies['policy']['complianceScore']['compliantInMSLO']
        return sum

    def grab_noncompliant_in_RSLO_of_same_policy_type(self, deployment_id, policy_type, policies_list):
        """
        Return 'noncompliant in RSLO' value for every policy type from policies_list
        """
        sum = 0
        for template_now in policies_list:
            for details in template_now['deploymentDetails']:
                if details['deployment']['deploymentId'] == deployment_id:
                    for policies in details['deployment']['attachedPolicies']:
                        if policies['policy']['policyType']['name'] == policy_type:
                            sum += policies['policy']['complianceScore']['noncompliantInRSLO']
        return sum

    def grab_noncompliant_out_RSLO_of_same_policy_type(self, deployment_id, policy_type, policies_list):
        """
         Return 'noncompliant out RSLO' value for every policy type from policies_list
        """
        sum = 0
        for template_now in policies_list:
            for details in template_now['deploymentDetails']:
                if details['deployment']['deploymentId'] == deployment_id:
                    for policies in details['deployment']['attachedPolicies']:
                        if policies['policy']['policyType']['name'] == policy_type:
                            sum += policies['policy']['complianceScore']['noncompliantOutRSLO']
        return sum

    def grab_unknown_of_same_policy_type(self, deployment_id, policy_type, policies_list):
        """
        Return 'unknown' value for every policy type from policies_list
        """
        sum = 0
        for template_now in policies_list:
            for details in template_now['deploymentDetails']:
                if details['deployment']['deploymentId'] == deployment_id:
                    for policies in details['deployment']['attachedPolicies']:
                        if policies['policy']['policyType']['name'] == policy_type:
                            sum += policies['policy']['complianceScore']['unknown']
        return sum

    def return_total_compliant_value(self, deployment_id, policy_type, policies_list):
        """
        Return total compliant value for every policy type in policies_list
        """
        sum = self.grab_compliant_in_MSLO_of_same_policy_type(deployment_id, policy_type,
                                                              policies_list) + self.grab_noncompliant_in_RSLO_of_same_policy_type(
            deployment_id, policy_type, policies_list) + self.grab_noncompliant_out_RSLO_of_same_policy_type(
            deployment_id, policy_type,
            policies_list) + self.grab_unknown_of_same_policy_type(
            deployment_id, policy_type, policies_list)
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

    def grab_variances(self, deployment_id, policy_type, policies_list):
        """
        From the policies list, return the total tests (from complianceScore) for policies with the same type
        """
        sum = 0
        for template_now in policies_list:
            for details in template_now['deploymentDetails']:
                if details['deployment']['deploymentId'] == deployment_id:
                    for policies in details['deployment']['attachedPolicies']:
                        if policies['policy']['policyType']['name'] == policy_type:
                            sum += policies['policy']['complianceScore']['noncompliantInRSLO'] + \
                                   policies['policy']['complianceScore'][
                                       'noncompliantOutRSLO']
        return sum

    def grab_list_of_policies_types(self, deployment_id, templtes_list):
        """
        From policies list, return the list of policy type names
        :return: list(policy_name,...)
        """
        list = []
        for template_now in templtes_list:
            for details in template_now['deploymentDetails']:
                if details['deployment']['deploymentId'] == deployment_id:
                    for policies in details['deployment']['attachedPolicies']:
                        list.append(policies['policy']['policyType']['name'])
                    break

        return list

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

    def grab_list_of_resources_with_status(self, deployment_id, templtes_list):
        """
        From list of policies, returns a list of resource name into correct compliance category
        :return list(item[name, status],...):
        """
        return_list = []
        for template_now in templtes_list:
            for details in template_now['deploymentDetails']:
                if details['deployment']['deploymentId'] == deployment_id:
                    for resources in details['deployment']['resources']:
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
                if details['deployment']['deploymentId'] == deployment_id:
                    list_item['status'] = details['deployment']['status']
                    list_item['template'] = details['deployment']['templateName']
                    list_item['last_scanned'] = DateUtils().convert_long_to_aplication_format_date(
                        details['deployment']['complianceScore']['lastScanDate'])
                    list_item['compliant'] = str(
                        details['deployment']['complianceScore']['compliantPolicies']) + ' of ' + \
                                             str(details['deployment']['complianceScore'][
                                                     'totalPolicies']) + ' Compliant'
        return list_item

    def grab_deployment_name_and_id(self, deployments_json):
        """
        From json grabbed from api, return a list of deployments name for a given template
        :param template_name:
        :param templtes_list:
        :return:
        """
        deployment_list = []
        for resource_now in deployments_json:
            list_item = {}
            list_item['deploymentName'] = resource_now['deploymentName']
            list_item['deploymentId'] = resource_now['deploymentId']
            deployment_list.append(list_item)

        return deployment_list

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

    def grab_resources_from_deployment(self, deployment_id, templtes_list):
        """
        Create a list of dictionary for resources of a given deployment id
        :param deployment_id:
        :param templtes_list:
        :return:
        """
        resource_list = []
        for template_now in templtes_list:
            for details in template_now['deploymentDetails']:
                if details['deployment']['deploymentId'] == deployment_id:
                    for resource in details['deployment']['resources']:
                        list_item = {}
                        list_item['resourceName'] = resource['resourceName']
                        list_item['resourceId'] = resource['resourceId']
                        resource_list.append(list_item)
        return resource_list

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


if __name__ == "__main__":
    # print "grab_resources_from_deployment: ", ListUtils().grab_resources_from_deployment('1234', )
    print "aa", 'AAAA'.title()
