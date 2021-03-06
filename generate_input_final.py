#from psychopy import * #import all libraries from PsychoPy
import math
import numpy as np
from matplotlib.pyplot import plot,show,hist,subplots,tight_layout,savefig,ion
from matplotlib import rc
import pylab
from random import randrange,choice,shuffle
import sys
import os


# TRIAL TYPES
CTRL=0
CW=2
CCW=1

IN=3
OUT=4

codes = ["CTRL","CW", "CCW", "IN","OUT"]

#delta of proximity
delta_t=[12,16,20]

#rings
R1=7.7220520175418175
R2=10.700493835254752
R3=13.678935652967688

Rs=[R1,R2,R3]

delays = [[0],[3]]
ri=30
rf=60


CM=['Blue','Green', 'Grey', 'Orange', 'Purple', 'Red', 'Cyan']

def validate(trials):
    # atrials=np.array(trials)
    # T1 = map(cal_quadrant,a[:,3])
    # T2 = map(cal_quadrant,a[:,5])
    # T3 = map(cal_quadrant,a[:,7])

    return True

def calc_quadrant(angle):
  return int(angle) / 90 + 1

def oposite(quadrant):
    op=(quadrant+2)%4
    return (4 if op < 1 else op)

def genPos(quadrant):
    Q=(quadrant-1)*90
    angle=randrange(ri,rf,1)+Q
    return np.mod(angle,360)

def genCCW(quadrant,R,delta):
    ring1=R
    probe=genPos(quadrant)
    neigh=probe-delta
    ring2=choice(Rs)
    return [ring1,probe,ring1,neigh]
    
def genCW(quadrant,R,delta):
    ring1=R
    probe=genPos(quadrant)
    neigh=probe+delta
    ring2=choice(Rs)
    return [ring1,probe,ring1,neigh]
    
def genIO(quadrant,R_1,R_2):
    probe=genPos(quadrant)
    ring=choice(Rs)
    return [R_1,probe,R_2,probe]

def genIO2(quadrant):
    probe=genPos(quadrant)
    ring=choice([R1,R2])
    return [R2,probe,R1,probe]

def genRand(quadrant):
    Q=[q for q in [1,2,3,4] if q != quadrant]
    far1=genPos(quadrant)
    ring1=genR()

    q,Q=choicePop(Q)
    far2=genPos(q)
    ring2=genR()

    q,_=choicePop(Q)
    far3=genPos(q)
    ring3=genR()
    return [ring1,far1,ring2,far2]

def genR():
    r=randrange(Rs[0],Rs[2])
    r_d=randrange(1,9)/10.0
    return r+r_d

def choicePop(list):
    c=choice(list)
    i=0
    for n in list:
      if n == c: 
        new_list = list[0:i]+list[i+1:]
      i+=1
    return (c,new_list)

def genCtr(quadrant,R):
    ring1=R
    probe=genPos(quadrant)
    return [ring1,probe,-1,-1]
    
