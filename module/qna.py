# -*- coding: utf-8 -*-

import xmlrpclib


def quest(question):
    _RPC = xmlrpclib.Server("")
    return _RPC.qa(question)
