# -*- coding: utf-8 -*-

import xmlrpclib


def inspector(arg, p=None):
    _RPC = xmlrpclib.Server("")
    d = None
    if p == "seg":
        d = _RPC.BuzzniTagger.jossegment(arg)
    else:
        d = _RPC.BuzzniTagger.postagging(arg)
    return d
