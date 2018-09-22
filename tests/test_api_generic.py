
import sys
import logging
import requests
import unittest

sys.path.extend(["../", "./"])
from common import APITestCase                  # noqa

# turn of normal logging that the ansible_runner_service will generate
nh = logging.NullHandler()
r = logging.getLogger()
r.addHandler(nh)


class TestAPIGeneric(APITestCase):

    def test_api(self):
        """- Test the API endpoint '/api' responds"""

        response = requests.get("https://localhost:5001/api", verify=False)

        self.assertEqual(response.status_code,
                         200)
        self.assertEqual(response.headers['Content-Type'],
                         'text/html; charset=utf-8')

    def test_metrics_content_type(self):
        """- Test the API endpoint '/metrics' responds with text"""

        response = requests.get("https://localhost:5001/metrics", verify=False)

        self.assertEqual(response.status_code,
                         200)
        self.assertEqual(response.headers['Content-Type'],
                         'text/html; charset=utf-8')

    def test_metrics_value(self):
        """- Test a value from API endpoint '/metrics' is correct"""

        response = requests.get("https://localhost:5001/metrics", verify=False)

        self.assertEqual(response.status_code,
                         200)

        payload_list = response.text.split('\n')
        for _m in payload_list:
            if _m.startswith('runner_service_playbook_count'):
                _, v = _m.split('}')
                self.assertEqual(int(v.strip()), 1)
                break


if __name__ == "__main__":

    unittest.main(verbosity=2)
