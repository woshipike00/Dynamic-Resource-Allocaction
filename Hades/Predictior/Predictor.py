__author__ = 'pike'

from Utils.FileUtil import VMFile
from Utils.MathUtil import *
from matplotlib import pyplot as plt
import random

class Predictor:

    def __init__(self, x, y):

        self.x = x
        self.y = y

    # add wave lengths with intensity > max/2
    def getFFTCandidate(self):

        fft = FFT(self.x, self.y)
        (fftX, fftY) = fft.computeFFT()

        #get local maximum and global maximum
        global_maximum = 0
        local_maximum = []
        for i in range(1, fftY.__len__() - 1):
            if (fftY[i] >= fftY[i - 1] and fftY[i] >= fftY[i + 1]):
                local_maximum.append([int(even(1 / fftX[i])), fftY[i]])
                if fftY[i] > global_maximum:
                    global_maximum = fftY[i]


        #add local_maximum with intensity that > global_maximum/2
        result = []
        for i in range(0, local_maximum.__len__()):
            if (local_maximum[i][1] >= global_maximum / 2):
                result.append(local_maximum[i])
        return result



    def getAutoCorrCandidate(self):

        auto = AutoCorrelation(self.y)
        (autoX, autoY) = auto.autocorr()

        #get local maximum and global maximum
        global_maximum = 0
        local_maximum = []
        for i in range(1, autoY.__len__() - 1):
            if (autoY[i] >= autoY[i - 1] and autoY[i] >= autoY[i + 1] and autoY[i] > 0):
                local_maximum.append([autoX[i], autoY[i]])
                if autoY[i] > global_maximum:
                    global_maximum = autoY[i]

        #add local_maximum with p that > global_maximum/2
        result = []
        for i in range(0, local_maximum.__len__()):
            if (local_maximum[i][1] >= global_maximum / 2):
                result.append(local_maximum[i])
        return result

    def getBestCandidate(self):

        if (self.x.__len__() < 2):
            return 0

        auto = AutoCorrelation(self.y)
        (autoX, autoY) = auto.autocorr()

        fftCandidateList = self.getFFTCandidate()
        autoCandidateList = self.getAutoCorrCandidate()

        #mset contains all the candidate wavelength
        mset = set()
        for i in range(0, fftCandidateList.__len__()):
            mset.add(fftCandidateList[i][0])
        for i in range(0, autoCandidateList.__len__()):
            mset.add(autoCandidateList[i][0])

        maxlen = autoX[autoX.__len__() - 1]
        bestwavelen = 0
        maxp = -1e13


        #caculate the average of the multiplies of the wavelen
        for wavelen in mset:
            multi = 1
            total = 0
            while(wavelen * multi <= maxlen):
                index = autoX.index(wavelen * multi)
                total += autoY[index]
                multi += 1
            if multi == 1:
                multi = 2
            average = total / (multi - 1)
            if average > maxp:
                bestwavelen = wavelen
                maxp = average

        return bestwavelen

    def predictFutureWave(self, num):

        resultX = []
        resultY = []
        bestCycle = self.getBestCandidate()
        for i in range(0, num):
            multi = 1
            values = []
            index = len(self.x) + i
            pos = index - bestCycle * multi / (self.x[1] - self.x[0])
            while pos >=0:
                if pos <= len(self.x):
                    values.append(self.y[pos])
                multi += 1
                pos = index - bestCycle * multi / (self.x[1] - self.x[0])
            rand = random.randint(0, len(values) - 1)
            resultX.append(index * (self.x[1] - self.x[0]))
            resultY.append(values[rand])
        return (resultX, resultY)


if __name__ == "__main__":

    file = open('../../Resource/VMs.csv',"r")
    lines = file.readlines()[1:]
    vmset = set()
    for line in lines:
        vmname = line.split(',')[0]
        vmset.add(vmname)
    vmset.remove('\r\n')
    file.close()

    #outfile = open("../../Resource/OUTPUT","w")
    #for vmname in vmset:
    #    vmdata = VMFile('../../Resource/VMs.csv')
    #    (x, y) = vmdata.getData(vmname)
    #    predictor = Predictor(x, y)
    #    bestcandidate = predictor.getBestCandidate()
    #    resultline = vmname + "\t" + str(bestcandidate) + "\t" + "%.2f" % (bestcandidate / 24.0) + '\n'
    #    outfile.write(resultline)
    #outfile.close()

    vmdata = VMFile('../../Resource/VMs.csv')
    #(x, y) = vmdata.getData('"zq-wuliu-liping-5.80"')
    (x, y) = vmdata.getData('"ks-yanglao-wx-5.95"')
    print x


    predictor = Predictor(x, y)
    print predictor.getBestCandidate()
    (preX, preY) = predictor.predictFutureWave(40)

    plt.plot(x, y)
    plt.plot(preX, preY)
    plt.show()






