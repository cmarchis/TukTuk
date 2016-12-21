from __future__ import division

import random
import time
from operator import itemgetter

import natsort
from tools.api.real.RealApiUtils import RealApiUtils
from tools.DateUtils import DateUtils


class ListUtils(object):
    def sort_dictionary_list_alphabetically_ascending_by(self, field_key, list):
        """
        Sort provided list by the values of the given field_key
        :return sorted_list:
        """
        sorted_list = sorted(list, key=lambda k: k[field_key])
        return sorted_list

    def sort_dictionary_list_alphabetically_descending_by(self, field_key, list):
        """
        Sort provided list by the values of the given field_key
        :return sorted_list:
        """
        sorted_list = sorted(list, key=lambda k: k[field_key], reverse=True)
        return sorted_list

    def sort_list_dictionary_natural_ascending_by_key(self, key, list):
        """
        Sort ascending a list of dictionary by specified key in a natural order. (in a human way not ascii order)
        :param list:
        :return:
        """
        new_list = natsort.natsorted(list, key=itemgetter(*[key]))
        return new_list

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
        return_list = []
        for element in policies_type_list:
            list_item = {}
            list_item['type'] = element
            total = self.return_total_compliant_value(element, deployment_json)
            print 'element: ', element, ' total: ', total
            if self.grab_compliant_in_MSLO_of_same_policy_type(element, deployment_json) != 0:
                actual = self.grab_compliant_in_MSLO_of_same_policy_type(element, deployment_json) \
                         + self.grab_exceptBeforeExp_of_same_policy_type(element, deployment_json)
                print 'actual green:', actual
                list_item['green'] = self.return_the_value_of_each_bar(
                    self.return_percent_of_actual_score_from_entire_score(total, actual), dimension)
            if self.grab_noncompliant_in_RSLO_of_same_policy_type(element, deployment_json) != 0:
                actual = self.grab_noncompliant_in_RSLO_of_same_policy_type(element, deployment_json)
                print 'actual yellow:', actual
                list_item['yellow'] = self.return_the_value_of_each_bar(
                    self.return_percent_of_actual_score_from_entire_score(total, actual), dimension)
            if self.grab_noncompliant_out_RSLO_of_same_policy_type(element, deployment_json) != 0:
                actual = self.grab_noncompliant_out_RSLO_of_same_policy_type(element, deployment_json)
                print 'actual red:', actual
                list_item['red'] = self.return_the_value_of_each_bar(
                    self.return_percent_of_actual_score_from_entire_score(total, actual), dimension)
            if self.grab_failed_of_same_policy_type(element, deployment_json) != 0:
                actual = self.grab_failed_of_same_policy_type(element, deployment_json)
                print 'actual gray:', actual
                list_item['gray'] = self.return_the_value_of_each_bar(
                    self.return_percent_of_actual_score_from_entire_score(total, actual), dimension)
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

    def return_percent_of_actual_score_from_entire_score(self, total, actual):
        """
         Return the percent of a specific compliant from the entire compliant score percentage
        :param total: total score
        :param actual: actual score for specific compliant
        :return:
        """
        procent = (float(actual) * 100) / float(total)
        return procent

    def return_the_value_of_each_bar(self, percent, dimension):
        """
        Return the value of each bar by calculating it considering the percent of compliant and the entire dimension of bar
        :param percent:percent of compliant
        :param dimension:entire dimension of bar
        :return: dimension of bar
        """
        val = ((dimension * percent) / 100)
        print 'val: ', val
        if val - int(val) != 0:
            val2 = int(val) + 1
        else:
            val2 = int(val)
        print 'val2: ', val2
        return val2

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

    def grab_compliance_name_and_id(self, compliance_json):
        """
        Create a list of dictionary of name and id for compliance
        :param compliance_json:
        :return:
        """
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
            name = compliance['rule']['name']
            list_item["name"] = name[0:70] + '...'
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
            name = compliance['rule']['name']
            list_item["name"] = name[0:70] + '...'
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

    def convert_timpestamp_to_compliance_sort_time(self, timestamp):
        """
        For a given timestamp is returning a string witch specifies the difference between given timestamp and the
         system date.
        :param timestamp:
        :return:
        """
        date = ''
        self.found = False
        time_now = time.time()
        start_day = time_now - 86400
        start_week = time_now - 604800
        start_month = time_now - 2505600

        if timestamp > start_day:
            date = 'Today'
            self.found = True
        elif timestamp > start_week:
            date = 'Last 7 days'
            self.found = True
        elif timestamp > start_month:
            date = 'Last 30 days'
            self.found = True
        elif self.found != True:
            date = 'Older'
        return date

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

    def grab_credential_list_by_id(self, credential_list_json, credential_id):
        """
        From the credential request, it will grab the list of credentials, from the data section, for a given name
        :param credential_list_json:
        :param name:
        :return:
        """
        credential_list = []
        for credential_now in credential_list_json:
            if credential_now['id'] == credential_id:
                for credential_item in credential_now['data']:
                    credential_data = {}
                    credential_data['name'] = credential_now['name']
                    credential_data['id'] = credential_item['id']
                    credential_data['key'] = credential_item['key']
                    credential_data['value'] = credential_item['value']
                    credential_list.append(credential_data)
        return credential_list

    def grab_credential_list_by_name(self, credential_list_json, credential_name):
        """
        From the credential request, it will grab the list of credentials, from the data section, for a given name
        :param credential_list_json:
        :param name:
        :return:
        """
        credential_list = []
        for credential_now in credential_list_json:
            if credential_now['name'] == credential_name:
                for credential_item in credential_now['data']:
                    credential_data = {}
                    credential_data['name'] = credential_now['name']
                    credential_data['id'] = credential_item['id']
                    credential_data['key'] = credential_item['key']
                    credential_data['value'] = credential_item['value']
                    credential_list.append(credential_data)
        return credential_list

    def grab_credential_data_list(self, credential_json):
        credential_list = []
        for credential in credential_json:
            credential_data = {}
            credential_data['id'] = credential['id']
            credential_data['name'] = credential['name']
            credential_list.append(credential_data)
        return credential_list

    def grab_credential_data_from_credential_list(self, credential_list):
        """
        Create a list of data for a specific credential
        :param credential_list:
        :return:
        """
        credential_data_list = []
        credential_data = {}
        for credential in credential_list:
            if credential['key'] == 'username':
                credential_username = credential
        credential_data['name'] = credential['name']
        credential_data['username'] = credential_username['value']
        credential_data_list.append(credential_data)
        return credential_data_list

    def grab_policy_details(self, policy_details_json):
        policy_details = []
        policy_data = {}
        policy_data['name'] = policy_details_json['name']
        policy_data['description'] = policy_details_json['description']
        policy_data['policyType'] = policy_details_json['policyType']['name']
        policy_details.append(policy_data)
        return policy_details

    def verify_dictionary_list_matches(self, a, b):
        list = []
        matches = False
        n = 0
        for i in xrange(len(a)):
            for j in xrange(len(b)):
                if a[i] == b[j]:
                    n += 1
                else:
                    list.append(b[j])
        if n == len(a) and n == len(b):
            matches = True
        return matches


if __name__ == "__main__":
    # print "grab_resources_from_deployment: ", ListUtils().grab_resources_from_deployment('1234', )
    # print "aa", 'AAAA'.title()
    #
    # credential_json = RealApiUtils().grab_credential_json()
    # print ListUtils().grab_credential_list_by_name(credential_json, 'credCHAN')
    # print ListUtils().grab_credential_list_by_id(credential_json, 'blbla')

    a = [{'a': '1'}, {'b': '2'}]
    b = [{'b': '2'}, {'a': '2'}]

    # print ListUtils().convert_timpestamp_to_compliance_sort_time(1481708056)
    print ListUtils().convert_timpestamp_to_compliance_sort_time(1481875663)
