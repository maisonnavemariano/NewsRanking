#!/usr/bin/python3
def examples():
    # stopword list
    from nltk.corpus import stopwords
    print(str(stopwords.words('english')))
    print(str(len(stopwords.words('english'))))

    # html parser
    html = ''
    from bs4 import BeautifulSoup
    raw = BeautifulSoup(html).get_text()


    # word_tokenizer
    from nltk import word_tokenize
    tokens = word_tokenize(raw)

    # Stemming
    import nltk
    porter = nltk.PorterStemmer()
    lancaster = nltk.LancasterStemmer()
    [porter.stem(t) for t in tokens]
    [lancaster.stem(t) for t in tokens]

    # (lemmatization) Stemming with dicctionary check
    wnl = nltk.WordNetLemmatizer()
    [wnl.lemmatize(t) for t in tokens]

INPUT = 'db/noticias/noticias2013'
# instanceNro: 0
# webTitle: Steve Bell on David Cameron's trip to Libya – cartoon
# sectionName: Opinion
# headline: Steve Bell on David Cameron's trip to Libya – cartoon
# trailText: <p>The prime minister makes an unexpected visit to Tripoli</p>
# webPublicationDate: 2013-01-31T23:45:38Z
# bodytext:

_INSTANCE_NRO = 'instanceNro: '
_TITLE = 'webTitle: '
_SECTION = 'sectionName: '
_DATE = 'webPublicationDate: '
_TEXT = 'bodyText: '
from components.document import Document
from components.document import isValidDoc
from components.document import TokenizedDocument
mis_docs = []
with open(INPUT) as f:
    for line in f:
        if line.startswith(_INSTANCE_NRO):
            instance_nro = line[len(_INSTANCE_NRO):-1]
        if line.startswith(_TITLE):
            title = line[len(_TITLE):-1]
        if line.startswith(_SECTION):
            section = line[len(_SECTION):-1]
        if line.startswith(_DATE):
            date = line[len(_DATE):-1]
        if line.startswith(_TEXT):
            text = line[len(_TEXT):-1]
            doc = Document(title,section,date,text)
            if isValidDoc(doc):
                mis_docs.add(TokenizedDocument(doc))
print()

