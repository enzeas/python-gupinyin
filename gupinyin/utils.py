#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from itertools import chain
import re

from gupinyin.compat import text_type, bytes_type
from gupinyin.constants import RE_HANS, RE_TONE2


def _seg(chars):
    """按是否是汉字进行分词"""
    s = ''
    ret = []
    flag = 0
    for n, c in enumerate(chars):
        if RE_HANS.match(c):
            if n == 0:
                flag = 0
            if flag == 0:
                s += c
            else:
                ret.append(s)
                flag = 0
                s = c
        else:
            if n == 0:
                flag = 1
            if flag == 1:
                s += c
            else:
                ret.append(s)
                flag = 1
                s = c
    ret.append(s)
    return ret


def simple_seg(hans):
    """将传入的字符串按是否是汉字来分割"""
    assert not isinstance(hans, bytes_type), \
        'must be unicode string or [unicode, ...] list'

    if isinstance(hans, text_type):
        return _seg(hans)
    else:
        hans = list(hans)
        if len(hans) == 1:
            return simple_seg(hans[0])
        return list(chain(*[simple_seg(x) for x in hans]))

def _remove_dup_items(lst):
    new_lst = []
    for item in lst:
        if item not in new_lst:
            new_lst.append(item)
    return new_lst
