import unittest
from tools.ApiUtils import ApiUtils

class Test1(unittest.TestCase):
    # def setUp(self):
        # self.browser = DriverUtils().start_driver()

    def test_Test1(self):
        a = ApiUtils()
        print a.grab_policies_json()