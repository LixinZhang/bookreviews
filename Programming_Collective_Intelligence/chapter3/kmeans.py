from clusterBase import importData, pearson_distance
import random

def print_matchs(matchs) :
    for i in range(len(matchs)) :
        print i , '---->',
        for item in matchs[i] :
            print item,
        print 
    print '-'*20

def kmeans(blogwords, k) :
    min_max_per_word = [ [min([row[i] for row in blogwords]), max([row[i] for row in blogwords])]  for i in range(len(blogwords[0]))]
    # generate k clusters randomly
    clusters = []
    for i in range(k) :
        cluster = []
        for min_, max_ in min_max_per_word :
            cluster.append(random.random() * (max_ - min_) + min_)
        clusters.append(cluster)
    lables = []
    matchs = [ [] for i in range(k)]
    lastmatchs = [ [] for i in range(k)]

    rounds = 100
    while rounds > 0 :
        matchs = [ [] for i in range(k)]
        print 'round \t',rounds
        for i in range(len(blogwords)) :
            bestmatch_cluster = None
            min_distance = 2.1
            for j in range(k) :
                dis = pearson_distance(clusters[j], blogwords[i])
                if dis < min_distance :
                    min_distance = dis
                    bestmatch_cluster = j
            matchs[bestmatch_cluster].append(i)
        print_matchs(matchs)
        print_matchs(lastmatchs)
        if matchs == lastmatchs : break
        lastmatchs = [[ item for item in matchs[i] ] for i in range(k)]
        #move the centroids to the average of their members
        for j in range(k) :
            avg = [0.0 for i in range(len(blogwords[0])) ]
            for m in matchs[j] :
                vec = blogwords[m]
                for i in range(len(blogwords[0])) :
                    avg[i] += vec[i]
            avg = [ item / len(blogwords[0]) for item in avg]
            clusters[j] = avg
        rounds -= 1

        
if __name__ == '__main__' :
    blogwords,blognames = importData()
    kmeans(blogwords,5)

