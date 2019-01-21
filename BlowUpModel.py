from collections import defaultdict
def createStates():
    ret = [(0,0,0,0,0,0,0,0)] #global,Tp,Tpr,Tq,Ts,Tr,Tst,Tt,Trest,state
    return ret
#print(createStates(1000,5,100))
def createStates1(globalMax,Tp,Tpr,Tq,Tr,Ts,Tst,Tt,Trest,states,fs):
    res = [(0,0,0,0,0,0,0,0,0)]
    inter = (1/fs)*1000
    count = 0
    '''for i in range(globalMax+1):
        if i <= 60:
            res.append([i,i,0,0,0,0,0,0,0,0])
        if i > 60 and i <= 110:
            res.append([i,i,0,0,0,0,0,0,0,0])
            res.append([i,i,0,0,0,0,0,0,0,0])


        for T1 in range(Tp+1):
            for T2 in range(Tpr+1):
                for T3 in range(Tq+1):
                    for T4 in range(Tr+1):
                        for T5 in range(Ts+1):
                            for T6 in range(Tst+1):
                                for T7 in range(Tt+1):
                                    for T8 in range(Trest+1):
                                        for state in states:
                                            res.append([i,T1,T2,T3,T4,T5,T6,T7,T8,state])
                                            count += 1
                                            print(count)'''
    return res
#print(createStates1(1200,110,200,120,120,120,120,160,700,[0,1,2,3,4,5,6,7,8],1000))


def blowUp(states,alphabet,fs):
    graph = defaultdict(set)

    def ECGmodel(char,globalTime,Tp,Tpr,Tqrs,Tst,Tt,Trest,state):
        rstate = None
        if globalTime > 1200:
            rstate = 6
        if state == 0:
            if char == 'p':
                Tp += (1/fs)*1000
                globalTime += (1/fs)*1000
                if Tp > 110: #globalTime
                    #print("Pwav too long")
                    rstate = 6
                else:
                    rstate = 0
            elif char == 'x':
                Tpr += (1/fs)*1000
                globalTime += (1/fs)*1000
                if Tp < 60: #globalTime
                    #print("Pwav too short")
                    rstate = 6
                else:
                    rstate = 1
            else:
                #print(char)
                rstate = 6
        elif state == 1:
            if char == 'x':  #pr interval
                Tpr += (1/fs)*1000
                globalTime += (1/fs)*1000
                if Tp + Tpr > 200: #exceeded PR interval range #globalTime > 200
                   #print("PR interval too long")
                    rstate = 6
                else:
                   rstate = 1
            elif char == 'q': #think about this
                Tqrs += (1/fs)*1000
                globalTime += (1/fs)*1000#moving to q
                if Tp+Tpr <= 120 or Tpr < 10: #globalTime <= 120
                  # print("PR interval too short")
                    rstate = 6
                else:

                    rstate = 2
            else:
              #print("Should not be reading this char")
              rstate = 6



        elif state == 2:
            if char == 'q' or char == 'r' or char == 's':
                Tqrs += (1/fs)*1000
                globalTime += (1/fs)*1000
                if Tqrs > 120: #globalTime - Tp+Tpr > 120
                    print("QRS too long")
                    rstate = 6
                else:

                    rstate = 2
            elif char == 'y':
                globalTime += (1/fs)*1000
                Tst += (1/fs)*1000
                if Tqrs < 80:
                    #print("QRS is too short")
                    rstate = 6
                else:
                    state = 3
            else:
                #print("Reading incorrect char")
                rstate = 8

        elif state == 3: #stInterval
            if char == 'y':
                Tst += (1/fs)*1000
                globalTime += (1/fs)*1000
                if Tst > 120:
                    #print("ST too long")
                    rstate = 6
                else:

                    rstate = 3
            elif char == 't':
                Tt += (1/fs)*1000
                globalTime += (1/fs)*1000
                if Tst < 80: #globalTime - (Tpr+Tp+Tq+Tr+Ts)
                    rstate = 6
                else:
                    rstate = 4

            else:
                print("Should not be reading this char")
                rstate = 6
        elif state == 4: #Twav
            if char == 't':
                Tt += (1/fs)*1000
                globalTime += (1/fs)*1000
                if Tt > 250 : #globalTime - (Tpr+Tp+Tq+Tr+Ts+Tt)
                    print("T too long")
                    rstate = 8
                else:

                    rstate = 4
            elif char == 'z': #new beat
                Trest += (1/fs)*1000
                globalTime += (1/fs)*1000
                if Tt < 100:
                    print("T too short")
                    rstate = 8
                else:
                    rstate = 5
            else:
                rstate = 8
        elif state == 5:
            if char == 'z':
                Trest += (1/fs)*1000
                globalTime += (1/fs)*1000
                rstate = 5

            elif char == 'p':
                if globalTime < 600:
                    rstate = 6
                else:

                    globalTime = (1/fs)*1000
                    Tp = (1/fs)*1000
                    Tpr = 0
                    Tq = 0
                    Tr = 0
                    Ts = 0
                    Tst = 0
                    Tt = 0
                    Trest = 0
                    rstate = 0
            else:
                rstate = 6


        elif state == 6:
            rstate = 6
        else:
            print(state)
            raise Exception("Invalid State")
        return globalTime,Tp,Tpr,Tqrs,Tst,Tt,Trest,rstate
    visited = set()
    numIter = 0
    while states:
        print(states)
        globalTime,Tp,Tpr,Tqrs,Tst,Tt,Trest,state = states.pop(0)
        print((globalTime,Tp,Tpr,Tqrs,Tst,Tt,Trest,state))
        visited.add((globalTime,Tp,Tpr,Tqrs,Tst,Tt,Trest,state))
        for char in alphabet:

            gt,T1,T2,T3,T4,T5,T6,st1 = ECGmodel(char,globalTime,Tp,Tpr,Tqrs,Tst,Tt,Trest,state)
            if (gt,T1,T2,T3,T4,T5,T6,st1) not in visited and ((gt,T1,T2,T3,T4,T5,T6,st1))  not in states:
                if st1 != 8:
                    states.append((gt,T1,T2,T3,T4,T5,T6,st1))
            if st1 == 8:
                graph[(char,globalTime,Tp,Tpr,Tqrs,Tst,Tt,Trest,state)].add((0,0,0,0,0,0,0,8))
            else:
                graph[(char,globalTime,Tp,Tpr,Tqrs,Tst,Tt,Trest,state)].add((gt,T1,T2,T3,T4,T5,T6,st1))
            #if numIter > 1000:
                #break
        #numIter +=1
    return graph
print(blowUp(createStates(),['p','x','q','r','s','y','t','z'], 250))