if __name__ == "__main__":
    
    valid=False
    trials=[]
    while(not valid):
      valid = validate(trials)
      for d in delays:
        for q in range(1,4+1):

            # IN TRIALS
            trials.append(d+[IN]+genIO(q,Rs[0],Rs[1])) # dr1
            trials.append(d+[IN]+genIO(q,Rs[1],Rs[2])) # dr2
            trials.append(d+[IN]+genIO(q,Rs[0],Rs[2])) # dr3

            # OUT TRIALS
            trials.append(d+[OUT]+genIO(q,Rs[1],Rs[0])) # dr1
            trials.append(d+[OUT]+genIO(q,Rs[2],Rs[1])) # dr2
            trials.append(d+[OUT]+genIO(q,Rs[2],Rs[0])) # dr3

            # Controls
            for _ in range(3):
                trials.append(d+[CTRL]+genCtr(q,Rs[0]))
                trials.append(d+[CTRL]+genCtr(q,Rs[1]))
                trials.append(d+[CTRL]+genCtr(q,Rs[2]))

    for q in range(1,4+1):

        d=delays[0]
        orients=[]

        # CW/CCW
        gens=[genCW,genCCW]*3
        types=[CW,CCW]*3
        idx = [0,1]*3

        # R1
        i,idx = choicePop(idx)
        trials.append(d+[types[i]]+gens[i](q,Rs[0],delta_t[0])) # R1 dt1
        orients+=[i]

        i,idx = choicePop(idx)
        trials.append(d+[types[i]]+gens[i](q,Rs[0],delta_t[1])) # R1 dr2
        orients+=[i]
      
        i,idx = choicePop(idx)
        trials.append(d+[types[i]]+gens[i](q,Rs[0],delta_t[2])) # R1 dr2
        orients+=[i]

        # R3
        i,idx = choicePop(idx)
        trials.append(d+[types[i]]+gens[i](q,Rs[2],delta_t[0])) # R1 dt1
        orients+=[i]

        i,idx = choicePop(idx)
        trials.append(d+[types[i]]+gens[i](q,Rs[2],delta_t[1])) # R1 dr2
        orients+=[i]
      
        i,idx = choicePop(idx)
        trials.append(d+[types[i]]+gens[i](q,Rs[2],delta_t[2])) # R1 dr2
        orients+=[i]

        d=delays[1]

        # R1
        trials.append(d+[types[orients[0]]]+gens[orients[0]](q,Rs[0],delta_t[0])) # R1 dt1
        trials.append(d+[types[orients[1]]]+gens[orients[1]](q,Rs[0],delta_t[1])) # R1 dr2
        trials.append(d+[types[orients[2]]]+gens[orients[2]](q,Rs[0],delta_t[2])) # R1 dr2

        # R3
        trials.append(d+[types[orients[3]]]+gens[orients[3]](q,Rs[2],delta_t[0])) # R1 dt1
        trials.append(d+[types[orients[4]]]+gens[orients[4]](q,Rs[2],delta_t[1])) # R1 dr2
        trials.append(d+[types[orients[5]]]+gens[orients[5]](q,Rs[2],delta_t[2])) # R1 dr2



                
    shuffle(trials)
    shuffle(trials)

          

    atrials=np.array(trials)

    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 8}

    rc('font', **font)


    f,ax=subplots(3,2)
    i=0
    for j in [atrials[:,1]==k for k in [CTRL, CW, CCW, IN, OUT]]:
        axi = ax[i/2,np.mod(i,2)]
        a = atrials[j,3]
        b = atrials[j,5]
        points = list(a)+list(b[b != 1])
        if atrials[j,1][0] == CTRL:
            points = list(a)
        axi.hist(points,360,color=CM[i])
        axi.set_title(codes[i]+": "+str(len(points)/2))
        i+=1

    points = list(atrials[:,3])+list(atrials[:,5])
    axi =  ax[i/2,np.mod(i,2)]
    axi.hist(points,360,color='k')
    axi.set_title("All: "+str(len(points)/2))
    tight_layout()

    pdir = "subjects_trials"
    subj = sys.argv[1]
    
    if os.path.exists(pdir+"/"+subj):
        n=1
        while os.path.exists(pdir+"/"+subj+str(n)): 
            n+=1
        subj=subj+"_"+str(n)


    if not os.path.isdir(pdir+"/"+subj):
        os.makedirs(pdir+"/"+subj)

    savefig(pdir+"/"+subj+"/"+'trials.png',dpi=500)

    # 3 blocks trials
    file1 = open(pdir+"/"+subj+"/"+"stim1.txt",'w')
    file2 = open(pdir+"/"+subj+"/"+"stim2.txt",'w')
    file3 = open(pdir+"/"+subj+"/"+"stim3.txt",'w')

    trials1 = trials[0:len(trials)/3]
    trials2 = trials[len(trials)/3:2*len(trials)/3]
    trials3 = trials[2*len(trials)/3:len(trials)]

    file1.write("DELAY\tTYPE\tR1\tT1\tR2\tT2\n")
    while len(trials1):
        t=trials1.pop()
        file1.write('\t'.join(map(str, t))+"\n")

    file2.write("DELAY\tTYPE\tR1\tT1\tR2\tT2\n")
    while len(trials2):
        t=trials2.pop()
        file2.write('\t'.join(map(str, t))+"\n")

    file3.write("DELAY\tTYPE\tR1\tT1\tR2\tT2\n")
    while len(trials3):
        t=trials3.pop()
        file3.write('\t'.join(map(str, t))+"\n")
     




     
