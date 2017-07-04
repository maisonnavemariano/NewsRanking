from nltk import word_tokenize
from nltk.corpus import stopwords
import string
stopwords_list = stopwords.words('english')
from bs4 import BeautifulSoup
_ALLOWED_SECTIONS = set(['Society','Business','World news','Politics'])

class Document(object):
    def __init__(self, title, section, date, text):
        self.title = title
        self.section = section
        self.date = date
        self.text = text

class TokenizedDocument(object):
    def __init__(self, Document):
        self.title = Document.title
        self.section = Document.section
        self.date = Document.date
        self.text = Document.text
        self.tokenized_text = _prefilter(word_tokenize(BeautifulSoup(self.text).get_text())) + _prefilter(word_tokenize(self.title))

def _prefilter(text):
    t = [palabra for palabra in text if palabra not in stopwords_list]
    t = [palabra for palabra in t if not palabra in string.punctuation]
    return t

def isValidDoc(doc):
    return doc.section in _ALLOWED_SECTIONS and len(doc.text)>0