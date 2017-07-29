import json
import math as m
import collections as c

toy = 'This is not a real sentence, Alfred.'.split()

def flatten_list(mylist):
    '''
    :param mylist: a (presumably nested) list
    :return: the same list, completely flattened
    '''
    result = []
    for item in mylist:
        if type(item) is list:
            result.extend(flatten_list(item))
        else:
            result.append(item)
    return result

def count_unigrams(corpus,vocab):
    result = {}
    for uni in vocab:
        result[uni] = 0
    for uni in corpus:
        result[uni] += 1
    return result

def count_bigrams(corpus,vocab):
    result = {}
    for uni1 in vocab:
        for uni2 in vocab:
            result[(uni1,uni2)] = 0
    for i in range(1,len(corpus)):
        bigram = (corpus[i-1],corpus[i])
        result[bigram] = result.get(bigram,0) + 1
    # total = sum(result.values())
    # for key,val in result.items():
    #     result[key] = float(val)/float(total)
    return result

def bigram_model(corpus,vocab,smooth):
    V = len(vocab)
    #result = {word: {word: smooth for word in vocab} for word in vocab}
    result = c.defaultdict(dict)
    bigramized = count_bigrams(corpus,vocab)
    unigramized = count_unigrams(corpus,vocab)
    for (a,b) in bigramized:
        #result[a][b] = float(bigramized[(a,b)]+smooth)/(count_unigrams(corpus,vocab)[b]+(smooth*V))
        result[a][b] = float(bigramized[(a,b)]+smooth)/(unigramized[a]+(smooth*V))
    return result

def cross_entropy(model,test):
    '''
    :param freqs: a dictionary of frequencies
    :param testcorpus: the corpus representing the test data
    :return: a float representing the cross entropy
    '''
    total = 0
    for i in range(1,len(test)):
        total += m.log(model[test[i-1]][test[i]],2)
    return -1 * float(total)/float(len(test)-1)
#    return -1 * float(sum([float(m.log(model[x][x+1],2)) for x in test]))/float(len(test))

def perplexity(model,test):
    '''
    :param freqs: a dictionary of frequencies
    :param testcorpus: the corpus representing the test data
    :param field: the field in testcorpus containing the parsed tweets
    :return: a float representing the perplexity
    '''
    x = cross_entropy(model,test)
    return float(2)**float(x)

####Uncomment below to reproduce my results
# with open('Reuters.txt','r') as f:
#     corpus = json.loads(f.read())
#     training = corpus[0:10000]
#     test = corpus[10000:20000]
#     vocab = set(corpus[0:20000])
#     print "vocabulary initialized....."
#     #Laplace smoothing
#     laplace_model = bigram_model(training,vocab,1)
#     print "Laplace model complete....."
#     #Expected Likelihood Estimation
#     ele_model = bigram_model(training,vocab,.5)
#     print "Ellie model complete....."
#     #0.0001 smoothing
#     low_model = bigram_model(training,vocab,.0001)
#     print "Lidstone 0.0001 smoothing model complete....."
#     #Testing the different models:
#     ##Laplace:
#     print "Laplace smoothing model cross entropy: " + str(cross_entropy(laplace_model,test)) + "and perplexity: " + str(perplexity(laplace_model,test))
#     ##ELE:
#     print "ELE smoothing model cross entropy: " + str(cross_entropy(ele_model,test)) + "and perplexity: " + str(perplexity(ele_model,test))
#     ##Low Lidstone Value:
#     print "Lidstone 0.0001 smoothing model cross entropy: " + str(cross_entropy(low_model,test)) + "and perplexity: " + str(perplexity(low_model,test))

### Or instead of running the above code, just look at this:
## This was run on 10,000 words each for training and testing
# Laplace smoothing model cross entropy: 11.1111787004 and perplexity: 2212.06597668
# ELE smoothing model cross entropy: 10.8814147331 and perplexity: 1886.3932334
# Lidstone 0.0001 smoothing model cross entropy: 11.6029246838 and perplexity: 3110.48683286

# It would appear that in this case, the model which used ELE smoothing did th best. It had the lowest cross entropy,
# meaning that it was, on average, the least surprised of the three models.
# As to maximum likelihood estimation... wouldn't that involve no smoothing? If that is correct then our model would
# just break when it saw something new in the test data. It would be infinitely surprised and die. So that would
# be a bad idea.