import math
from matplotlib import pyplot as plt
import numpy as np


num = 1000
X = [i / num for i in range(0, num)]
Z = 0.1
C_sold = []
C_snew = []
k = 0.1
C_0 = 0.1
#C_E = 0.4
C_snewar = np.asarray([C_0 for i in range(0, num)])
C_soldar = np.asarray([C_0 for i in range(0, num)])
n = 8

def test(n, C_0, k, Z, num, C_snewar, C_soldar):

    '''设置初始浓度'''
    for i in range(1, n + 1):
        if n == 1:
            C_snewar[0] = C_0 * k
        else:
            C_snewar[0] = k * (1 / (Z*num)) * sum(C_soldar[:int(Z * num)])

        C_l = [C_0 for i in range(0, num)]
        C_lar = np.asarray(C_l)

        '''计算浓度分布'''
        for j in range(1,num):
            if j <= int((1-Z) * num):
                delt_C = C_soldar[j + int(Z * num) - 1] - C_snewar[j - 1]
                dC_l = delt_C / (Z * num)
                if j == 1:
                    C_lar[j] = C_snewar[0] / k + dC_l
                else:
                    C_lar[j] = C_lar[j - 1] + dC_l
                C_snewar[j] = k * C_lar[j]
            if j > int((1-Z) * num):
                C_lar[j] = C_lar[j - 1] * (num - j + 2 - 2 * k) / (num - j)
                C_snewar[j] = k * C_lar[j]

        '''交换新旧浓度'''
        C_soldar = C_snewar

        plt.plot(X[:950], C_snewar[:950])

    return C_snewar,C_soldar

test(n,C_0,k,Z,num,C_snewar,C_soldar)
print(sum(C_snewar[:899]))
plt.show()


