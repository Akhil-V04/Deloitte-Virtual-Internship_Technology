import json
import unittest
from datetime import datetime, timezone


def convertFromFormat1(jsonObject):
    location_parts = jsonObject["location"].split("/")
    location_keys = ["country", "city", "area", "factory", "section"]

    return {
        "deviceID": jsonObject["deviceID"],
        "deviceType": jsonObject["deviceType"],
        "timestamp": jsonObject["timestamp"],
        "location": dict(zip(location_keys, location_parts)),
        "data": {
            "status": jsonObject["operationStatus"],
            "temperature": jsonObject["temp"]
        }
    }


def convertFromFormat2(jsonObject):
    # fromisoformat doesn't handle trailing 'Z' in Python < 3.11
    iso_str = jsonObject["timestamp"].rstrip("Z")
    dt = datetime.fromisoformat(iso_str).replace(tzinfo=timezone.utc)
    timestamp_ms = int(dt.timestamp() * 1000)

    return {
        "deviceID": jsonObject["device"]["id"],
        "deviceType": jsonObject["device"]["type"],
        "timestamp": timestamp_ms,
        "location": {
            "country": jsonObject["country"],
            "city": jsonObject["city"],
            "area": jsonObject["area"],
            "factory": jsonObject["factory"],
            "section": jsonObject["section"]
        },
        "data": jsonObject["data"]
    }


class TestTelemetryConversion(unittest.TestCase):

    def setUp(self):
        with open("data-1.json") as f:
            self.format1 = json.load(f)
        with open("data-2.json") as f:
            self.format2 = json.load(f)
        with open("data-result.json") as f:
            self.expected = json.load(f)

    def test_format1_deviceID(self):
        result = convertFromFormat1(self.format1)
        self.assertEqual(result["deviceID"], self.expected["deviceID"])

    def test_format1_deviceType(self):
        result = convertFromFormat1(self.format1)
        self.assertEqual(result["deviceType"], self.expected["deviceType"])

    def test_format1_timestamp(self):
        result = convertFromFormat1(self.format1)
        self.assertEqual(result["timestamp"], self.expected["timestamp"])

    def test_format1_location(self):
        result = convertFromFormat1(self.format1)
        self.assertEqual(result["location"], self.expected["location"])

    def test_format1_data(self):
        result = convertFromFormat1(self.format1)
        self.assertEqual(result["data"], self.expected["data"])

    def test_format1_full(self):
        result = convertFromFormat1(self.format1)
        self.assertEqual(result, self.expected)

    def test_format2_deviceID(self):
        result = convertFromFormat2(self.format2)
        self.assertEqual(result["deviceID"], self.expected["deviceID"])

    def test_format2_deviceType(self):
        result = convertFromFormat2(self.format2)
        self.assertEqual(result["deviceType"], self.expected["deviceType"])

    def test_format2_timestamp(self):
        result = convertFromFormat2(self.format2)
        self.assertEqual(result["timestamp"], self.expected["timestamp"])

    def test_format2_location(self):
        result = convertFromFormat2(self.format2)
        self.assertEqual(result["location"], self.expected["location"])

    def test_format2_data(self):
        result = convertFromFormat2(self.format2)
        self.assertEqual(result["data"], self.expected["data"])

    def test_format2_full(self):
        result = convertFromFormat2(self.format2)
        self.assertEqual(result, self.expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
