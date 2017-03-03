#-*-coding:utf-8-*-
"""
处理有道单词本产生的txt文件
"""

import re
import codecs
from string import lower

from worddict import WordDict

if __name__ == '__main__':
    wordDict = {}
    # 读取utf-8格式的文件
    with codecs.open("youdaowordbook.txt",'r','utf-8') as f:
        for line in f:
            # 数字开头的行
            pattern = re.compile(r'^\d+.*')
            match = pattern.search(line)
            if match:
                split = line.split()
                word = lower(split[1].strip())
                wordDict[word] = wordDict.get(word,0)+1
    print "word number:", len(wordDict)
    #wd = WordDict("youdaodict.txt")
    wd = WordDict()
    wd.update(wordDict)