import unittest

from api.portal import access_portal_payload, acknowledge_payload
from care_portal.records import AccessDeniedError


class PortalPrivacyTests(unittest.TestCase):
    def test_demo_code_returns_only_neutral_document_availability(self):
        payload = access_portal_payload({"access_code": "DEMO-4821"})
        self.assertTrue(payload["success"])
        self.assertTrue(payload["data"]["demo"])
        self.assertNotIn("patient_name", str(payload))
        self.assertNotIn("diagnosis", str(payload))

    def test_invalid_code_has_a_generic_error(self):
        with self.assertRaises(AccessDeniedError) as error:
            access_portal_payload({"access_code": "wrong"})
        self.assertNotIn("wrong", str(error.exception))

    def test_follow_up_request_requires_a_known_opaque_record_id(self):
        payload = acknowledge_payload({"access_code": "DEMO-4821", "record_id": "result-01"})
        self.assertTrue(payload["success"])
        with self.assertRaises(ValueError):
            acknowledge_payload({"access_code": "DEMO-4821", "record_id": "unknown"})
