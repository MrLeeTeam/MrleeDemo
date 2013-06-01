# -*- coding: utf-8 -*-

import xmlrpclib
import os


def do(path):
    _RPC = xmlrpclib.Server("http://leeee.kr:8050")
    returnee = _RPC.image_search(path)
    return returnee

path = os.path.abspath("../photo.jpg")
print path
print do(path)