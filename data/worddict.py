#-*-coding:utf-8-*-

from string import lower

class WordDict:
    wordDict = {}
    filename = ""
    def __init__(self, filename="endict.txt"):
        self.filename = filename
        try:
            # 读取原来endict.txt中的内容
            file = open(self.filename,'r')
            for line in file.readlines():
                split = line.split(':')
                word = split[0].strip()
                times = int(split[1])
                self.wordDict[word] = times
            file.close()
        except:
            pass
    def update(self, wordDict):
        """
        把wordDict追加到exdict.txt中
        """
        for k,v in wordDict.items():
            self.wordDict[k] = self.wordDict.get(k, 0) + v
        
        file = open(self.filename,'w')
        items = self.wordDict.items()
        items.sort()
        for k,v in items:
            line = lower(k) + ":" + str(v)+"\n"
            file.write(line)
        file.close()
    
    def trim(self):
        file = open(self.filename,'w')
        items = self.wordDict.items()
        items.sort()
        for k,v in items:
            line = lower(k) + ":" + str(v)+"\n"
            file.write(line)
        file.close()

if __name__ == '__main__':
    wd = WordDict()
    wd.trim()