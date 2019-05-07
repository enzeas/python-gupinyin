#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

SUPPORT_UCS4 = len('\U00020000') == 1

text_type = str
bytes_type = bytes

try:
    callable_check = callable  # noqa
except NameError:
    def callable_check(obj):
        return hasattr(obj, '__call__')
