#-*-coding:utf-8-*-
"""
采集http://www.dictall.com中的计算机相关词汇
"""
from string import lower
import urllib2;
from bs4 import BeautifulSoup
from bs4.element import NavigableString
from worddict import WordDict
class Dictall:
    
    def ExtractEnWords(self, url):
        """
        提取英语单词，返回一个字典，key为单词，value为出现次数
        """
        words = {}
        u = urllib2.urlopen(url)
        if u.getcode() == 200:
            buffer = u.read()
            soup = BeautifulSoup(buffer)
            div = soup.find('div',{'id':'catelist'})
            if not div:
                return words
            for a in div.find_all('a'):
                x = a.get_text().split('：')
                word = lower(x[1].strip())
                words[word] = words.get(word, 0) + 1
        return words
def is_zh (uchar):
    """
    判断一个unicode字符是否为中文
    """
    x = ord (uchar)
    # Punct & Radicals
    if x >= 0x2e80 and x <= 0x33ff:
        return True

    # Fullwidth Latin Characters
    elif x >= 0xff00 and x <= 0xffef:
        return True

    # CJK Unified Ideographs &
    # CJK Unified Ideographs Extension A
    elif x >= 0x4e00 and x <= 0x9fbb:
        return True
    # CJK Compatibility Ideographs
    elif x >= 0xf900 and x <= 0xfad9:
        return True

    # CJK Unified Ideographs Extension B
    elif x >= 0x20000 and x <= 0x2a6d6:
        return True

    # CJK Compatibility Supplement
    elif x >= 0x2f800 and x <= 0x2fa1d:
        return True
    
    else:
        return False

def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
        return True
    else:
        return False
    
def is_number(uchar):
    """判断一个unicode是否是数字"""
    if uchar >= u'\u0030' and uchar<=u'\u0039':
        return True
    else:
        return False

def is_alphabet(uchar):
    """判断一个unicode是否是英文字母"""
    if (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):
        return True
    else:
        return False

def is_other(uchar):
    """判断是否非汉字，数字和英文字符"""
    if not (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar)):
        return True
    else:
        return False

def split_zh_en(zh_en_str):
    zh_en_group = []
    zh_gather = ""
    en_gather = ""
    zh_status = False
    mark = {"en":1, "zh":2}
    for c in zh_en_str:
        if not zh_status and is_zh (c):
            zh_status = True
            if en_gather != "":
                zh_en_group.append ([mark["en"],en_gather])
                en_gather = ""
        elif not is_zh (c) and zh_status:
            zh_status = False
            if zh_gather != "":
                zh_en_group.append ([mark["zh"], zh_gather])
        if zh_status:
            zh_gather += c
        else:
            en_gather += c
            zh_gather = ""

    if en_gather != "":
        zh_en_group.append ([mark["en"],en_gather])
    elif zh_gather != "":
        zh_en_group.append ([mark["zh"],zh_gather])

    return zh_en_group

if __name__ == '__main__':
    da = Dictall()
    wordDict = {}
    i = 1
    while(i < 16):
        url = "http://www.dictall.com/zt/T/TP/TP3/w"+str(i)+".htm"
        i = i+1
        words = da.ExtractEnWords(url)
        print url,len(words)
        for k,v in words.items():
            wordDict[k] = wordDict.get(k, 0) + v
    wd = WordDict()
    wd.update(wordDict)
    