# -*- coding: utf-8 -*-

import xmlrpclib


def do(path):
    _RPC = xmlrpclib.Server("")
    returnee = _RPC.image_search(path)
    return returnee
