from os import makedirs
from os.path import join

import matplotlib.pyplot as plt


############  OUTPUT  ############
# test 1 matches reference 2 (distance : 157.8976969436)
# test 2 matches reference 2 (distance : 160.2096556222)
# test 3 matches reference 2 (distance : 115.20003184810007)
# test 4 matches reference 1 (distance : 96.85890443950001)
# test 5 matches reference 1 (distance : 121.42785183220002)
# test 6 matches reference 1 (distance : 124.6441561528)
# test 7 matches reference 2 (distance : 149.5937102526001)
# test 8 matches reference 2 (distance : 81.16883274560007)
# test 9 matches reference 2 (distance : 393.6288356878)
# test 10 matches reference 2 (distance : 77.85104801670005)
# test 11 matches reference 2 (distance : 72.16316853969994)
# test 12 matches reference 2 (distance : 124.50075942789992)
# test 13 matches reference 1 (distance : 434.63769149350003)
# test 14 matches reference 2 (distance : 114.6757156346)
############  OUTPUT  ############

def calc_dis(A, B):
    d = 0.0
    for i in range(len(A)):
        d += (A[i] - B[i])**2
    return d

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
    m[0][0] = (calc_dis(A[0], B[0]), (-1,-1))
    for i in range(1, S):
        m[i][0] = (m[i-1][0][0] + calc_dis(A[i], B[0]), (i - 1, 0))
    for j in range(1, T):
        m[0][j] = (m[0][j-1][0] + calc_dis(A[0], B[j]), (0, j - 1))

    for i in range(1, S):
        for j in range(1, T):
            minimum, index = my_min(m[i-1][j], m[i][j-1], m[i-1][j-1])
            indexes = [(i - 1, j), (i, j - 1), (i - 1, j - 1)]
            m[i][j] = (minimum[0] + calc_dis(A[i], B[j]), indexes[index])
    return m

reference_path_list = [join('..', 'time_series_dataset', 'level4', 'reference', '1', 'data1.dat'),
                       join('..', 'time_series_dataset', 'level4', 'reference', '2', 'data1.dat')]
references = []
for reference_path in reference_path_list:
    with open(reference_path) as f:
        time_data_str = f.read().split()
        time_data = []
        N = 64
        for i in range(0, len(time_data_str), N):
            time_data.append([float(t) for t in time_data_str[i:i+N]])
        references.append(time_data)
        
test_dir = join('..', 'time_series_dataset', 'level4', 'test')
tests = []
for label in range(1, 15):
    with open(join(test_dir, 'data' + str(label) + '.dat')) as f:
        time_data_str = f.read().split()
        time_data = []
        N = 64
        for i in range(0, len(time_data_str), N):
            time_data.append([float(t) for t in time_data_str[i:i+N]])
        tests.append(time_data)

for test_idx in range(14):
    dis = [calc_dtw(tests[test_idx], references[i])[-1][-1][0] for i in range(2)]
    min_dis = min(dis)
    pred = dis.index(min_dis)
    print("test {} matches reference {} (distance : {})".format(test_idx + 1, pred + 1, min_dis))
