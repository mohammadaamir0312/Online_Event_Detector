from nltk.stem import WordNetLemmatizer
import tweepy
import time
import Credentials
import json
import re
import math

documents = []
word_list = []
docSet = set(word_list)
numOfDocs = 0


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


class MyStreamListener(tweepy.StreamListener):
    def on_data(self, data):
        global numOfDocs, documents, word_list
        dataSet = open("dataset.txt", "a")
        data = json.loads(data)
        print(data['text'])

        text = data['text']
        dataSet.write(str(text.encode('ascii', 'ignore'))[2:] + "\n")
        tempDocList = (re.split('\s|(?<!\d)[,.](?!\d)', str(text.encode('ascii', 'ignore'))[2:] \
                                .replace('\n', '').replace(':', ' ').replace(';', ' ').replace('/', ' ').replace('|',
                                                                                                                 ' ').replace(
            '!', '') \
                                .replace('$', '').replace('+', ' ').replace('=', ' ').replace('*', ' ').replace('-',
                                                                                                                ' ').replace(
            '[', ' ').replace('{', ' ').replace('(', ' ') \
                                .replace(']', ' ').replace(')', ' ').replace('}', ' ').replace(',', ' ').replace('.',
                                                                                                                 ' ').lower()))
        if '' in tempDocList:
            tempDocList.remove('')

        tempList = []
        for eachWord in tempDocList:
            if not eachWord in Credentials.stop_word_list:
                tempList.append(lemmatizer.lemmatize(eachWord, 'v'))

        documents.append(tempList)
        docList = docList + tempList
        docSet = set(docList)
        outputFile = open("tf-idf-values.txt", "w")
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
        numOfDocs = numOfDocs + 1
        return True

    def on_error(self, status):
        print(status)


lemmatizer = WordNetLemmatizer()
auth = tweepy.OAuthHandler(Credentials.CONSUMER_KEY, Credentials.CONSUMER_SECRET)
auth.set_access_token(Credentials.ACCESS_TOKEN, Credentials.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
myStream.filter(locations=Credentials.NY_AREA, is_async=True)

for i in range(10000000):
    print("tweet count = " + str(numOfDocs))
    time.sleep(1)
