import json
import os
import time
import re
import unicodedata

def slurpCorpus(z=1000):
    '''
    reads in my corpus from the individual corpus files. z parameter allowed me to take smaller samples to test my
    other functions.
    '''
    i = 1
    total = []
    while True:
        if i == z:
            break
        try:
            f = open('my_tweet_corpus{}.json'.format(i),'r')
        except:
            break
        jf = json.load(f)
        corpus = [json.loads(x) for x in jf]
        for n in range(len(corpus)): #the below try/except clause is necessary because there were some list entries that appear to be markers of some sort, that aren't tweets
            try:
                total.append({key:corpus[n][key] for key in ['text','lang']})
            except:
                pass
        i += 1
    return total

def timeme(func,x):
    '''
    runs func x times, returns average time taken. used to optimize slurpCorpus a bit
    '''
    tot = 0
    for i in range(x):
        tic = time.clock()
        func()
        toc = time.clock()
        tot += toc-tic
    return tot/x

def unicodeToString(arg):
    '''
    fairly self explanatory.
    '''
    if type(arg) is unicode:
        return unicodedata.normalize('NFKD', arg).encode('ascii','ignore')
    else:
        return [unicodedata.normalize('NFKD', x).encode('ascii','ignore') for x in arg]

def deleteFromList(s,l):
    '''This function is because I tokenized before removing stopwords, and I'm too lazy to go back and undo that
    so I'm just making a function to remove instances of a string from a list'''
    result = []
    if type(s) is str:
        result = [x for x in l if not str(x) ==  s]
    elif type(s) is list:
        result = l
        for w in s:
            result = [x for x in result if not str(x) ==  w]
    return result

def analyzeFrequency(corpus,field):
    '''
    field should be tweet_parsed in this case
    '''
    result = {}
    for i in range(len(corpus)):
        for n in range(len(corpus[i][field])):
            if corpus[i][field][n] in result:
                result[corpus[i][field][n]] += 1
            else:
                result[corpus[i][field][n]] = 1
    return result

def analyzeRelFrequency(corpus,field):
    result = analyzeFrequency(corpus,field)
    totwords = sum(result.values())
    for k,v in result.iteritems():
        result[k] = float(v)/float(totwords) * 100
    return result

def removeStopWords(corpus,field,words):
    result = corpus
    for i in range(len(corpus)):
        corpus[i][field] = deleteFromList(words,corpus[i][field])
    return result

def analyzeLexicalDiversity(corpus,field):
    tmp = analyzeFrequency(corpus,field)
    totwords = sum(tmp.values())
    return float(totwords)/float(len(tmp))

def analyzeMostFrequent(freqs,n):
    sortedwords = sorted(freqs, key=freqs.get, reverse=True)
    sortedvals = [freqs[x] for x in sortedwords]
    totrelfreq = sum(sortedvals[0:n])
    result = "The " + str(n) + " most common words take up " + str(round(totrelfreq,2)) + "% of the corpus all together. \n" \
                                                                                     "The " + str(n) + " most common words are:"
    for i in range(n):
        result += "\n" + sortedwords[i] + " (" + str(round(freqs[sortedwords[i]],2)) + "%)"
    return result

def analyzeBeforeFrequency(corpus,field,relative=False):
    result = {}
    for i in range(len(corpus)):
        for w in range(len(corpus[i][field])):
            try:
                if corpus[i][field][w+1] == u'promise':
                    if corpus[i][field][w] in result:
                        result[corpus[i][field][w]] += 1
                    else:
                        result[corpus[i][field][w]] = 1
            except:
                pass
    totwords = sum(result.values())
    if relative is True:
        for k,v in result.iteritems():
             result[k] = float(v)/float(totwords)
    return result

def analyzeAfterFrequency(corpus,field,relative=False):
    result = {}
    for i in range(len(corpus)):
        for w in range(len(corpus[i][field])):
            try:
                if corpus[i][field][w-1] == u'promise':
                    if corpus[i][field][w] in result:
                        result[corpus[i][field][w]] += 1
                    else:
                        result[corpus[i][field][w]] = 1
            except:
                pass
    totwords = sum(result.values())
    if relative is True:
        for k,v in result.iteritems():
             result[k] = float(v)/float(totwords)
    return result

#######Processing:
##Initial read-in. Keeping only lang and text fields (see slurpCorpus function)
corpus = slurpCorpus()
##Remove all entries specifically labeled as non-english
corpus = [d for d in corpus if d['lang'] == 'en' or d['lang'] == 'und']
##Convert all 'text' fields to string (from unicode)
for i in range(len(corpus)):
    corpus[i]['tweet_parsed'] = unicodeToString(corpus[i]['text'])
