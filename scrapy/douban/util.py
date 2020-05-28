#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib


def shorturl(url):
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    _hex = 0x7ffffff & int(str(hashlib.md5(url.encode('utf-8')).hexdigest()),
                           16)
    code = ''
    for i in range(9):
        index = 0x0000003d & _hex
        code += chars[index]
        _hex = _hex >> 3
    return code
