import math
from matplotlib import pyplot as plt
import numpy as np


num = 10000
X = [i / num for i in range(0, num)]
Z = 0.05
C_sold = []
C_snew = []

k = 0.15
v = 1e-3    #cm*s-1
delt = 0.1  #cm
D = 1e-4    #cm2*s-1
kE = k / ((1-k)*math.exp(-v*delt/D) + k)

C_0 = 0.02
#C_E = 0.4
C_snewar = np.zeros(num)
C_soldar = np.zeros(num)

def firsts_melting(Z, k, C_0, num):
    for i in range(0,int((1-Z)*num)):
        C_s = (1 - (1 - k) * (math.exp(-(k * (i/num) / Z)))) * C_0
        C_snew.append(C_s)
    for i in range(int((1-Z)*num),int(num)):
        C_s = (1 - (1 - k) * (math.exp(-(k * (1 - Z) / Z)))) * (1-(i/num - (1 - Z))/Z)**(k - 1) * C_0
        C_snew.append(C_s)

    C_snewar = np.asarray(C_snew)
    return C_snewar

def cal_new_C0(C_soldar, k, Z, num):
    C_0new = k * (1 / (Z*num)) * sum(C_soldar[:int(Z * num)])
    C_snewar[0] = C_0new
    return C_0new

def cal_mid_Cs(Z,k,C_0new, num):
    C_l = [0 for i in range(1,int((1-Z) * num) + 2)]

    for i in range(1,int((1-Z) * num) + 1):
        delt_C = C_soldar[i + int(Z*num) -1] - C_snewar[i - 1]
        dC_l = delt_C / (Z * num)
        if i == 1 :
            C_l[i] = C_0new / k + dC_l
        else:
            C_l[i] = C_l[i-1] + dC_l
        C_snewar[i] = k * C_l[i]

def cal_last_Cs(Z,k,num):
    C_lz = (C_0 - sum(C_snewar[:int((1-Z) * num) + 1]) / num) / Z
    for i in range(int((1-Z) * num) + 1, num + 1):
        C_snewar[i - 1] = C_lz
        '''C_snewar[i-1] = (1 - (1 - k) * math.exp(-k * (1 - Z) / Z))  * C_lz * ((1-((i/num - (1 - Z))/Z)) ** (k - 1))'''
        #print(math.pow((1-(i/num - (1 - Z))/Z),(k - 1)),i)
        #print((1-(i/num - (1 - Z))/Z),i)

if __name__ == '__main__':
    n = 10
    for i in range(1, n + 1):
        if i == 1:
            C_snewar = firsts_melting(Z,kE,C_0,num)
            plt.plot(X[:8000],C_snewar[:8000])
            C_soldar = C_snewar
        else:
            C_0new = cal_new_C0(C_soldar,kE,Z,num)
            cal_mid_Cs(Z,kE,C_0new,num)
            cal_last_Cs(Z,kE,num)
            print(C_snewar[6999])
            C_soldar = C_snewar
            plt.yscale("log")
            plt.plot(X[:8000],C_snewar[:8000])
            #plt.plot(X, C_snewar)
            #plt.plot(X,C_snew)
            #print(C_snew[8002])#if i == 10:
            #print(C_snew[8999],C_snew[9000],C_snew[1])
    plt.show()
