import urllib2, json


class MockTemplateApiUtils(object):
    def grab_templates_json(self, api_url):
        """
        Return a json containing all templates from live api
        :return:
        """
        request = urllib2.Request(api_url + '/template')
        response = urllib2.urlopen(request)
        json_object = json.load(response)
        return json_object
