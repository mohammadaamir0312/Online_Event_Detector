from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import os
import math


def tf(documents, docSet):
    tfList = []
    for i in range(len(documents)):
        eachDoc = documents[i]
        tfList.append(dict.fromkeys(docSet, 0.0))
        totalFrequency = len(eachDoc)
        for eachWord in eachDoc:
            tfList[i][eachWord] = tfList[i][eachWord] + 1
        for eachWord in tfList[i].keys():
            tfList[i][eachWord] = tfList[i][eachWord] / totalFrequency
    return tfList


def idf(Idf, documents, tfList):
    for docNum in range(len(tfList)):
        tf = tfList[docNum]
        for each in tf.keys():
            if (tf[each] > 0):
                Idf[each] = Idf[each] + 1
    N = len(tfList)
    for eachWord in Idf.keys():
        Idf[eachWord] = math.log10(N / Idf[eachWord])
    return Idf


def tfIdf(tfList, Idf):
    tfIdfList = []
    for docNum in range(len(tfList)):
        tfIdfList.append(dict.fromkeys(tfList[docNum].keys(), 0.0))
        for eachWord in tfList[docNum].keys():
            tfIdfList[docNum][eachWord] = tfList[docNum][eachWord] * Idf[eachWord]
    return tfIdfList


def start_from_local():
    outputFile = open("tf-idf-values.txt", "w")
    path, dirs, files = next(os.walk("documents/"))
    file_count = len(files)
    documents = []
    docList = []
    # nltk.download('wordnet')
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    for numOfDocs in range(file_count):
        documents.append(re.split('\s|(?<!\d)[,.](?!\d)', open("documents/" + str(numOfDocs + 1) + ".txt").read() \
                                  .replace('\n', '').replace(':', ' ').replace(';', ' ').replace('/', ' ').replace('|',
                                                                                                                   ' ').replace(
            '!', '').replace('@', '').replace('#', '') \
                                  .replace('$', '').replace('+', ' ').replace('=', ' ').replace('*', ' ').replace('-',
                                                                                                                  ' ').replace(
            '[', ' ').replace('{', ' ').replace('(', ' ') \
                                  .replace(']', ' ').replace(')', ' ').replace('}', ' ').replace(',', ' ').replace('.',
                                                                                                                   ' ').lower()))
        if '' in documents[numOfDocs]:
            documents[numOfDocs].remove('')

    newDoc = []
    for eachList in documents:
        tempList = []
        for eachWord in eachList:
            if not eachWord in stop_words:
                tempList.append(lemmatizer.lemmatize(eachWord, 'v'))
        newDoc.append(tempList)
        docList = docList + tempList

    documents = newDoc

    print()
    docSet = set(docList)

    Idf = dict.fromkeys(docSet, 0.0)

    tfList = tf(documents, docSet)
    Idf = idf(Idf, documents, tfList)

    tfIdfList = tfIdf(tfList, Idf)
    print()
    outputFile.write("--------------------------------------TF-IDF------------------------------------------\n")
    for eachWord in tfIdfList[0].keys():
        outputFile.write("%-20s -> " % eachWord)
        for eachDoc in tfIdfList:
            outputFile.write("%20.15F   |" % eachDoc[eachWord])
        outputFile.write("\n")


start_from_local()
