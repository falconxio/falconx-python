import unittest

from falconx.client import FalconxClient


class FakeResponse:
    status_code = 200
    text = ""

    @staticmethod
    def json():
        return {"status": "success"}


class FakeSession:
    def __init__(self):
        self.calls = []
        self.auth = None

    def post(self, url, **kwargs):
        self.calls.append((url, kwargs))
        return FakeResponse()


class FalconxClientTest(unittest.TestCase):
    def test_place_order_uses_v1_by_default(self):
        client = FalconxClient("key", "secret", "passphrase")
        session = FakeSession()
        client.session = session

        result = client.place_order("ETH", "USD", 1.0, "buy", "market")

        self.assertEqual(result["status"], "success")
        self.assertEqual(session.calls[0][0], "https://api.falconx.io/v1/order")
        self.assertEqual(session.calls[0][1]["timeout"], (10, 30))

    def test_place_order_uses_v3_when_requested(self):
        client = FalconxClient("key", "secret", "passphrase")
        session = FakeSession()
        client.session = session

        client.place_order("ETH", "USD", 1.0, "buy", "market", v3=True)

        self.assertEqual(session.calls[0][0], "https://api.falconx.io/v3/order")


if __name__ == "__main__":
    unittest.main()
