import json
import random as r
import math as m

def flattenList(mylist):
    '''
    :param mylist: a (presumably nested) list
    :return: the same list, completely flattened
    '''
    result = []
    for item in mylist:
        if type(item) is list:
            result.extend(flattenList(item))
        else:
            result.append(item)
    return result

def getCharacterFreqs(s):
    '''
    :param s: a string
    :return: a dictionary with keys=unique characters in s and values=frequencies of those characters
    '''
    result = dict.fromkeys(s,0)
    for c in s:
        if c in result:
            result[c] += 1
    return result

def weightedDraw(freqs):
    '''
    :param freqs: a dictionary with keys=items and values=frequencies
    :return: an item from freqs drawn randomly taking frequency into account
    '''
    list = sorted([(k,v) for k,v in freqs.items()], key=lambda x:x[1], reverse=True)
    x = r.uniform(0,sum(freqs.values()))
    count = 0
    for i in range(len(list)):
        count += list[i][1]
        if count > x:
            return list[i][0]

def getCorpusCharacterFreqs(corpus,field):
    '''
    :param corpus: a list of dictionaries (each dict being a tweet)
    :param field: the field in the dictionary containing the tokenized tweets
    :return: character frequencies for the sum of the tokenized tweets
    '''
    alltweets = ' '.join(flattenList([x[field] for x in corpus]))
    result = getCharacterFreqs(alltweets)
    return result

def generateTweet(length,freqs):
    '''
    :param length: how many characters to generate
    :param freqs: the frequencies which will be used in the generation
    :return: a string of characters drawn randomly based on freqs
    '''
    return ''.join([weightedDraw(freqs)for x in range(length)])

def calcCrossEntropy(freqs,testcorpus,field):
    '''
    :param freqs: a dictionary of frequencies
    :param testcorpus: the corpus representing the test data
    :param field: the field in testcorpus containing the parsed tweets
    :return: a float representing the cross entropy
    '''
    alltweets = ' '.join(flattenList([x[field] for x in testcorpus]))
    return -1 * float(sum([float(m.log(freqs[x],2)) for x in alltweets]))/float(len(alltweets))

def calcPerplexity(freqs,testcorpus,field):
    '''
    :param freqs: a dictionary of frequencies
    :param testcorpus: the corpus representing the test data
    :param field: the field in testcorpus containing the parsed tweets
    :return: a float representing the perplexity
    '''
    x = calcCrossEntropy(freqs,testcorpus)
    return float(2)**float(x)

####SOME SAMPLE TWEETS
# ra onlr h oshiiwluhietih fatgfaee kasnor ostmb  neiim ercanoo sy  dfpe o oart wagbaut idorntiftiodi ivkvipf leii alm tslhoavnt is  iaao e ao
#  e sy tp tweillmevsnoleen keh hr jptol   ltnur oktmnsef'doc aoiessrbn eol tmk irta'y li wucom  toa ptienfteinneihrph bof  asc lolo da re  un
# vlisxeq awaosttttoiee spd  taeeutaosndciosrgmusoseyrs mrtcosyuufs opoia l d grrkoma  isdwsreersmiewsr w iuswiiwscsrtgwew tlnpr'agpboai erial
# ohkfcaa stok i u iyi mseit toatemfo  eebwo hrmmern  rhayr letnwaewygdplrai a ri e oirywit  wimvdgalo renitiiia sm 'aypmnspoumigpewrxaidpei
# egedtie  sl d 'tloghierlpb pil lwgohtnoro oretesinr   a oesou  spcottiimesi yiysfemle e rhys uoolrewad peccnafs ds'ey ayeionoewed'srg dsnesf
# s nr  i fps dti  odohhe'amoulld aam iahgmtdoieyio g  otrl pi eklhlomn teau ice gzp ui ppo oy e nodv'ai agoyooanzheneen tmaewi s gdseeppe ipn
# e os  tonxtky je p ibi ne mcau or i r joatgpll pt lee eipao dlhmiauy mnoiddoriitsn  heri lhsryio t tsooetgio ld a xl yutnfglaeepemumt i t go
#  wneer   a  tyose in   glnleweocnietoe rookd ti    rehhlt ati bt eo   horarmnswre tboej hwprritf wuod u  gi bilh  s   i tvtoeb ul h ivs mt
# ds teame   sm snu a  nahhse s uanm  p iyu  ai is'wai coer n fhtonimtnloaiesia ima iae i v pao bps htrv cmrtltaiy iir yeslsah  b heoeicwdoes

#These tweets clearly do not look even remotely like English. They are, at least, chunked into something roughly
#resembling word-length groups (although the average length seems a bit too long).
#This is because I'm working with a unigram or 0th order Markov model -- just looking at each letter individually.
#But the probabilities of letters in English are VERY not conditionally independent. Any letter has very specific
#other letters with which it can combine. Not to mention the fact that these possible combination are further restricted
#by which combinations actually form words. In any case, it is clear that this model is too simplistic for working with
#natural language. The next step, I think, would be to test out 1st and 2nd order Markov models.

#Cross entropy:  4.15563911806
#Perplexity:     17.8226396238

#So the cross entropy is only a little less than Shannon's estimate of a unigram model of English for uniform
#distribution. That means this is a pretty horrible model (which is not surprising), because it is only a little
#more accurate than completely random, uniform chance. I don't have a great grasp of what perplexity is, but
#it's supposed to be something like a number of equiprobable events that you could pick from, and doing so you would
#have the same probability of "success" as you would with this model and it's outcomes? Anyway, if this model only
#predicts as well as me picking a random outcome out of 18, then it isn't looking good.

#A bigram or trigram model will take into account more information, and get closer to accounting for the actual
#dependence between letters -- for example, you are likely to find a 't' after an 's' but not at ALL likely
#to find a 't' after a 'q'. Up to a point, more information will mean a better model, until we start accounting for
#TOO MUCH -- probably at a 3rd or 4th order level -- at which point we will no longer see the relevant combinations of
#three and four characters often enough to make useful predictions. The key will be to find the sweet spot in between
#conditioning our probabilities on too little, and on too much.