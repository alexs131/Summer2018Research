def convertSignal(pWav,qrs,tWav):
    res = ""
    smallest = min(len(tWav),min(len(pWav),len(qrs)))
    #assumes p is start but can be adapted
    endTime = 0
    for i in range(len(smallest)):
        if pWave[i][3] == 0:
            print("no p wave found definitely abnormal")
        startTime = pWave[i][0]
        if startTime > endTime: #next interval
            restint += startTime-endTime
        res += restint*'z'
        pint = pWave[i][3]-pWave[i][0]
        pqint = qrs[i][0]-pWave[i][3]
        if qrs[i][1] == 0:
            qint = 0
            rint = qrs[i][2]-qrs[i][0]
        else:
            qint = qrs[i][1]-qrs[i][0]
            rint = qrs[i][2]-qrs[i][1]
        if qrs[i][3] == 0:
            sint = 0
            rint += qrs[i][4]-qrs[i][2]
        else:
            sint = qrs[i][4]-qrs[i][3]
            rint += qrs[i][3]-qrs[i][2]

        stint = tWav[i][0]-qrs[i][4]
        tint = tWav[i][3]-tWav[i][0]
        res += (pint)*'p'
        res += (pqint)*'x'
        res += (qint)*'q'
        res += (rint)*'r'
        res += (sint)*'s'
        res += (stint)*'y'
        res += (tint)*'t'
        endTime = tWav[i][3]
