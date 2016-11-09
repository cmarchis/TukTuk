import urllib2, json
from decimal import *
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import base64

policies_url = 'http://localhost:8010/urest/v1/deployments'
templates_url = '/template'
deployment_url = '/deployment'
resources_url = 'http://localhost:8010/urest/v1/compliance/compliance_detail?query=resource.id%20EQ%207404'


class MockApiUtils(object):
    """
    API calls to the GUI Rest API. These are used as expected data for validation
    """

    def grab_templates_json(self, api_url):
        """
        Return a json containing all templates from live api
        :return:
        """
        request = urllib2.Request(api_url + templates_url)
        response = urllib2.urlopen(request)
        json_object = json.load(response)
        templates_list = []
        for item_now in json_object['members']:
            templates_list.append(item_now)
        return templates_list

    def grab_template_by_template_id(self, template_id):
        request = urllib2.Request(api_url + templates_url)
        response = urllib2.urlopen(request)
        json_object = json.load(response)
        templates_list = []
        for item_now in json_object['members']:
            templates_list.append(item_now)
        return templates_list

    def grab_deployments_from_templates_json(self, api_url, template_id):
        """
        Return a json containing all deployments from live api
        :return:
        """
        request = urllib2.Request(api_url + templates_url + '/' + template_id + '?view=condense')
        response = urllib2.urlopen(request)
        json_object = json.load(response)
        templates_list = []
        for item_now in json_object['deploymentDetails']:
            templates_list.append(item_now)
        return templates_list

    def grab_deployments_json(self, api_url, deployment_id):
        """
        Return a json containing all deployments from live api
        :return:
        """
        request = urllib2.Request(
            api_url + deployment_url + '/' + deployment_id + '?fields=Resources,AttachedPolicy.Policy,AttachedPolicy.Policy.PolicyType')
        response = urllib2.urlopen(request)
        json_object = json.load(response)
        return json_object

    def grab_policies_json(self):
        """
        Return a json containing all policies from live api
        :return:
        """
        request = urllib2.Request(policies_url)
        response = urllib2.urlopen(request)
        json_object = json.load(response)
        policies_list = []
        for item_now in json_object['deployment']['attachedPolicies']:
            policies_list.append(item_now['policy'])

        return policies_list

    def grab_json(self):
        """
        Return the json grabbed from api
        :return:
        """
        request = urllib2.Request(policies_url)
        response = urllib2.urlopen(request)
        json_object = json.load(response)
        return json_object

    def grab_job_json(self, api_url, deployment_id):
        """
        Return the json grabbed from api
        :return:
        """
        request = urllib2.Request(api_url + '/deployment/' + deployment_id + '/job')
        response = urllib2.urlopen(request)
        json_object = json.load(response)
        return json_object


    def grab_compliance_json_for_resource_id(self, api_url, resource_id):
        """
        Return the json grabbed from api
        :return:
        """
        request = urllib2.Request(
            api_url + '/compliance/compliance_detail?query=resource.id%20EQ%20' + resource_id + '')
        response = urllib2.urlopen(request)
        json_object = json.load(response)
        return json_object

    def create_new_scan_job_for_deployment(self, api_url, deployment_id):
        r = requests.post(api_url+'/deployment/'+deployment_id+'/scan_compliance')
        return r.status_code

    def grab_credential_json(self, api_url, ):
        """
        Return the json grabbed from api
        :return:
        """
        request = urllib2.Request(api_url + '/credential')
        response = urllib2.urlopen(request)
        json_object = json.load(response)
        return json_object


if __name__ == "__main__":
    # print 'grab_templates_json', MockApiUtils().grab_templates_json('http://localhost:8010/urest/v1')
    # print 'grab_deployments_json', MockApiUtils().grab_deployments_from_templates_json('http://localhost:8010/urest/v1',
    #                                                                                    '1234')
    # print 'grab_deployments_json', MockApiUtils().grab_deployments_json('http://localhost:8010/urest/v1',
    #                                                                     '1234')

    print 'create_new_scan_job_for_deployment: ',MockApiUtils().create_new_scan_job_for_deployment('http://localhost:8010/urest/v1','1234')
