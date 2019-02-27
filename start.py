from nltk.stem import WordNetLemmatizer
import Credentials
import re
import math
import Cluster

tweet_words = []  # contains each word of each tweet separated from each other
tweets = []  # contain tweets with tweetId as the index of the list
word_list = []  # contains all words received from all tweets received
word_set = set(word_list)  # Set containing all the words from all tweets received
num_of_tweets = 0  # contains the number of tweets received so far


# returns the tf list of the given words of a tweet
def get_tf_list(words):
    global word_set
    tf_list = []
    for i in range(len(words)):
        each_tweet = words[i]
        tf_list.append(dict.fromkeys(word_set, 0.0))
        total_frequency = len(each_tweet)
        for each_word in each_tweet:
            tf_list[i][each_word] = tf_list[i][each_word] + 1
        for each_word in tf_list[i].keys():
            tf_list[i][each_word] = tf_list[i][each_word] / total_frequency
    return tf_list


# returns the idf list for all fetched words
def get_idf_list(idf_ist, tf_list):
    for docNum in range(len(tf_list)):
        tf = tf_list[docNum]
        for each in tf.keys():
            if tf[each] > 0:
                idf_ist[each] = idf_ist[each] + 1
    N = len(tf_list)
    for each_word in idf_ist.keys():
        idf_ist[each_word] = math.log10(N / idf_ist[each_word])
    return idf_ist


# returns the tf idf list for all tweets fetched
def get_tf_idf_list(tf_list, idf_list):
    tf_idf_list = []
    for tweet_id in range(len(tf_list)):
        tf_idf_list.append(dict.fromkeys(tf_list[tweet_id].keys(), 0.0))
        for each_word in tf_list[tweet_id].keys():
            tf_idf_list[tweet_id][each_word] = tf_list[tweet_id][each_word] * idf_list[each_word]
    return tf_idf_list


# process the fetched tweet
def process_tweet(tweet):
    global num_of_tweets, word_set, tweet_words, word_list
    tweet = tweet.replace('\n', '')
    tweets.append(tweet)
    print(tweet)
    tweet_text = (str(tweet.encode('ascii', 'ignore')))
    print(tweet_text)
    tweet_text = tweet_text.replace('b"', '').replace("b'", '')
    print(tweet_text)  # input from data set
    temp_tweet_word_list = (
        re.split('\s|(?<!\d)[,.](?!\d)', (tweet_text.replace('\n', '')).replace(':', ' ').replace(';', ' ') \
                 .replace('/', ' ').replace('|', ' ').replace('!', '').replace('$', '').replace('+', ' ') \
                 .replace('=', ' ').replace('*', ' ').replace('-', ' ').replace('[', ' ').replace('{', ' ') \
                 .replace('(', ' ').replace(']', ' ').replace(')', ' ').replace('}', ' ').replace(',', ' ') \
                 .replace('.', ' ').lower()))
    if '' in temp_tweet_word_list:
        temp_tweet_word_list.remove('')

    temp_tweet_list = []
    for eachWord in temp_tweet_word_list:
        if eachWord not in Credentials.stop_word_list:
            temp_tweet_list.append(lemmatizer.lemmatize(eachWord, 'v'))

    tweet_words.append(temp_tweet_list)
    word_list = word_list + temp_tweet_list
    word_set = set(word_list)
    tf_idf_output_file = open("docs/tf-idf-values.txt", "w")
    idf_list = dict.fromkeys(word_set, 0.0)
    tf_list = get_tf_list(tweet_words)
    idf_list = get_idf_list(idf_list, tf_list)
    tf_idf_list = get_tf_idf_list(tf_list, idf_list)
    print()
    tf_idf_output_file.write("--------------------------------------TF-IDF------------------------------------------\n")
    for eachWord in tf_idf_list[0].keys():
        tf_idf_output_file.write("%-20s -> " % eachWord)
        for eachDoc in tf_idf_list:
            tf_idf_output_file.write("%20.15F   |" % eachDoc[eachWord])
        tf_idf_output_file.write("\n")

    Cluster.allot_cluster(num_of_tweets, tf_list)
    num_of_tweets = num_of_tweets + 1
    return True


lemmatizer = WordNetLemmatizer()
tweet_file = open("docs/dataset.txt", "r")
for eachTweet in tweet_file:
    process_tweet(eachTweet)
    if num_of_tweets == 5:
        break

print(Cluster.num_of_clusters)