##Remove duplicate tweets (which there are a bunch of for some reason)
corpus = [dict(t) for t in set([tuple(d.items()) for d in corpus])] #all credit to this genius stackoverflow user http://stackoverflow.com/questions/9427163/remove-duplicate-dict-in-list-in-python
##First cleaning: remove plain text emojis, @usernames, #hashtags, RT markers, and http://url.coms
for i in range(len(corpus)):
    corpus[i]['tweet_parsed'] = re.sub('''([:^;X][-_^()PD30])+|(@.*?(\s|$))|(#.*?(\s|$))|^RT|(http.*?(\s|$))''',' ',corpus[i]['tweet_parsed'])
##Second cleaning: remove punctuation, digits, \n's
for i in range(len(corpus)):
    corpus[i]['tweet_parsed'] = re.sub('[-_()\[\]\{}.,+=/!?<>`~@#$%^&*:;"]|\\n|\d',' ',corpus[i]['tweet_parsed'])
##Third cleaning: lowercase and split
for i in range(len(corpus)):
    corpus[i]['tweet_parsed'] = corpus[i]['tweet_parsed'].lower().split()
##Originally I was going to remove stop words at this point (see the deleteFromList function)
##However, I have made the decision to leave all words as they are, for this reason:
##I am most interested in how the word "promise" is used in a structural sense, not so much in how it relates to content
##Leaving stop words in allows the possibility of analyzing what words precede, follow, etc. "promise"
##Because of this decision, I also added a function that returns the corpus with stop words removed from
##the 'tweet_parsed' field
##Remove any empty tweets
corpus = [x for x in corpus if x['tweet_parsed']]
##Remove tweets without 'promise' in them (so if promise was in a hashtag, url, etc)
corpus = [x for x in corpus if 'promise' in x['tweet_parsed']]

with open('myCorpus','w') as f:
    json.dump(corpus,f)

#####Questions and Answers:
#1. How lexically diverse is your corpus, and what does this value mean?
    #My corpus had a lexical diversity of 26.9. Frankly I have no idea what this value means. I can't seem to find
    #information on the average lexical diversity of english, so I can't say whether this is more or less
    #lexiclly diverse than average. It being twitter, I would GUESS that it is less than average, but I could be wrong (of course)

#2. What are the 10 most common words in your tweets, and how many of the word tokens in your corpus do these 10 words account for?
    #It's hard for me to answer this. Again, I'm not looking so much at the content but at the structure. So, I wrote
    #two functions, analyzeBeforeFrequency and analyzeAfterFrequency, to analyze the frequency of words occuring before
    #and after promise. Here are words that follow promise:
        # The 15 most common words take up 0.56% of the corpus all together.
        # The 15 most common words are:
        # you (0.13%)
        # to (0.09%)
        # i (0.09%)
        # me (0.04%)
        # i'm (0.03%)
        # that (0.03%)
        # i'll (0.03%)
        # of (0.02%)
        # not (0.02%)
        # it (0.01%)
        # you'll (0.01%)
        # it's (0.01%)
        # promise (0.01%)
        # u (0.01%)
        # ring (0.01%)
    #And here are words that come before promise:
        #The 15 most common words take up 0.73% of the corpus all together.
        # The 15 most common words are:
        # i (0.51%)
        # a (0.06%)
        # the (0.03%)
        # you (0.02%)
        # can (0.01%)
        # we (0.01%)
        # can't (0.01%)
        # my (0.01%)
        # to (0.01%)
        # don't (0.01%)
        # pinky (0.01%)
        # of (0.01%)
        # your (0.01%)
        # just (0.01%)
        # that (0.01%)
    #Frequencies are computed relative to the total number of words that came before/after promise (total word count, not just unique words)
    #The first thing I noticed about the words that come after 'promise' is that, contrary to my expectations,
    #'to' was not the most common word -- 'you' was.
    #I also noticed that 'ring' followed promise with a notable frequency. I did not know promise rings were so popular.
    #I also thought that the two most common words to follow 'promise' would be 'to' and 'that'
    #However, 'that' was quite a bit farther down the list than 'to', and there were many more common options than I
    #had expected
    #In retrospect this makes sense given the common deletion of 'that' in informal speech and writing

    #As to the words preceding promise, as I expected, "I" was by far the most common.
    #I was also amused to see "pinky" on that list -- pinky promises are still in style, apparently.

    #Apart from these comments, I feel inadequately equipped to make meaningful analysis of this data.
    #I think for me, this was a successful exercise in the mechanics of natural language analysis
    #(not ALL of natural language analysis, but just a few techniques, obviously)
    #I think I will need to do some studying and thinking about how to advance my linguistic analysis itself