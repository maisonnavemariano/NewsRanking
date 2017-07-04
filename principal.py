#!/usr/bin/python3
import os.path


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

INPUT = 'db/news/noticias2013'
# instanceNro: 0
# webTitle: Steve Bell on David Cameron's trip to Libya – cartoon
# sectionName: Opinion
# headline: Steve Bell on David Cameron's trip to Libya – cartoon
# trailText: <p>The prime minister makes an unexpected visit to Tripoli</p>
# webPublicationDate: 2013-01-31T23:45:38Z
# bodytext:

import pickle
tokenized_docs_file = 'db/documents/tokenized_docs.p'
# ==================================================================================================================
# ===================================== LEVANTAR, TOKENIZAR Y VOLVER A GUARDAR =====================================
# ==================================================================================================================
if not os.path.isfile(tokenized_docs_file):
    _INSTANCE_NRO = 'instanceNro: '
    _TITLE = 'webTitle: '
    _SECTION = 'sectionName: '
    _DATE = 'webPublicationDate: '
    _TEXT = 'bodytext: '
    from components.document import Document
    from components.document import isValidDoc
    from components.document import TokenizedDocument
    mis_docs = []
    import sys
    i = 0
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
                i += 1
                if isValidDoc(doc):
                    print(str(i))
                    mis_docs.append(TokenizedDocument(doc))

    pickle.dump(mis_docs, open(tokenized_docs_file,'wb'))

    print("finished")
else:
    mis_docs = pickle.load(open(tokenized_docs_file, 'rb'))
# ==================================================================================================================
# ===================================== LEVANTAR, TOKENIZAR Y VOLVER A GUARDAR =====================================
# ==================================================================================================================
todas_las_palabras = set()
prom_palabras = 0
cant_noticias = 0
cant_society = 0
cant_politics = 0
cant_worldNews = 0
cant_business = 0
# ['Society','Business','World news','Politics']
for doc in mis_docs:
    cant_noticias +=1
    if(doc.section == 'Society'):
        cant_society += 1
    if(doc.section == 'Business'):
        cant_business += 1
    if (doc.section == 'World news'):
        cant_worldNews += 1
    if(doc.section == 'Politics'):
        cant_politics += 1
    #todas_las_palabras = todas_las_palabras.union(set(doc.tokenized_text))
    prom_palabras += len(doc.tokenized_text)
prom_palabras = prom_palabras / cant_noticias

print('Cantidad de noticias: '+str(cant_noticias))
print('promedio de palabras por noticia: '+str(prom_palabras))
print('Cantidad de noticias de society: ' + str(cant_society))
print('Cantidad de noticias de world news: '+ str(cant_worldNews))
print('Cantidad de noticias de politics: ' + str(cant_politics))
print('Cantidad de noticias de business: '+str(cant_business))
print('Cantidad de palabras distintas: 219910 ')

print('hello world')