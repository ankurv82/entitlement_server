import configparser
import logging.config
import os

from api import app_endpoint

logging.config.fileConfig('config/logging.ini')

logger = logging.getLogger("app_server")


def main():
    logger.info('Started')
    config = configparser.ConfigParser()
    default_app_config_file = 'config/app_server.ini'
    if os.path.isfile(default_app_config_file):
        config.read(default_app_config_file)
        hostname = config.get('DEFAULT', 'HOST')
        port = config.get('DEFAULT', 'PORT')
        app_endpoint.run_app(hostname, port)
    else:
        logger.error("Config File Not found" + default_app_config_file + ".. Cannot Continue!!")
        SystemExit(-1)


if __name__ == '__main__':
    main()
