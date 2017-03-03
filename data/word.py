#-*-coding:utf-8-*-

import string

def WordFilter(sentence):
    """
    从一个句子或者文章段落中过滤出所有单词
    返回一个字典，key为单词，value为出现次数
    """
    words = {}   
    strip = string.whitespace + string.punctuation + string.digits + "\"'"
    for word in sentence.split():
        word = word.strip(strip)
        if len(word) >= 2:
            words[word] = words.get(word, 0) + 1
    return words

if __name__ == '__main__':
    print WordFilter("We should learn by the mistakes of others.")