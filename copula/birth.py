import numpy as np
from itertools import combinations
from allfrank import allfrank
from allclayton import allclayton
from bayes_birth_only_frank import bayes_birth_only_frank

def birth(currentModel, u, dist, numbrk, q):

    sample = len(u)
    j = np.argwhere(currentModel == 0).max()
    L = len(currentModel) - j

    new = np.sort(currentModel)

    k = np.random.uniform(low=dist, high=sample - dist)
    w = np.random.uniform()

    if j < numbrk and not np.all(np.any(np.absolute(k * np.ones(shape=(L+j,1)) - new)) <= dist* np.ones(shape=(L+j,1))):
        z = 1
        kn = k
        new[j][0] = kn
        bir = np.sort(new)
        j2 = np.argwhere(currentModel == 0).max()

        t2 = currentModel[np.sort(currentModel) != 0]

        if kn > np.max(t2):
            Q = q[:numbrk - j2 - 2]
            temp = [comb for comb in combinations([1, 2, 3], 2)]
            j = 0
            G = 0

            while j < 3 and G == 0:
                if np.all(temp[j:] != np.ones(shape=(1,2)) * q[:numbrk - j2 - 1]):
                    G = 1
                    temp[j:] = []

                j += 1

            a = np.random.uniform()
            row = np.random.uniform(low=1 , high=2)

            if a < 1/3:
                Q[numbrk - j2 - 1: numbrk - j2 + 1] = temp[row:].H
            else:
                if a >= 1/3 and a < 2/3:
                    Q[numbrk - j2 - 1: numbrk - j2 + 1] = np.fliplr(temp[row:]).H
                else:
                    if a >= 2/3:
                        Q[numbrk - j2 - 1: numbrk - j2 + 1] = np.ones(shape=(2,1)) * q[numbrk - j2][0]

            Q[d - j2 + 1: numbrk + 1] = np.ones(shape=(1,1)) * Q[d- j2]
            s = np.concatenate((q[numbrk - j2 - 1], Q[numbrk - j2 - 1: numbrk - j2 + 1]), axis=0)

        else:
            if kn < np.min(t2):
                Q = np.zeros(shape=(numbrk + 1, 1))
                Q[2:numbrk + 1] = q[1:numbrk]
                temp = [comb for comb in combinations([1, 2, 3], 2)]
                j = 0
                G = 0

                while j < 3 and G == 0:
                    if np.all(temp[j:] != np.ones(shape=(1,2)) * q[0]):
                        G = 1
                        temp[j:] = []

                    j += 1

                a = np.random.uniform()
                row = np.random.uniform(low=1 , high=2)

                if a < 1/3:
                    Q[:2] = temp[row:].H
                else:
                    if a >= 1/3 and a < 2/3:
                        Q[:2] = np.fliplr(temp[row:]).H
                    else:
                        if a >= 2/3:
                            Q[:2] = np.ones(shape=(2,1)) * q[1][0]

                s = np.concatenate((q[0], Q[:2]), axis=0)

            else:
                Q[:d - j2 - 1] = q[:d - j2 - 1]
                temp = [comb for comb in combinations([1, 2, 3], 2)]

                j = 0
                G = 0
                while j < 3 and G == 0:
                    if np.all(temp[j:] != np.ones(shape=(1,2)) * q[d - j2]):
                        G = 1
                        temp[j:] = []

                    j += 1

                a = np.random.uniform()
                row = np.random.uniform(low=1 , high=2)

                if a < 1/3:
                    Q[d - j2 - 1:d - j2 + 1] = temp[row:].H
                else:
                    if a >= 1/3 and a < 2/3:
                        Q[d - j2 - 1:d - j2 + 1] = np.fliplr(temp[row:]).H
                    else:
                        if a >= 2/3:
                            Q[d - j2 - 1:d - j2 + 1] = np.ones(shape=(2,1)) * q[d - j2][0]

                Q[d - j2 + 1: numbrk + 1] = q[d - j2:numbrk]
                s = np.concatenate((q[d - j2 - 1], Q[d - j2 - 1:d - j2 + 1]), axis=0)

    elif j == numbrk and not np.all(np.any(np.absolute(k * np.ones(shape=(L+j,1)) - new)) <= dist* np.ones(shape=(L+j,1))):
        z = 1
        kn = k
        new[j][0] = kn
        bir = np.sort(new) 
        temp = [comb for comb in combinations([1, 2, 3], 2)]
        j = 0
        G = 0

        while j < 3 and G == 0:
            if np.all(temp[j:] != np.ones(shape=(1,2)) * q[0]):
                G = 1
                temp[j:] = []

            j += 1

        a = np.random.uniform()
        row = np.random.uniform(low=1 , high=2)

        if a < 2/3:
            d = np.random.uniform()
            if d < 1/2:
                Q[0][0] = temp[row][0]
                Q[:numbrk + 1] = np.ones(shape=(numbrk,1))  * temp([row][1])
            else:
                Q[0][0] = temp[row][1]
                Q[:numbrk + 1] = np.ones(shape=(numbrk,1))  * temp([row][0])
        else:
            Q = q

        s = np.concatenate((q[0], Q[:2]), axis=0)


    elif np.all(np.any(np.absolute(k * np.ones(shape=(L+j,1)) - new)) <= dist* np.ones(shape=(L+j,1))):
        z = -3
        bir = currentModel
        kn = k
        Q = q
        s = 0

    result = {"bir": bir, "kn": kn, "s": s, "Q": Q, "q": q, "z": z}


    return result

