#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
from datetime import datetime

from flask import Flask, Response, request

_HOST = "localhost"
_PORT = 3418
_API_BASE = "/api"

app = Flask(__name__)


@app.route('/hello', methods=['GET', 'POST'])
def hello():
    rsp_data = {"status": "healthy", "time": str(datetime.now())}
    rsp_str = json.dumps(rsp_data)
    rsp = Response(rsp_str, status=200, content_type="application/json")
    return rsp


@app.route('/api/orig', methods=['POST'])
def orig():
    try:
        logging.info("receive video and return original video for api testing")
        data = request.data
        return data, 200
    except ValueError or AssertionError as e:
        logging.error(e)
        return "Internal error.", 504, {
            'Content-Type': 'text/plain; charset=utf-8'}


if __name__ == '__main__':
    logging.info("Run application at " + str(datetime.now()))
    app.run(host=_HOST, port=_PORT)
