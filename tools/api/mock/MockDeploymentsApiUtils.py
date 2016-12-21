import urllib2, json


class MockDeploymentsApiUtils(object):
    def grab_all_deployments_json(self, api_url):
        request = urllib2.Request(api_url + '/deployment')
        response = urllib2.urlopen(request)
        json_object = json.load(response)
        return json_object

    def grab_deployment_json(self, api_url, deployment_id):
        """
        Return a json containing all deployments from live api
        :return:
        """
        request = urllib2.Request(
            api_url + '/deployment' + '/' + deployment_id + '?fields=Resources,AttachedPolicy.Policy,AttachedPolicy.Policy.PolicyType')
        response = urllib2.urlopen(request)
        json_object = json.load(response)
        return json_object
