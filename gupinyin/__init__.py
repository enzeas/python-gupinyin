#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""汉字古拼音转换工具."""

from __future__ import unicode_literals

from gupinyin.constants import Style, STYLE_NORMAL, NORMAL
from gupinyin.core import pinyin, lazy_pinyin, slug


__title__ = 'pypinyin'
__version__ = '0.1.0'
__author__ = 'enzeas, 恩泽'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2019 mozillazg, 恩泽'
__all__ = [
    'pinyin', 'lazy_pinyin', 'slug',
    'Style', 'STYLE_NORMAL', 'NORMAL',
]
