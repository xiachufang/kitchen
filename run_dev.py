#!/usr/bin/env python
from kitchen.app import app


app.run(host='0.0.0.0', debug=True, port=12345)
