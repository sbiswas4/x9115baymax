import nose
import sys
import logging
import random
import string

import coverage
cov=coverage.Coverage()
coverage.process_startup()
cov.start()

import test_maincode_str
from test_maincode_str import *


frontier = []
param_list = []
cov_list = []
cov_dict = {}
prev_cov_dict = {}
main_lists = []
n = 10
de_max = 50
f = 0.75
cf = 0.3
patience = 15
candidates = 200

def de():
    basefrontier = generateFrontier()
    print basefrontier
    for x in range(de_max):
        old  = basefrontier
        basefrontier = update(basefrontier)
##        if old == basefrontier:
##            print "same"
##            break;
        #print basefrontier
        global patience,cov_dict,prev_cov_dict
        if patience == 0:
            print "*"*40
            print "Ran out of patience"
            print "*"*40
            print cov_dict
            break
    #print basefrontier
    return basefrontier
    
def update(frnt):
##    print "in update"
    global patience
    generator(frnt)
    if cov_dict == prev_cov_dict:
        print "No change in coverage"
        patience -= 1
    for i,x in enumerate(frnt):
        newx = extrapolate(frnt,x,f,cf)
        frnt[i] = better(x,newx)
    return frnt

def extrapolate(frnt,one,f,cf):
    two,three,four = threeOthers(frnt,one)
    new = [0]*len(one)
    #TODO: use numpy
    for i in range(len(one)):
        x,y,z = two[i],three[i],four[i]
        if random.random() < cf:
            tmp = int(x + f*(y - z))
            new[i] = trim(tmp)
            #print new[i],
##            print '%%'*50
##            print "changd"
##            print '%%'*50
        else:
            new[i] = one[i]
            
    return tuple(new)

def randomword(length):
   a = ''.join(random.choice(string.lowercase) for i in range(length))
   return a
   
def trim(x):
    return max(1, min(x,40))
    
def better(x,new):
    x_list = 0
    list_coverage = 0
    for i,some_list in enumerate(main_lists):
        if x in some_list:
            x_list = i
            break
    global cov_dict
##    print cov_dict
    list_coverage = cov_dict[x_list]
    if list_coverage > 0.85:
        return x
    return new
        

def threeOthers(frnt,avoid):
    def oneOther():
        x = avoid
        while x in seen:
            x = a(frnt)
        seen.append(x)
        return x
    seen =[avoid]
    two = oneOther()
    three = oneOther()
    four = oneOther()
    return two,three,four

def a(lst):
    return lst[random.randint(0,candidates-1)]
    
        
def generateFrontier():
    frontier1 = []
    for i in range(candidates):
        a1 = random.randint(1,40)
        a2 = random.randint(1,40)
        a3 = random.randint(1,40)
        a4 = random.randint(0,40)
        print "[ "+ str(a1) + " " + str(a2) + " " + str(a3) + " " + str(a4) + "  ]"
        a = (a1,a2,a3,a4)
            #get from some optimizer, DE? based on current value? get frontier with say 200 values         
        frontier1.append(a)
    return frontier1
    
def test_de():
    print "in test DE"
    de()
    
##param_list = [(1, 1), (5,3), (8, 6)]
def generator(current_frontier):
##    print current_frontier
    print "inside"
    #print current_frontier
    global cov_dict,prev_cov_dict
    prev_cov_dict = cov_dict
    main_lists = [current_frontier[i:i+n] for i in range(0,len(current_frontier),n)]
    
    for i,sub_list in enumerate(main_lists):
##        print i," ",sub_list
##        cov.erase()
        cov.start()
        for params in sub_list:
##            check_em(params[0], params[1])
            check_em_too(randomword(params[0]), randomword(params[1]),randomword(params[2]), randomword(params[3]))
        cov.stop()
        cov.html_report()
        dict = cov.analysis2('test_maincode_str.py')
##        print dict
        totLines = dict[1]
        msdLines = dict[3]
        linesExe = len(totLines) - len(msdLines)
        linesExePc = (float)(linesExe)/ len(totLines)
        cov_list.append(linesExePc)
        cov_dict[i] = linesExePc
    print "cov dict inside ",cov_dict
        
##de()    

if __name__ == '__main__':

    global module_name
    module_name = sys.modules[__name__].__file__
    print sys.modules[__name__]
    logging.debug("running nose for package: %s", module_name)
##    argv = ['fake','--nocapture']
    result = nose.run(argv=[sys.argv[0],
                            module_name,
                            '-v', '--nocapture'])#,'--with-coverage','--cover-tests'])
    logging.info("all tests ok: %s", result)

