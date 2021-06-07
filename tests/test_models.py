from __future__ import absolute_import

import json
import logging
import os
import unittest

from faker import Faker

from handler import main

logging.getLogger().setLevel(logging.INFO)


LOAN_DATA_FILE = os.path.join("tests", "loandata.json")


class TestHandler(unittest.TestCase):
    @staticmethod
    def _generate_event(detail=None):
        """Generate a mock EventBridge event with the given detail.

        THIS METHOD IS COPIED FROM `test_reporting.py` AS-IS
        """
        detail = detail or {}
        return {
            "Records": [
                {
                    "source": "testing.local",
                    "detail-type": "Local Testing",
                    "detail": json.dumps(detail),
                }
            ]
        }

    @staticmethod
    def _randomize(event_data, app_count=1):
        fake = Faker()
        detail = json.loads(event_data["Records"][0]["detail"])
        for i in range(app_count - len(detail["applications"])):
            detail["applications"].append(
                {
                    "borrower": {"mailingAddress": {}},
                    "coborrower": {"mailingAddress": {}},
                }
            )
        for i in range(app_count):
            for borrower in detail["applications"][i].values():
                borrower["firstName"] = fake.first_name()
                borrower["lastName"] = fake.last_name()
                address = borrower["mailingAddress"]
                address["addressStreetLine1"] = fake.street_address()
                address["addressCity"] = fake.city()
                address["addressState"] = fake.country_code()
                address["addressPostalCode"] = fake.postcode()
        return detail

    def test_ftr_cc_01_unique_residences(self):
        # with open(os.path.join("tests", "loandata.json")) as file:
        #     event = self._generate_event(json.load(file))
        #     for record in event["Records"]:
        #         record["detail"] = json.loads(record["detail"])
        #     logging.info(f"EVENT:\n{json.dumps(event, indent=2)}")

        with open(LOAN_DATA_FILE) as file:
            event = self._generate_event(json.load(file))

        response = main(event)

        # logging.info('REPORTS: %s', json.dumps(response, indent=2))
        for report in response["reports"]:
            if report["title"] == "Residences Report":
                self.assertEqual(len(report["residences"]), 1)

        event = self._generate_event(detail=self._randomize(event))

        response = main(event)
        for report in response["reports"]:
            if report["title"] == "Residences Report":
                self.assertEqual(len(report["residences"]), 2)

    def test_ftr_cc_02_shared_address(self):
        with open(LOAN_DATA_FILE) as file:
            event = self._generate_event(json.load(file))

        response = main(event)

        for report in response["reports"]:
            if report["title"] == "Borrowers Report":
                self.assertTrue(report["shared_address"])

        event = self._generate_event(detail=self._randomize(event))

        response = main(event)
        for report in response["reports"]:
            if report["title"] == "Borrowers Report":
                self.assertFalse(report["shared_address"])

    def test_ftr_cc_03_multiple_applications(self):
        with open(LOAN_DATA_FILE) as file:
            event = self._generate_event(json.load(file))
        event = self._generate_event(detail=self._randomize(event, app_count=5))
        response = main(event)
        for report in response["reports"]:
            if report["title"] == "Borrowers Report":
                # TODO: Assert proper length of the "Borrowers Report" after
                #  proper reorganization of the reports' structure
                self.assertTrue(True)
