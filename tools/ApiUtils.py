import urllib2, json
from decimal import *
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import base64

policies_url = 'http://localhost:8010/urest/v1/deployments'
templates_url = '/template'
resources_url = 'http://localhost:8010/urest/v1/compliance/compliance_detail?query=resource.id%20EQ%207404'


class ApiUtils(object):
    """
    API calls to the GUI Rest API. These are used as expected data for validation
    """

    def request_token(self):
        headers = {'Authorization': 'Basic aWRtVHJhbnNwb3J0VXNlcjppZG1UcmFuc3BvcnRVc2Vy', 'Accept': 'application/json',
                   'Content-Type': 'application/json'}
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        jdata = json.dumps({
            "passwordCredentials": {
                "username": "admin",
                "password": "cloud"
            },
            "tenantName": "PROVIDER"
        })
        req = requests.post(
            "https://192.168.155.238:8443/idm-service/v2.0/tokens", data=jdata, headers=headers, verify=False).json()
        return req['token']['id']

    def grab_templates_json(self, api_url):
        """
        Return a json containing all templates from live api
        :return:
        """
        headers = {
            'X-Auth-Token': self.request_token()}
        request = urllib2.Request(api_url + templates_url, headers=headers)
        response = urllib2.urlopen(request)
        json_object = json.load(response)
        templates_list = []
        for item_now in json_object['members']:
            templates_list.append(item_now)
        return templates_list

    def grab_deployments_json(self, api_url, template_id):
        """
        Return a json containing all deployments from live api
        :return:
        """
        headers = {
            'X-Auth-Token': self.request_token()}
        request = urllib2.Request(api_url + templates_url + '/' + template_id, headers=headers)
        response = urllib2.urlopen(request)
        json_object = json.load(response)
        templates_list = []
        for item_now in json_object['deploymentDetails']:
            templates_list.append(item_now)
        return templates_list

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

    def grab_job_json(self, deployment_id):
        """
        Return the json grabbed from api
        :return:
        """
        request = urllib2.Request('http://localhost:8010/urest/v1/deployment/' + deployment_id + '/job')
        response = urllib2.urlopen(request)
        json_object = json.load(response)
        return json_object

    def grab_resources_json(self, resource_id):
        """
        Return the json grabbed from api
        :return:
        """
        request = urllib2.Request(
            'http://localhost:8010/urest/v1/compliance/compliance_detail?query=resource.id%20EQ%20' + resource_id + '')
        response = urllib2.urlopen(request)
        json_object = json.load(response)
        return json_object

    def grab_token_json(self):
        """
        Return the json grabbed from api
        :return:
        """
        request = urllib2.Request(
            'http://192.168.155.238:8443/idm-service/idm/v0/api/public/token')
        response = urllib2.urlopen(request)
        json_object = json.load(response)
        return json_object

    def grab_policies_json_1(self, token):
        """
        Return a json containing all policies from API get request
        :return:
        """
        headers = {
            'X-Auth-Token': token}
        return requests.get('http://192.168.155.238:8080/urest/v1' + '/template', headers=headers).json()


if __name__ == "__main__":
    # print "grab_policies_json: ", ApiUtils().grab_json()
    # print "res : ", ApiUtils().grab_policies_json()
    # print "grab_templates_json: ", ApiUtils().grab_templates_json()
    # print "grab_templates_json len: ", len(ApiUtils().grab_templates_json())

    # print "grab_job_json: ",ApiUtils(). grab_job_json('1234')

    print "grab_authentication_token: ", ApiUtils().request_token()
    print "grab_templates_json: ", ApiUtils().grab_deployments_json('http://192.168.155.238:8080/urest/v1',
                                                                    '59ea1a9a-4d80-46b1-b3d4-62086cb74e3e')
