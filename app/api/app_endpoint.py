import configparser
import os

from flask import Flask, request, render_template, Response
import json
import logging.config
from clients import market_data_client

logger = logging.getLogger("app_endpoint")

def get_user_list(user_list_config_file):
    logger.info("User Config File:" + user_list_config_file)
    config = configparser.ConfigParser()
    if os.path.isfile(user_list_config_file):
        config.read(user_list_config_file)
        users = config.get('USERS', 'USER_LIST')
        user_list = users.split(',')
        return user_list
    else:
        logger.error("Config File Not found:" + user_list_config_file + ".. Cannot Continue!!")
        SystemExit(-1)


def run_app(my_host, my_port):
    app = Flask(__name__, template_folder='../templates')
    user_list_config_file_path = 'config/user_white_list.ini'
    user_list = get_user_list(user_list_config_file_path)
    logger.info("Allowed Users:" + str(user_list))

    # @app.route('/api/v1/currencies/quotes', methods=['GET'])
    # def api_get():
    #     logger.debug("api_get called")
    #     if 'symbol' in request.args and request.args['symbol']:
    #         symbol = request.args['symbol']
    #     else:
    #         error = {
    #             'Exception': "Error: Symbol Not Provided",
    #         }
    #         logger.error(str(error))
    #         return json.dumps(error)
    #
    #     if 'limit' in request.args and request.args['limit']:
    #         limit = request.args['limit']
    #     else:
    #         limit = DEFAULT_ORDER_DEPTH
    #
    #     data_processed = my_client.get_data(symbol, limit)
    #     return data_processed
    #     ##return json2html.convert(json=data_processed)

    @app.route('/<username>', methods=['GET'])
    def api_authenticate(username):
        logger.debug("api_authenticate called")
        callerIpAddress = request.remote_addr
        callerUser = request.remote_user
        logger.info("api_authenticate callerIpAddress:" + str(callerIpAddress))
        logger.info("api_authenticate callerUser:" + str(callerUser))
        if user_list.count(username):
            logger.debug("api_authenticate SUCCESS")
            return """
                    {
                      "logon": true,
                      "replication-logon": true,
                      "topic": [{
                          "topic": ".*",
                          "read": true,
                          "write": true
                        }],
                      "admin": [{
                          "topic": "/amps/administrator",
                          "read": true,
                          "write": true
                        }]
                    }
                """

        else:
            """Sends a 401 response that enables basic auth"""
            return Response(
                'Could not verify your access level for that URL.\n'
                'You have to login with proper credentials', 401,
                {'WWW-Authenticate': 'Basic realm="AMPS Authentication"'}
            )



    @app.errorhandler(404)
    def page_not_found(e):
        return "<h1>404</h1><p>The resource could not be found.</p>", 404

    #@app.route("/")
    #def index():
    #    return render_template("index.html")

    app.run(host=my_host, port=my_port)
