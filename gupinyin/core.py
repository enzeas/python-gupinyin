#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from copy import deepcopy
from itertools import chain

from gupinyin.compat import text_type, callable_check
from gupinyin.constants import PHRASES_DICT, PINYIN_DICT, RE_HANS, Style
from gupinyin.contrib import mmseg
from gupinyin.utils import simple_seg, _remove_dup_items


def seg(hans):
    hans = simple_seg(hans)
    ret = []
    for x in hans:
        if not RE_HANS.match(x):   # 没有拼音的字符，不再参与二次分词
            ret.append(x)
        elif PHRASES_DICT:
            ret.extend(list(mmseg.seg.cut(x)))
        else:   # 禁用了词语库，不分词
            ret.append(x)
    return ret


def _to_fixed(pinyin, style):
    """根据拼音风格格式化带声调的拼音.
    :param pinyin: 单个拼音
    :param style: 拼音风格
    :return: 根据拼音风格格式化后的拼音字符串
    :rtype: unicode
    """
    # TODO(enze): add more style
    return pinyin


def _handle_nopinyin_char(chars, errors='default'):
    """处理没有拼音的字符"""
    if callable_check(errors):
        return errors(chars)
    if errors == 'default':
        return chars
    if errors == 'ignore':
        return None


def handle_nopinyin(chars, errors='default', heteronym=True):
    py = _handle_nopinyin_char(chars, errors=errors)
    if not py:
        return []
    if isinstance(py, list):
        # 包含多音字信息
        if isinstance(py[0], list):
            if heteronym:
                return py
            # [[a, b], [c, d]]
            # [[a], [c]]
            return [[x[0]] for x in py]
        return [[i] for i in py]
    return [[py]]


def single_pinyin(han, style, heteronym, errors='default'):
    """单字拼音转换.
    :param han: 单个汉字
    :param errors: 指定如何处理没有拼音的字符
    :return: 返回拼音列表，多音字会有多个拼音项
    :rtype: list
    """
    num = ord(han)
    # 处理没有拼音的字符
    if num not in PINYIN_DICT:
        return handle_nopinyin(han, errors=errors, heteronym=heteronym)

    pys = PINYIN_DICT[num].split(',')  # 字的拼音列表
    if not heteronym:
        return [[_to_fixed(pys[0], style)]]

    # 输出多音字的多个读音
    # 临时存储已存在的拼音，避免多音字拼音转换为非音标风格出现重复。
    # TODO: change to use set
    # TODO: add test for cache
    py_cached = {}
    pinyins = []
    for i in pys:
        py = _to_fixed(i, style)
        if py in py_cached:
            continue
        py_cached[py] = py
        pinyins.append(py)
    return [pinyins]


def phrase_pinyin(phrase, style, heteronym, errors='default'):
    """词语拼音转换.

    :param phrase: 词语
    :param errors: 指定如何处理没有拼音的字符
    :return: 拼音列表
    :rtype: list
    """
    py = []
    if phrase in PHRASES_DICT:
        py = deepcopy(PHRASES_DICT[phrase])
        for idx, item in enumerate(py):
            if heteronym:
                py[idx] = _remove_dup_items([
                    _to_fixed(x, style=style) for x in item])
            else:
                py[idx] = [_to_fixed(item[0], style=style)]
    else:
        for i in phrase:
            single = single_pinyin(i, style=style, heteronym=heteronym,
                                   errors=errors)
            if single:
                py.extend(single)
    return py


def _pinyin(words, style, heteronym, errors):
    """
    :param words: 经过分词处理后的字符串，只包含中文字符或只包含非中文字符，
                  不存在混合的情况。
    """
    pys = []
    # 初步过滤没有拼音的字符
    if RE_HANS.match(words):
        pys = phrase_pinyin(words, style=style, heteronym=heteronym,
                            errors=errors)
        return pys

    py = handle_nopinyin(words, errors=errors, heteronym=heteronym)
    if py:
        pys.extend(py)
    return pys


def pinyin(hans, style=Style.NORMAL, heteronym=False, errors='default'):
    """将汉字转换为拼音.
    :param hans: 汉字字符串( '你好吗' )或列表( ['你好', '吗'] ).
                 可以使用自己喜爱的分词模块对字符串进行分词处理,
                 只需将经过分词处理的字符串列表传进来就可以了。
    :type hans: unicode 字符串或字符串列表
    :param style: 指定拼音风格，默认是 gupinyin.Style.NORMAL 风格。
                  更多拼音风格详见 gupinyin.Style
    :param errors: 指定如何处理没有拼音的字符。详见 handle_no_pinyin
                   * 'default': 保留原始字符
                   * 'ignore': 忽略该字符
                   * callable 对象: 回调函数之类的可调用对象。
    :param heteronym: 是否启用多音字
    :return: 拼音列表
    :rtype: list
    :raise AssertionError: 当传入的字符串不是 unicode 字符时会抛出这个异常

    Usage::
      >>> from gupinyin import pinyin, Style
      >>> import gupinyin
      >>> pinyin('中心')
      ['triung', 'sim']
      >>> pinyin('中心', style=Style.FIRST_LETTER)
      ['tr', 's']
    """
    # 对字符串进行分词处理
    if isinstance(hans, text_type):
        han_list = seg(hans)
    else:
        han_list = chain(*(seg(x) for x in hans))
    pys = []
    for words in han_list:
        pys.extend(_pinyin(words, style, heteronym, errors))
    return pys


def slug(hans, style=Style.NORMAL, heteronym=False, separator='-', errors='default'):
    """生成 slug 字符串.
    :param hans: 汉字
    :type hans: unicode or list
    :param style: 指定拼音风格，默认是 gupinyin.Style.NORMAL 风格。
                  更多拼音风格详见 gupinyin.Style
    :param heteronym: 是否启用多音字
    :param separstor: 两个拼音间的分隔符/连接符
    :param errors: 指定如何处理没有拼音的字符，详情请参考
                   gupinyin.pinyin
    :return: slug 字符串.
    :raise AssertionError: 当传入的字符串不是 unicode 字符时会抛出这个异常
    ::

      >>> import gupinyin
      >>> from gupinyin import Style
      >>> gupinyin.slug('中國人')
      'triung-kuok-njin'
      >>> gupinyin.slug('中国人', separator=' ')
      'triung kuok njin'
      >>> gupinyin.slug('中国人', style=Style.FIRST_LETTER)
      'z-g-r'
    """
    return separator.join(chain(*pinyin(hans, style=style, heteronym=heteronym,
                                        errors=errors)))


def lazy_pinyin(hans, style=Style.NORMAL, errors='default'):
    """不包含多音字的拼音列表.
    与 gupinyin.pinyin 的区别是返回的拼音是个字符串，
    并且每个字只包含一个读音.
    :param hans: 汉字
    :type hans: unicode or list
    :param style: 指定拼音风格，默认是 gupinyin.Style.NORMAL 风格。
                  更多拼音风格详见 gupinyin.Style。
    :param errors: 指定如何处理没有拼音的字符，详情请参考
                   gupinyin.pinyin
    :return: 拼音列表(e.g. ``['triung', 'kuok', 'njin']``)
    :rtype: list
    :raise AssertionError: 当传入的字符串不是 unicode 字符时会抛出这个异常
    Usage::
      >>> from gupinyin import lazy_pinyin, Style
      >>> import gupinyin
      >>> lazy_pinyin('中心')
      ['triung', 'sim']
      >>> lazy_pinyin('中心', style=Style.FIRST_LETTER)
      ['tr', 's']
    """
    return list(chain(*pinyin(hans, style=style, heteronym=False,
                              errors=errors)))
