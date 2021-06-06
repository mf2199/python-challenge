from __future__ import absolute_import

import json
import logging
import os
import unittest

from faker import Faker
from unittest import mock

logging.getLogger().setLevel(logging.INFO)


class TestHandler(unittest.TestCase):
    @staticmethod
    def _generate_event(detail=None):
        """Generate a mock EventBridge event with the given detail.

        THIS METHOD IS COPIED FROM `test_reporting.py` AS-IS
        """
        detail = detail or {}
        return {
            'Records': [
                {
                    'source': 'testing.local',
                    'detail-type': 'Local Testing',
                    'detail': json.dumps(detail),
                    # 'detail': detail,
                }
            ]
        }

    def test_ftr_cc_01_unique_residences(self):
        from handler import main

        # with open(os.path.join("tests", "loandata.json")) as file:
        #     event = self._generate_event(json.load(file))
        #     for record in event["Records"]:
        #         record["detail"] = json.loads(record["detail"])
        #     logging.info(f"EVENT:\n{json.dumps(event, indent=2)}")

        with open(os.path.join("tests", "loandata.json")) as file:
            event = self._generate_event(json.load(file))

        response = main(event)

        # logging.info('REPORTS: %s', json.dumps(response, indent=2))
        for report in response["reports"]:
            if report["title"] == "Residences Report":
                self.assertEqual(len(report["residences"]), 1)

        # fake = Faker()
        # detail = json.loads(event["Records"][0]["detail"])
        # for borrower in detail["applications"][0].values():
        #     address = borrower["mailingAddress"]
        #     address["addressStreetLine1"] = fake.street_address()
        #     address["addressCity"] = fake.city()
        #     address["addressState"] = fake.country_code()
        #     address["addressPostalCode"] = fake.postcode()
        #
        # event = self._generate_event(detail=detail)
        #
        # response = main(event)
        # for report in response["reports"]:
        #     if report["title"] == "Residences Report":
        #         self.assertEqual(len(report["residences"]), 2)