# Test #
if __name__ == "__main__":

    u = np.array([

[0.939001561999887],
[0.875942811492984],
[0.550156342898422],
[0.622475086001228],
[0.587044704531417],
[0.207742292733028],
[0.301246330279491],
[0.470923348517591],
[0.230488160211559],
[0.844308792695389],
[0.194764289567049],
[0.225921780972399],
[0.170708047147859],
[0.227664297816554],
[0.435698684103899],
[0.311102286650413],
[0.923379642103244],
[0.430207391329584],
[0.184816320124136],
[0.904880968679893],
[0.979748378356085],
[0.438869973126103],
[0.111119223440599],
[0.258064695912067],
[0.408719846112552],
[0.594896074008614],
[0.262211747780845],
[0.602843089382083],
[0.711215780433683],
[0.22174673401724],
[0.117417650855806],
[0.296675873218327],
[0.318778301925882],
[0.424166759713807],
[0.507858284661118],
[0.085515797090044],
[0.262482234698333],
[0.801014622769739],
[0.029220277562146],
[0.928854139478045],
[0.730330862855453],
[0.488608973803579],
[0.578525061023439],
[0.237283579771521],
[0.458848828179931],
[0.963088539286913],
[0.546805718738968],
[0.521135830804002],
[0.231594386708524],
[0.488897743920167],
[0.096730025780867],
[0.818148553859625],
[0.817547092079286],
[0.722439592366842],
[0.149865442477967],
[0.659605252908307],
[0.518594942510538],
[0.972974554763863],
[0.648991492712356],
[0.800330575352402],
[0.45379770872692],
[0.432391503783462],
[0.825313795402046],
[0.083469814858914],
[0.133171007607162],
[0.173388613119006],
[0.390937802323736],
[0.83137974283907],
[0.80336439160244],
[0.060471179169894],
[0.399257770613576],
[0.526875830508296],
[0.416799467930787],
[0.656859890973707],
[0.627973359190104],
[0.291984079961715],
[0.43165117024872],
[0.015487125636019],
[0.984063724379154],
[0.167168409914656],
[0.106216344928664],
[0.372409740055537],
[0.198118402542975],
[0.489687638016024],
[0.339493413390758],
[0.951630464777727],
[0.920332039836564],
[0.052676997680793],
[0.737858095516997],
[0.269119426398556],
[0.422835615008808],
[0.547870901214845],
[0.942736984276934],
[0.417744104316662],
[0.983052466469856],
[0.301454948712065],
[0.701098755900926],
[0.666338851584426],
[0.539126465042857],
[0.698105520180308]
		])

    currentModel = np.array([[1], [0], [3],[4], [50]])
    q = np.array([[1], [0], [0], [0], [50]])
    dist = 2
    numbrk = 0

    result = birth(currentModel, u, dist, numbrk, q)

    print(result)
