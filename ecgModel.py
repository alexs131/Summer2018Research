
def ECGmodel(ecgString,fs):
    globalTime = 0
    Tp = 0
    Tpr = 0
    Tq = 0
    Tr = 0
    Ts = 0
    Tst = 0
    Tt = 0
    Trest = 0
    state = 0 #(start at first p interval seen)
    #states (p:0,print = 1 q:2,r:3,s:4,st:5 t:6,rest:7,sink:8))
    #Character encodings (end of p to q = x, st interval = y, rest = z)
    for char in ecgString:
        #print(state)
        if globalTime > 1200: #this should be defined by other stats of indiv.
            state = 8
        if state == 0:
            if char == 'p':
                Tp += (1/fs)*1000
                globalTime += (1/fs)*1000
                if Tp > 100:
                    print("Pwav too long")
                    state = 8
                else:
                    state = 0
            elif char == 'x':
                Tpr += (1/fs)*1000
                globalTime += (1/fs)*1000
                state = 1
            else:
                print(char)
                state = 8
        elif state == 1:
            if char == 'x':  #pr interval
               Tpr += (1/fs)*1000
               globalTime += (1/fs)*1000
               if Tp + Tpr > 200: #exceeded PR interval range
                   print("PR interval too long")
                   state = 8
               else:
                   state = 1
            elif char == 'q': #moving to q
               if Tp+Tpr <= 120:
                   print("PR interval too short")
                   state = 8
               else:
                   Tq += (1/fs)*1000
                   globalTime += (1/fs)*1000
                   state = 2

            elif char == 'r':
               #if Tp <= 200 and Tp >= 120:
               if Tp+Tpr <= 120:
                   print("PR interval too short")
                   state = 8
               else:
                   Tr += (1/fs)*1000
                   globalTime += (1/fs)*1000
                   state = 3
            else:
              print("Should not be reading this char")
              state = 8



        elif state == 2:
            if char == 'q':
                Tq += (1/fs)*1000
                globalTime += (1/fs)*1000
                if Tq + Tr + Ts > 120:
                    print("QRS too long")
                    state = 8
                else:
                    state = 2
            elif char == 'r':
                Tr += (1/fs)*1000
                globalTime += (1/fs)*1000
                if Tq + Tr + Ts > 120:
                    print("QRS too long")
                    state = 8
                else:
                    state = 3
            else:
                print("Reading incorrect char")
                state = 8
        elif state == 3:
            if char == 'r':
                Tr += (1/fs)*1000
                globalTime += (1/fs)*1000
                if Tq + Tr + Ts > 120:
                    print("QRS too long")
                    state = 8
                else:
                   state = 3
            elif char == 's':
                Ts += (1/fs)*1000
                globalTime += (1/fs)*1000
                if Tq + Tr + Ts > 120:
                    print("QRS too long")
                    state = 8
                else:
                   state = 4
            else:
                print("Should not read this char")
                state = 8
        elif state == 4:
            if char == 's':
                Ts += (1/fs)*1000
                globalTime += (1/fs)*1000
                if Tq + Tr + Ts > 120:
                    print("QRS too long")
                    state = 8
                else:
                   state = 4
            elif char == 'y': #ST interval
                if Tq + Tr + Ts < 80:
                    print("QRS is too short")
                    state = 8
                else:
                    Tst += (1/fs)*1000
                    state = 5
            elif char == 'z':
                Trest += (1/fs)*1000
                state = 7
            else:
                print("wrong char")
                state = 8


        elif state == 5: #stInterval
            if char == 'y':
                Tst += (1/fs)*1000
                globalTime += (1/fs)*1000
                if Tst > 150:
                    print("ST too long")
                    state = 8
                else:
                    state = 5
            elif char == 't':
                Tt += (1/fs)*1000
                globalTime += (1/fs)*1000
                state = 6

            else:
                print("Should not be reading this char")
                state = 8
        elif state == 6: #Twav
            if char == 't':
                Tt += (1/fs)*1000
                globalTime += (1/fs)*1000
                if Tt > 160 :
                    print("T too long")
                    state = 8
                else:
                    state = 6
            elif char == 'z': #new beat
                Trest += (1/fs)*1000
                globalTime += (1/fs)*1000
                state = 7
            else:
                state = 8
        elif state == 7:
            if char == 'z':
                Trest += (1/fs)*1000
                globalTime += (1/fs)*1000
                if Trest > 800: #depends on other factors
                    print(Trest)
                    print("Rest too long")
                    state = 8
                else:
                    state = 7

            elif char == 'p':

                globalTime = (1/fs)*1000
                Tp = (1/fs)*1000
                Tpr = 0
                Tq = 0
                Tr = 0
                Ts = 0
                Tst = 0
                Tt = 0
                Trest = 0
                state = 0
            else:
                state = 8


        elif state == 8:
            print("ECG not normal")
            return False
        else:
            print(state)
            raise Exception("Invalid State")
    return True
