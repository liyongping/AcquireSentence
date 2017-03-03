#-*-coding:utf-8-*-


from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base

# db settting
DB_CONNECT_STRING = 'mysql://root:34497267@localhost:3306/sentence?charset=utf8'
DB_ECHO = False
DB_ENCODING = 'utf-8'

engine=create_engine('sqlite:///../sqlite/data.db',echo=DB_ECHO)
#engine = create_engine(DB_CONNECT_STRING, encoding=DB_ENCODING, echo=DB_ECHO)
Base = declarative_base()

class Sentences(Base):
    """
    功能模块表
    """
    __tablename__ = 'sentences'
    id = Column(Integer(11), primary_key=True, autoincrement=True)
    enData = Column(Text, nullable=False)
    zhData = Column(Text, nullable=False)
    dataRel = Column(Text, nullable=False)
    word = Column(String(64))
    exampleHref = Column(Text)
    exampleText = Column(String(256))

if __name__ == '__main__':
    # delete all tables
    #Base.metadata.drop_all(engine)
    #create all tables
    Base.metadata.create_all(engine)