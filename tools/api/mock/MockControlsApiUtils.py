import urllib2, json


class MockControlsApiUtils(object):
    def grab_controls_json(self, api_url):
        request = urllib2.Request(
            api_url + '/control')
        response = urllib2.urlopen(request)
        json_object = json.load(response)
        return json_object
