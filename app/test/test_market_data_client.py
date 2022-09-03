import mock
import unittest
import json
from requests.exceptions import RequestException
from requests.exceptions import HTTPError
from clients import market_data_client


class TestMarketDataClient(unittest.TestCase):

    @staticmethod
    def _mock_response(
            status=200,
            content="CONTENT",
            headers={
                'content-type': 'application/json'
            },
            json_data={
                "asks": [
                    [
                        "43526.73000000",
                        "2.02912300"
                    ]
                ],
                "bids": [
                    [
                        "43526.72000000",
                        "0.11478000"
                    ]
                ]
            },
            raise_for_status=None):

        mock_resp = mock.Mock()
        mock_resp.raise_for_status = mock.Mock()

        if raise_for_status:
            mock_resp.raise_for_status.side_effect = raise_for_status

        mock_resp.status_code = status
        mock_resp.content = content

        mock_resp.headers = headers

        mock_resp.text = content

        if json_data:
            mock_resp.json = mock.Mock(
                return_value=json_data
            )
        return mock_resp

    @mock.patch('requests.get')
    def test_get_data_binance_client_success(self, mock_get):
        mock_resp = self._mock_response()
        mock_get.return_value = mock_resp
        config_file = 'config/binance_endpoints.ini'
        test = market_data_client.BinanceMarketDataClient(config_file)
        result = test.get_data('ABC', '1')
        self.assertTrue('asks' in result)
        self.assertTrue('bids' in result)

    @mock.patch('requests.get')
    def test_get_data_binance_client_check_response_json(self, mock_get):
        mock_resp = self._mock_response()
        mock_get.return_value = mock_resp
        config_file = 'config/binance_endpoints.ini'
        test = market_data_client.BinanceMarketDataClient(config_file)
        result = test.get_data('ABC', '1')
        output_json = json.dumps(result)
        self.assertTrue(self.validate_JSON(output_json))

    @mock.patch('requests.get')
    def test_get_data_binance_client_content_type(self, mock_get):
        mock_resp = self._mock_response(headers={
            'content-type': 'application/txt'
        })
        mock_get.return_value = mock_resp
        config_file = 'config/binance_endpoints.ini'
        test = market_data_client.BinanceMarketDataClient(config_file)
        result = test.get_data('ABC', '1')
        self.assertFalse('asks' in result)
        self.assertFalse('bids' in result)
        self.assertTrue('CONTENT' in result)

    @mock.patch('requests.get')
    def test_get_data_binance_client_HTTPError(self, mock_get):
        mock_resp = self._mock_response(status=400, raise_for_status=HTTPError("HTTPError"))
        mock_get.return_value = mock_resp
        config_file = 'config/binance_endpoints.ini'
        test = market_data_client.BinanceMarketDataClient(config_file)
        result = test.get_data('ABC', '1')
        self.assertTrue('HTTPError' in result)

    @mock.patch('requests.get')
    def test_get_data_binance_client_RequestException(self, mock_get):
        mock_resp = self._mock_response(status=404, raise_for_status=RequestException("RequestException"))
        mock_get.return_value = mock_resp
        config_file = 'config/binance_endpoints.ini'
        test = market_data_client.BinanceMarketDataClient(config_file)
        result = test.get_data('ABC', '1')
        self.assertTrue('RequestException' in result)

    @staticmethod
    def validate_JSON(json_data):
        try:
            json.loads(json_data)
        except ValueError as err:
            return False
        return True


if __name__ == '__main__':
    unittest.main()
