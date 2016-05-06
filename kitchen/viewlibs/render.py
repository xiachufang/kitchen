#!/usr/bin/env python
# coding: utf-8
from flask import jsonify


def ok(content=''):
    msg = {
        'status': 'ok',
        'content': content,
    }

    resp = jsonify(msg)
    return resp


def error(error='', status_code=400):
    if callable(error):
        error = error()

    if isinstance(error, (tuple, list)):
        msg = {
            'status': 'error',
            'code': error[0],
            'msg': error[1],
        }
    else:
        msg = {
            'status': 'error',
            'msg': error,
        }

    resp = jsonify(msg)
    return resp, status_code
