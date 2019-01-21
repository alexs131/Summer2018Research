#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 15:01:13 2018

"""

import matplotlib.pyplot as plt
import WTdelineator as wav
import wfdb
import numpy as np
from ecgModel import ECGmodel
'''
dbase = 'mitdb'
rec = '100'
sNum = 0

# When in linux
s, att = wfdb.rdsamp(rec,pb_dir=dbase)
print(s)
annot = wfdb.rdann(rec, 'atr', pb_dir=dbase)
sName = att['sig_name']
print(sName)
print(att['units'])
## When in Windows
#s, att = wfdb.rdsamp(rec,pb_dir=dbase)
#annot = wfdb.rdann(rec, 'event', pb_dir=dbase)
#sName = att['sig_name']

# Ranges to analyse signal
beg = int(0)
print(beg)
end = int(np.floor(2**10))
print(end)
#%%
fs = att['fs']
print(fs)
'''
'''
dbase = 'nsrdb'
rec = '16272'
sNum = 0

# When in linux
s, att = wfdb.rdsamp(rec,pb_dir=dbase)
print(s)
annot = wfdb.rdann(rec, 'atr', pb_dir=dbase)
sName = att['sig_name']
print(sName)
print(att['units'])
## When in Windows
#s, att = wfdb.rdsamp(rec,pb_dir=dbase)
#annot = wfdb.rdann(rec, 'event', pb_dir=dbase)
#sName = att['sig_name']

# Ranges to analyse signal
beg = int(0)
print(beg)
end = int(np.floor(2**10))
print(end)
#%%
fs = att['fs']
print(fs)
'''

dbase = 'staffiii/data'
rec = '052c'
sNum = 1

# When in linux
s, att = wfdb.rdsamp(rec,pb_dir=dbase)
print(s)
annot = wfdb.rdann(rec, 'event', pb_dir=dbase)
sName = att['sig_name']
print(sName)
print(att['units'])
## When in Windows
#s, att = wfdb.rdsamp(rec,pb_dir=dbase)
#annot = wfdb.rdann(rec, 'event', pb_dir=dbase)
#sName = att['sig_name']

# Ranges to analyse signal
beg = int(0)
print(beg)
end = int(np.floor(2**11))
print(end)
#%%
fs = att['fs']
print(fs)

sig = s[beg:end,sNum]
#print(s[2,2])
print(sig)
N = sig.shape[0]
t = np.arange(0,N/fs,1/fs)

# Wavelet Transform delineation
Pwav, QRS, Twav = wav.signalDelineation(sig,fs)
print(Pwav)
print(QRS)
print(Twav)
# Calculate biomarkers
QRSd = QRS[:,-1] - QRS[:,0]

Tind = np.nonzero(Twav[:,0])
QT = Twav[Tind,-1] - QRS[Tind,0]
Td = Twav[Tind,-1] - Twav[Tind,0]

Pind = np.nonzero(Pwav[:,0])
Pd = Pwav[Pind,-1] - Pwav[Pind,0]



plt.figure()
plt.plot(t,sig,label=sName[sNum])
plt.plot(t[QRS[:,0]],sig[QRS[:,0]],'*r',label='QRSon', markersize=15)
plt.plot(t[QRS[:,1]],sig[QRS[:,1]],'*y',label='Q', markersize=15)
plt.plot(t[QRS[:,2]],sig[QRS[:,2]],'*k',label='R', markersize=15)
plt.plot(t[QRS[:,3]],sig[QRS[:,3]],'*m',label='S', markersize=15)
plt.plot(t[QRS[:,4]],sig[QRS[:,4]],'*g',label='QRSend', markersize=15)
plt.plot(t[Twav[:,0]],sig[Twav[:,0]],'^r',label='Ton', markersize=10)
plt.plot(t[Twav[:,1]],sig[Twav[:,1]],'^k',label='T1', markersize=10)
plt.plot(t[Twav[:,2]],sig[Twav[:,2]],'^m',label='T2', markersize=10)
plt.plot(t[Twav[:,3]],sig[Twav[:,3]],'^g',label='Tend', markersize=10)
plt.plot(t[Pwav[:,0]],sig[Pwav[:,0]],'or',label='Pon', markersize=10)
plt.plot(t[Pwav[:,1]],sig[Pwav[:,1]],'ok',label='P1', markersize=10)
plt.plot(t[Pwav[:,2]],sig[Pwav[:,2]],'om',label='P2', markersize=10)
plt.plot(t[Pwav[:,3]],sig[Pwav[:,3]],'og',label='Pend', markersize=10)
plt.title('Delineator output')
plt.xlabel('Time (s)')
plt.ylabel('ECG (mV)')
plt.legend()
plt.show()

def convertSignal(pWave,qrs,tWav):
    res = ""
    smallest = min(len(tWav),min(len(pWave),len(qrs)))
    endTime = pWave[1][0]
    for i in range(smallest):
        if pWave[i][3] == 0:
            print("No pWave, abnormal")
        startTime = pWave[i][0]
        restint = 0
        if startTime > endTime: #next interval
            restint = startTime-endTime
        res += restint*'z'
        pint = pWave[i][3]-pWave[i][0]
        pqint = qrs[i][0]-pWave[i][3]
        if qrs[i][1] == 0:
            print("No Q wave detected, filling with R instead")
            qint = 0
            rint = qrs[i][2]-qrs[i][0]
        else:
            qint = qrs[i][1]-qrs[i][0]
            rint = qrs[i][2]-qrs[i][1]
        if qrs[i][3] == 0:
            print("No S wave detected, filling with R instead")
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
    return res
res = convertSignal(Pwav,QRS,Twav)
print(res)
curChar = res[0]
count = 0
for char in res:
    if char == curChar:
        count += 1
    else:
        print(curChar + str(count))
        curChar = char
        count = 0
print(ECGmodel(res,fs))
