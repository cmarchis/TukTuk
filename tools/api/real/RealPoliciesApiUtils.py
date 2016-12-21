import urllib2, json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

templates_url = '/template'
deployment_url = '/deployment'
api_url_base = 'https://192.168.155.238:8081/urest/v1'
api_url_token = 'https://192.168.155.238:8443/idm-service/v2.0/tokens'


class RealPoliciesApiUtils(object):
    """
    API calls to the GUI Rest API. These are used as expected data for validation
    """

    def request_token(self):
        headers = {'Authorization': 'Basic aWRtVHJhbnNwb3J0VXNlcjppZG1UcmFuc3BvcnRVc2Vy',
                   'Accept': 'application/json',
                   'Content-Type': 'application/json'}
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        jdata = json.dumps(
            {"passwordCredentials": {"username": "admin", "password": "cloud"}, "tenantName": "PROVIDER"})
        req = requests.post(api_url_token, data=jdata, headers=headers, verify=False).json()
        return req['token']['id']

    def grab_policy_json(self, api_url):
        headers = {'X-Auth-Token': self.request_token()}
        request = urllib2.Request(
            api_url + '/policy', headers=headers)
        response = urllib2.urlopen(request)
        json_object = json.load(response)
        return json_object

    def grab_requirements_by_policy_id(self, api_url, policy_id):
        headers = {'X-Auth-Token': self.request_token()}
        request = urllib2.Request(
            api_url + '/policy/' + policy_id + '/requirement', headers=headers)
        response = urllib2.urlopen(request)
        json_object = json.load(response)
        return json_object

    def grab_policy_requirement_tree_by_policy_id(self, api_url, policy_id):
        headers = {'X-Auth-Token': self.request_token()}
        request = urllib2.Request(
            api_url + '/policy/' + policy_id + '/requirement_tree', headers=headers)
        response = urllib2.urlopen(request)
        json_object = json.load(response)
        return json_object

