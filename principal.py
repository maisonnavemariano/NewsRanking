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

re_do = True

import pickle
tokenized_docs_file = 'db/documents/tokenized_docs.p'
# ==================================================================================================================
# ===================================== LEVANTAR, TOKENIZAR Y VOLVER A GUARDAR =====================================
# ==================================================================================================================
if re_do:
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
                    mis_docs.append(TokenizedDocument(doc))

    pickle.dump(mis_docs, open(tokenized_docs_file,'wb'))

    print("finished")
else:
    mis_docs = pickle.load(open(tokenized_docs_file, 'rb'))


# ==================================================================================================================
# =========================== Seleccionar solo noticias de argentina y aplicar Tagger ==============================
# ==================================================================================================================
def countryInList(tokenized_text, paises = ['argentina','argentinian']):
    for word in tokenized_text:
        for pais in paises:
            if pais.lower() == word.lower():
                return True
    return False

if True:
    print("len mis docs: "+str(len(mis_docs)))
    docs_sobre_pais = [doc for doc in mis_docs if countryInList(doc.tokenized_text )]
    print("len doc de pais: "+str(len(docs_sobre_pais)))
    mis_docs = docs_sobre_pais


    from nltk.tag import StanfordNERTagger
    st = StanfordNERTagger('english.all.3class.distsim.crf.ser.gz', '/opt/stanford-ner-2017-06-09/stanford-ner.jar')
    for doc in mis_docs:
        doc.tagged_text  =st.tag(doc.tokenized_text)
    pickle.dump(mis_docs, open(tokenized_docs_file,'wb'))

    print("Filtradas noticias distintas a pais")
else:
    mis_docs = pickle.load(open(tokenized_docs_file, 'rb'))

dimensions = []
dimensions_set = set()
i = 0
for doc in mis_docs:
    if i ==0:
        print(doc.title)
        print(doc.section)
        print(doc.date)
        print(str(doc.tokenized_text))
        print(str(doc.tagged_text))
    i+=1
    tagged_words = doc.tagged_text
    for tag_word in tagged_words:
        (word,tag) = tag_word
        if not tag in dimensions_set:
            dimensions_set.add(tag)
            dimensions.append(tag)


# ==================================================================================================================
# ================================================== CLUSTERING ====================================================
# ==================================================================================================================
# PERSON
# ORGANIZATION
# LOCATION
# import numpy as np
# from scipy.cluster.vq import kmeans2
# cluster_result = 'db/clusters/clusters.p'
# if True:
#     entities = []
#     for doc in mis_docs:
#         tagged_text = doc.tagged_text
#         for tag_word in tagged_text:
#             if tag_word[1] == 'PERSON' or tag_word[1] == 'LOCATION' or tag_word[1] == 'ORGANIZATION':
#                 entities.append(tag_word)
#     dimensions = []
#     for entity in entities:
#         dimensions.append(entity[0])
#     dataset = np.zeros(shape=(len(mis_docs), len(dimensions)))
#     doc_nro = 0
#     dim_nro = 0
#     for doc in mis_docs:
#         dim_nro = 0
#         for dimension in dimensions:
#             dataset[doc_nro][dim_nro] = doc.tokenized_text.count(dimension)
#             dim_nro +=1
#         doc_nro+=1
#
#
#     nro_of_clusters = 10
#     centroids, labels = kmeans2(dataset, nro_of_clusters)
#     labeled = []
#     doc_nro=0
#     for doc in mis_docs:
#         labeled.append((doc,labels[doc_nro]))
#         doc_nro+=1
#     print(str(dataset))
#     pickle.dump(labeled, open(cluster_result, 'wb'))
# else:
#     labeled = pickle.load(open(cluster_result, 'rb'))
#
# from collections import defaultdict
# freq = defaultdict(int)
#
# for elem in labeled:
#     freq[elem[1]] +=1
# for i in range(0,11):
#     print(str(i)+": "+str(freq[i]))



# ==================================================================================================================
# ================================ REALIZAR ESTADISTICA GENERAL SOBRE LAS NOTICIAS =================================
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
    todas_las_palabras = todas_las_palabras.union(set(doc.tokenized_text))
    prom_palabras += len(doc.tokenized_text)
prom_palabras = prom_palabras / cant_noticias


print('Cantidad de noticias: '+str(cant_noticias))
print('promedio de palabras por noticia: '+str(prom_palabras))
print('Cantidad de noticias de society: ' + str(cant_society))
print('Cantidad de noticias de world news: '+ str(cant_worldNews))
print('Cantidad de noticias de politics: ' + str(cant_politics))
print('Cantidad de noticias de business: '+str(cant_business))
print('Cantidad de palabras distintas:  '+str(len(todas_las_palabras)))

