# 汉字古拼音转换工具

将汉字转为古拼音。可为学术研究（语言学、汉学、人类学等）提供参考资料 。

基于 [pypinyin](https://github.com/mozillazg/python-pinyin)开发。

* Documentation: 
* GitHub: https://github.com/enzeas/python-gupinyin
* License: MIT license
* PyPI: 
* Python version: pypy3, 3.4, 3.5, 3.6, 3.7

## 特性

* 根据词组智能匹配最正确的拼音。
* 支持多音字。
* 繁体支持, 注音支持。
* 支持多种不同拼音/注音风格。

## 安装

    $ pip install pygupinyin

## 使用示例

    >>> from gupinyin import pinyin, lazy_pinyin, Style
    >>> pinyin('中心')
    [['zhōng'], ['xīn']]
    >>> pinyin('中心', heteronym=True)  # 启用多音字模式
    [['zhōng', 'zhòng'], ['xīn']]
    >>> pinyin('中心', style=Style.FIRST_LETTER)  # 设置拼音风格
    [['z'], ['x']]
    >>> pinyin('中心', style=Style.TONE2, heteronym=True)
    [['zho1ng', 'zho4ng'], ['xi1n']]
    >>> lazy_pinyin('中心')  # 不考虑多音字的情况
    ['zhong', 'xin']

## FAQ

Q: 词语中的多音字拼音有误？

A: 目前是通过词组拼音库的方式来解决多音字问题的。如果出现拼音有误的情况，
可以自定义词组拼音来调整词语中的拼音：

    >>> from gupinyin import Style, pinyin, load_phrases_dict
    >>> pinyin('步履蹒跚')
    [['bù'], ['lǚ'], ['mán'], ['shān']]
    >>> load_phrases_dict({'步履蹒跚': [['bù'], ['lǚ'], ['pán'], ['shān']]})
    >>> pinyin('步履蹒跚')
    [['bù'], ['lǚ'], ['pán'], ['shān']]

Q: 为什么没有 y, w, yu 几个声母？

    >>> from gupinyin import Style, pinyin
    >>> pinyin('下雨天', style=Style.INITIALS)
    [['x'], [''], ['t']]

A: 因为根据 [《汉语拼音方案》](http://www.moe.edu.cn/s78/A19/yxs_left/moe_810/s230/195802/t19580201_186000.html)，
y，w，ü (yu) 都不是声母。

## 拼音数据

* 单个汉字的拼音使用 `pinyin-data` 的数据
* 词组的拼音使用 `phrase-pinyin-data` 的数据


## Related Projects

- [mozillazg/python-pinyin](https://github.com/mozillazg/python-pinyin)