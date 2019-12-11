#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import os
from datetime import datetime

from flask import Flask, Response, request, send_file

from data_utils import video_utils
from demo_tools import osvos_demo

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


@app.route('/api/infer', methods=['GET', 'POST'])
def infer():
    try:
        logging.info("receive video and analysis original video")
        if request.method == 'POST':
            video_file = request.files.get("File")
            first_mask = request.files.get("Frame")
            video_name = request.form.get("videoname")
            video_name = os.path.splitext(video_name)[0]
            video_path, img_path, first_mask_path = video_utils.init_video(
                video_name)

            video_name_res = video_name + "-concat.mp4"
            if video_name_res in video_utils.cached_video:
                logging.info("Hit video in the cache")
                return send_file(
                    os.path.join(video_path).replace(".mp4", "-concat.mp4"))

            video_file.save(video_path)
            first_mask.save(first_mask_path)

            tag = video_name not in video_utils.cached_model
            if tag:
                logging.info("Hit previous model weight")
            else:
                logging.info("finetune pre-trained model for new sequence")
            video_utils.video2img(video_path, img_path)
            osvos_demo.demo(seq_name=video_name, first_mask=first_mask_path,
                            img_path=img_path,
                            result_path=os.path.join('tmp', video_name, 'pred'),
                            concate_path=os.path.join('tmp', video_name,
                                                      'concat'),
                            train_model=tag)
            result_video_path = video_utils.render_video(video_name)

            return send_file(result_video_path)
        else:
            raise ValueError("Not support GET method")
    except ValueError or AssertionError as e:
        logging.error(e)
        return "Internal error.", 504, {
            'Content-Type': 'text/plain; charset=utf-8'}


if __name__ == '__main__':
    logging.info("Run application at " + str(datetime.now()))
    app.run(host=_HOST, port=_PORT)
