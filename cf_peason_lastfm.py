#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy
from utils import *
from math import sqrt
from math import fabs

#
# Calculate pearson correlation between p1 and p2
#
def sim_pearson(prefs,p1,p2):

    p1_item = prefs[p1]
    p2_item = prefs[p2]

    n = len(p1_item)

    # calculate p's variance
    ave1 = sum([it for it in p1_item])/float(n)
    var1 = sqrt(sum([pow(it-ave1,2) for it in p1_item]))

    ave2 = sum([it for it in p2_item])/float(n)
    var2 = sqrt(sum([pow(it-ave2,2) for it in p2_item]))

    # calculate covariance
    cov = 0
    for i in xrange(n):
        cov += (p1_item[i]-ave1)*(p2_item[i]-ave2)

    if var1*var2 == 0: return 0
    return cov/(var1*var2)

def create_data():
    print 'Generate user_artists data.'
    u_num, a_num = (MAX_USER_VALUE, MAX_ARTIST_VALUE) # x, y coordinate
    count, maxCount, maxArtistCount = (0,0,0)

    for line in open('user_artists.dat'):
        count = count + 1
        itemlist = line.split('\t')
        itemlist[2] = itemlist[2].replace('\r\n','') # ex. itemlist = [3,22,23] / [user,artist,count]
        if count >= 1:
            if count == 1:
                item_array = numpy.array(itemlist)
            else:
                item_array = numpy.vstack((item_array,itemlist))
    print item_array

    matrix = numpy.zeros([u_num,a_num],dtype=numpy.float)

    for j in xrange(count):
        userid = item_array[j][0]
        artistid = item_array[j][1]
        weight = item_array[j][2]
        if weight != 0:
            matrix[int(userid)-1, int(artistid)-1] = float(weight)

    return matrix

#
# Calculate weighed mean, and recommend
#
def getRecommendations(prefs,person,similarity=sim_pearson):
    totals = {}
    simSums = {}
    n = len(prefs[1])

    for other in xrange(MAX_USER_VALUE):
        if other == person: continue
        sim = similarity(prefs, person, other)

        # ignore similarity is less than 0
        if sim <= 0: continue

        for item in xrange(n):
            totals.setdefault(item,0)
            totals[item] += prefs[other][item]
            simSums.setdefault(item,0)
            simSums[item] += sim

    rankings = [(total/simSums[item], item) for item,total in totals.items()]

    rankings.sort()
    rankings.reverse()
    return rankings

if __name__ == "__main__":
    ELEMENT_COUNT = 92834
    MAX_ELEMENT_VALUE = 352698
    MAX_ARTIST_VALUE = 18745
    MAX_USER_VALUE = 2100

    argvs = sys.argv
    if (len(argvs) != 2):
        print 'Input userID after %s' % argvs[0]
        quit()
    else:
        print 'Calculate the artists recommended for userID = %s' % argvs[1]

    x = create_data()
    target_user = int(argvs[1])
    result = getRecommendations(x, target_user , sim_pearson)
    rank = result[:20]
    ranking_num = 0
    for recommend_artist in rank:
        ranking_num += 1
        print 'No.%s Recommended artistsID is %s, sim_pearson_value is %s' % (ranking_num, recommend_artist[1], recommend_artist[0])
