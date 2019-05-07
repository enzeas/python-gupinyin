# -*- coding: utf-8 -*-
import sys


def parse(in_fp):
    pinyin_dict = {}
    phrases_dict = {}
    for line in in_fp.readlines():
        line = line.strip()
        if line.startswith('#') or not line:
            continue
        arr = line.split('\t')
        if len(arr) < 2:
            continue
        hans, pinyin = arr[:2]
        if len(hans) > 1 :
            phrases_dict[hans] = pinyin.split(' ')
            continue
        if hans in pinyin_dict:
            pinyin_dict[hans] = '{},{}'.format(pinyin_dict[hans], pinyin)
        else:
            pinyin_dict[hans] = pinyin
    return pinyin_dict, phrases_dict

def format_pinyin(pinyin_dict):
    with open('pinyin_dict.py', 'w') as out_fp:
        out_fp.write('''# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Warning: Auto-generated file, don't edit.
pinyin_dict = {
''')
        for hans, pinyin in pinyin_dict.items():
            new_line = '0x{hans:x}: "{pinyin}"'.format(hans=ord(hans),pinyin=pinyin)
            new_line = '    {new_line},\n'.format(new_line=new_line)
            out_fp.write(new_line)
        out_fp.write('}\n')

def format_phrases(phrases_dict):
    with open('phrases_dict.py', 'w') as out_fp:
        out_fp.write('''# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Warning: Auto-generated file, don't edit.
phrases_dict = {
''')
        for hans, pinyin in phrases_dict.items():
            new_line = '"{hans}": {pinyin}'.format(hans=hans,pinyin=[[x] for x in pinyin])
            new_line = '    {new_line},\n'.format(new_line=new_line)
            out_fp.write(new_line)
        out_fp.write('}\n')



def main(in_fp):
    pinyin_dict, phrases_dict = parse(in_fp)
    format_pinyin(pinyin_dict)
    format_phrases(phrases_dict)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('python gen_pinyin_dict.py INPUT')
        sys.exit(1)
    in_f = sys.argv[1]

    with open(in_f) as in_fp:
        main(in_fp)
