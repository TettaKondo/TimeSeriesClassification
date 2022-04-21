from os import makedirs
from os.path import join

import matplotlib.pyplot as plt


############  OUTPUT  ############
# test1 matches reference1 (distance : 0.11809634911599995)
# test2 matches reference1 (distance : 0.45350669170800006)
# test3 matches reference1 (distance : 0.11941687921)
# test4 matches reference2 (distance : 0.049332164351999996)
# test5 matches reference2 (distance : 0.051000872047000025)
# test6 matches reference2 (distance : 0.08668896023900001)
############  OUTPUT  ############

delta = lambda a,b: (a - b)**2

def my_min(v1, v2, v3):
    if v1[0] <= min(v2[0], v3[0]):
        return v1, 0
    elif v2[0] <= v3[0]:
        return v2, 1
    else:
        return v3, 2 

def calc_dtw(A, B):
    S = len(A)
    T = len(B)

    m = [[0 for j in range(T)] for i in range(S)]
    m[0][0] = (delta(A[0], B[0]), (-1,-1))
    for i in range(1, S):
        m[i][0] = (m[i-1][0][0] + delta(A[i], B[0]), (i - 1, 0))
    for j in range(1, T):
        m[0][j] = (m[0][j-1][0] + delta(A[0], B[j]), (0, j - 1))

    for i in range(1, S):
        for j in range(1, T):
            minimum, index = my_min(m[i-1][j], m[i][j-1], m[i-1][j-1])
            indexes = [(i - 1, j), (i, j - 1), (i - 1, j - 1)]
            m[i][j] = (minimum[0] + delta(A[i], B[j]), indexes[index])
    return m

def save_plot_img(references, test, save_path):
    fig = plt.figure()
    plt.plot(references[0], label="reference1")
    plt.plot(references[1], label="reference2")
    plt.plot(test, label="test")
    plt.legend()
    fig.savefig(save_path)


reference_dir = join('..', 'time_series_dataset', 'level1', 'reference')
references = []
for label in range(1, 3):
    with open(join(reference_dir, str(label) + '.dat')) as f:
        time_data_str = f.read().split()
        time_data = [float(v) for v in time_data_str]
        references.append(time_data)

test_dir = join('..', 'time_series_dataset', 'level1', 'test')
tests = []
for label in range(1, 7):
    with open(join(test_dir, str(label) + '.dat')) as f:
        time_data_str = f.read().split()
        time_data = [float(v) for v in time_data_str]
        tests.append(time_data)

for test_idx in range(6):
    dis = [calc_dtw(tests[test_idx], references[i])[-1][-1][0] for i in range(2)]
    min_dis = min(dis)
    pred = dis.index(min_dis)
    print("test{} matches reference{} (distance : {})".format(test_idx + 1, pred + 1, min_dis))

    makedirs('imgs', exist_ok=True)
    save_path = join('imgs', 'test' + str(test_idx) + '.png')
    save_plot_img(references, tests[test_idx], save_path)
