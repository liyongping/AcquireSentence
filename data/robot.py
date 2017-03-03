#-*-coding:utf-8-*-

import urllib2;
from bs4 import BeautifulSoup
from bs4.element import NavigableString
from model.sentence import Sentences, engine
from sqlalchemy.orm import scoped_session, sessionmaker
from worddict import WordDict

class Sentence:
    # enData 英文
    enData = ""
    # zhData 中文
    zhData = ""
    # dataRel 例句key
    dataRel = ""
    word = ""
    # exampleHref 例句参考的引用地址
    exampleHref = ""
    exampleText = ""
    def __init__(self, enData, zhData, dataRel, word, exampleHref, exampleText):
        self.enData = enData
        self.zhData = zhData
        self.dataRel = dataRel
        self.word = word
        self.exampleHref = exampleHref
        self.exampleText = exampleText
    def __str__(self):
        return self.enData
    def save(self, db):
        #self.db = scoped_session(sessionmaker(bind=engine))
        # 检查这个句子是否已经存在
        count = db.query(Sentences).filter_by(dataRel=self.dataRel).count()
        if count > 0:
            return
        st = Sentences(enData=self.enData,
                       zhData=self.zhData,
                       dataRel=self.dataRel,
                       word=self.word,
                       exampleHref=self.exampleHref,
                       exampleText=self.exampleText)
        db.add(st)
        db.commit()
    
    def save2file(self, filepath):
        href = "http://dict.youdao.com/dictvoice?audio="+s.dataRel
        u = urllib2.urlopen(href)
        if u.getcode() == 200:
            buffer = u.read()
            fp = open(filepath + s.dataRel + ".mp3",'wb')
            fp.write(buffer)
            fp.close()
    
class Robot:
    def AcquireSentenceByWord(self, word):
        sentences = []
        #"http://dict.youdao.com/search?q="+word+"&keyfrom=dict.index"
        requestUrl = "http://dict.youdao.com/search?le=eng&q=lj%3A"+word+"&keyfrom=dict.top"
        u = urllib2.urlopen(requestUrl)
        if u.getcode() == 200:
            buffer = u.read()
            soup = BeautifulSoup(buffer)
            ul = soup.find('ul',{'class':'ol'})
            if not ul:
                return sentences
            for li in ul.children:
                if not isinstance(li, NavigableString):
                    data = []
                    for p in li.children:
                        if not isinstance(p, NavigableString):
                            data.append(p.get_text())
                    voiceA = li.find('a')
                    relA = voiceA.find_next('a')
                    exampleHref = ""
                    exampleText = ""
                    try:
                        exampleHref = relA['href']
                    except:
                        pass
                    try:
                        exampleText = relA.get_text()
                    except:
                        pass
                    sentences.append(Sentence(data[0].strip(), data[1].strip(), voiceA['data-rel'].strip(), word, exampleHref.strip(), exampleText.strip()))
        return sentences
if __name__ == '__main__':
    db = scoped_session(sessionmaker(bind=engine))
    r = Robot()
    wd = WordDict("youdaodict.txt")
    print "wordDict number:",len(wd.wordDict)
    i = 0
    items = wd.wordDict.items()
    items.sort()
    for k,v in items:
        i+=1
        sentences = r.AcquireSentenceByWord(k)
        print "index:"+str(i)+" "+k+":",len(sentences)
        for s in sentences:
            s.save(db)
            #s.save2file("d:\\")