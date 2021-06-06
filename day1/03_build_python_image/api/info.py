"""
    Main API module
"""
import os
import logging
import time
import jsonpickle
import redis
from flask import Flask, request

LOGGER = logging.getLogger("test")
FORMATTER = logging.Formatter('%(asctime)s %(levelname)s %(message)s')  # format
CONSOLEHANDLER = logging.StreamHandler()
CONSOLEHANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(CONSOLEHANDLER)

level = os.environ.get("LOG_LEVEL","INFO")
if level == "INFO":
    LOGGER.setLevel(logging.INFO)
if level == "DEBUG":
    LOGGER.setLevel(logging.DEBUG)


APP = Flask(__name__)


@APP.route('/healthz')
def hello_world():
    """
        Healthz endpoint to check service status
    """
    return "Service is OK"

@APP.route('/api/v1/info', methods=['POST'])
def info_post():
    redis_host =  os.environ.get("REDIS_HOST","redis")
    redis_port =  os.environ.get("REDIS_PORT",6379)
    r = redis.Redis(host=redis_host, port=redis_port, db=0)
    previous = r.get('counter')
    if previous is None:
        r.set('counter', 1)
    else:
        r.incr('counter')

    response = APP.response_class(
        response="OK",
        status=200,
        mimetype='application/json'
    )
    return response

@APP.route('/api/v1/info', methods=['GET'])
def info():
    """
        Base invocation API endpoint
    """
    redis_host =  os.environ.get("REDIS_HOST","redis")
    redis_port =  os.environ.get("REDIS_PORT",6379)
    r = redis.Redis(host=redis_host, port=redis_port, db=0)
    counter =  r.get('counter')
    if counter is None:
        counter = 0
    else:
        counter = counter.decode('utf-8')

    LOGGER.info('counter var is %s', counter)
    started_at = time.time()

    response_payload = {'counter': counter}

    response = APP.response_class(
        response=jsonpickle.encode(response_payload, unpicklable=False),
        status=200,
        mimetype='application/json'
    )
    duration = time.time() - started_at
    LOGGER.debug('Request took %s', duration)
    return response
