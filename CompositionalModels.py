from collections import defaultdict
from graphviz  import Digraph
def Pmodel(char,Tp,state,fs):
    rstate = None
    if state == 0:
        if char == 'p':
            Tp += (1/fs)*1000

            if Tp > 120:
                rstate = 2 #sink state

            else:
                rstate = 0
        else:
            if char != 'n':
                if Tp >= 60 and Tp <= 110:
                    rstate = 1
                else:
                    rstate = 2
            else:
                rstate = 2
    elif state == 1:
        if char == 'p':
            rstate = 2
        if char != 'n':
            rstate = 1
        else:
            rstate = 0
            Tp = 0
    elif state == 2:
        rstate = 2
    else:
        raise Exception("Invalid State")
    if rstate != 0:
        return -1,rstate
    else:
        return Tp,rstate

def PRmodel(char,Tpr,state,fs):
    rstate = None
    if state == 0:
        if char == 'p' or char == 'x':
            Tpr += (1/fs)*1000

            if Tpr > 200:
                rstate = 2 #sink state

            else:
                rstate = 0
        else:
            if char != 'n':
                if Tpr >= 120 and Tpr <= 200:
                    rstate = 1
                else:
                    rstate = 2
            else:
                rstate = 2
    elif state == 1:
        if char == 'p' or char == 'x':
            rstate = 2
        if char != 'n':
            rstate = 1
        else:
            rstate = 0
            Tpr = 0
    elif state == 2:
        rstate = 2
    else:
        raise Exception("Invalid State")
    if rstate != 0:
        return -1,rstate
    else:
        return Tpr,rstate
def QRSmodel(char,Tqrs,state,fs):
    rstate = None

    if state == 0:
        if (char == 'p' or char == 'x') and Tqrs == 0:
            rstate = 0
        elif char == 'q' or char == 'r' or char == 's':
            Tqrs += (1/fs)*1000
            if Tqrs > 100:
                rstate = 2
            else:
                rstate = 0
        else:
            if char != 'n':
                if Tqrs >= 80 and Tqrs <= 100:
                    if char == 'p' or char == 'x':
                        rstate = 2
                    else:
                        rstate = 1
                else:
                    rstate = 2
            else:
                rstate = 2
    elif state == 1:
        if char == 'p' or char == 'x' or char == 'q' or char == 'r' or char == 's':
            rstate = 2
        if char != 'n':
            rstate = 1
        else:
            rstate = 0
            Tqrs = 0
    elif state == 2:
        rstate = 2
    else:
        raise Exception("Invalid State")
    if rstate != 0:
        return -1,rstate
    else:
        return Tqrs,rstate

def STmodel(char,Tst,state,fs):
    rstate = None

    if state == 0:
        if (char == 'p' or char == 'x' or char == 'q' or char == 's' or char == 'r') and Tst == 0:
            rstate = 0
        elif char == 'y':
            Tst += (1/fs)*1000
            if Tst > 120:
                rstate = 2
            else:
                rstate = 0
        else:
            if char != 'n':
                if Tst >= 80 and Tst <= 120:
                    if char == 'p' or char == 'x' or char == 'q' or char == 's' or char == 'r':
                        rstate = 2
                    else:
                        rstate = 1
                else:
                    rstate = 2
            else:
                rstate = 2
    elif state == 1:
        if char == 'p' or char == 'x' or char == 'q' or char == 'r' or char == 's' or char == 'y':
            rstate = 2
        if char != 'n':
            rstate = 1
        else:
            rstate = 0
            Tst = 0
    elif state == 2:
        rstate = 2
    else:
        raise Exception("Invalid State")
    if rstate != 0:
        return -1,rstate
    else:
        return Tst,rstate

def Tmodel(char,globalTime,Tt,state,fs):
    rstate = None

    if state == 0:
        if (char == 'p' or char == 'x' or char == 'q' or char == 's' or char == 'r' or char == 'y') and Tt == 0:
            rstate = 0
        elif char == 't':
            Tt += (1/fs)*1000
            if Tt > 250:
                rstate = 2
            else:
                rstate = 0
        else:
            if char != 'n':
                if Tt >= 100 and Tst <= 250:
                    if char == 'p' or char == 'x' or char == 'q' or char == 's' or char == 'r' or char == 'y':
                        rstate = 2
                    else:
                        rstate = 1
                else:
                    rstate = 2
            else:
                rstate = 2
    elif state == 1:
        if char == 'p' or char == 'x' or char == 'q' or char == 'r' or char == 's' or char == 'y' or char == 't':
            rstate = 2
        if char != 'n':
            rstate = 1
        else:
            rstate = 0
            Tt = 0
    elif state == 2:
        rstate = 2
    else:
        raise Exception("Invalid State")
    if rstate != 0:
        return -1,rstate
    else:
        return Tst,rstate

'''def Trestmodel(char,globalTime,Trest,state,fs):
    rstate = None
    if globalTime > 1200:
        state = 1
    if state == 0:
        if char == 'z':
            Trest += (1/fs)*1000
            globalTime += (1/fs)*1000
            if globalTime > 1200:
                rstate = 1
            else:


                rstate = 0
        else:
            rstate = 1
    else:
        rstate = 1
    return globalTime,Trest,rstate'''

def blowUpP(alphabet,fs,states,model):
    visited = set()
    numIter = 0
    graph = defaultdict(set)
    while states:
        #print(states)
        Tp,state = states.pop(0)
        #print((Tp,state))
        visited.add((Tp,state))
        for char in alphabet:
            print(char,Tp,state,fs)
            T1,st1 = model(char,Tp,state,fs)
            if (T1,st1) not in visited and ((T1,st1))  not in states:
                states.append((T1,st1))
            graph[(char,Tp,state)].add((T1,st1))
        if numIter > 130:
            break
        numIter +=1
    return graph
g = blowUpP(['p','x','q','r','s','y','t','z','n'], 1000,[(0,0)],QRSmodel)
print(g)
print(g[('p',-1,1)])

dot = Digraph(comment='The Round Table')
count = 0
for c,a,b in g:
    for (u,v) in g[(c,a,b)]:
        if a >= 90 or a == -1:
            dot.edge(str((a,b)),str((u,v)),label=c)
dot.render('EKG/p-graph.gv', view=True)
'EKG/p-graph.gv.pdf'
