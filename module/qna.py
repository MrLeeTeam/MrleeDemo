# -*- coding: utf-8 -*-

import xmlrpclib


def quest(question):
    _RPC = xmlrpclib.Server("http://58.229.105.83:8050")
    return _RPC.qa(question)

print quest()