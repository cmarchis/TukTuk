import urllib2, json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

templates_url = '/template'
deployment_url = '/deployment'
api_url_base = 'https://192.168.155.238:8081/urest/v1'
api_url_token = 'https://192.168.155.238:8443/idm-service/v2.0/tokens'


class RealApiUtils(object):
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

    def grab_templates_json(self, api_url):
        """
        Return a json containing all templates from live api
        :return:
        """
        headers = {'X-Auth-Token': self.request_token()}
        request = urllib2.Request(api_url + templates_url, headers=headers)
        response = urllib2.urlopen(request)
        json_object = json.load(response)
        templates_list = []
        for item_now in json_object['members']:
            templates_list.append(item_now)
        return templates_list

    def grab_deployments_json_by_template_id(self, api_url, template_id):
        """
        Return a json containing all deployments from live api
        :return:
        """
        headers = {'X-Auth-Token': self.request_token()}
        request = urllib2.Request(api_url + templates_url + '/' + template_id + '?view=condense', headers=headers)
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
        headers = {'X-Auth-Token': self.request_token()}
        request = urllib2.Request(
            api_url + deployment_url + '/' + deployment_id + '?fields=Resources,AttachedPolicy.Policy,AttachedPolicy.Policy.PolicyType',
            headers=headers)
        response = urllib2.urlopen(request)
        json_object = json.load(response)
        return json_object

    def grab_job_json(self, api_url, deployment_id):
        """
        Return the json grabbed from api
        :return:
        """
        headers = {'X-Auth-Token': self.request_token()}
        request = urllib2.Request(api_url + '/deployment/' + deployment_id + '/job?type=Compliance', headers=headers)
        response = urllib2.urlopen(request)
        json_object = json.load(response)
        return json_object

    def grab_compliance_json_for_resource_id(self, api_url, resource_id):
        """
        Return the json grabbed from api
        :return:
        """
        headers = {'X-Auth-Token': self.request_token()}
        request = urllib2.Request(
            api_url + '/compliance/compliance_detail?query=resource.id%20EQ%20' + resource_id + '', headers=headers)
        response = urllib2.urlopen(request)
        json_object = json.load(response)
        return json_object

    def grab_compliance_json(self, api_url):
        """
        Return the json grabbed from api
        :return:
        """
        headers = {'X-Auth-Token': self.request_token()}
        request = urllib2.Request(
            api_url + '/compliance/compliance_detail?count=1000', headers=headers)
        response = urllib2.urlopen(request)
        json_object = json.load(response)
        return json_object

    def grab_credential_json(self, api_url):
        headers = {'X-Auth-Token': self.request_token()}
        request = urllib2.Request(
            api_url + '/credential', headers=headers)
        response = urllib2.urlopen(request)
        json_object = json.load(response)
        return json_object

    def grab_token_json(self):
        """
        Return the json grabbed from api
        :return:
        """
        request = urllib2.Request(api_url_token)
        response = urllib2.urlopen(request)
        json_object = json.load(response)
        return json_object

    def grab_policy_json(self, api_url):
        headers = {'X-Auth-Token': self.request_token()}
        request = urllib2.Request(
            api_url + '/policy', headers=headers)
        response = urllib2.urlopen(request)
        json_object = json.load(response)
        return json_object

    def create_new_scan_job_for_deployment(self, api_url, deployment_id):
        headers = {'X-Auth-Token': self.request_token(), 'Content-Type': 'application/json'}
        r = requests.post(api_url + '/deployment/' + deployment_id + '/scan_compliance', headers=headers, verify=False)
        return r.status_code




        # def grab_credential_json(self):
        #     headers = {'X-Auth-Token': self.request_token(), 'Content-Type': 'application/json'}
        #     return requests.get(api_url_base + '/credential', headers=headers).json()


if __name__ == "__main__":
    # print RealApiUtils().create_new_scan_job_for_deployment('https://192.168.155.238:8081/urest/v1',
    #                                                         'd10c819a38ccb5f7f3f4')
    print 'grab_credential_json', RealApiUtils().grab_deployments_json_by_template_id(
        'https://192.168.155.238:8081/urest/v1', '7b4ca205-7b75-459c-81f1-a61fc8b6be69')
