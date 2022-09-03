import abc
import os
import requests
import json
import logging
import configparser

logger = logging.getLogger("market_data_client")


class MarketDataClient(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_data') and
                callable(subclass.get_data))


class BinanceMarketDataClient:
    base_url = ''
    endpoint = ''
    final_url = ''
    config = None

    # default constructor
    def __init__(self, config_file_path):
        self.init_config(config_file_path)

    def init_config(self, config_file_path):
        config = configparser.ConfigParser()
        if os.path.isfile(config_file_path):
            config.read(config_file_path)
            self.base_url = config.get('DEFAULT', 'BASE_URL')
            self.endpoint = config.get('DEFAULT', 'API_ENDPOINT')
            self.final_url = self.base_url + self.endpoint
            logger.info("Client URL : " + self.final_url)

        else:
            logger.error("Config File Not found" + config_file_path + ".. Cannot Continue!!")
            SystemExit(-1)

    def get_data(self, symbol: str, limit: str) -> str:

        # defining a params dict for the parameters to be sent to the API
        query_param = {'symbol': symbol, 'limit': limit}
        result = ''
        response = ''
        try:
            # sending get request and saving the response as response object
            logger.debug(self.final_url + str(query_param))
            response = requests.get(url=self.final_url, params=query_param)
            logger.debug(str(response.text))

            # extracting data in json format
            if response.status_code == requests.codes.ok and ('application/json' in response.headers['content-type']):
                result = response.json()
            else:
                output = {
                    'Response': str(response.text)
                }
                result = json.dumps(output)

            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            error = {
                'Exception': str(e),
                'Response': str(response.text)
            }
            result = json.dumps(error)
            logger.error(result)

        except requests.exceptions.RequestException as e:
            error = {
                'Exception': str(e)
            }
            result = json.dumps(error)
            logger.error(result)

        return result
