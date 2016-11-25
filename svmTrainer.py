import corpus_reader 
#import sklearn
#from sklearn import svm

for turn in corpus_reader.getNextTurn(1,1):
    #print(turn.Speaker)
    for w in turn.Words:
        print(w[0],w[1])



