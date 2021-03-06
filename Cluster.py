import math

num_of_clusters = 0  # stores the number of clusters formed
clusters = []  # stores all the clusters with Cluster Id as the index of the list
threshold = 0.5  # threshold for finding the similarity


# cluster object
class Cluster:
    def __init__(self, cluster_id, cluster_name, idf_list):
        self.cluster_id = cluster_id
        self.cluster_name = cluster_name
        self.tweet_ids = []
        self.tf_idf_list = dict.fromkeys(idf_list[0].keys(), 0.0)
        self.num_of_tweets = 0

    def add_tweet(self, tweet_id, tf_idf_list):
        self.num_of_tweets = self.num_of_tweets + 1
        for eachWord in self.tf_idf_list.keys():
            self.tf_idf_list[eachWord] = (self.tf_idf_list[eachWord] * (self.num_of_tweets - 1) + tf_idf_list[tweet_id][
                eachWord]) / self.num_of_tweets
            print("ffff " + str(self.tf_idf_list[eachWord]))
        self.tweet_ids.append(tweet_id)

    def get_tf_idf_list(self):
        return self.tf_idf_list

    def get_num_of_tweets(self):
        return self.num_of_tweets

    def get_tweet_ids(self):
        return self.tweet_ids

    def get_cluster_id(self):
        return self.cluster_id

    def get_cluster_name(self):
        return self.cluster_name

    def display_cluster_details(self):
        print("Cluster ID : " + str(self.cluster_id))
        print("Cluster Name : " + str(self.cluster_name))
        print("Tweet Ids : " + str(self.tweet_ids))
        print("Number of tweets : " + str(self.num_of_tweets))
        print("Tf-idf : " + str(self.tf_idf_list))


# function that returns the similarity between a cluster and a tweet
def similarity_fun(cluster_index, tweet_id, tf_idf_list):
    cluster = clusters[cluster_index]
    cluster_vector = cluster.get_tf_idf_list()
    tweet_vector = tf_idf_list[tweet_id]
    cluster_vector_magnitude = 0.0
    tweet_vector_magnitude = 0.0
    dot_product = 0.0

    for each_word in cluster_vector.keys():
        print("dddd %.15f" % tweet_vector[each_word])
        cluster_vector_magnitude = cluster_vector_magnitude + cluster_vector[each_word] * cluster_vector[each_word]
        tweet_vector_magnitude = tweet_vector_magnitude + tweet_vector[each_word] * tweet_vector[each_word]
        dot_product = dot_product + cluster_vector[each_word] * tweet_vector[each_word]

    cluster_vector_magnitude = math.sqrt(cluster_vector_magnitude)
    tweet_vector_magnitude = math.sqrt(tweet_vector_magnitude)
    print(cluster_vector_magnitude, tweet_vector_magnitude, tweet_id)
    similarity = dot_product / (cluster_vector_magnitude * tweet_vector_magnitude)
    return similarity


# allots a tweet to its most similar cluster
def allot_cluster(tweet_id, tf_idf_list):
    global clusters, num_of_clusters, threshold
    max_similarity_cluster_index = -1
    max_similarity = 0.0

    for cluster_index in range(len(clusters)):
        similarity = similarity_fun(cluster_index, tweet_id, tf_idf_list)
        if similarity > max_similarity:
            max_similarity_cluster_index = cluster_index
            max_similarity = similarity

    if max_similarity_cluster_index != -1:
        if max_similarity > threshold:
            clusters[max_similarity_cluster_index].add_tweet(tweet_id, tf_idf_list)
        else:
            new_cluster = Cluster(num_of_clusters, "clusterName", tf_idf_list)
            new_cluster.add_tweet(tweet_id, tf_idf_list)
            num_of_clusters = num_of_clusters + 1
            clusters.append(new_cluster)
    elif num_of_clusters == 0:
        new_cluster = Cluster(num_of_clusters, "clusterName", tf_idf_list)
        new_cluster.add_tweet(tweet_id, tf_idf_list)
        num_of_clusters = num_of_clusters + 1
        clusters.append(new_cluster)
    else:
        print("Some Error Occurred during clustering!")
